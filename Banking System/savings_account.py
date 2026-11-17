from bank_account import BankAccount


class SavingsAccount(BankAccount):
    """
    Savings account subclass that inherits from BankAccount.
    Features an interest rate and enforces a minimum balance rule.
    """

    def __init__(
        self,
        account_holder: str,
        account_number: str,
        initial_balance: float = 0.0,
        interest_rate: float = 0.03,
        minimum_balance: float = 100.0,
    ):
        super().__init__(account_holder, account_number, initial_balance)
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        if minimum_balance < 0:
            raise ValueError("Minimum balance cannot be negative.")

        self.interest_rate = float(interest_rate)
        self.minimum_balance = float(minimum_balance)

    def add_interest(self) -> bool:
        """
        Calculates and adds interest to the balance based on interest_rate.
        """
        if self.interest_rate <= 0:
            print("[Info] Interest rate is 0.0%. No interest earned.")
            return False

        interest_earned = round(self.balance * self.interest_rate, 2)
        new_balance = self.balance + interest_earned
        self._set_balance(new_balance)
        rate_percent = self.interest_rate * 100
        self._record_transaction(
            "Interest Added",
            interest_earned,
            self.balance,
            f"Rate: {rate_percent:.2f}%"
        )
        print(
            f"[Success] Interest of ${interest_earned:,.2f} ({rate_percent:.2f}%) added. "
            f"New balance: ${self.balance:,.2f}"
        )
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Overrides BankAccount.withdraw.
        Refuses any withdrawal that would drop the balance below the minimum balance.
        """
        if amount <= 0:
            print(f"[Error] Withdrawal amount must be greater than zero. Provided: ${amount:,.2f}")
            return False

        if amount > self.balance:
            print(
                f"[Error] Insufficient funds. Requested: ${amount:,.2f}, Available: ${self.balance:,.2f}"
            )
            return False

        if (self.balance - amount) < self.minimum_balance:
            print(
                f"[Error] Withdrawal refused. Account requires a minimum balance of ${self.minimum_balance:,.2f}. "
                f"Remaining balance would be ${(self.balance - amount):,.2f}."
            )
            return False

        new_balance = self.balance - amount
        self._set_balance(new_balance)
        self._record_transaction("Withdrawal", amount, self.balance, "Savings withdrawal")
        print(f"[Success] Successfully withdrew ${amount:,.2f}. Current balance: ${self.balance:,.2f}")
        return True

    def show_balance(self) -> None:
        """Displays balance with savings-specific details."""
        super().show_balance()
        print(f"Interest Rate  : {self.interest_rate * 100:.2f}%")
        print(f"Minimum Balance: ${self.minimum_balance:,.2f}")
        print(f"{'=' * 35}")
