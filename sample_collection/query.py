"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import stock

# YOUR CODE STARTS HERE
from datetime import datetime
def main():
    # Get the user name
    user_name=input("please enter your name: ")
    # Greet the user
    print(f"Hello {user_name}")

    # Show the menu and ask to pick a choice
    while True:
        print(f"\nMenu:")
        print("1. List items by warehouse")
        print("2. Search an item and place an order")
        print("3. Browse by category")
        print("4. Quit")
        choice=input("Please choose one of the option (1/2/3/4):")
        # If they pick 1
        if choice =="1":
            items_in_warehouse_1=[]
            items_in_warehouse_2=[]
            for i in stock:
                item_fullname=i["state"]+" "+i["category"]
                if i["warehouse"]==1:
                    items_in_warehouse_1.append(item_fullname)
                else:
                    items_in_warehouse_2.append(item_fullname)

            print(f"Items in warehouse 1:{items_in_warehouse_1}")
            print(f"Total items in warehouse 1:{len(items_in_warehouse_1)}\n")
            print("="*50)
            print(f"Items in warehouse 2:{items_in_warehouse_2}")
            print(f"Total items in warehouse 2:{len(items_in_warehouse_2)}\n")
            print("="*50)
            print(f"Thank you for visiting, {user_name}!")
            break
        # Else, if they pick 2
        elif choice == '2':
            # Search an item and place an order
            item_name = input("Enter the item name to search: ").lower()
            search_item_state=" ".join(item_name.split()[:-1]).capitalize()
            search_item_category=item_name.split(" ")[-1].capitalize()
            location=[]
            items_in_warehouse_1=0
            items_in_warehouse_2=0
            for item in stock:
                if item["state"]==search_item_state and item["category"]==search_item_category:
                    date_str=item["date_of_stock"]
                    date_format="%Y-%m-%d %H:%M:%S"
                    number_of_days=(datetime.now()-datetime.strptime(date_str,date_format)).days
                    location.append("Warehouse "+str(item["warehouse"])+f"(in stock for {number_of_days} days)")
                    if item["warehouse"]==1:
                        items_in_warehouse_1+=1
                    else:
                        items_in_warehouse_2+=1
            total_amount=items_in_warehouse_1+items_in_warehouse_2
            if len(location)>0:
                print(f"\nAmount available: {total_amount}")
                print("location: ")
                for i in location:
                    print(i)
                order_choice = input("Would you like to order this item? (y/n) ").lower()
                if order_choice=="y":
                    desired_amount = int(input("How many would you like? "))
                    if desired_amount<=total_amount:
                        print(f"{desired_amount} {item_name} have been ordered.")
                    else:
                        print(f"**************************************************")
                        print(f"There are not this many available. The maximum amount that can be ordered is {total_amount}")
                        print(f"**************************************************")
                        max_order_choice = input("Would you like to order the maximum available? (y/n) ").lower()
                        if max_order_choice == "y":
                            print(f"{total_amount} {item_name} have been ordered.")
            else: 
                print("Amount available: 0")
                print("Location: Not in stock")
            print(f"Thank you for visiting, {user_name}!")
            break



        elif choice=="3":
            # Brows by category 
            list_item_category = []
            dict_item_category = {}
            for item in stock:
                list_item_category.append(item["category"])
            dict_item_category = {i: list_item_category.count(i) for i in list_item_category}
            print("Categories:")
            for index, (category, count) in enumerate(dict_item_category.items(), start=1):
                print(f"{index}. {category} ({count})")
            
            choose_category = input("Type the number of the category to browse: ")

            for index, (category, _) in enumerate(dict_item_category.items(), start=1):
                if index == int(choose_category):
                    print(f"List of {category} available:")
                    for item in stock:
                        if item["category"] == category:
                            print(f"{item['state']}{category}, Warehouse {item['warehouse']}")
            print(f"Thank you for your visit, {user_name}!")
            break       

            # Else, if they pick 4
        elif choice == '4':
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


