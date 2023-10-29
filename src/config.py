import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    host = config.get("Server", "host")
    port = config.getint("Server", "port")

    sellers = dict(config.items("Sellers"))
    buyers = dict(config.items("Buyers"))

    # Check for duplicate seller and buyer IDs
    seller_ids = set(sellers.values())
    buyer_ids = set(buyers.values())

    if len(seller_ids) != len(sellers):
        raise ValueError("Duplicate seller IDs found in config file.")

    if len(buyer_ids) != len(buyers):
        raise ValueError("Duplicate buyer IDs found in config file.")

    return host, port, sellers, buyers
