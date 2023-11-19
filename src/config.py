import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    host = config.get("Server", "host")
    port = config.getint("Server", "port")

    buyers = dict(config.items("Buyers"))
    buyer_ids = set(buyers.values())

    sellers = dict(config.items("Sellers"))
    seller_ids = set(sellers.values())

    # checks for dupes
    if len(buyer_ids) != len(buyers):
        raise ValueError("Duplicate buyer IDs found in config file.")

    if len(seller_ids) != len(sellers):
        raise ValueError("Duplicate seller IDs found in config file.")

    # Create a modified sellers dictionary with incremented port numbers
    sellers = {
        key: (value, port + i)
        for i, (key, value) in enumerate(sellers.items(), start=1)
    }

    return host, port, buyers, sellers
