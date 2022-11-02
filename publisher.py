import socket
import argparse
import struct
import time
import pickle
import datetime

def publish(message, mcast_addr, port, count, ttl, interval):
    print ("""-------------------------------------------------------
A Python Multicast Traffic Generator\nBy <usman@usman.network> See https://blog.usman.network.
-------------------------------------------------------""")

    multicast_group = (mcast_addr, port)  # mcast group and port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(0.2)

    ttl = struct.pack('b', ttl)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    for i in range(1, count+1): # TX loop
        final_message = [message, i, 0]                                       # increments message counter every loop 
        final_message[2] = datetime.datetime.now().strftime("%H:%M:%S")       # appends timestamp to message at index 2

        data = pickle.dumps(final_message)

        print ("{} | Generating message: '{}' | to {}:{} | at {}".format(final_message[1], final_message[0], multicast_group[0], port, final_message[2]))
        sent = sock.sendto(data, multicast_group)

        time.sleep(interval)

parser = argparse.ArgumentParser(prog="py-mcast",
        allow_abbrev=True,
        description="A Python Multicast Traffic Generator.",
        epilog="By <usman@usman.network> See https://blog.usman.network."
    )

parser.add_argument("-addr", "--mcastaddr", 
                    action="store", 
                    type=str,
                    default="224.3.29.71",
                    required=False,
                    help="multicast address to publish to")

parser.add_argument("-p", "--port",
                    action="store", 
                    required=False,
                    default=10000,
                    type=int,
                    help="port to publish to multicast packets on.")

parser.add_argument("-m", "--message",
                    action="store", 
                    required=False,
                    default="Hello World!",
                    type=str,
                    help="message to multicast")

parser.add_argument("-c", "--count",
                    action="store", 
                    required=False,
                    default=1000,
                    type=int,
                    help="number of messages to send")

parser.add_argument("-ttl", "--ttl",
                    action="store", 
                    required=False,
                    default=5,
                    type=int,
                    help="TTL of multicast packets .")

parser.add_argument("-ivl", "--interval",
                    action="store", 
                    required=False,
                    default=1,
                    type=int,
                    help="Interval between multicast packets. 0 = 20mbps flood.")

args = parser.parse_args()

publish(args.message, args.mcastaddr, args.port, args.count, args.ttl, args.interval)