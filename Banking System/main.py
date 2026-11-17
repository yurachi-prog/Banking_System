"""
Banking System - Interactive Menu-Driven Program
Demonstrates classes, objects, encapsulation, and inheritance.
"""

import sys
from bank_account import BankAccount
from savings_account import SavingsAccount
from checking_account import CheckingAccount


def get_non_empty_string(prompt: str) -> str:
    """Prompt the user for a non-empty string."""
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            print("[Input Error] Input cannot be blank. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return ""


def get_valid_float(prompt: str, min_val: float = 0.0, allow_zero: bool = True) -> float:
    """Prompt the user for a valid floating-point number within acceptable range."""
    while True:
        try:
            raw = input(prompt).strip()
            # Allow cancellation
            if raw.lower() == "cancel":
                return -1.0

            val = float(raw)
            if not allow_zero and val <= 0:
                print("[Input Error] Amount must be strictly greater than 0.")
                continue
            if val < min_val:
                print(f"[Input Error] Value cannot be less than {min_val:,.2f}.")
                continue
            return val
        except ValueError:
            print("[Input Error] Invalid number. Please enter a valid decimal number (or 'cancel' to abort).")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return -1.0


def select_account(accounts: dict) -> BankAccount | None:
    """Helper to select an existing account by account number."""
    if not accounts:
        print("\n[Notice] No accounts found. Please create an account first.")
        return None

    print("\n--- Available Accounts ---")
    for acc_num, acc in accounts.items():
        print(f"[{acc_num}] {acc.account_holder} ({acc.__class__.__name__}) - Balance: ${acc.balance:,.2f}")

    while True:
        try:
            chosen = input("\nEnter account number (or 'cancel' to return): ").strip()
            if chosen.lower() == "cancel":
                return None
            if chosen in accounts:
                return accounts[chosen]
            print(f"[Error] Account number '{chosen}' not found. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nSelection cancelled.")
            return None


def create_account(accounts: dict) -> None:
    """Handles creating a new account (BankAccount, SavingsAccount, or CheckingAccount)."""
    print("\n" + "=" * 40)
    print("           CREATE NEW ACCOUNT           ")
    print("=" * 40)
    print("Select Account Type:")
    print("1. Standard Bank Account")
    print("2. Savings Account (Earns Interest, Minimum Balance)")
    print("3. Checking Account (Withdrawal Fee)")
    print("4. Cancel")

    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        print("[Input Error] Please enter a valid option between 1 and 4.")

    if choice == "4":
        print("Account creation cancelled.")
        return

    name = get_non_empty_string("Enter account holder's full name: ")
    if not name:
        return

    while True:
        acc_num = get_non_empty_string("Enter unique account number: ")
        if not acc_num:
            return
        if acc_num in accounts:
            print(f"[Error] Account number '{acc_num}' already exists. Please choose a different number.")
            continue
        break

    initial_deposit = get_valid_float("Enter initial deposit amount ($): ", min_val=0.0, allow_zero=True)
    if initial_deposit < 0:
        print("Account creation cancelled.")
        return

    if choice == "1":
        account = BankAccount(name, acc_num, initial_deposit)
    elif choice == "2":
        min_balance = get_valid_float(
            "Enter minimum balance requirement ($) [Default: 100.00]: ",
            min_val=0.0,
            allow_zero=True,
        )
        if min_balance < 0:
            print("Account creation cancelled.")
            return

        rate_input = get_valid_float(
            "Enter annual interest rate in percent (e.g., 3 for 3%) [Default: 3.0]: ",
            min_val=0.0,
            allow_zero=True,
        )
        if rate_input < 0:
            print("Account creation cancelled.")
            return
        interest_rate = rate_input / 100.0

        if initial_deposit < min_balance:
            print(
                f"[Warning] Initial deposit (${initial_deposit:,.2f}) is below minimum balance (${min_balance:,.2f})."
            )
            confirm = input("Do you still wish to proceed? (y/n): ").strip().lower()
            if confirm != "y":
                print("Account creation cancelled.")
                return

        account = SavingsAccount(
            account_holder=name,
            account_number=acc_num,
            initial_balance=initial_deposit,
            interest_rate=interest_rate,
            minimum_balance=min_balance,
        )
    elif choice == "3":
        fee = get_valid_float(
            "Enter per-withdrawal transaction fee ($) [Default: 2.50]: ",
            min_val=0.0,
            allow_zero=True,
        )
        if fee < 0:
            print("Account creation cancelled.")
            return
        account = CheckingAccount(
            account_holder=name,
            account_number=acc_num,
            initial_balance=initial_deposit,
            withdrawal_fee=fee,
        )

    accounts[acc_num] = account
    print(f"\n[Success] {account.__class__.__name__} successfully created for {name} (Acc #: {acc_num})!")


def handle_deposit(accounts: dict) -> None:
    """Handles deposit operation."""
    account = select_account(accounts)
    if not account:
        return

    amount = get_valid_float(f"Enter amount to deposit into account {account.account_number} ($): ", allow_zero=False)
    if amount <= 0:
        print("Deposit aborted.")
        return
    account.deposit(amount)


def handle_withdraw(accounts: dict) -> None:
    """Handles withdraw operation."""
    account = select_account(accounts)
    if not account:
        return

    amount = get_valid_float(f"Enter amount to withdraw from account {account.account_number} ($): ", allow_zero=False)
    if amount <= 0:
        print("Withdrawal aborted.")
        return
    account.withdraw(amount)


def handle_check_balance(accounts: dict) -> None:
    """Handles checking the account balance."""
    account = select_account(accounts)
    if not account:
        return
    account.show_balance()


def handle_add_interest(accounts: dict) -> None:
    """Handles applying interest to a SavingsAccount."""
    account = select_account(accounts)
    if not account:
        return

    # Check if the chosen account is a SavingsAccount (inheritance / polymorphism check)
    if isinstance(account, SavingsAccount):
        account.add_interest()
    else:
        print(f"\n[Error] 'Add Interest' is only permitted for Savings accounts.")
        print(f"Selected account '{account.account_number}' is of type: {account.__class__.__name__}.")


def handle_view_history(accounts: dict) -> None:
    """Handles displaying transaction history."""
    account = select_account(accounts)
    if not account:
        return
    account.show_history()


def display_menu() -> None:
    """Displays the main system menu."""
    print("\n" + "=" * 45)
    print("      BANK ACCOUNT MANAGEMENT SYSTEM         ")
    print("=" * 45)
    print("  1. Create Account")
    print("  2. Deposit")
    print("  3. Withdraw")
    print("  4. Check Balance")
    print("  5. Add Interest (Savings Account Only)")
    print("  6. View Transaction History")
    print("  7. Exit")
    print("=" * 45)


def main() -> None:
    """Main program loop. Runs until the user explicitly chooses to exit."""
    accounts: dict[str, BankAccount] = {}

    print("Welcome to the Bank Account Management System!")

    while True:
        display_menu()
        try:
            choice = input("Enter your option (1-7): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! Thank you for using the Banking System.")
            sys.exit(0)

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            handle_deposit(accounts)
        elif choice == "3":
            handle_withdraw(accounts)
        elif choice == "4":
            handle_check_balance(accounts)
        elif choice == "5":
            handle_add_interest(accounts)
        elif choice == "6":
            handle_view_history(accounts)
        elif choice == "7":
            print("\nExiting Bank Account Management System. Have a great day!")
            break
        else:
            print(f"[Input Error] '{choice}' is not a valid menu option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
