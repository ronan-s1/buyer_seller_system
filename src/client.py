import threading
from colours import *
import socket
import sys


class Client:
    def __init__(self, buyer_id, host="localhost", port=5000):
        self.buyer_id = buyer_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_msg(self, msg):
        self.socket.send(msg.encode())

    def recv_msg(self):
        try:
            msg = self.socket.recv(1024).decode()
            if not msg:
                return
            print(msg)
        except:
            print(f"{FAIL}Connection lost!{ENDC}")
            self.socket.close()


if __name__ == "__main__":
    valid_commands = ["buy <int>", "list", "quit", "join", "leave"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    joined = False
    client = Client(buyer_id, host, port)
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
            print(
                f"{WARNING}You are not currently in the market. Use 'join' to enter.{ENDC}"
            )

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
                        print(f"{WARNING}Amount must be greater than 0!{ENDC}")
                        continue
                except (IndexError, ValueError):
                    print(f"{WARNING}Invalid 'buy' command. Usage: buy <integer>{ENDC}")
                    continue

            client.recv_msg()