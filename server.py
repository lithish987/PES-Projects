import socket

# Define the protocol
PROTOCOL = {
    "browse": 1,
    "purchase": 2,
    "response": 3
}

# Define the inventory
inventory = {
        'iPhone13': 59,
        'iPhone12': 31,
        'iPhone11': 8,
        'iPhoneSE': 7,
        'iPhoneXR': 4,
        'GalaxyS21': 50,
        'GalaxyS20': 45,
        'GalaxyS10': 32,
        'GalaxyNote20': 56,
        'GalaxyA52': 120,
        'Pixel6': 70,
        'Pixel5': 40,
        'Pixel4a': 37,
        'Pixel3': 20,
        'Pixel2': 3,
        'OnePlus9Pro': 98,
        'OnePlus8Pro': 76, 
        'OnePlus7T': 130,
        'OnePlusNord': 54,
        'OnePlus6T': 51,
        'Mi11': 230,
        'Mi10T': 170,
        'RedmiNote10Pro': 400,
        'PocoX3Pro': 321,
        'Mi9T':211,
}

# Define the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 9999))
server_socket.listen()

print("Server waiting for response...")

def handle_client(client_socket):
    while True:
        # Receive command from the client
        command = client_socket.recv(1024).decode()

        if not command:
            # If the client disconnects, exit the loop
            break

        if command == str(PROTOCOL["browse"]):
            # If the client wants to browse the inventory, send it back
            response = "\n".join([f"{name},{quantity}" for name, quantity in inventory.items()])
            client_socket.send(f"{PROTOCOL['response']}\n{response}".encode())
        elif command.startswith(str(PROTOCOL["purchase"])):
            # If the client wants to purchase an item, deduct it from the inventory
            items = command.split()[1:]
            responses = []
            for item in items:
                if inventory.get(item, 0) > 0:
                    inventory[item] -= 1
                    remaining_qty = inventory.get(item, 0)
                    response = f"{PROTOCOL['response']}\nItem purchased: {item}, Remaining quantity: {remaining_qty}"
                else:
                    response = f"{PROTOCOL['response']}\nItem out of stock: {item}"
                responses.append(response)
            response = "\n".join(responses)
            client_socket.send(response.encode())

    client_socket.close()


# Listen for incoming connections and handle them in separate threads
while True:
    client_socket, address = server_socket.accept()
    print(f"Client connected from {address}")
    handle_client(client_socket)
