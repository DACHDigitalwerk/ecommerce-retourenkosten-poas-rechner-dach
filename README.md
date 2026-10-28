# 📦 DACH E-Commerce-Retourenkosten-, Marktplatz-Gebühren-, Stückdeckungsbeitrags- & POAS-Rechner 2026

[![Live Web-App](https://img.shields.io/badge/Live_Web--App-E--Commerce_Retourenkosten_&_POAS_Rechner_2026-4f46e5?style=for-the-badge)](https://dachdigitalwerk.github.io/ecommerce-retourenkosten-marktplatz-gebuehren-rechner/)

Open-Source Python-Engine & interaktiver Online-Rechner für **E-Commerce Unit Economics (DB I, DB II, DB III)**, **Retouren-Schadensformel**, **Kompensations-Multiplikator**, **Marktplatz-Provisionen** (Amazon FBA, Zalando ZFS, Otto Market, Digitec Galaxus CH vs. Shopify/Shopware D2C), **Break-Even-ROAS** und **POAS (Profit on Ad Spend)** für Deutschland (`19 % USt`), Österreich (`20 % USt`) und die Schweiz (`8,1 % MWST`).

👉 **[Direkt zum interaktiven DACH E-Commerce-Retourenkosten- & POAS-Rechner 2026](https://dachdigitalwerk.github.io/ecommerce-retourenkosten-marktplatz-gebuehren-rechner/)**

---

## Kernformeln (Unit Economics & POAS nach Retouren)

- **Deckungsbeitrag einer behaltenen Bestellung ($	ext{DB}_{	ext{kept}}$):**
  `DB_kept = Nettoumsatz - COGS - Pick&Pack - Hinversand - Payment_Gebühren - Marktplatz_Provision`
- **Gesamtschaden einer einzelnen Retoure ($S_{	ext{Retoure}}$):**
  `S_Retoure = Pick&Pack + Hinversand + Rückversand_Aufbereitung + (COGS * Wertverlust_%) + Payment_Fixgebühr`
- **Erwarteter Stückdeckungsbeitrag pro versendeter Bestellung bei Retourenquote $r$:**
  `DB_nach_Retoure = (1 - r) * DB_kept - r * S_Retoure`
- **POAS & Break-Even-ROAS:**
  `POAS = DB_nach_Retoure / CPA` und `Break_Even_ROAS = Nettoumsatz / DB_nach_Retoure`

## Schnellstart

```bash
pip install -e .
pytest -v
dach-ecommerce-poas --country DE --aov 119.0 --cogs 28.0 --return-rate 42.0 --cpa 14.0
```

## Rechtlicher Hinweis

Regelbasiertes mathematisch-schematisches Kalkulationswerkzeug gem. BGH, Urteil v. 09.09.2021 – I ZR 226/20 (Smartlaw). Keine individuelle Steuer- oder Rechtsberatung i.S.d. § 2 RDG / § 5 StBerG.
