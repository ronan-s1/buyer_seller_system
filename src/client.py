import socket
import sys


class Client:
    def __init__(self, host="localhost", port=5000):
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
        except:
            print("Connection lost!")
            self.socket.close()


if __name__ == "__main__":
    valid_commands = ["buy", "list", "quit", "join", "leave"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])

    client = Client(host, port)
    print(f"Buyer {buyer_id} connected to {host}:{port}")

    joined = False

    while True:
        request = input(f"Enter your request ({', '.join(valid_commands)}): ").lower()

        if request not in valid_commands:
            print("Invalid command!")
            
        elif request == "join" and joined:
            print("You are already in the market.")

        elif request == "join":
            joined = True
            print("You have joined the market.")
            
        elif not joined:
            print("You are not currently in the market. Use 'join' to enter.")

        elif joined:
            if request == "quit":
                print("Exiting...")
                client.send_msg(f"Buyer {buyer_id} has left and quit the market!")
                break

            elif request == "leave":
                joined = False
                print("You have left the market.")
                
            elif request == "list":
                client.send_msg("list")
            
            
            
            
            if request != "leave":
                client.receive_msg()
                
