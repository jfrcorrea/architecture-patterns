"""
Classes that represent entities of the domain
"""

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional, Set


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
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented
        return not self.__gt__(other)

    def allocate(self, line: OrderLine) -> None:
        """Allocate a order line to the batch"""
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        """Deallocate a line from the batch"""
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        """Check if can allocate a Order Line to the Batch"""
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def allocated_quantity(self) -> int:
        """Total allocated quantity"""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """Available quantity in the batch """
        return self._purchased_quantity - self.allocated_quantity

def allocate(line: OrderLine, batches: Iterable[Batch]) -> str:
    """Alocate a line in one of a set of batches"""
    batch = [b for b in sorted(batches) if b.can_allocate(line)][0]
    batch.allocate(line)
    return batch.reference
