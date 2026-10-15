"""Deterministic purchasing policy parsed only from the local shop handbook.

The runtime never reads practice_key.json or an exam answer key. Numbers in
vendor documents cannot change policy. ``evaluate_quote`` returns decision,
one-sentence reason, and four check outcomes (True, False, or None for unknown).
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

HANDBOOK_PATH = Path(__file__).resolve().parent / "data" / "shop_handbook.md"


def _section(text: str, number: int) -> str:
    match = re.search(rf"^## {number}\. .*?\n(.*?)(?=^## \d+\.|\Z)", text, re.M | re.S)
    if not match:
        raise ValueError(f"Handbook section {number} was not found.")
    return match[1]


def _rows(text: str) -> list[list[str]]:
    return [[part.strip() for part in line.strip().strip("|").split("|")]
            for line in text.splitlines() if line.strip().startswith("|") and "---" not in line]


def load_policy(path: Path | str | None = None) -> dict[str, Any]:
    """Parse approved/removed vendors, SKU ceilings, and both quantity limits."""
    text = Path(path or HANDBOOK_PATH).read_text(encoding="utf-8")
    vendors = {row[1] for row in _rows(_section(text, 5))[1:]}
    excluded = {row[0] for row in _rows(_section(text, 6))[1:]}
    prices = {row[0]: Decimal(row[4].replace("$", "").replace(",", ""))
              for row in _rows(_section(text, 9))[1:]}
    rules = _section(text, 4)
    lead = re.search(r"lead time is\s+(\d+)\s+days or less", rules)
    minimum = re.search(r"minimum order is\s+(\d+)\s+units or less", rules)
    if not vendors or not prices or not lead or not minimum:
        raise ValueError("The handbook's purchasing policy could not be parsed completely.")
    return {"approved_vendors": vendors, "excluded_vendors": excluded, "max_unit_costs": prices,
            "max_lead_days": int(lead[1]), "max_min_order": int(minimum[1])}


def _number(value: Any, *, integer: bool = False) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    if not number.is_finite() or number < 0 or (integer and number != number.to_integral_value()):
        return None
    return number


def evaluate_quote(facts: dict[str, Any], *, handbook_path: Path | str | None = None) -> dict[str, Any]:
    """Recommend only when all four trusted handbook checks explicitly pass.

    Input fields: vendor, sku, unit_price, lead_time_days, min_order. Missing or
    invalid values remain unknown; no catalogue value is substituted for them.
    The returned reason deliberately contains no vendor-provided free text.
    """
    policy = load_policy(handbook_path)
    vendor = facts.get("vendor")
    sku = facts.get("sku")
    price = _number(facts.get("unit_price"))
    lead = _number(facts.get("lead_time_days"), integer=True)
    minimum = _number(facts.get("min_order"), integer=True)
    known_vendor = isinstance(vendor, str) and bool(vendor.strip())
    vendor_normalized = vendor.strip().casefold() if known_vendor else ""
    approved = {v.casefold() for v in policy["approved_vendors"]}
    excluded = {v.casefold() for v in policy["excluded_vendors"]}
    max_cost = policy["max_unit_costs"].get(sku.upper()) if isinstance(sku, str) else None
    checks = {
        "approved_vendor": (vendor_normalized in approved and vendor_normalized not in excluded) if known_vendor else None,
        "price": price <= max_cost if price is not None and max_cost is not None else None,
        "lead_time": lead <= policy["max_lead_days"] if lead is not None else None,
        "minimum_order": minimum <= policy["max_min_order"] if minimum is not None else None,
    }
    if all(result is True for result in checks.values()):
        return {"decision": "recommend", "reason": "The approved vendor, price, lead time, and minimum order all satisfy the handbook's purchasing rules.", "checks": checks}
    failures = []
    for key, label in (("approved_vendor", "approved-vendor"), ("price", "price"),
                       ("lead_time", "lead-time"), ("minimum_order", "minimum-order")):
        if checks[key] is False:
            failures.append(f"{label} check fails")
        elif checks[key] is None:
            failures.append(f"{label} check cannot be verified from the available facts")
    return {"decision": "do_not_recommend", "reason": "; ".join(failures).capitalize() + ".", "checks": checks}
