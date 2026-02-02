from random import choice
import string

import json
import os
USER_INFO_FILE = "user_info.json"
USER_CART_FILE = "user_cart.json"


user_info={"subhash":"Subhash@mits1234","prasanth":"p1016@bkk"}
shopping_cart={"electronics":{"smart phone":25000, "laptop":50000, "LED TV":45000, "music speakers":10000, "bluetooth":1500},"fashion":{"shirt":1000,"pant":1000,"saree":1500,"silk saree":5000, "blazer":2000, "T-Shirt":750,"Inner Wear":800,"ChudiDhar":2500},"furniture":{"Dining Table":15000,"chair":2000,"cot":25000,"sofa":30000,"booksShelves":13000},
               "books":{"Ramayan":1500,"mahabarath":1800,"pyhon":1200,"C":1150,"Java":1850,"Machine Learning":2000,"Full Stack":1900},
               "grocery":{"sugar":55,"Red Gram":85,"salt":35,"chilli powder":75,"Oil":130,"Rice":1600,"Groundnuts":100,"pasta":60,"bread":60,"honey":250}}
user_shopping_cart={}



def load_data():
    global user_info, user_shopping_cart
    if os.path.exists(USER_INFO_FILE):
        with open(USER_INFO_FILE, "r") as f:
            user_info = json.load(f)
    if os.path.exists(USER_CART_FILE):
        with open(USER_CART_FILE, "r") as f:
            user_shopping_cart = json.load(f)

def save_data():
    with open(USER_INFO_FILE, "w") as f:
        json.dump(user_info, f, indent=4)
    with open(USER_CART_FILE, "w") as f:
        json.dump(user_shopping_cart, f, indent=4)



def display_user_info():
    print("User Information")
    print("-----------------")
    print("UserName","Password",sep="--") 
    for user in user_info:
        print(user,user_info[user],sep="--")
display_user_info()
def validate_password(password):
    upper=string.ascii_uppercase
    lower=string.ascii_lowercase
    special_chars=string.punctuation
    digits="0123456789"
    valid=False
    u=any(x in upper for x in password)
    l=any(x in lower for x in password)
    d=any(x in digits for x in password)
    sp=any(x in digits for x in password)
    size=len(password)>=8
    if u and l and d and sp and size:
        valid=True
    return valid

def generate_password():
    upper=string.ascii_uppercase
    lower=string.ascii_lowercase
    special_chars=string.punctuation
    digits="0123456789"
    password=""
    password+=choice(upper)
    password+=choice(lower)
    password+=choice(special_chars)
    for i in range(5):
        password+=choice(digits)
    return password
    
def register():
    global current_user
    print("Welcome to Registration")
    print("------------------------")
    userName=input("Enter the UserName:")
    if userName in user_info:
        while True:
            print("UserName Already Exist! Try Again")
            userName=input("Enter the UserName Again:")
            if userName not in user_info:
                break
    password=input("Enter The Password:")
    if validate_password(password):
        user_info[userName]=password
        current_user=userName
        save_data()
        print("Registration is Successful!..")
        print(f"Welcome {userName.title()}")
    else:
        print("Your Password is Invalid")
        choice=int(input("Can I generate the Password for YOu [1.Yes 2.No]:"))
        if choice==1:
            password=generate_password()
            user_info[userName]=password
            save_data()
            current_user=userName
            print("Registration is Successful!..")
            print(f"Welcome {userName.title()}")
            print("Your password is -->",password)
        else:
            
            while True:
                password=input("ReEnter the Password Again:")
                if validate_password(password)==True:
                    user_info[userName]=password
                    current_user=userName
                    save_data()
                    print("Registration is Successful!..")
                    print(f"Welcome {userName.title()}")
                    break
    shopping_cart_main()


def login():
    global current_user
    userName=input("Enter the userName:".title())
    if userName in user_info:
        password=input("Enter the Password:")
        if user_info[userName]==password:
            print("Your details are exist in the dataBase".title())
            current_user=userName
            print(f"Welcome {userName.title()}")
        else:
            print("Invalid Credentials! Try Again..")
            login()
    else:
        print("Invalid Credentials! Try Again..")
        login()

    shopping_cart_main()


def reset_password():
    
        userName=input("Enter the userName:")
        if userName in user_info:
            password=generate_password()
            user_info[userName]=password
            save_data()
            print("Your Password is Updated!")
            print("New Password:",password)
        else:
            print("Invalid UserName! Try Again")
            reset_password()

def forgot_password():
    print("To Know Your Details:")
    userName=input("Enter the UserName:")
    if userName in user_info:
        print("Your Password-->",user_info[userName])
    else:
        print("Invalid userName! Try Again")
        forgot_password()


#shopping cart funtions

def display_cart():
    print("Cart Contains:")
    print("---------------------------")
    for category, items in shopping_cart.items():
        print(f"\n{category.upper()} Items:")
        print("-" * 40)
        for item, price in items.items():
            print(f"{item:<25} ₹{price}")
        

def display_your_cart():
    global current_user
    if current_user is None:
        print("Please login to view your cart.")
        return

    if current_user not in user_shopping_cart or not user_shopping_cart[current_user]:
        print("Your cart is empty.")
        return

    print(f"\n{current_user.title()}'s Shopping Cart")
    print("-" * 45)
    print(f"{'Item':<20} {'Quantity':<10} {'Price (₹)':>10}")
    print("-" * 45)

    total = 0
    for item, details in user_shopping_cart[current_user].items():
        quantity = details["Quantity"]
        price = details["Price"]
        total += price
        print(f"{item:<20} {quantity:<10} {price:>10}")
    
    print("-" * 45)
    print(f"{'Total':<30} ₹{total:>10}")

              
def add_item_to_cart():
    global current_user
    if current_user is None:
        print("Please login to add items.")
        return

    print("Please select the item from the available products:")
    print("(Type the exact item name as shown.)")

    for category, items in shopping_cart.items():
        print(f"\n{category.upper()} Items:")
        print("-" * 40)
        for item, price in items.items():
            print(f"{item:<25} ₹{price}")

    item = input("\nEnter the item you need: ").strip().lower()
    found = False
    item_price = 0
    item_original = ""

    for category, items in shopping_cart.items():
        for name, price in items.items():
            if name.lower() == item:
                found = True
                item_price = price
                item_original = name
                break
        if found:
            break

    if not found:
        print("Item not found! Please enter an item exactly as shown above.")
        return

    try:
        quantity = int(input("Enter quantity you need: "))
        if quantity <= 0:
            print("Quantity must be positive.")
            return
    except ValueError:
        print("Invalid quantity. Must be an integer.")
        return

    if current_user not in user_shopping_cart:
        user_shopping_cart[current_user] = {}

    if item_original in user_shopping_cart[current_user]:
        user_shopping_cart[current_user][item_original]["Quantity"] += quantity
        user_shopping_cart[current_user][item_original]["Price"] += item_price * quantity
    else:
        user_shopping_cart[current_user][item_original] = {
            "Quantity": quantity,
            "Price": item_price * quantity
        }
    save_data()

    print(f"{quantity} x {item_original} added to your cart (Total ₹{item_price * quantity})")
    display_your_cart()


def delete_item_from_cart():
    global current_user
    if current_user is None:
        print("Please login to delete items.")
        return

    if current_user not in user_shopping_cart or not user_shopping_cart[current_user]:
        print("Your cart is empty.")
        return

    print(f"\n{current_user.title()}'s Cart Items:")
    for item in user_shopping_cart[current_user]:
        print(f"- {item}")

    item_to_delete = input("Enter the item name to delete: ").strip()

    if item_to_delete in user_shopping_cart[current_user]:
        del user_shopping_cart[current_user][item_to_delete]
        save_data()
        print(f"{item_to_delete} has been removed from your cart.")
    else:
        print(f"{item_to_delete} not found in your cart.")
    display_your_cart()

def update_cart():
    display_your_cart()
    global current_user
    if current_user is None:
        print("Please login to update your cart.")
        return

    if current_user not in user_shopping_cart or not user_shopping_cart[current_user]:
        print("Your cart is empty.")
        return

    item = input("Enter the item name to update: ").strip()
    if item not in user_shopping_cart[current_user]:
        print("Item not found in your cart.")
        return

    quantity = int(input("Enter new quantity: "))
    for category in shopping_cart.values():
        if item in category:
            price = category[item]
            break

    user_shopping_cart[current_user][item]["Quantity"] = quantity
    user_shopping_cart[current_user][item]["Price"] = price * quantity
    save_data()
    print("Cart updated successfully.")
    display_your_cart()
                
def main():
    print(" Welcome to Shopping Mall ".center(75,"*"))
    while True:
        print("\nAvailable Options:")
        print("------------------")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Forgot Password")
        print("5. Exit")
        choice=int(input("Enter Your Choice:"))
        if choice==1:
            register()
            break
        elif choice==2:
            login()
            break
        elif choice==3:
            reset_password()
            break
        elif choice==4:
            forgot_password()
            break
        elif choice==5:
            break
        else:
            print("Invalid Choice! Enter your Choice Again")




def shopping_cart_main():
    while True:
        print("\nYou Can Perform:")
        print("------------------")
        print("1. Display The Products")
        print("2. View Your Cart")
        print("3. Add Item to Cart")
        print("4. Delete Item From Cart")
        print("5. Update Your Cart")
        print("6. Exit")
        choice=int(input("Enter Your Choice:"))
        if choice==1:
            display_cart()
        elif choice==2:
            display_your_cart()
        elif choice==3:
            add_item_to_cart()
        elif choice==4:
            delete_item_from_cart()
        elif choice==5:
            update_cart()
        elif choice==6:
            display_your_cart()
            break
        else:
            print("Invalid Choice! Enter Valid Option..")
    
load_data()       
main()
