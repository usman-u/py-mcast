import socket
import struct
import time
import pickle

message = ["PublisherMSG", 0]
multicast_group = ("224.3.29.71", 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(0.2)

ttl = struct.pack('b', 5)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

for i in range(0, 1000): # TX loop
    message[1] = message[1] + 1
    data = pickle.dumps(message)

    print ("{} | Sending message: '{}' to {}".format(message[1], message[0], multicast_group[0]))
    sent = sock.sendto(data, multicast_group)
    time.sleep(1.5)