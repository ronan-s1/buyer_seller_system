import socket
import sys
import threading

class Client:
    def __init__(self, buyer_id, host="localhost", port=5000):
        self.buyer_id = buyer_id
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.server_address = (host, port)

    def send_msg(self, msg):
        self.client.sendto(msg.encode(), self.server_address)


    def recv_msg_thread(self):
        while True:
            print(self.client)
            data, _ = self.client.recvfrom(1024)
            msg = data.decode()
            print(msg)

    def start_recv_msg_thread(self):
        recv_thread = threading.Thread(target=self.recv_msg_thread)
        recv_thread.start()

    

if __name__ == "__main__":
    valid_commands = ["buy <int>", "list", "quit", "join", "leave"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    joined = False
    
    client = Client(buyer_id, host, port)
    client.start_recv_msg_thread()
    
    print(f"Buyer {buyer_id} connected to {host}:{port}\n")

    while True:
        request = input(f"Enter your request ({', '.join(valid_commands)}): ").lower()

        if (request not in valid_commands[1:]) and not (request.startswith("buy")):
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
                continue

            elif request == "list":
                client.send_msg("list")

            elif request.startswith("buy"):
                try:
                    amount = int(request.split()[1])
                    if amount > 0:
                        client.send_msg(f"buy {amount} {buyer_id}")
                    else:
                        print("Amount must be greater than 0!")
                        continue
                except (IndexError, ValueError):
                    print("Invalid 'buy' command. Usage: buy <integer>")
                    continue
