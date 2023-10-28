import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    host = config.get("Server", "host")
    port = config.getint("Server", "port")

    sellers = dict(config.items("Sellers"))
    buyers = dict(config.items("Buyers"))
    
    return host, port, sellers, buyers
