import os
from config import read_config


def start_server(host, port, seller_id):
    os.system(f"start cmd /K python src/server.py {host} {port} {seller_id}")


def start_client(host, port, buyer_id):
    os.system(f"start cmd /K python src/client.py {host} {port} {buyer_id}")


if __name__ == "__main__":
    host, port, buyers = read_config()

    # Start the server
    start_server(host, port, 1)

    # Start the clients
    for buyer_id in buyers.values():
        start_client(host, port, int(buyer_id))
