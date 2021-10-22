"""
Tests about batches operations
"""

from datetime import date
from typing import Tuple

from src.model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int) -> Tuple[Batch, OrderLine]:
    """Create a Batch and a Order Line"""
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    """Test allocating to a batch reduces the available quantity"""
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    """Test if can allocate if available quantity is greater than required"""
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required():
    """Test if cannot allocate id available quantity is smaller than required"""
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    """Test if can allocate if available quantity is equal to required"""
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_do_not_match():
    """Test if cannor allocate if skus from batch and order line do not match"""
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False
