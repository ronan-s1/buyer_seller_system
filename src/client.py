import socket
import sys
import threading
from colours import *

BUFFER = 3000

class Client:
    def __init__(self, buyer_id, host="127.0.0.1", port=9999):
        self.buyer_id = buyer_id
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.server_address = (host, port)

    def send_msg(self, msg):
        self.client.sendto(msg.encode(), self.server_address)


    def recv_msg(self):
        while True:
            data, _ = self.client.recvfrom(BUFFER)
            msg = data.decode()
            print(msg)
            break
    

if __name__ == "__main__":
    valid_commands = ["buy <int>", "list", "quit", "join", "leave"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    joined = False
    
    client = Client(buyer_id, host, port)
    # client.start_recv_msg()
    
    print(f"{HEADER}Buyer {buyer_id} connected to {host}:{port}{ENDC}\n")

    while True:
        request = input(f"Enter your request ({', '.join(valid_commands)}): ").lower()

        if (request not in valid_commands[1:]) and not (request.startswith("buy")):
            print(f"{WARNING}Invalid command!{ENDC}")

        elif request == "join" and joined:
            print(f"{WARNING}You are already in the market.{ENDC}")

        elif request == "join":
            joined = True
            print(f"{GREEN}You have joined the market.{ENDC}")

        elif not joined:
            print(f"{WARNING}You are not currently in the market. Use 'join' to enter.{ENDC}")

        elif joined:
            if request == "quit":
                print("Exiting...")
                client.send_msg(f"{FAIL}Buyer {buyer_id} has left and quit the market!{ENDC}")
                break

            elif request == "leave":
                joined = False
                print(f"{FAIL}You have left the market.{ENDC}")
                continue

            elif request == "list":
                client.send_msg("list")

            elif request.startswith("buy"):
                try:
                    amount = int(request.split()[1])
                    if amount > 0:
                        client.send_msg(f"buy {amount} {buyer_id}")
                    else:
                        print(f"{WARNING}Amount must be greater than 0!{ENDC}")
                        continue
                except (IndexError, ValueError):
                    print(f"{WARNING}Invalid 'buy' command. Usage: buy <integer>{ENDC}")
                    continue
            
            client.recv_msg()
