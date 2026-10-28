"""DACH E-Commerce-Retourenkosten-, Marktplatz-Gebühren- & POAS-Engine 2026 (DE/AT/CH)."""
from .calculator import EcommerceOrderInput, EcommerceOrderResult, calculate_ecommerce_unit_economics

__all__ = ["EcommerceOrderInput", "EcommerceOrderResult", "calculate_ecommerce_unit_economics"]
__version__ = "1.0.0"
