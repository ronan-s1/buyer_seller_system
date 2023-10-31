import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    host = config.get("Server", "host")
    port = config.getint("Server", "port")

    buyers = dict(config.items("Buyers"))
    buyer_ids = set(buyers.values())

    # checks for dupes
    if len(buyer_ids) != len(buyers):
        raise ValueError("Duplicate buyer IDs found in config file.")

    return host, port, buyers
