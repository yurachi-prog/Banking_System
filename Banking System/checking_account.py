from bank_account import BankAccount


class CheckingAccount(BankAccount):
    """
    Checking account subclass that inherits from BankAccount.
    Features a transaction fee deducted on top of every withdrawal.
    """

    def __init__(
        self,
        account_holder: str,
        account_number: str,
        initial_balance: float = 0.0,
        withdrawal_fee: float = 2.50,
    ):
        super().__init__(account_holder, account_number, initial_balance)
        if withdrawal_fee < 0:
            raise ValueError("Withdrawal fee cannot be negative.")
        self.withdrawal_fee = float(withdrawal_fee)

    def withdraw(self, amount: float) -> bool:
        """
        Overrides BankAccount.withdraw.
        Deducts the withdrawal fee on top of the amount withdrawn.
        """
        if amount <= 0:
            print(f"[Error] Withdrawal amount must be greater than zero. Provided: ${amount:,.2f}")
            return False

        total_deduction = amount + self.withdrawal_fee
        if total_deduction > self.balance:
            print(
                f"[Error] Insufficient funds for withdrawal plus fee. "
                f"Requested: ${amount:,.2f} + Fee: ${self.withdrawal_fee:,.2f} = ${total_deduction:,.2f}. "
                f"Available Balance: ${self.balance:,.2f}"
            )
            return False

        new_balance = self.balance - total_deduction
        self._set_balance(new_balance)
        self._record_transaction(
            "Withdrawal",
            amount,
            self.balance,
            f"Included Fee: ${self.withdrawal_fee:,.2f}"
        )
        print(
            f"[Success] Successfully withdrew ${amount:,.2f} with a fee of ${self.withdrawal_fee:,.2f}. "
            f"Total deducted: ${total_deduction:,.2f}. Current balance: ${self.balance:,.2f}"
        )
        return True

    def show_balance(self) -> None:
        """Displays balance with checking-specific details."""
        super().show_balance()
        print(f"Withdrawal Fee : ${self.withdrawal_fee:,.2f}")
        print(f"{'=' * 35}")
