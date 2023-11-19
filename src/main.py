import os
import json
from config import read_config


def start_server(host, port, seller_name, seller_id):
    os.system(
        f"start cmd /K python src/server.py {host} {port} {seller_name} {seller_id}"
    )


def start_client(server_host, sellers, buyer_id):
    sellers_str = json.dumps(sellers)
    # Escape the double quotes in the JSON string
    sellers_str_escaped = json.dumps(sellers_str)
    os.system(f"start cmd /K python src/client.py {server_host} {sellers_str_escaped} {buyer_id}")


if __name__ == "__main__":
    server_host, port, buyers, sellers = read_config()

    # launch sellers
    for seller_name, (seller_id, seller_port) in sellers.items():
        start_server(server_host, seller_port, seller_name, seller_id)

    # launch clients, also pass in seller data
    for buyer_id in buyers.values():
        start_client(server_host, sellers, buyer_id)
