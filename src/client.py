import threading
from colours import *
import socket
import sys

class Client:
    def __init__(self, buyer_id, host="localhost", port=5000):
        self.buyer_id = buyer_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.valid_requests = ["buy <int>", "list", "quit", "join", "leave"]
        self.joined = False

        self.recv_thread = threading.Thread(target=self.recv_msg)
        self.recv_thread.daemon = True
        self.recv_thread.start()

        self.input_thread = threading.Thread(target=self.enter_request)
        self.input_thread.daemon = True
        self.input_thread.start()
        
    
    def send_msg(self, msg):
        self.socket.send(msg.encode())

    def recv_msg(self):
        try:
            while True:
                msg = self.socket.recv(1024).decode()
                if not msg:
                    break
                print(msg)
        except:
            print(f"{FAIL}Connection lost!{ENDC}")
            self.socket.close()

    def enter_request(self):
        while True:
            request = input(f"Enter your request ({', '.join(self.valid_requests)}): ").lower()

            if (request not in self.valid_requests[1:]) and not (request.startswith("buy")):
                print(f"{WARNING}Invalid command!{ENDC}")

            elif request == "join" and self.joined:
                print(f"{WARNING}You are already in the market.{ENDC}")

            elif request == "join":
                self.joined = True
                print(f"{GREEN}You have self.joined the market.{ENDC}")

            elif not self.joined:
                print(f"{WARNING}You are not currently in the market. Use 'join' to enter.{ENDC}")

            elif self.joined:
                if request == "quit":
                    print("Exiting...")
                    self.send_msg(f"Buyer {self.buyer_id} has left and quit the market!")
                    break

                elif request == "leave":
                    self.joined = False
                    print("You have left the market.")
                    continue

                elif request == "list":
                    self.send_msg("list")

                elif request.startswith("buy"):
                    try:
                        amount = int(request.split()[1])
                        if amount > 0:
                            self.send_msg(f"buy {amount} {self.buyer_id}")
                        else:
                            print(f"{WARNING}Amount must be greater than 0!{ENDC}")
                            continue
                    except (IndexError, ValueError):
                        print(f"{WARNING}Invalid 'buy' command. Usage: buy <integer>{ENDC}")


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    client = Client(buyer_id, host, port)
    print(f"{HEADER}Buyer {buyer_id} connected to {host}:{port}{ENDC}\n")
    
    # This main thread will continue running, and the input_thread in the Client class will handle user input.
    while True:
        pass
