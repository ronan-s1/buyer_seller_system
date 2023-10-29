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

    def handle_client(self, client):
        def send_msg(msg):
            client.send(msg.encode())

        try:
            while True:
                msg = client.recv(1024).decode()

                if "left and quit" in msg:
                    print(msg)
                    client.close()
                    return

                if msg.startswith("buy"):
                    amount = int(msg.split()[1])
                    buyer_id = int(msg.split()[2])

                    if self.current_item:
                        if self.items[self.current_item] >= amount:
                            self.items[self.current_item] -= amount
                            send_msg(
                                f"{GREEN}Buyer {buyer_id} bought {UNDERLINE}{amount}kg{ENDC}{GREEN} of {UNDERLINE}{self.current_item}{ENDC}{GREEN} from seller {self.seller_id}.{ENDC}"
                            )
                        else:
                            send_msg(f"{WARNING}Insufficient amount of {self.current_item} left.{ENDC}")
                    else:
                        send_msg(f"{WARNING}No item is currently on sale.{ENDC}")

                elif msg == "list":
                    send_msg(
                        f"{GREEN}Stock and Items:   {str(self.items)}\nCurrently on Sale: {UNDERLINE}{self.current_item}{ENDC}"
                    )

                else:
                    send_msg("ack")
        except:
            print(f"{FAIL}Connection lost!{ENDC}")

    def timer(self):
        if self.current_item:
            duration = 15
            while duration > 0:
                if self.items[self.current_item] == 0:
                    print(f"{BLUE}{self.current_item} is fully sold!{ENDC}")
                    break

                if duration == 30:
                    print(f"{CYAN}30 seconds left until new item{ENDC}")

                time.sleep(1)
                duration -= 1

        self.select_next_item()

    def select_next_item(self):
        # Logic to select the next item to put on sale
        items_with_stock = [item for item, stock in self.items.items() if stock > 0]
        if items_with_stock:
            while True:
                next_item = random.choice(items_with_stock)
                # if next item is diff or if theres only 1 option
                if (next_item != self.current_item) or (len(items_with_stock) == 1):
                    break

            self.current_item = next_item
            print(f"{CYAN}Next item on sale: {UNDERLINE}{self.current_item}{ENDC}")
            timer_thread = threading.Thread(target=self.timer)
            timer_thread.start()

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
