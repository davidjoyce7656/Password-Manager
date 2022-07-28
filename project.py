from cryptography.fernet import Fernet
from time import sleep
import csv
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
    sleep(1)
    print("""
Please choose from the following options
(1) Create key (If not already created)
(2) Add a passwords
(3) View saved passwords
(4) Generate a random password
(q) Quit program
""")
    try:
        users_input = input(">>> ").lower()
        if users_input == "1":
            generate_key()
        elif users_input == "2":
            add_password()
        elif users_input == "3":
            print(view_password())
        elif users_input == "4":
            generate_password()
        elif users_input == "":
            print("No valid input")
            main()
        elif users_input == "q" or "quit":
            print("Goodbye!")
            quit()
    except KeyboardInterrupt:
        print("\nProgram terminated!")
        
        
def generate_key():
    key_generation = Encryptor()
    if os.path.exists('mykey.key'):
        print("Key already exists!")
        sleep(0.5)
    else:
        user_key = key_generation.create_key()
        key_generation.write_key(user_key, 'mykey.key')
        print("Master key has been created!")
        pass_file = open("passwords.csv", "w")
        pass_file.close()
        
        encryptor = Encryptor()
        key_file = encryptor.load_key('mykey.key')
        encryptor.file_encryption(key_file, 'passwords.csv', 'passwords.csv')
    main()


def add_password():
    try:
        encryptor = Encryptor()
        load_key = encryptor.load_key('mykey.key')
        encryptor.file_decrypt(load_key, 'passwords.csv', 'passwords.csv')
        website = input("Enter site: ").capitalize()
        user_name = input("Enter Username/Email: ")
        password = input("Enter password: ")

        with open("passwords.csv", "a") as passfile:
            write_pass = csv.writer(passfile, delimiter=',')
            write_pass.writerow([website, user_name, password])
        print("Information saved!")

        encryptor.file_encryption(load_key, 'passwords.csv', 'passwords.csv')
        main()
    
    except FileNotFoundError:
        print("File not found, please select the first option to create the necessary files to continue!")
        main()
    

def view_password():
    try:
        decryptor = Encryptor()
        load_key = decryptor.load_key('mykey.key')
        decryptor.file_decrypt(load_key, 'passwords.csv', 'passwords.csv')

        with open('passwords.csv', 'r') as file:
            print(file.read())

        print("Hit Enter to return to the menu")    
        go_back = input(">>> ")

        while True:
            if go_back == "":
                decryptor.file_encryption(load_key, 'passwords.csv', 'passwords.csv')
                main()
            else:
                view_password()
    except FileNotFoundError:
        print("File not found, please select the first option to create the necessary files to continue!")
        main()
        

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
            main()
        else:
            generate_password()
    
    
    
if __name__ == "__main__":
    main()