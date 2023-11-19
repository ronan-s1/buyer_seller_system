from colours import *
import socket
import sys
import threading
import time
import random


class Server:
    def __init__(self, seller_name, seller_id, host, port):
        self.seller_name = seller_name
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
                client.send(
                    f"{BLUE}BROADCAST ({self.seller_name}):{ENDC} {msg}".encode()
                )
            except:
                print(f"{RED}Failed to send broadcast message to:{ENDC}\n{client}")

    # when all items are sold, disconnect all the clients
    def disconnect_all_clients(self):
        for client in self.clients:
            try:
                client.send(
                    f"{RED}All items are sold! No stock left...bye bye👋{ENDC}".encode()
                )
                client.close()
            except:
                pass
        self.clients = []
        exit(0)

    # recieves client message
    def handle_client(self, client):
        def send_msg(msg):
            client.send(msg.encode())

        try:
            while True:
                msg = client.recv(1024).decode()
                
                # user leaving market 
                if "left and quit" in msg:
                    print(f"{WARNING}{msg}{ENDC}")
                    client.close()
                    self.clients.remove(client)
                    return

                # user leaving stall, may still be in the market however
                elif "left the stall" in msg:
                    print(f"{WARNING}{msg}{ENDC}")
                    send_msg(
                        f"{GREEN}You left the stall, enter 'join' to join a seller's stall.{ENDC}"
                    )
                    client.close()
                    self.clients.remove(client)
                    return

                elif msg.startswith("buy"):
                    self.handle_buy_request(msg, send_msg)

                elif msg == "list":
                    self.handle_list_request(send_msg)
        except:
            print(f"{RED}Connection lost!{ENDC}")

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
            f"{GREEN}{item:<6}{ENDC} -> {CYAN}{stock}{ENDC}"
            for item, stock in self.items.items()
        ]
        send_msg(
            f"{GREEN}Item{ENDC} and {CYAN}Stock:\n{ENDC}"
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
                    item_switch_reason = f"No stock left for {self.current_item}..."
                    break

                if duration == 30:
                    self.broadcast(
                        f"{UNDERLINE}30 seconds{ENDC} left until a {GREEN}new item{ENDC} is being sold!"
                    )

                time.sleep(1)
                duration -= 1

            if duration == 0:
                item_switch_reason = "Times up..."

        # When time is up, select a new item to be sold
        self.select_next_item(item_switch_reason)

    def select_next_item(self, item_switch_reason=None):
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
                f"{GREEN}{item_switch_reason}new item on sale: {UNDERLINE}{self.current_item}{ENDC}"
            )
            timer_thread = threading.Thread(target=self.timer)
            timer_thread.start()
        else:
            self.disconnect_all_clients()

    # accepting client and setting up server instance
    def run(self):
        while True:
            if not self.current_item:
                self.select_next_item()

            client, _ = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

# creating server object using the command line arg data
if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    seller_name = sys.argv[3]
    seller_id = int(sys.argv[4])

    server = Server(seller_name, seller_id, host, port)
    print(f"{HEADER}{seller_name} started on {host}:{port}{ENDC}\n")
    server.run()
