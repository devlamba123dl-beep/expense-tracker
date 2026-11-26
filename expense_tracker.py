import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


class Expense:
    def __init__(self, date, category, amount, note=""):
        self.date = date
        self.category = category
        self.amount = amount
        self.note = note

    def describe(self):
        return f"{self.date} | {self.category:<13} | Rs {self.amount:>8.2f} | {self.note}"


class RecurringExpense(Expense):
    def __init__(self, date, category, amount, note="", frequency="Monthly"):
        super().__init__(date, category, amount, note)
        self.frequency = frequency

    def describe(self):
        return super().describe() + f" ({self.frequency})"


class ExpenseTracker:
    def __init__(self):
        self.__budget = 0  # encapsulated (private)
        self.expenses = []

    def set_budget(self, budget):
        if budget <= 0:
            raise ValueError("Budget must be positive")
        self.__budget = budget

    def get_budget(self):
        return self.__budget

    def add_expense(self, expense):
        if expense.amount <= 0:
            raise ValueError("Amount must be positive")
        self.expenses.append(expense)

    def view_expenses(self, category=None):
        found = False
        for e in self.expenses:
            if category is None or e.category.lower() == category.lower():
                print(e.describe())
                found = True
        if not found:
            print("No expenses found.")

    def total_spent(self):
        return sum(e.amount for e in self.expenses)

    def category_summary(self):
        summary = {}
        for e in self.expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
        return summary

    def top_category(self):
        summary = self.category_summary()
        return max(summary, key=summary.get)

    def remaining(self):
        return self.__budget - self.total_spent()

    def budget_status(self):
        if self.__budget == 0:
            return "NO BUDGET SET"
        percent = self.total_spent() / self.__budget * 100
        if percent > 100:
            return "OVER BUDGET"
        elif percent >= 80:
            return "WARNING"
        else:
            return "SAFE"

    def save_to_file(self):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["BUDGET", self.__budget])
            for e in self.expenses:
                writer.writerow([e.date, e.category, e.amount, e.note])

    def load_from_file(self):
        try:
            with open(FILE_NAME, newline="") as f:
                for row in csv.reader(f):
                    if row[0] == "BUDGET":
                        self.__budget = float(row[1])
                    else:
                        self.expenses.append(Expense(row[0], row[1], float(row[2]), row[3]))
        except FileNotFoundError:
            pass  # first run: start with an empty list


def show_summary(tracker):
    total = tracker.total_spent()
    if total == 0:
        print("No expenses recorded yet.")
        return
    print("\n--- CATEGORY SUMMARY ---")
    summary = tracker.category_summary()
    for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        percent = amount / total * 100
        bar = "#" * int(amount // 50)
        print(f"{category:<13} {bar:<14} Rs {amount:>7.2f} ({percent:.1f}%)")
    print(f"Total spent : Rs {total:.2f}")
    print(f"Top category: {tracker.top_category()}")
    if tracker.get_budget() > 0:
        print(f"Budget      : Rs {tracker.get_budget():.2f}")
        print(f"Remaining   : Rs {tracker.remaining():.2f}")
        print(f"Status      : {tracker.budget_status()}")


def main():
    tracker = ExpenseTracker()
    tracker.load_from_file()
    while True:
        print("\n1. Add  2. View  3. Set Budget  4. Summary  5. Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number from 1 to 5.")
            continue
        if choice == 1:
            try:
                date = input("Date (YYYY-MM-DD): ")
                datetime.strptime(date, "%Y-%m-%d")
                category = input("Category: ").strip().title()
                amount = float(input("Amount: "))
                note = input("Note: ")
                tracker.add_expense(Expense(date, category, amount, note))
                print("Expense added.")
            except ValueError as err:
                print("Invalid input:", err)
        elif choice == 2:
            cat = input("Category (press Enter for all): ").strip()
            tracker.view_expenses(cat if cat else None)
        elif choice == 3:
            try:
                tracker.set_budget(float(input("Monthly budget: ")))
                print("Budget saved.")
            except ValueError as err:
                print("Invalid input:", err)
        elif choice == 4:
            show_summary(tracker)
        elif choice == 5:
            tracker.save_to_file()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()