import socket
import sys

class Client:
    def __init__(self, host = "localhost", port = 5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_msg(self, msg):
        self.socket.send(msg.encode())

    def receive_msg(self):
        try:
            msg = self.socket.recv(1024).decode()
            if msg == "ack":
                return
            print(msg)
            # return
        except:
            print("Connection lost!")
            self.socket.close()


if __name__ == "__main__":
    valid_commands = ["buy", "list", "quit"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])

    client = Client(host, port)
    print(f"Buyer {buyer_id} connected to {host}:{port}")

    while True:
        prompt = f"Buyer {buyer_id}, enter your request ({', '.join(valid_commands)}): "
        request = input(prompt).lower()

        if request in valid_commands:
            if request == "quit":
                print("Exiting...")
                client.send_msg(f"Buyer {buyer_id} has left the market!")
                break

            client.send_msg(request)
            client.receive_msg()
        else:
            print("Invalid command!")
