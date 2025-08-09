import csv
from datetime import datetime

def save_expense(description, amount):

    with open("expenses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        

        if file.tell() == 0:
            writer.writerow(["Date", "Description", "Amount"])
        

        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description, amount])

def start_calculator():
    print("Welcome to Expenses Calculator!")
    print("Type 'exit' at any time to quit.\n")

    while True:

        description = input("What did you spend on? > ")
        if description.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            amount = float(input("How much did you spend? $"))
        except ValueError:
            print("Please enter a valid number.\n")
            continue

        # Save the expense
        save_expense(description, amount)
        print(f"Saved: {description} - ${amount:.2f}\n")

# Run the app
if __name__ == "__main__":
    start_calculator()
