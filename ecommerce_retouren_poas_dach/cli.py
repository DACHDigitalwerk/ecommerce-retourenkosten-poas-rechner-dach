import argparse
import json
from dataclasses import asdict
from .calculator import EcommerceOrderInput, calculate_ecommerce_unit_economics


def main() -> None:
    p = argparse.ArgumentParser(description="DACH E-Commerce-Retourenkosten-, Marktplatz- & POAS-Rechner 2026")
    p.add_argument("--country", default="DE", choices=["DE", "AT", "CH"])
    p.add_argument("--aov", type=float, default=119.0)
    p.add_argument("--cogs", type=float, default=28.0)
    p.add_argument("--return-rate", type=float, default=42.0)
    p.add_argument("--cpa", type=float, default=14.0)
    args = p.parse_args()
    res = calculate_ecommerce_unit_economics(
        EcommerceOrderInput(
            country=args.country,
            aov_gross=args.aov,
            cogs_net=args.cogs,
            return_rate_pct=args.return_rate,
            cpa_ad_spend=args.cpa,
        )
    )
    print(json.dumps(asdict(res), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
