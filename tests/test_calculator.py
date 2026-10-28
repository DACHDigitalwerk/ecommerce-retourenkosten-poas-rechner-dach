import pytest
from ecommerce_retouren_poas_dach import EcommerceOrderInput, calculate_ecommerce_unit_economics


def test_de_fashion_zalando_preset():
    res = calculate_ecommerce_unit_economics(EcommerceOrderInput())
    assert res.country == "DE"
    assert res.currency == "EUR"
    assert res.net_revenue == 100.0
    assert res.db_kept == 48.73
    assert res.return_damage == 20.70
    assert res.db_after_return == 19.57
    assert res.db3_per_order == 5.57
    assert res.is_profitable_after_ads is True


def test_amazon_fba_15_pct_referral():
    res = calculate_ecommerce_unit_economics(
        EcommerceOrderInput(
            country="DE",
            aov_gross=59.90,
            cogs_net=14.50,
            pick_pack_cost=1.20,
            shipping_outbound=4.80,
            payment_fee_pct=0.0,
            payment_fee_fixed=0.0,
            marketplace_fee_pct=15.0,
            return_rate_pct=12.0,
            return_shipping_and_grading=5.20,
            writeoff_pct_of_cogs=25.0,
            cpa_ad_spend=9.50,
        )
    )
    assert res.payment_fee_kept == 0.0
    assert res.marketplace_fee_kept == 8.98
    assert res.poas > 1.5
    assert res.is_profitable_after_ads is True


def test_d2c_shopify_high_writeoff_cosmetics():
    res = calculate_ecommerce_unit_economics(
        EcommerceOrderInput(
            country="DE",
            aov_gross=68.0,
            cogs_net=11.20,
            pick_pack_cost=1.90,
            shipping_outbound=3.90,
            payment_fee_pct=2.1,
            payment_fee_fixed=0.35,
            marketplace_fee_pct=0.0,
            return_rate_pct=4.0,
            return_shipping_and_grading=5.50,
            writeoff_pct_of_cogs=80.0,
            cpa_ad_spend=22.0,
        )
    )
    assert res.writeoff_cost == 8.96
    assert res.marketplace_fee_kept == 0.0
    assert res.db3_per_order > 14.0


def test_austria_20_pct_vat_default():
    res = calculate_ecommerce_unit_economics(EcommerceOrderInput(country="AT", aov_gross=120.0))
    assert res.vat_pct == 20.0
    assert res.net_revenue == 100.0
    assert res.currency == "EUR"


def test_switzerland_8_1_pct_mwst_and_chf():
    res = calculate_ecommerce_unit_economics(EcommerceOrderInput(country="CH", aov_gross=108.10))
    assert res.vat_pct == 8.1
    assert res.net_revenue == 100.0
    assert res.currency == "CHF"


def test_zero_return_rate_has_zero_return_drag():
    res = calculate_ecommerce_unit_economics(EcommerceOrderInput(return_rate_pct=0.0))
    assert res.db_after_return == res.db_kept
    assert res.return_drag_per_order == 0.0


def test_poas_break_even_identity():
    base = calculate_ecommerce_unit_economics(EcommerceOrderInput(cpa_ad_spend=10.0))
    at_be = calculate_ecommerce_unit_economics(EcommerceOrderInput(cpa_ad_spend=base.db_after_return))
    assert abs(at_be.poas - 1.0) < 1e-3
    assert abs(at_be.db3_per_order) < 0.02


def test_excessive_return_rate_turns_unprofitable_before_ads():
    res = calculate_ecommerce_unit_economics(EcommerceOrderInput(return_rate_pct=80.0, cpa_ad_spend=5.0))
    assert res.db_after_return < 0
    assert res.is_profitable_after_ads is False
    assert res.break_even_cpa == 0.0


def test_invalid_country_raises():
    with pytest.raises(ValueError):
        calculate_ecommerce_unit_economics(EcommerceOrderInput(country="US"))


def test_invalid_return_rate_raises():
    with pytest.raises(ValueError):
        calculate_ecommerce_unit_economics(EcommerceOrderInput(return_rate_pct=100.0))
