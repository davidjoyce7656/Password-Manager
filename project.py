from cryptography.fernet import Fernet
from time import sleep
import csv
import getpass
import os
import random
import string



class Encryptor():
    def create_key(self):
        key = Fernet.generate_key()
        return key
    
    def write_key(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)
            
    def load_key(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key
    
    def file_encryption(self, key, original_file, encrypted_file):
        fernet = Fernet(key)
        
        with open(original_file, 'rb') as file:
            original_file = file.read()
            
        encrypted = fernet.encrypt(original_file)
        
        with open(encrypted_file, 'wb') as file:
            file.write(encrypted)
    
    def file_decrypt(self, key, encrypted_file, decrypted_file):
        f = Fernet(key)
        
        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()
            
        decrypted = f.decrypt(encrypted)
        
        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)
            
            


print("Welcome to Password Manager")

def main():
    print("""
Choose an option(1 or 2):
(1) Sign In
(2) Sign Up
(q) Quit
""")
    
    try:
        users_input = input(">>> ").lower()
        if users_input == "1":
            profile()
        elif users_input == "2":
            create_profile()
        elif users_input == "":
            print("No valid input")
            sleep(0.5)
            main()
        elif users_input == "q" or "quit":
            print("Goodbye!")
            quit()
        
    except KeyboardInterrupt:
            print("\nProgram terminated!")
            quit()
        
def menu():
        sleep(1)
        print("""
Please choose from the following option:
(1) Add a passwords
(2) View saved passwords
(3) Generate a random password
(q) Sign Out
""")
        try:
            users_input = input(">>> ").lower()
            if users_input == "1":
                add_password()
            elif users_input == "2":
                print(view_password())
            elif users_input == "3":
                generate_password()
            elif users_input == "":
                print("No valid input")
                sleep(0.5)
                menu()
            elif users_input == "q" or "quit":
                print("Signed Out!")
                sleep(0.5)
                main()
        except KeyboardInterrupt:
            print("\nProgram terminated!")
            quit()
        
def create_profile():
    global user
    user = input("Username: ")
    generate_key(user)
    password = getpass.getpass("Password: ")
    
    with open(f"{user}_creds.csv", "w") as file:
        write_file = csv.writer(file, delimiter=",")
        write_file.writerow([user, password])
        
    encrypt = Encryptor()
    key = encrypt.load_key(f"{user}.key")
    encrypt.file_encryption(key, f"{user}_creds.csv", f"{user}_creds.csv")
    print("Profile created!")
    menu()    

def profile():
    global user
    user = input("Username: ")
    decrypt = Encryptor()
    if not os.path.exists(f"{user}.key"):
        print("User does not exist!")
        sleep(0.5)
        main()
    else:
        key = decrypt.load_key(f"{user}.key")
        decrypt.file_decrypt(key, f"{user}_creds.csv", f"{user}_creds.csv")
        password = getpass.getpass("Password: ")

        file = open(f"{user}_creds.csv", 'r')
        for i in file:
            name, pwd = i.split(',')
            pwd = pwd.strip()
            if name == user and pwd == password:
                print("Login Successful")
                decrypt.file_encryption(key, f"{user}_creds.csv", f"{user}_creds.csv")
                menu()
            else:
                print("Login failed!")
                decrypt.file_encryption(key, f"{user}_creds.csv", f"{user}_creds.csv")
                main()
                
    

    
            
def generate_key(username):
    key_generation = Encryptor()
    if os.path.exists(f'{username}.key'):
        print("User already exists!")
        sleep(0.5)
    else:
        user_key = key_generation.create_key()
        key_generation.write_key(user_key, f'{username}.key')
        pass_file = open(f"{username}_passwords.csv", "w")
        pass_file.close()
        
        encryptor = Encryptor()
        key_file = encryptor.load_key(f'{username}.key')
        encryptor.file_encryption(key_file, f'{username}_passwords.csv', f'{username}_passwords.csv')


def add_password():
    try:
        encryptor = Encryptor()
        load_key = encryptor.load_key(f'{user}.key')
        encryptor.file_decrypt(load_key, f'{user}_passwords.csv', f'{user}_passwords.csv')
        website = input("Enter site: ").capitalize()
        user_name = input("Enter Username/Email: ")
        password = input("Enter password: ")

        with open(f"{user}_passwords.csv", "a") as passfile:
            write_pass = csv.writer(passfile, delimiter=',')
            write_pass.writerow([website, user_name, password])
        print("Information saved!")

        encryptor.file_encryption(load_key, f'{user}_passwords.csv', f'{user}_passwords.csv')
        menu()
    
    except FileNotFoundError:
        print("File not found, please select the first option to create the necessary files to continue!")
        menu()
    

def view_password():
    try:
        decryptor = Encryptor()
        load_key = decryptor.load_key(f'{user}.key')
        decryptor.file_decrypt(load_key, f'{user}_passwords.csv', f'{user}_passwords.csv')

        with open(f'{user}_passwords.csv', 'r') as file:
            print(file.read())

        print("Hit Enter to return to the menu")    
        go_back = input(">>> ")

        while True:
            if go_back == "":
                decryptor.file_encryption(load_key, f'{user}_passwords.csv', f'{user}_passwords.csv')
                menu()
            else:
                view_password()
    except FileNotFoundError:
        print("File not found, please select the first option to create the necessary files to continue!")
        menu()
        

def generate_password():
    try:
        length = int(input("How long would you like your password? "))
        if length <= 7:
            print("Too short for a password!")
            generate_password()
        else:
            random_password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)) 
            print(random_password)
    except ValueError:
        print("Invalid Input!")
        generate_password()
        
    print("Hit Enter to return to the menu")
    menu_return = input(">>> ")
    
    while True:
        if menu_return == "":
            menu()
        else:
            generate_password()
    
    
    
if __name__ == "__main__":
    main()