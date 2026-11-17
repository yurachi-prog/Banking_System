"""
Comprehensive automated test suite to verify all requirements.
"""

from bank_account import BankAccount
from savings_account import SavingsAccount
from checking_account import CheckingAccount


def test_bank_account():
    print("Testing BankAccount...")
    b = BankAccount("Alice Smith", "BA100", 500.0)
    assert b.account_holder == "Alice Smith"
    assert b.account_number == "BA100"
    assert b.balance == 500.0
    
    # Encapsulation test: __balance is private
    assert not hasattr(b, "__balance")
    assert hasattr(b, "_BankAccount__balance")

    # Deposit tests
    assert b.deposit(200.0) is True
    assert b.balance == 700.0
    assert b.deposit(0) is False
    assert b.deposit(-50) is False
    assert b.balance == 700.0

    # Withdraw tests
    assert b.withdraw(150.0) is True
    assert b.balance == 550.0
    assert b.withdraw(600.0) is False  # exceeds balance
    assert b.withdraw(-10.0) is False
    assert b.withdraw(0) is False
    assert b.balance == 550.0

    # History tests
    assert len(b.transaction_history) == 3
    print("BankAccount tests passed!\n")


def test_savings_account():
    print("Testing SavingsAccount...")
    s = SavingsAccount("Bob Jones", "SA200", 1000.0, interest_rate=0.05, minimum_balance=200.0)
    assert isinstance(s, BankAccount)
    assert s.interest_rate == 0.05
    assert s.minimum_balance == 200.0
    assert s.balance == 1000.0

    # Add interest test: 1000 * 0.05 = 50.0 -> new balance 1050.0
    assert s.add_interest() is True
    assert s.balance == 1050.0

    # Withdraw test: minimum balance enforcement
    # Current balance 1050, min balance 200. Max withdrawal allowed is 850.
    assert s.withdraw(851.0) is False  # Drops below min balance (1050 - 851 = 199 < 200)
    assert s.balance == 1050.0
    assert s.withdraw(850.0) is True   # Leaves exactly 200 min balance
    assert s.balance == 200.0
    assert s.withdraw(1.0) is False    # Leaves 199 < 200
    assert s.balance == 200.0
    print("SavingsAccount tests passed!\n")


def test_checking_account():
    print("Testing CheckingAccount...")
    c = CheckingAccount("Charlie Brown", "CA300", 500.0, withdrawal_fee=3.0)
    assert isinstance(c, BankAccount)
    assert c.withdrawal_fee == 3.0
    assert c.balance == 500.0

    # Withdraw test: fee deducted on top of amount
    # Withdraw 100 -> total deduction 103 -> balance 397
    assert c.withdraw(100.0) is True
    assert c.balance == 397.0

    # Exceeding balance including fee
    # balance is 397, withdraw 395 -> total deduction 398 > 397 -> should reject
    assert c.withdraw(395.0) is False
    assert c.balance == 397.0

    # Valid withdrawal
    # withdraw 390 -> total deduction 393 -> balance 4.0
    assert c.withdraw(390.0) is True
    assert c.balance == 4.0
    print("CheckingAccount tests passed!\n")


if __name__ == "__main__":
    test_bank_account()
    test_savings_account()
    test_checking_account()
    print("ALL TESTS PASSED SUCCESSFULLY!")
