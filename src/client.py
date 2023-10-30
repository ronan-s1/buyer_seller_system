import socket
import sys
import threading
import struct
from colours import *

BUFFER = 10024
MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5005

class Client:
    def __init__(self, buyer_id, host, port, server_host, server_port):
        self.buyer_id = buyer_id
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(("", MULTICAST_PORT))
        self.mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        self.client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
        self.server_address = (server_host, server_port)
        
        # Create a separate point-to-point socket for direct communication
        self.point_to_point_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.point_to_point_client.bind((host, port))

        # Create a thread to continuously receive multicast messages
        self.multicast_thread = threading.Thread(target=self.receive_multicast_messages)
        self.multicast_thread.daemon = True
        self.multicast_thread.start()

    def send_msg(self, msg):
        self.point_to_point_client.sendto(msg.encode(), self.server_address)

    def recv_msg(self):
        data, _ = self.point_to_point_client.recvfrom(BUFFER)
        msg = data.decode()
        print(msg)

    def receive_multicast_messages(self):
        while True:
            data, _ = self.client.recvfrom(BUFFER)
            msg = data.decode()
            print(f"Multicast: {msg}")

if __name__ == "__main__":
    valid_commands = ["buy <int>", "list", "quit", "join", "leave"]
    host = sys.argv[1]
    port = int(sys.argv[2])
    buyer_id = int(sys.argv[3])
    server_host = sys.argv[4]
    server_port = int(sys.argv[5])
    joined = False
    
    
    client = Client(buyer_id, host, port, server_host, server_port)
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
            
            # client.recv_multicast_msg()
