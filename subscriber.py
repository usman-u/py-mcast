import socket
import struct
import pickle
import argparse

def subscribe(mcast_addr, port):
    print ("""-------------------------------------------------------
A Python Multicast Traffic Generator\nBy <usman@usman.network> See https://blog.usman.network.
-------------------------------------------------------""")
    multicast_group = mcast_addr # macst group
    server_address = ('', port)    # port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(server_address)

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print ("Listening for multicast packets on {}:{}...".format(multicast_group, port))
    while True:  # RX loop
        message, address = sock.recvfrom(1024)
        
        data = pickle.loads(message)
        print ("{} | Received Message: '{}' | on {}:{} | at {}".format(data[1], data[0], multicast_group, port, data[2]))

parser = argparse.ArgumentParser(prog="py-mcast",
        allow_abbrev=True,
        description="A Python Multicast Traffic Generator.",
        epilog="By <usman@usman.network> See https://blog.usman.network."
    )

parser.add_argument("-addr", "--multicast-address", 
                    action="store", 
                    type=str,
                    default="224.3.29.71",
                    required=False,
                    help="multicast address to subscribe to")

parser.add_argument("-p", "--port",
                    action="store", 
                    required=False,
                    default=10000,
                    type=int,
                    help="port to publish/subscribe to traffic on.")

args = parser.parse_args()
subscribe(args.multicast_address, args.port)