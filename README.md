# PASSWORD MANAGER

This is my first project that I've created as a final project for CS50, this is my first dive into creating a program with cryptography so I will warn:
# DO NOT USE THIS A REGULAR PASSWORD MANAGER
I have an obsession with security and privacy, so this is my first crack at it!

### Generating a key
The Encryption Method I used was Fernet. Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography. By creating an Encryptor class, I can then automate the process of creating a key, storing that key and able to retrieve it when I need to view my encrypted files. The key is automatically paired with the password file, so we will no longer need to create another key. If the key is accidentally deleted, the file will be no longer accessible. 


### Adding a password
When adding a password, the class method is called to load the key that was created when the program is first ran, if the key or password file has not been created (which is automatically done with the first option), you will see an error stating that you need to select the first option in order to continue. You can add any value you wish to the encrypted file. The file is decrypted with the key we created, the information the user has provided will then be added to the file. Then after the information has been saved, the file will close then will be encrypted once again, keeping your information safe.


### View password
If you need to view information you have stored already within the password file, the view password option will then decrypt the file, display the information saved within the file and as soon as you hit the enter button, the file is then encrypted once again and can only be viewable through the command line via the program.


### Generating a random password
Here I implemented an option to spit out a random string that consist of random uppercased, lowercased and digits to form a password that would be harder to crack than a generic password would be. You can input how long you would like your password, but if you enter a value lower than 8, you'll be re-prompted to enter a higher value(having a short password may not be a good security practice for your accounts).
