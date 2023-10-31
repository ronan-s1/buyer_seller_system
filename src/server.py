from colours import *
import socket
import sys
import threading
import time
import random


class Server:
    def __init__(self, seller_id, host="localhost", port=5000):
        self.seller_id = seller_id
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.clients = []
        self.items = {"flour": 5, "sugar": 5, "potato": 5, "oil": 5}
        self.current_item = None
        self.start_time = None

    # send message to all connected sockets
    def broadcast(self, msg):
        for client in self.clients:
            try:
                client.send(f"{BLUE}BROADCAST:{ENDC} {msg}".encode())
            except:
                print(f"{FAIL}Failed to send broadcast message to:\n{client}.{ENDC}")

    # recieves client message
    def handle_client(self, client):
        def send_msg(msg):
            client.send(msg.encode())

        try:
            while True:
                msg = client.recv(1024).decode()
                if "left and quit" in msg:
                    print(f"{WARNING}{msg}{ENDC}")
                    client.close()
                    self.clients.remove(client)
                    return

                if msg.startswith("buy"):
                    self.handle_buy_request(msg, send_msg)

                elif msg == "list":
                    self.handle_list_request(send_msg)
        except:
            print(f"{FAIL}Connection lost!{ENDC}")

    def handle_buy_request(self, msg, send_msg):
        # get the buyer id and and amount of the item thats being bought
        amount = int(msg.split()[1])
        buyer_id = int(msg.split()[2])

        # if there's a current item
        if self.current_item:
            # if the stock is more than or equal to what the buyer wnats
            if self.items.get(self.current_item, 0) >= amount:
                self.items[self.current_item] -= amount
                self.broadcast(
                    f"{GREEN}Buyer {buyer_id} bought {UNDERLINE}{amount}kg{ENDC}{GREEN} of {UNDERLINE}{self.current_item}{ENDC}{GREEN} from seller {self.seller_id}.{ENDC}"
                )
            else:
                # if stock is less than requested amount
                send_msg(
                    f"{WARNING}Insufficient amount of {self.current_item} left.{ENDC}"
                )
        else:
            send_msg(f"{WARNING}No item is currently on sale.{ENDC}")

    # just formatting the items dictionary nicely and sending it back to client
    def handle_list_request(self, send_msg):
        stock_and_items = [
            f"{GREEN}{item:<6}{ENDC} {CYAN}->{ENDC} {stock}"
            for item, stock in self.items.items()
        ]
        send_msg(
            f"{GREEN}Stock{ENDC} and {CYAN}Items:\n{ENDC}"
            + "\n".join(stock_and_items)
            + f"\n\n{UNDERLINE}Selling Now: {self.current_item}{ENDC}"
        )

    # timer countdown
    def timer(self):
        if self.current_item:
            duration = 60
            while duration > 0:
                # if item is fully sold
                if self.items[self.current_item] == 0:
                    print(f"{BLUE}{self.current_item} is fully sold!{ENDC}")
                    break

                if duration == 30:
                    self.broadcast(
                        f"{UNDERLINE}30 seconds{ENDC} left until a {GREEN}new item{ENDC} is being sold!"
                    )

                time.sleep(1)
                duration -= 1

        # When time is up, select a new item to be sold
        self.select_next_item()

    def select_next_item(self):
        # list of items that have stock greater than 0
        items_with_stock = [item for item, stock in self.items.items() if stock > 0]
        if items_with_stock:
            # making sure not the same item is being put on sale again
            while True:
                next_item = random.choice(items_with_stock)

                if (next_item != self.current_item) or (len(items_with_stock) == 1):
                    break

            # setting new current item on sale and broadcasting it
            self.current_item = next_item
            self.broadcast(
                f"{GREEN}New item on sale: {UNDERLINE}{self.current_item}{ENDC}"
            )
            timer_thread = threading.Thread(target=self.timer)
            timer_thread.start()

    # accepting client and setting up server instance
    def run(self):
        while True:
            if not self.current_item:
                self.select_next_item()

            client, _ = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    seller_id = int(sys.argv[3])

    server = Server(seller_id, host, port)
    print(f"{HEADER}Seller started on {host}:{port}{ENDC}\n")
    server.run()
