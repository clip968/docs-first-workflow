"""
Tests for example_adder module.

These tests demonstrate the TDD workflow:
1. Write a failing test first
2. Implement minimal code
3. Verify test passes
"""

import unittest
from src.example_adder import add, subtract


class TestAdder(unittest.TestCase):

    def test_add_positive_numbers(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self) -> None:
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self) -> None:
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)

    def test_subtract_positive_numbers(self) -> None:
        self.assertEqual(subtract(5, 3), 2)

    def test_subtract_negative_result(self) -> None:
        self.assertEqual(subtract(3, 5), -2)


if __name__ == "__main__":
    unittest.main()
