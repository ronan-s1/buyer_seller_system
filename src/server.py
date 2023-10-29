import socket
import sys
import threading
import time


class Server:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.clients = []
        self.items = {"flour": 5, "sugar": 5, "potato": 5, "oil": 5}
        self.current_item = None
        self.start_time = None

    def broadcast(self, msg, source):
        for client in self.clients:
            if client != source:
                client.send(msg)

    def handle_client(self, client):
        try:
            while True:
                msg = client.recv(1024).decode()

                if "left and quit" in msg:
                    print(msg)
                    client.close()
                    return

                if msg == "buy":
                    client.send("bought".encode())

                elif msg == "list":
                    client.send(str(self.items).encode())

                else:
                    client.send("ack".encode())
        except:
            print("Connection lost!")

    def run(self):
        while True:
            if not self.current_item or time.time() - self.start_time > 60:
                self.current_item = self.items.popitem()[0]
                self.start_time = time.time()

            client, _ = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    server = Server(host, port)
    print(f"Seller {sys.argv[2]} started on {host}:{port}")
    server.run()
