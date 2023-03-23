import json
import os
import sys
import matplotlib.pyplot as plt

TRANSACTION_TYPES = []
MONTH_YR = ""


def print_transaction_types():
    for i, type in enumerate(TRANSACTION_TYPES):
        print(f"{i}. {type}")


def refresh_transaction_types():
    with open("transaction_types", "r") as f:
        transaction_types = f.readlines()
        TRANSACTION_TYPES = [x.strip() for x in transaction_types]


def parse_amount(amount):
    return float(amount)


def render_pie_chart():
    with open(f"{MONTH_YR}.json", "r") as f:
        group_by_transaction = json.loads(f.read())
        # print(group_by_transaction)
        # create a pie chart based on groups
        labels = []
        sizes = []

        income_labels = []
        income_sizes = []

        for key, value in group_by_transaction.items():
            try:
                # if not numeric, skip
                if parse_amount(value[0]["amount"]) > 0.0:
                    income_labels.append(key)
                    income_sizes.append(sum([parse_amount(x["amount"]) for x in value]))
                    continue
                labels.append(key)
                sizes.append(-sum([parse_amount(x["amount"]) for x in value]))
            except:
                continue
        if "unknown" in labels:
            labels.remove("unknown")

        if "unknown" in income_labels:
            income_labels.remove("unknown")

        # add on hover show the amount
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle(f"Transactions for {MONTH_YR}")
        # show size of each slice instead of percentage
        ax1.pie(
            sizes,
            labels=labels,
            autopct=lambda p: f"{p * sum(sizes) / 100:.2f}",
            shadow=True,
            startangle=90,
        )
        ax1.axis("equal")
        ax1.set_title("Expenses")
        ax2.pie(
            income_sizes,
            labels=income_labels,
            autopct=lambda p: f"{p * sum(income_sizes) / 100:.2f}",
            shadow=True,
            startangle=90,
        )
        ax2.axis("equal")
        ax2.set_title("Income")
        plt.show()


def fix_transaction_types_file():
    with open("transaction_types", "r") as f:
        transaction_types = f.readlines()
        TRANSACTION_TYPES = [x.strip() for x in transaction_types]
    # move unknown to the end
    if "unknown" in TRANSACTION_TYPES:
        TRANSACTION_TYPES.remove("unknown")
        TRANSACTION_TYPES.append("unknown")
    with open("transaction_types", "w") as f:
        for type in TRANSACTION_TYPES:
            f.write(type + "\n")


def main():
    global TRANSACTION_TYPES
    if os.path.exists(f"{MONTH_YR}.json"):
        use_existing = input(f"Use existing {MONTH_YR}.json? (y/n): ")
        if use_existing == "y":
            render_pie_chart()
            return
    with open("transaction_types", "r") as f:
        transaction_types = f.readlines()
        TRANSACTION_TYPES = [x.strip() for x in transaction_types]
        print_transaction_types()
    with open(f"{MONTH_YR}.csv", "r") as f:
        date_dict = {}
        for i, line in enumerate(f.readlines()):
            clean_line = lambda x: x.replace('"', "").strip()
            clean_array = [x for x in map(clean_line, line.split(","))]
            if clean_array[0] == "":
                continue
            date = clean_array[0]
            curr_dict = {
                "description": clean_array[5],
                "amount": clean_array[7],
            }
            if date not in date_dict:
                date_dict[date] = [curr_dict]
            else:
                date_dict[date].append(curr_dict)

    group_by_transaction = {}
    exit = False
    for date, transactions in date_dict.items().__reversed__():
        if exit:
            break
        for i, transaction in enumerate(transactions):
            os.system("clear")
            print(transaction["description"])
            print(transaction["amount"])

            print_transaction_types()
            valid = False
            while not valid:
                user_input = input("Transaction type number (n for new): ")
                if (
                    user_input == "exit"
                    or user_input == "e"
                    or user_input == "quit"
                    or user_input == "q"
                    or user_input == "stop"
                    or user_input == "-1"
                ):
                    exit = True
                    break
                elif user_input == "n":
                    new_transaction_type = input("New transaction type: ")
                    TRANSACTION_TYPES.append(new_transaction_type)
                    with open("transaction_types", "a") as f:
                        f.write(new_transaction_type + "\n")
                    refresh_transaction_types()
                    x = new_transaction_type
                    valid = True
                elif int(user_input) >= 0 and int(user_input) < len(TRANSACTION_TYPES):
                    x = TRANSACTION_TYPES[int(user_input)]
                    valid = True
                else:
                    print("Invalid input. Try again.")

            if x not in group_by_transaction:
                group_by_transaction[x] = [transaction]
            else:
                group_by_transaction[x].append(transaction)
    with open(f"{MONTH_YR}.json", "w") as f:
        f.write(json.dumps(group_by_transaction))
    render_pie_chart()


if __name__ == "__main__":
    fix_transaction_types_file()
    if len(sys.argv) < 2:
        print("Please provide the monthyr as an argument. e.g. mar23 (same as your source filename without the extension)")
        sys.exit(1)
    else:
        MONTH_YR = sys.argv[1]
        main()
