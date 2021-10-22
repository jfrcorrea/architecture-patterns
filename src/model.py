"""
Classes that represent entities of the domain
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    """"Represents a order line"""
    orderid: str
    sku: str
    qty: int


class Batch:
    """Represents a batch"""
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine) -> None:
        """Allocate a order line to the batch"""
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        """Check if can allocate a Order Line to the Batch"""
        return self.sku == line.sku and self.available_quantity >= line.qty
