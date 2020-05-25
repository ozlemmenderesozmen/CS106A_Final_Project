# Program is a stock tracking program which can be used especially by social media sales
# and also by any store, shops or supermarkets.
# Program has an inventory as a dictionary type, where the new products can be added,
# details of the products can be edited,
# out of stock products can be removed and
# sales to the customer can be made and customer bill can be prepared.


from time import strftime
import pandas as pd


def main():
    # an empty dictionary is formed and stored as inventory.
    # for the 'inventory' dictionary -> key = product id, value=[name, price, quantity]
    # To initialize the dictionary, some products were added as an example.
    inventory = {1: ['Apple', 2.99, 50],
                 2: ['Banana', 3.99, 50],
                 3: ['Cherry', 4.99, 100],
                 4: ['Orange', 1.99, 50],
                 5: ['Blackberry', 2.00, 1],
                 6: ['Strawberry', 2.49, 100],
                 7: ['Apricot', 2.99, 75],
                 8: ['Kiwi', 3.49, 75]}
    last_given_product_id = len(inventory)
    print_welcome_message()

    while True:
        print_main_menu()
        last_given_product_id = selection_of_operation(inventory, last_given_product_id)


def print_welcome_message():
    # Cash register program starts with an opening message and then date & time.
    print("---WELCOME TO CASH REGISTER PROGRAM---")
    print_current_time()
    print("")


def print_current_time():
    # 'time' function puts date (day month year) and time (hour:minutes:seconds) in two consecutive rows.
    print(strftime("%d %b %Y".center(30)))
    print(strftime("%H:%M:%S".center(32)))


def print_main_menu():
    # The operations and the keys to enter are listed with 'print_main_menu' function.
    print("Select your operation, please!\n"
          "'1' for starting a new sale\n"
          "'2' for adding item to inventory\n"
          "'3' for removing item from inventory\n"
          "'4' for editing details of an inventory item\n"
          "If you want to quit, please enter '0'")
    print("")


def selection_of_operation(inventory, last_given_product_id):
    # With "selection_of_operation" function, the operation can be selected by user.
    selection = get_integer_input_from_user("What is your selection? ")
    if selection == 1:
        start_a_new_sale(inventory)
    elif selection == 2:
        last_given_product_id = add_item(inventory, last_given_product_id)
    elif selection == 3:
        remove_item(inventory)
    elif selection == 4:
        edit_product_details(inventory)
    elif selection == 0:
        quit_program(inventory)
    elif selection != -1:  # No need to show another error message. We already showed.
        print("You entered an invalid number. Please try again.")

    return last_given_product_id


def print_inventory_list(inventory):
    # In order to print the dictionary as a table , a DataFrame is formed and stored as inventory_list.
    inventory_list = pd.DataFrame.from_dict(inventory, orient='index')
    inventory_list.columns = ['Name', 'Price', 'Quantity']
    print(inventory_list)


def start_a_new_sale(inventory):
    # Starting a new sale is possible by entering 1.
    print_inventory_header()
    print_inventory_list(inventory)
    print("")
    customer_list = []

    # The products sold to customer are appended to the customer list.
    while True:
        sold_product = get_integer_input_from_user("Please enter the product id to be sold: ")
        if sold_product in inventory.keys():
            quantity_of_sold_product = inventory[sold_product][2]
            if quantity_of_sold_product > 0:
                customer_list.append(sold_product)
                reduce_one_item_from_stock(inventory, sold_product)
                print("Product id: " + str(sold_product) + " is added to customer list.")
            else:
                print("Product id: " + str(sold_product) + " is out of stock")
        else:
            print(str(sold_product) + " is not a valid product id!")

        if ask_user_continue_or_quit("Will you sell another item? Yes or No"):
            break

    # When the sales over, customer bill is formed.
    customer_bill_list = {}
    total_price = 0
    for item in customer_list:
        if item in customer_bill_list.keys():
            customer_bill_list[item][2] += 1  # increases already sold product's quantity by 1.
        else:
            name = inventory[item][0]
            price = inventory[item][1]
            customer_bill_list[item] = [name, price, 1]
        total_price = total_price + customer_bill_list[item][1]

    print("")
    print_customer_bill_header()
    print_inventory_list(customer_bill_list)
    print("")
    print(str("%.2f" % total_price) + '$ for ' + str(len(customer_list)) + ' products.')
    print("")

    print_inventory_header()
    print_inventory_list(inventory)
    print("")

    print_sale_completed_header()


def reduce_one_item_from_stock(inventory, product_id):
    # This function will reduce the quantity of the product by 1.
    inventory[product_id][2] -= 1


def ask_user_continue_or_quit(message):
    # This function asks user to continue or end the current operation.
    answer = input(message)
    return answer == 'No' or answer == 'N' or answer == 'no' or answer == 'n'


def print_customer_bill_header():
    print("------------------------------")
    print("Customer Bill".center(30))
    print("------------------------------")


def print_inventory_header():
    print("-------------------------------")
    print("Inventory".center(30))
    print("-------------------------------")


def print_sale_completed_header():
    print("-------------------------------")
    print("Sale completed".center(30))
    print("-------------------------------")


def add_item(inventory, last_given_product_id):
    # Adding items to inventory is possible by entering 2.
    print_inventory_header()
    print_inventory_list(inventory)
    print("")

    while True:
        name = get_product_name_from_user()
        price = get_positive_float_number_from_user("Please enter the price of the new product: ")
        quantity = get_positive_integer_number_from_user("Please enter the quantity of the new product: ")

        last_given_product_id += 1
        inventory[last_given_product_id] = [name, price, quantity]

        if ask_user_continue_or_quit("Will you add another item? Yes or No"):
            break

    print_inventory_header()
    print_inventory_list(inventory)
    print("")

    return last_given_product_id


def remove_item(inventory):
    # Removing a product from the inventory is possible by entering 3.
    while True:
        print_inventory_header()
        print_inventory_list(inventory)
        print("")

        product_id = get_integer_input_from_user("Please enter the product id to be removed: ")
        if product_id in inventory.keys():
            del inventory[product_id]
            print("Product id: " + str(product_id) + " is removed.")
        else:
            print(str(product_id) + " is not a valid product id!")

        print_inventory_header()
        print_inventory_list(inventory)
        print("")

        if ask_user_continue_or_quit("Will you remove another item? Yes or No"):
            break


def edit_product_details(inventory):
    # Editing the details of the product in inventory is possible by entering 4.
    while True:
        print_inventory_header()
        print_inventory_list(inventory)
        print("")

        product_id = get_integer_input_from_user("Please enter the product id to be edited: ")

        if product_id in inventory.keys():
            new_name = get_product_name_from_user()
            new_price = get_positive_float_number_from_user("Please enter the new product price: ")
            new_quantity = get_positive_integer_number_from_user("Please enter the new product amount: ")

            inventory[product_id] = [new_name, new_price, new_quantity]
            print("Product id: " + str(product_id) + " is edited.")
        else:
            print(str(product_id) + " is not a valid product id!")

        print_inventory_header()
        print_inventory_list(inventory)
        print("")

        if ask_user_continue_or_quit("Will you edit another item? Yes or No"):
            break


def quit_program(inventory):
    # Quiting from the program is possible by entering 0.
    print_inventory_header()
    print_inventory_list(inventory)
    print("The program is closing")
    exit()


def get_product_name_from_user():
    # In order to prevent user mistake while entering the product name, this function is formed.
    new_name = input("Please enter the product name: ")
    while new_name == '':
        new_name = input("Product name is invalid. Please enter a product name: ")

    return new_name


def get_float_input_from_user(message):
    # In addition to user inputs, this function performs validity checks for float input.
    user_input = -1
    try:
        user_input = float(input(message))
    except ValueError:
        print("Please enter a numeric value.")

    return user_input


def get_integer_input_from_user(message):
    # In addition to user inputs, this function performs validity checks for integer input.
    user_input = -1
    try:
        user_input = int(input(message))
    except ValueError:
        print("Please enter an integer value.")

    return user_input


def get_positive_float_number_from_user(message):
    # In addition to user inputs, this function performs validity checks for positive float numbers.
    while True:
        user_input = get_float_input_from_user(message)
        if user_input > 0:
            return user_input


def get_positive_integer_number_from_user(message):
    # In addition to user inputs, this function performs validity checks for positive integer numbers.
    while True:
        user_input = get_integer_input_from_user(message)
        if user_input > 0:
            return user_input


if __name__ == '__main__':
    main()
