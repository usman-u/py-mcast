import socket
import struct
import time
import pickle
import datetime

multicast_group = ("224.3.29.71", 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(0.2)

ttl = struct.pack('b', 5)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

for i in range(0, 1000): # TX loop
    message = ["PublisherMSG", i, 0]
    message[2] = datetime.datetime.now().strftime("%H:%M:%S.%f")    # appends timestamp to message at index 2

    data = pickle.dumps(message)

    print ("{} | Sending message: '{}' to {} at {}".format(message[1], message[0], multicast_group[0], message[2]))
    sent = sock.sendto(data, multicast_group)

    time.sleep(1.5)