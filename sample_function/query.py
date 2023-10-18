
from collections import OrderedDict
from datetime import datetime

from data import stock, personnel


# Defining a dictionary to store our params, instead of variables, will allow us
# to change the value of the global scope from inside the functions.
params = {
    "is_authenticated": False,
    "user_name": None
}


def get_user_name():
    """Return the user name."""
    return input("What is your user name? ")


def greet_user():
    """Send a greeting to the user."""
    print(f"Hello, {params['user_name']}!")


def get_selected_operation():
    """Return the number selected by the user on the main menu."""
    print()
    print("What would you like to do?")
    print("1. List items by warehouse")
    print("2. Search an item and place an order")
    print("3. Browse by category")
    print("4. Quit")
    return input("Type the number of the operation: ")


def list_items_by_warehouse():
    """Print a list of items by warehouse."""
    other_warehouses = {}

    print("Items in warehouse 1:")
    amount_in_warehouse1 = 0
    for item in stock:
        if item["warehouse"] == 1:
            amount_in_warehouse1 = amount_in_warehouse1 + 1
            print(f"- {item['state']} {item['category'].lower()}")
        else:
            # We get the id of the warehouse.
            warehouse_id = str(item["warehouse"])
            # If the id does not exist in other_warehouses, we create it.
            if warehouse_id not in other_warehouses:
                other_warehouses[warehouse_id] = []
            # We append the item to the warehouse.
            other_warehouses[warehouse_id].append(item)

    for warehouse_id, items in other_warehouses.items():
        print(f"Items in warehouse {warehouse_id}:")
        for item in items:
            print(f"- {item['state']} {item['category'].lower()}")

    print()
    print("Total items in warehouse 1:", amount_in_warehouse1)
    total = amount_in_warehouse1
    for warehouse_id, items in other_warehouses.items():
        total_warehouse = len(items)
        total = total + total_warehouse
        print(f"Total items in warehouse {warehouse_id}:", total_warehouse)

    return f"Listed {total} items"


def search_item(searched_item):
    """Search an item in all warehouses."""
    results = {}
    for item in stock:
        full_name = f"{item['state']} {item['category'].lower()}"
        if full_name.lower() == searched_item.lower():
            warehouse_id = str(item["warehouse"])
            if str(warehouse_id) not in results:
                results[warehouse_id] = []
            results[warehouse_id].append(item)
    return results


def print_warehouse_list(warehouse):
    """Print a list from a single warehouse."""
    for item in warehouse:
        date_of_stock = datetime.strptime(item['date_of_stock'], '%Y-%m-%d %H:%M:%S')
        time_passed = str(datetime.now() - date_of_stock)
        days_passed = time_passed.split(",").pop(0)
        stock_text = f"in stock for {days_passed}"
        print(f"- Warehouse {item['warehouse']} ({stock_text})")


def print_results(**warehouses):
    """Print the results of a search."""
    # Get the total amount
    totals = [len(items) for items in warehouses.values()]
    total_amount = sum(totals)

    # Print results
    print("Amount available:", total_amount)
    if total_amount:
        print("Location:")
        for items in warehouses.values():
            print_warehouse_list(items)

        if len(warehouses) > 1:
            max_availability = max(*totals)
            max_warehouse = next(iter([id for id, items in warehouses.items()
                                       if len(items) == max_availability]), None)
            print(f"Maximum availability: {max_availability} in Warehouse {max_warehouse}")
    else:
        print("Location: Not in stock")


def order_an_item(searched_item, **warehouses):
    """Order an item from the list in either warehouse."""
    # Get the total amount
    totals = [len(items) for items in warehouses.values()]
    total_amount = sum(totals)

    if total_amount:
        print()
        order = input("Would you like to order this item?(y/n) ")
        if order == "y":
            place_an_order(searched_item, total_amount)


def get_employee(personnel_list, password):
    """Return the employee matching user_name and password."""
    result = None
    for user in personnel_list:
        if user["user_name"] == params["user_name"] and user["password"] == password:
            return user
        if "head_of" in user:
            result = get_employee(user["head_of"], password)
    return result


# Decorator
def employees_only(func):
    """Protect a function."""
    def inner(*args, **kwargs):
        """Allow only authenticated users to call the func."""
        if params["is_authenticated"]:
            func(*args, **kwargs)
        else:
            password = input("Please, type your employee password: ")
            employee = None
            for user in personnel:
                if user["user_name"] == params["user_name"] and user["password"] == password:
                    employee = user
            employee = get_employee(personnel, password)
            if employee:
                params["is_authenticated"] = True
                print()
                func(*args, **kwargs)
            else:
                again = input("There is no user with these credentials.\n"
                              "Would you like to try again?(y/n) ")
                if again.lower() in ["y", "yes"]:
                    params["user_name"] = get_user_name()
                    inner(*args, **kwargs)
    return inner


@employees_only
def place_an_order(searched_item, total_amount):
    """Place the order."""
    amount = int(input("How many would you like? "))
    if amount > total_amount:
        print("*" * 50)
        print("There are not this many available.",
              "The maximum amount that can be ordered is", total_amount)
        print("*" * 50)
        accept_available = input("Would you like to order the maximum available?(y/n) ")
        if accept_available == "y":
            amount = total_amount
    if amount <= total_amount:
        print(amount, searched_item, "have been ordered.")


def search_and_order_item():
    """Search and order an item."""
    searched_item = input("What is the name of the item? ")
    search_results = search_item(searched_item)

    print_results(**search_results)

    order_an_item(searched_item=searched_item, **search_results)

    return f"Searched a {searched_item}."


def browse_by_category():
    """Provide a category menu to list all items in the category."""
    categories = OrderedDict()
    # We will temporarily store all the categories in <categories>
    # We use an OrderedDict, because this way we can map the user input
    # with the category name.
    for item in stock:
        # If the category of this item is not in the previous OrderedDict,
        # we create the key and assign it the current counter (0).
        if item["category"] not in categories.keys():
            categories[item["category"]] = 0
        # Increase the counter for this category.
        categories[item["category"]] += 1

    # Print the category menu
    option_number = 1
    for category, amount in categories.items():
        print(f"{option_number}. {category} ({amount})")
        option_number += 1

    # Get the input selection
    chosen_number = int(input("Type the number of the category to browse: "))
    # Get the name of that category
    category_list = list(categories.items())
    chosen_name = category_list[chosen_number - 1][0]
    # Show all items from the selected option
    print()
    print(f"List of {chosen_name.lower()}s available:")
    for item in stock:
        if item["category"] == chosen_name:
            full_name = f"{item['state']} {item['category'].lower()}"
            print(f"{full_name}, Warehouse {item['warehouse']}")

    return f"Browsed the category {chosen_name}"


def run():
    """Execute the tool."""
    # Initial menu options
    stop_running = False
    operation = get_selected_operation()
    result = []

    print()

    if operation == "1":
        result.append(list_items_by_warehouse())

    elif operation == "2":
        result.append(search_and_order_item())

    elif operation == "3":
        result.append(browse_by_category())

    elif operation == "4":
        stop_running = True

    else:
        print("*" * 50)
        print(operation, "is not a valid operation.")
        print("*" * 50)

    if not stop_running:
        print()
        again = input("Would you like to perform another operation?(y/n) ")
        if again.lower() in ["y", "yes"]:
             result = result + run()
    return result


def print_session_summary(actions):
    """Print a summary of the actions takedn during this session."""
    print("\nThank you for your visit,", params["user_name"] + "!")
    print("In this session you have:")
    for num, action in enumerate(actions):
        print(f"\t{num+1}. {action}")


# Get the user name
params["user_name"] = get_user_name()
greet_user()
log = run()
print_session_summary(log)
