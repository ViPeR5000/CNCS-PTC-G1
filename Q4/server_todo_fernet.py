import os
import json
import socket
from cryptography.fernet import Fernet

# This class represents a single todo item
class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

# This class represents a list of TodoItems
class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description):
        item = TodoItem(title, description)
        self.items.append(item)

    def complete_item(self, index):
        if (index < 0 or index >= len(self.items)):
            raise IndexError("Invalid index")
        item = self.items[index]
        item.completed = True

    def count_items(self):
        return len(self.items)
    
    def save_cipher(self, key):
        cipher = Fernet(key)
        with open('todo_list.fernet', 'w') as file:
            for i, item in enumerate(self.items):
                plain_item = f"{item.title},{item.description},{item.completed}"
                c_item = cipher.encrypt(plain_item.encode()).decode()
                file.write(f"{c_item}\n")

    def get_list_of_items(self):
        result = ""
        for i, item in enumerate(self.items):
            status = "[ ]"
            if item.completed:
                status = "[x]"
            result += f"{i}. {status} {item.title}: {item.description}\n"
        return result

host = 'localhost'
port = 8888

# load key
with open('key.fernet', 'rb') as key_file:
    key = key_file.read()
    #key = key.strip()
    print("Loaded key: ", key)

# check if todo_list.fernet exists
try:
    with open('todo_list.fernet', 'r') as file:
        todo_list = TodoList()
        for line in file:
            cipher = Fernet(key)
            c_item = line.strip()
            print("going to decrypt: ", c_item)
            plain_item = cipher.decrypt(c_item.encode()).decode()
            print("decrypted: ", plain_item)
            title, description, completed = plain_item.split(",")
            todo_list.add_item(title, description)
except FileNotFoundError:
    with open('todo_list.fernet', 'w') as file:
        file.write("")
    todo_list = TodoList()

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server started on port {port}...")
print("Serving todo list...")
print(todo_list.get_list_of_items())

# Loop forever, waiting for client commands
while True:
    # Accept a connection
    print("Waiting for connection...")
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # receive operation and numbers and make calculation
    command = client_socket.recv(1024).decode()
    print(f"Received command: {command}")
    choice, data = command.split("-")
    if choice == "1":
        title, description = data.split(",")
        todo_list.add_item(title, description)
        result = "Todo added."
    elif choice == "2":
        result = todo_list.get_list_of_items()
    elif choice == "3":
        index = int(data)
        todo_list.complete_item(index)
        result = "Todo completed."
    else:
        result = "Invalid command."
    print("Logging: " + result)
    client_socket.send(result.encode())
    client_socket.close()
    todo_list.save_cipher(key)
