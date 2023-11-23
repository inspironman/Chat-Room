import socket
import threading

PORT = 50505
SERVER = "192.168.8.110"

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((SERVER, PORT))

nickname = input("Please enter your nickname: ")

def receive():
    while True:
        try:
            message = c.recv(1024).decode('ascii')
            if message == "name":
                c.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            c.close()
            break

def write():
    while True:
        try:
            message = input()
            full_message = f"{nickname}: {message}"
            c.send(full_message.encode('ascii'))
        except KeyboardInterrupt:
            c.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
