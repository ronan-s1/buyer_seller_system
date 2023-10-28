import socket
import sys

class Client:
    def __init__(self, host = "localhost", port = 5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_msg(self, msg):
        self.socket.send(msg.encode())

    def receive_msg(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode()
                print(msg)
            except:
                print("Connection lost!")
                self.socket.close()
                break


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])

    client = Client(host, port)
    print(f"Buyer {buyer_id} connected to {host}:{port}")
    while True:
        # Get user input
        request = input(f"Buyer {buyer_id}, enter your request ('buy', 'list', or 'quit'): ")
        if request == "quit":
            print("Exiting...")
            break
        # Send the request to the server
        client.send_msg(request)
        # Receive and print the response from the server
        client.receive_msg()