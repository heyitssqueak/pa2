import socket
import time

HOST = "10.140.41.16"
PORT = 20

# Creating server socket
print("establishing server on %s:%s..." % (HOST,PORT))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST,PORT))
    server_socket.listen()
    print("server running on %s:%s" % (HOST,PORT))

    # Checking for connections
    while True:
        connection, address = server_socket.accept()
        #print("-----BEGIN-----")

        # Sending png file
        start_time = time.time()
        f = open("img.jpg", "rb")
        l = f.read(1024)
        while l:
            connection.send(l)
            l = f.read(1024)
        f.close()

        #print(time.time()-start_time)
        connection.close()
        #print("-----END-----")
        print("img sent")

