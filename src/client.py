import threading
from colours import *
import socket
import sys
import textwrap


class Client:
    def __init__(self, buyer_id, host="localhost", port=5000):
        self.buyer_id = buyer_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.valid_requests = ["list", "quit", "join", "leave"]
        self.joined = False

        self.recv_thread = threading.Thread(target=self.recv_msg)
        self.recv_thread.daemon = True
        self.recv_thread.start()

        self.input_thread = threading.Thread(target=self.enter_request)
        self.input_thread.daemon = True
        self.input_thread.start()

    # print help menu
    def request_help(self):
        help_text = textwrap.dedent(
            f"""\
            {CYAN}1) buy <amount>:{ENDC} Buy an amount of the current item on sale
            {CYAN}2) list:{ENDC} List the items on sale and their stock
            {CYAN}3) join:{ENDC} Join the market
            {CYAN}4) leave:{ENDC} Leave the market
            {CYAN}5) quit:{ENDC} Leave the market and can't join back
            {CYAN}6) help:{ENDC} Display this message
        """
        )
        print(help_text)

    def send_msg(self, msg):
        try:
            self.socket.send(msg.encode())
        except:
            print(f"{FAIL}Connection lost!{ENDC}")
            self.socket.close()

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

    # takes in user input
    def enter_request(self):
        print(f"{HEADER}Buyer {self.buyer_id} connected to {host}:{port}{ENDC}\n")
        self.request_help()
        print("Type your request!\n")

        while True:
            request = input().lower()
            self.handle_request(request)

    # does error extensive checking
    def handle_request(self, request):
        # if request is in valid requests list and if its not a buy command
        if (request not in self.valid_requests) and (not request.startswith("buy ")):
            print(f"{WARNING}Invalid command!{ENDC}")

        elif request == "join" and self.joined:
            print(f"{WARNING}You are already in the market.{ENDC}")

        elif request == "join":
            self.joined = True
            print(f"{GREEN}You have joined the market.{ENDC}")

        elif not self.joined:
            print(
                f"{WARNING}You are not currently in the market. Use 'join' to enter.{ENDC}"
            )

        # if user joined the market and the request is valid
        elif self.joined:
            if request == "quit":
                print("Exiting...")
                self.send_msg(f"Buyer {self.buyer_id} has left and quit the market!")
                exit(0)

            elif request == "leave":
                self.joined = False
                print("You have left the market.")

            elif request == "list":
                self.send_msg("list")

            elif request.startswith("buy "):
                self.handle_buy_request(request)

    # handling the buy, extracting amount and sending buyer id to seller for broadcast
    def handle_buy_request(self, request):
        try:
            amount = int(request.split()[1])
            if amount > 0:
                self.send_msg(f"buy {amount} {self.buyer_id}")
            else:
                print(f"{WARNING}Amount must be greater than 0!{ENDC}")
        except (IndexError, ValueError):
            print(f"{WARNING}Invalid 'buy' command. Usage: buy <integer>{ENDC}")


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    client = Client(buyer_id, host, port)

    # This main thread will continue running
    while True:
        pass
