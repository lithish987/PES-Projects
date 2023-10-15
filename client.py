import socket

# Define the protocol
PROTOCOL = {
    "browse": 1,
    "purchase": 2,
    "response": 3
}

# Define the server address and port
SERVER_ADDRESS = "localhost"
SERVER_PORT = 9999

# Define the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

def send_command(command):
    # Send command to the server and receive the response
    client_socket.send(command.encode())
    response = client_socket.recv(1024).decode()
    return response.split("\n")[1:]

# Browse the inventory
response = send_command(str(PROTOCOL["browse"]))
items = response
print("Brands available for purchase:")
for item in items:
    name, quantity = item.split(",")
    print(f"{name} ({quantity} available)")

# Purchase items
item_to_purchase = input("Enter the brands to purchase (separated by commas):\t").split(",")
response = send_command(f"{PROTOCOL['purchase']} {' '.join(item_to_purchase)}")
for res in response:
   print(res)