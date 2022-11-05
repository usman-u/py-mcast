## py-mcast

* A simple python program to generate multicast traffic on a multicast group.
* Uses python sockets and argparse.

---

# Developer Notes
```bash
conda create -n py-mcast
create activate py-mcast
poetry install
```
If using VSCode SSH remote, change interpreter to conda env python path.

e.g. `/home/usman/miniconda3/envs/py-mcast/bin/python3`

Confirm with `which python3`
```bash
(network-automation) usman@dev-usman-lan:~/network-automation$ which python
/home/usman/miniconda3/envs/py-mcast/bin/python3
```

## Usage

* Assuming a multicast capable network (PIM, IGMP, etc) is in configured, run `publisher.py` on a server, and then `subscriber.py` on various hosts.

* Mcast group and port can be configured in `publisher.py`, remember to reflect changes in `subscriber.py`.

* Tested on a Linux hosts, but should work on Windows as well (might have to modify firewall).

* Set `--interval` as 0 to generate traffic continuously. 
    * This generates ~20mbps of traffic. 
    * Warning: this will cause a multicast storm if network isn't configured properly.

---


### Arguments for `publisher.py`
```n
python .\publisher.py -h
usage: py-mcast [-h] [-addr MCASTADDR] [-p PORT] [-m MESSAGE] [-c COUNT] [-ttl TTL] [-ivl INTERVAL]

A Python Multicast Traffic Generator.

options:
  -h, --help            show this help message and exit
  -addr MCASTADDR, --mcastaddr MCASTADDR
                        multicast address to publish to
  -p PORT, --port PORT  port to publish to multicast packets on.
  -m MESSAGE, --message MESSAGE
                        message to multicast
  -c COUNT, --count COUNT
                        number of messages to send
  -ttl TTL, --ttl TTL   TTL of multicast packets .
  -ivl INTERVAL, --interval INTERVAL
                        Interval between multicast packets. 0 = 20mbps flood.
```

### Arguments for `subscriber.py`
```n
python .\subscriber.py -h
usage: py-mcast [-h] [-addr MULTICAST_ADDRESS] [-p PORT]        

A Python Multicast Traffic Generator.

options:
  -h, --help            show this help message and exit
  -addr MULTICAST_ADDRESS, --multicast-address MULTICAST_ADDRESS
                        multicast address to subscribe to       
  -p PORT, --port PORT  port to publish/subscribe to traffic on.
```

---

## Example
![Example](example.PNG)