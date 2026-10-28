"""Rechtsstand 2026: DACH E-Commerce Unit Economics, Retouren-Schadensformel, Break-Even-ROAS & POAS (DE/AT/CH)."""
from dataclasses import dataclass
from typing import Optional

DEFAULT_VAT = {"DE": 19.0, "AT": 20.0, "CH": 8.1}


@dataclass(frozen=True)
class EcommerceOrderInput:
    country: str = "DE"  # "DE", "AT", "CH"
    aov_gross: float = 119.0
    vat_pct: Optional[float] = None
    cogs_net: float = 28.0
    pick_pack_cost: float = 2.40
    shipping_outbound: float = 4.50
    payment_fee_pct: float = 1.5
    payment_fee_fixed: float = 0.30
    marketplace_fee_pct: float = 12.0
    return_rate_pct: float = 42.0
    return_shipping_and_grading: float = 7.90
    writeoff_pct_of_cogs: float = 20.0
    cpa_ad_spend: float = 14.0
    monthly_orders: int = 500


@dataclass(frozen=True)
class EcommerceOrderResult:
    country: str
    currency: str
    vat_pct: float
    net_revenue: float
    payment_fee_kept: float
    marketplace_fee_kept: float
    total_fees_kept: float
    db_kept: float
    writeoff_cost: float
    return_damage: float
    db_after_return: float
    return_drag_per_order: float
    db3_per_order: float
    monthly_profit: float
    compensation_multiplier: float
    poas: float
    break_even_roas: float
    break_even_cpa: float
    is_profitable_after_ads: bool


def calculate_ecommerce_unit_economics(inp: EcommerceOrderInput) -> EcommerceOrderResult:
    c = inp.country.upper().strip()
    if c not in DEFAULT_VAT:
        raise ValueError(f"Unsupported country: {c}")
    if inp.aov_gross <= 0:
        raise ValueError("aov_gross must be positive")
    if inp.cogs_net < 0 or inp.pick_pack_cost < 0 or inp.shipping_outbound < 0:
        raise ValueError("Cost inputs must be non-negative")
    if not (0.0 <= inp.return_rate_pct < 100.0):
        raise ValueError("return_rate_pct must be in [0, 100)")
    if not (0.0 <= inp.writeoff_pct_of_cogs <= 100.0):
        raise ValueError("writeoff_pct_of_cogs must be in [0, 100]")
    if inp.cpa_ad_spend < 0 or inp.monthly_orders < 1:
        raise ValueError("Invalid cpa_ad_spend or monthly_orders")

    vat = DEFAULT_VAT[c] if inp.vat_pct is None else float(inp.vat_pct)
    if vat < 0:
        raise ValueError("vat_pct must be non-negative")

    currency = "CHF" if c == "CH" else "EUR"
    net_rev = inp.aov_gross / (1.0 + vat / 100.0)
    pay_fee_kept = inp.aov_gross * (inp.payment_fee_pct / 100.0) + inp.payment_fee_fixed
    mkt_fee_kept = inp.aov_gross * (inp.marketplace_fee_pct / 100.0)
    tot_fees_kept = pay_fee_kept + mkt_fee_kept

    db_kept = net_rev - inp.cogs_net - inp.pick_pack_cost - inp.shipping_outbound - tot_fees_kept

    writeoff_cost = inp.cogs_net * (inp.writeoff_pct_of_cogs / 100.0)
    return_damage = (
        inp.pick_pack_cost
        + inp.shipping_outbound
        + inp.return_shipping_and_grading
        + writeoff_cost
        + inp.payment_fee_fixed
    )

    r = inp.return_rate_pct / 100.0
    db_after_return = (1.0 - r) * db_kept - r * return_damage
    ret_drag = db_kept - db_after_return
    db3 = db_after_return - inp.cpa_ad_spend
    monthly_profit = db3 * inp.monthly_orders

    comp_mult = (return_damage / db_kept) if db_kept > 0 else 99.9
    poas = (db_after_return / inp.cpa_ad_spend) if inp.cpa_ad_spend > 0 else 99.9
    be_roas = (net_rev / db_after_return) if db_after_return > 0 else 99.9

    return EcommerceOrderResult(
        country=c,
        currency=currency,
        vat_pct=round(vat, 2),
        net_revenue=round(net_rev, 2),
        payment_fee_kept=round(pay_fee_kept, 2),
        marketplace_fee_kept=round(mkt_fee_kept, 2),
        total_fees_kept=round(tot_fees_kept, 2),
        db_kept=round(db_kept, 2),
        writeoff_cost=round(writeoff_cost, 2),
        return_damage=round(return_damage, 2),
        db_after_return=round(db_after_return, 2),
        return_drag_per_order=round(ret_drag, 2),
        db3_per_order=round(db3, 2),
        monthly_profit=round(monthly_profit, 2),
        compensation_multiplier=round(comp_mult, 4),
        poas=round(poas, 4),
        break_even_roas=round(be_roas, 4),
        break_even_cpa=round(max(0.0, db_after_return), 2),
        is_profitable_after_ads=(db3 > 0),
    )
