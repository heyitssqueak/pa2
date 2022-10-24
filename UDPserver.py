import socket

HOST = "10.140.41.16"
PORT = 20

# Creating server socket
print("establishing server on %s:%s" % (HOST,PORT))
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDP_server_socket:
    UDP_server_socket.bind((HOST,PORT))
    print("server running on %s:%s" % (HOST,PORT))

    # Waiting for incoming packets
    while True:
        incoming = UDP_server_socket.recvfrom(1024)
        message = incoming[0]
        address = incoming[1]

        # Sending file back when packet is received
        f = open("img.jpg", "rb")
        l = f.read(1024)
        while l:
            UDP_server_socket.sendto(l, address)
            l = f.read(1024)
        f.close()

        print("img sent")

