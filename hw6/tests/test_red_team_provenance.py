"""Offline regressions for red-team evidence reuse after document revisions."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import experiments
from validate_submission import Audit


@pytest.fixture
def red_team_project(tmp_path, monkeypatch):
    output = tmp_path / 'output'
    output.mkdir()
    (tmp_path / 'data/practice_docs').mkdir(parents=True)
    (tmp_path / 'data/practice_key.json').write_text('[]')
    directory = tmp_path / 'data/my_attacks'
    directory.mkdir()
    documents = [directory / 'a01_quote.html', directory / 'a02_quote.eml']
    for document in documents:
        document.write_text('Visible vendor quote. Hidden candidate payload.')
    for source in experiments.RUNTIME_SOURCES:
        path = tmp_path / source
        path.parent.mkdir(exist_ok=True)
        path.write_text('Unchanged runtime fixture.\n')
    (output / 'red_team_key.json').write_text(json.dumps([{'file': path.name} for path in documents]))
    monkeypatch.setattr(experiments, 'ROOT', tmp_path)
    monkeypatch.setattr(experiments, 'OUTPUT', output)

    async def forbidden_api_call(*args, **kwargs):
        raise AssertionError('A stale or already-complete result must never trigger a model call.')

    monkeypatch.setattr(experiments, 'run_document', forbidden_api_call)
    rows = [{'file': doc.name, 'mode': mode, 'run_id': f'{doc.stem}-{mode}', 'fooled': False,
             **experiments.red_team_inputs(doc)}
            for doc in documents for mode in ('undefended', 'defended')]
    experiments.save('red_team_results.json', rows)
    return tmp_path, documents, rows


@pytest.mark.parametrize('changed', ['document', 'key', 'runtime'])
def test_changed_inputs_fail_before_resume_or_any_api_call(red_team_project, changed):
    root, documents, _ = red_team_project
    paths = {'document': documents[0], 'key': root / 'output/red_team_key.json', 'runtime': root / 'tools.py'}
    path = paths[changed]
    path.write_text(path.read_text() + '\n')
    with pytest.raises(RuntimeError, match='inputs changed or lack provenance'):
        asyncio.run(experiments.run_suite('red_team'))
    assert not (root / 'output/red_team_provenance.json').exists()


def test_old_unfingerprinted_rows_fail_before_resume(red_team_project):
    _, _, rows = red_team_project
    del rows[0]['document_sha256']
    experiments.save('red_team_results.json', rows)
    with pytest.raises(RuntimeError, match='inputs changed or lack provenance'):
        asyncio.run(experiments.run_suite('red_team'))


def test_unchanged_completed_results_resume_and_detect_later_tampering(red_team_project):
    root, documents, rows = red_team_project
    original = (root / 'output/red_team_results.json').read_bytes()
    asyncio.run(experiments.run_suite('red_team'))
    assert (root / 'output/red_team_results.json').read_bytes() == original
    usage = [{'run_id': row['run_id'], 'response_id': row['run_id'] + '-response',
              'layers': [] if row['mode'] == 'undefended' else ['code', 'design', 'prompt'],
              'experiment': 'red_team_' + row['mode'], 'gateway_force_refresh_requested': True,
              'gateway_cache_status': 'REFRESH'} for row in rows]
    attacks = {path.name for path in documents}
    audit = Audit(root)
    audit.red_team_provenance(rows, usage, attacks)
    assert all(check['passed'] for check in audit.checks)

    # A new document paired with old measured answers must fail independently.
    documents[0].write_text('A different hidden attack with the same filename.')
    audit = Audit(root)
    audit.red_team_provenance(rows, usage, attacks)
    assert any(not check['passed'] and 'current two attack files' in check['check'] for check in audit.checks)
    assert any(not check['passed'] and 'input fingerprints' in check['check'] for check in audit.checks)


def test_final_evidence_rejects_reused_response_or_wrong_undefended_layers(red_team_project):
    root, documents, rows = red_team_project
    asyncio.run(experiments.run_suite('red_team'))
    usage = [{'run_id': row['run_id'], 'response_id': row['run_id'] + '-response',
              'layers': [] if row['mode'] == 'undefended' else ['code', 'design', 'prompt'],
              'experiment': 'red_team_' + row['mode'], 'gateway_force_refresh_requested': True,
              'gateway_cache_status': 'REFRESH'} for row in rows]
    usage[0]['layers'] = ['code']
    usage.append(deepcopy(usage[1]))
    audit = Audit(root)
    audit.red_team_provenance(rows, usage, {path.name for path in documents})
    failed = [check['check'] for check in audit.checks if not check['passed']]
    assert any('actual mode and layers' in name for name in failed)
    assert any('responses are fresh' in name for name in failed)
