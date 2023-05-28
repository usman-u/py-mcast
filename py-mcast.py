import socket
import argparse
import struct
import time
import pickle
import datetime


def publish(message, mcast_addr, port, count, ttl, interval):
    print(
        """-------------------------------------------------------
A Python Multicast Traffic Generator\nBy Usman <usman@usman.network> See https://blog.usman.network.
-------------------------------------------------------"""
    )

    multicast_group = (mcast_addr, port)  # mcast group and port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(0.2)

    ttl = struct.pack("b", ttl)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    for i in range(1, count + 1):  # TX loop
        final_message = [message, i, 0]  # increments message counter every loop
        final_message[2] = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )  # appends timestamp to message at index 2

        data = pickle.dumps(final_message)

        print(
            "{} | Generating message: '{}' | publishing to {}:{} | at {}".format(
                final_message[1],
                final_message[0],
                multicast_group[0],
                port,
                final_message[2],
            )
        )
        sent = sock.sendto(data, multicast_group)

        time.sleep(interval)


def subscribe(mcast_addr, port, raw):
    print(
        """-------------------------------------------------------
A Python Multicast Traffic Generator\nBy Usman <usman@usman.network> See https://blog.usman.network.
-------------------------------------------------------"""
    )
    multicast_group = mcast_addr  # macst group
    server_address = ("", port)  # port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(server_address)

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Listening for multicast packets on {}:{}...".format(multicast_group, port))
    while True:  # RX loop
        message, address = sock.recvfrom(1024)

        data = pickle.loads(message)
        if raw:
            print(data)
        else:
            print(
                "{} | Received Message: '{}' | on {}:{} | at {}".format(
                    data[1], data[0], multicast_group, port, data[2]
                )
            )

parser = argparse.ArgumentParser(
    prog="py-mcast",
    allow_abbrev=True,
    description="A Python Multicast Traffic Generator.",
    epilog="By Usman <usman@usman.network> See https://blog.usman.network.",
)

parser.add_argument(
    "job",
    metavar="job",
    type=str,
    nargs=1,
    choices=["publish", "subscribe"],
    help="Action to do, publish or subscribe",
)

parser.add_argument(
    "-addr",
    "--multicast-address",
    action="store",
    type=str,
    default="239.1.2.10",
    help="multicast address to publish traffic to",
)

parser.add_argument(
    "-p",
    "--port",
    action="store",
    default=10000,
    type=int,
    help="port to publish to multicast packets on.",
)

parser.add_argument(
    "-m",
    "--message",
    action="store",
    required=False,
    default="Hello World!",
    type=str,
    help="message to multicast",
)

parser.add_argument(
    "-c",
    "--count",
    action="store",
    required=False,
    default=10000,
    type=int,
    help="number of messages to send",
)

parser.add_argument(
    "-ttl",
    "--ttl",
    action="store",
    required=False,
    default=5,
    type=int,
    help="TTL of multicast packets .",
)

parser.add_argument(
    "-raw",
    "--raw",
    action=argparse.BooleanOptionalAction,
    default=False,
    type=bool,
    help="Display raw data on subscriber side.",
)

parser.add_argument(
    "-ivl",
    "--interval",
    action="store",
    required=False,
    default=1,
    type=int,
    help="Interval between multicast packets. 0 = 20mbps flood.",
)

args = parser.parse_args()

if args.job[0] == "publish":
    publish(
        args.message,
        args.multicast_address,
        args.port,
        args.count,
        args.ttl,
        args.interval,
    )

if args.job[0] == "subscribe":
    subscribe(args.multicast_address, args.port, args.raw)
