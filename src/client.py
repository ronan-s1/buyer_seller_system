import json
import os
import threading
from colours import *
import socket
import sys
import textwrap
import time


class Client:
    def __init__(self, buyer_id, server_host, server_port, sellers):
        self.buyer_id = buyer_id
        self.server_host = server_host
        self.server_port = server_port
        self.sellers = sellers
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

        self.valid_requests = ["help", "list", "quit", "join", "leave"]
        self.joined = True

        self.stop_thread = False

        self.recv_thread = threading.Thread(target=self.recv_msg)
        self.recv_thread.daemon = True
        self.recv_thread.start()

        self.input_thread = threading.Thread(target=self.enter_request)
        self.input_thread.daemon = True
        self.input_thread.start()

    def cls(self):
        os.system("cls" if os.name == "nt" else "clear")

    # print help menu
    def request_help(self):
        help_text = textwrap.dedent(
            f"""\
            {CYAN}1) buy <amount>:{ENDC} Buy an amount of the current item on sale
            {CYAN}2) list:{ENDC} List the items on sale and their stock
            {CYAN}3) join:{ENDC} Join a stall from a list of sellers
            {CYAN}4) leave:{ENDC} Leave a stall
            {CYAN}5) quit:{ENDC} Leave the market and can't join back
            {CYAN}6) help:{ENDC} Display this message
            """
        )
        print(help_text)

    # send message to server
    def send_msg(self, msg):
        try:
            self.socket.send(msg.encode())
        except:
            print(f"{RED}Connection lost!{ENDC}")
            self.socket.close()

    # receive message from server
    def recv_msg(self):
        try:
            while True and not self.stop_thread:
                msg = self.socket.recv(1024).decode()
                if not msg:
                    break

                print(msg)
        except:
            print(f"{RED}Connection lost!{ENDC}")
            self.socket.close()

    # takes in user input
    def enter_request(self):
        time.sleep(0.1)
        self.cls()
        print(
            f"{HEADER}Buyer {self.buyer_id} connected to {self.server_host}:{self.server_port}{ENDC}\n"
        )
        self.request_help()
        print("Type your request!\n")

        while True and not self.stop_thread:
            request = input().lower()
            self.handle_request(request)

    def join_new_seller(self):
        self.cls()
        while True:
            for i, (seller_name, (_, port)) in enumerate(self.sellers.items(), start=1):
                print(f"{CYAN}{i}) {seller_name} -> localhost:{port}{ENDC}")

            try:
                print(f"\nEnter a seller to join:")
                seller_choice = int(input())
                if 1 <= seller_choice <= len(self.sellers):
                    # getting chosen server data
                    chosen_seller = list(self.sellers.keys())[seller_choice - 1]
                    _, self.server_port = self.sellers[chosen_seller]

                    # close current socket, create new socket and connect to new server
                    self.socket.close()
                    self.socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    )  # Create a new socket
                    self.socket.connect((self.server_host, self.server_port))
                    self.joined = True

                    # begin threads again
                    self.stop_thread = False
                    self.recv_thread = threading.Thread(target=self.recv_msg)
                    self.recv_thread.daemon = True
                    self.recv_thread.start()

                    self.input_thread = threading.Thread(target=self.enter_request)
                    self.input_thread.daemon = True
                    self.input_thread.start()
                    break
                else:
                    print(
                        f"{WARNING}Invalid choice. Please enter a number between 1 and {len(self.sellers)}.{ENDC}"
                    )
            except ValueError:
                print(f"{WARNING}Invalid input. Please enter a valid number.{ENDC}")

    # does error extensive checking
    def handle_request(self, request):
        if request == "help":
            self.request_help()
        # if request is in valid requests list and if it's not a buy command
        elif (request not in self.valid_requests) and (not request.startswith("buy ")):
            print(f"{WARNING}Invalid command!{ENDC}")

        elif request == "join" and self.joined:
            print(f"{WARNING}You already joined a seller's stall.{ENDC}")

        elif request == "join":
            self.stop_thread = True
            self.join_new_seller()

        elif not self.joined:
            print(
                f"{WARNING}You haven't joined a seller's stall yet. Use 'join' to join a seller's stall.{ENDC}"
            )

        # if the user joined the market and the request is valid
        elif self.joined:
            if request == "quit":
                print(f"{RED}Exiting...{ENDC}")
                self.send_msg(f"Buyer {self.buyer_id} has left and quit the market!")
                exit(0)

            elif request == "leave":
                self.joined = False
                self.send_msg(f"Buyer {self.buyer_id} has left the stall!")

            elif request == "list":
                self.send_msg("list")

            elif request.startswith("buy "):
                self.handle_buy_request(request)

    # handling the buy request
    def handle_buy_request(self, request):
        try:
            # extracting amount
            amount = int(request.split()[1])
            if amount > 0:
                # also sending buyer id for broadcasting and letting every buyer know who bought what
                self.send_msg(f"buy {amount} {self.buyer_id}")
            else:
                print(f"{WARNING}Amount must be greater than 0!{ENDC}")
        except (IndexError, ValueError):
            print(f"{WARNING}Invalid 'buy' command. Usage: buy <integer>{ENDC}")


if __name__ == "__main__":
    server_host = sys.argv[1]
    sellers = json.loads(sys.argv[2])
    buyer_id = sys.argv[3]

    while True:
        for i, (seller_name, (_, port)) in enumerate(sellers.items(), start=1):
            print(f"{CYAN}{i}) {seller_name} -> localhost:{port}{ENDC}")

        try:
            print(f"\nEnter a seller to join:")
            seller_choice = int(input())
            if 1 <= seller_choice <= len(sellers):
                chosen_seller = list(sellers.keys())[seller_choice - 1]
                _, port = sellers[chosen_seller]
                client = Client(buyer_id, server_host, port, sellers)
                break
            else:
                print(
                    f"{WARNING}Invalid choice. Please enter a number between 1 and {len(sellers)}.{ENDC}"
                )
        except:
            print(f"{WARNING}Invalid input. Please enter a valid number.{ENDC}")

    # This main thread will continue running
    while True:
        pass
