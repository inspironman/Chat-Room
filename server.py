import socket
import threading

PORT = 50505
SERVER = "192.168.8.110"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))
s.listen()

print("Server is listening on {}".format((SERVER, PORT)))

Clients = []
Nickname = []


def broadcast(message):
    for client in Clients:
        client.send(message.encode('utf-8'))


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            broadcast(message)
        except:
            index = Clients.index(client)
            message = "{} left the chat !".format(Nickname[index])
            Nickname.remove(Nickname[index])
            Clients.remove(client)
            client.close()
            broadcast(message)


def receive():
    while True:
        client, address = s.accept()
        print("Connected with {}".format(str(address)))

        client.send('name'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        Nickname.append(nickname)
        Clients.append(client)

        print("{} joined the chat as {}".format(address, nickname))
        broadcast('{} has joined the chat'.format(nickname))
        client.send("Connected to the server !".encode('ascii'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive()
