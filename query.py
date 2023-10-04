"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import warehouse1, warehouse2

# YOUR CODE STARTS HERE
def list_items_by_warehouse():
    print("\nItems in Warehouse 1:")
    for item in warehouse1:
        print(item)

    print("\nItems in Warehouse 2:")
    for item in warehouse2:
        print(item)

def search_and_place_order(item_name):
    total_amount = 0
    locations = []

    if item_name in warehouse1:
        total_amount += warehouse1.count(item_name)
        locations.append("Warehouse 1")

    if item_name in warehouse2:
        total_amount += warehouse2.count(item_name)
        locations.append("Warehouse 2")

    if total_amount == 0:
        print("Not in stock")
        return

    print(f"\nAmount available: {total_amount}")
    if len(locations) == 1:
        print(f"Location: {locations[0]}")
    elif len(locations) == 2:
        print(f"Location: Both warehouses")
        max_location = max(set(locations), key=locations.count)
        max_available = locations.count(max_location)
        print(f"Maximum availability: {max_available} in {max_location}")

    order_choice = input("Would you like to order this item? (y/n) ").lower()
    if order_choice == "y":
        desired_amount = int(input("How many would you like? "))
        if desired_amount <= total_amount:
            print(f"{desired_amount} {item_name} have been ordered.")
        else:
            print(f"**************************************************")
            print(f"There are not this many available. The maximum amount that can be ordered is {total_amount}")
            print(f"**************************************************")
            max_order_choice = input("Would you like to order the maximum available? (y/n) ").lower()
            if max_order_choice == "y":
                print(f"{total_amount} {item_name} have been ordered.")

def main():
    # Get the user name
    user_name=input("please enter your name: ")
    # Greet the user
    print(f"Hello{user_name}")

    # Show the menu and ask to pick a choice
    while True:
        print(f"\nMenu:")
        print("1. List items by warehouse")
        print("2. Search an item and place an order")
        print("3. Quit")
        choice=input("Please choose one of the option (1/2/3):")
        # If they pick 1
        if choice =="1":
            print("\nItems by Warehouse1:")
            for x in warehouse1:
                print(x)
            print("\nItems by Warehouse2:")
            for x in warehouse2:
                print(x)                
        # Else, if they pick 2
        elif choice == '2':
            # Search an item and place an order
            item_name = input("Enter the item name to search: ")
            search_and_place_order(item_name)
            # Else, if they pick 3
        elif choice == '3':
            # Quit
            print(f"Thank you for visiting, {user_name}!")
            break
        # Else
        else:
            print(30*"*",f"\n{choice} is not a valid operation.")
            print(30*"*")
            print(f"Thank you for visiting, {user_name}!")
            break

# Thank the user for the visit
if __name__ == "__main__":
    main()