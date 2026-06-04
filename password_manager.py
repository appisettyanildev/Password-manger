from cryptography.fernet import Fernet
import json
import os

KEY_FILE = "key.key"
DATA_FILE = "passwords.json"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as file:
        file.write(key)


def load_key():
    return open(KEY_FILE, "rb").read()


if not os.path.exists(KEY_FILE):
    generate_key()

cipher = Fernet(load_key())


def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        encrypted_data = json.load(file)

    passwords = {}

    for site, encrypted_password in encrypted_data.items():
        passwords[site] = cipher.decrypt(
            encrypted_password.encode()
        ).decode()

    return passwords


def save_passwords(passwords):
    encrypted_data = {}

    for site, password in passwords.items():
        encrypted_data[site] = cipher.encrypt(
            password.encode()
        ).decode()

    with open(DATA_FILE, "w") as file:
        json.dump(encrypted_data, file, indent=4)


def add_password():
    site = input("Website: ")
    password = input("Password: ")

    passwords = load_passwords()
    passwords[site] = password
    save_passwords(passwords)

    print("Password saved.")


def view_password():
    site = input("Website: ")

    passwords = load_passwords()

    if site in passwords:
        print(f"Password: {passwords[site]}")
    else:
        print("Not found.")


def main():
    while True:
        print("\n1. Add Password")
        print("2. View Password")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_password()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
