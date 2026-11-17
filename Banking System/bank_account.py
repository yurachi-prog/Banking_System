from datetime import datetime


class BankAccount:
    """
    Base class representing a standard bank account.
    Demonstrates encapsulation by keeping the balance private (__balance).
    """

    def __init__(self, account_holder: str, account_number: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.account_holder = account_holder
        self.account_number = account_number
        self.__balance = float(initial_balance)
        self.transaction_history = []
        self._record_transaction("Account Created", initial_balance, self.__balance, "Initial deposit")

    @property
    def balance(self) -> float:
        """Getter property for the private __balance attribute."""
        return self.__balance

    def _set_balance(self, new_balance: float) -> None:
        """Protected helper to update private balance safely."""
        self.__balance = round(new_balance, 2)

    def _record_transaction(self, trans_type: str, amount: float, balance_after: float, note: str = "") -> None:
        """Internal helper to log all account transactions."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "type": trans_type,
            "amount": amount,
            "balance_after": balance_after,
            "note": note
        }
        self.transaction_history.append(entry)

    def deposit(self, amount: float) -> bool:
        """
        Deposits the specified amount into the account.
        Rejects zero or negative amounts.
        """
        if amount <= 0:
            print(f"[Error] Deposit amount must be greater than zero. Provided: ${amount:,.2f}")
            return False

        self._set_balance(self.__balance + amount)
        self._record_transaction("Deposit", amount, self.__balance)
        print(f"[Success] Successfully deposited ${amount:,.2f}. Current balance: ${self.__balance:,.2f}")
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws the specified amount from the account.
        Rejects amounts larger than the balance or non-positive amounts.
        """
        if amount <= 0:
            print(f"[Error] Withdrawal amount must be greater than zero. Provided: ${amount:,.2f}")
            return False

        if amount > self.__balance:
            print(
                f"[Error] Insufficient funds. Requested: ${amount:,.2f}, Available Balance: ${self.__balance:,.2f}"
            )
            return False

        self._set_balance(self.__balance - amount)
        self._record_transaction("Withdrawal", amount, self.__balance)
        print(f"[Success] Successfully withdrew ${amount:,.2f}. Current balance: ${self.__balance:,.2f}")
        return True

    def show_balance(self) -> None:
        """Displays the current balance."""
        print(f"\n{'=' * 35}")
        print(f"         ACCOUNT BALANCE           ")
        print(f"{'=' * 35}")
        print(f"Account Number : {self.account_number}")
        print(f"Account Holder : {self.account_holder}")
        print(f"Account Type   : {self.__class__.__name__}")
        print(f"Current Balance: ${self.__balance:,.2f}")
        print(f"{'=' * 35}")

    def show_history(self) -> None:
        """Prints every transaction made so far."""
        print(f"\n{'=' * 80}")
        print(f"TRANSACTION HISTORY: Account {self.account_number} ({self.account_holder})")
        print(f"{'=' * 80}")
        if not self.transaction_history:
            print("No transactions recorded yet.")
            print(f"{'=' * 80}")
            return

        print(f"{'Timestamp':<20} | {'Type':<16} | {'Amount ($)':<12} | {'Balance ($)':<12} | {'Notes'}")
        print(f"{'-' * 80}")
        for t in self.transaction_history:
            amt_str = f"{t['amount']:,.2f}"
            bal_str = f"{t['balance_after']:,.2f}"
            print(f"{t['timestamp']:<20} | {t['type']:<16} | {amt_str:<12} | {bal_str:<12} | {t['note']}")
        print(f"{'=' * 80}")
