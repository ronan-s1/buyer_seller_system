import json
import os
from config import read_config

# start cmd /K python src/server.py 127.0.0.1 9999 1
# start cmd /K python src/client.py 127.0.0.1 9999 1

def start_server(host, port, seller_id):
    print(f"start cmd /K python src/server.py {host} {port} {seller_id}")
    os.system(f"start cmd /K python src/server.py {host} {port} {seller_id}")


def start_client(host, port, buyer_id, server_host, server_port):
    print(f"start cmd /K python src/client.py {host} {port} {buyer_id}")
    os.system(f"start cmd /K python src/client.py {host} {port} {buyer_id} {server_host} {server_port}")


if __name__ == "__main__":
    with open("config.json", "r") as file:
        config = json.load(file)
        
    buyers = config["clients"]
    start_server(config["server_host"], config["server_port"], 1)
    
    for buyer in buyers:
        start_client(buyer['host'], buyer['port'], buyer['buyer_id'], config["server_host"], config["server_port"])
        if int(buyer["buyer_id"]) == 2:
            break
    # host, port, buyers = read_config()

    # # Start the server
    # start_server(host, port, 1)
    

    # # Start the clients
    # for buyer_id in buyers.values():
    #     start_client(host, port, int(buyer_id))
