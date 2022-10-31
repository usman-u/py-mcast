import socket
import struct
import pickle

multicast_group = '224.3.29.71' # macst group
server_address = ('', 10000)    # port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:  # RX loop
    message, address = sock.recvfrom(1024)
    
    data = pickle.loads(message)
    print ("{} | Received Message: '{}' on {} at {}".format(data[1], data[0], multicast_group, data[2]))