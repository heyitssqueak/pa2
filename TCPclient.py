import socket
import time

HOST = "10.141.164.25"
PORT = 20

# Creating client socket
print("trying to connect to %s:%s..." % (HOST,PORT))
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    print("connected to port %s:%s" % (HOST,PORT))
except socket.error as e:
    print("could not connect: ", e)
    exit()

# # Receiving incoming file (only used if running server.py simultanously)
# start_time = time.time()
# f = open("received.png", "wb")
# l = client_socket.recv(1024)
# while l:
#     f.write(l)
#     l = client_socket.recv(1024)

start_time = time.time()
f = open("img.jpg", "rb")
l = f.read(1024)
while l:
    client_socket.send(l)
    l = f.read(1024)

f.close()
client_socket.close()
print("img sent")
