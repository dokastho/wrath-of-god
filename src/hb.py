"""Class file for heartbeat thread."""

import json
import socket
import struct
import random


ICMP_ECHO_REQUEST = 8


class hb:
    def __init__(self, host, port, dest, signals):
        """Initialize heartbeat socket."""

        # init the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

        # get port number
        self.port = self.sock.getsockname()[1]
        self.host = host
        self.port = port
        self.signals = signals

        self.timeout = 1

        self.dest = dest

    def connection(self):
        """Maintain connection with google nameservers."""

        # start socket
        self.sock.listen()

        # listen on socket for client connection file descriptors
        # TODO stop when timeout
        while True:
            self.send_one()
            try:
                connectionfd, address = self.sock.accept()
            except socket.timeout:
                continue
            with connectionfd:
                msg_chunks = []
                while True:
                    try:
                        data = connectionfd.recv(4096)
                    except socket.timeout:
                        continue
                    if not data:
                        break
                    msg_chunks.append(data)
            # Decode list-of-byte-strings to UTF8 and parse JSON data
            msg_bytes = b''.join(msg_chunks)
            msg_str = msg_bytes.decode("utf-8")
            try:
                message_dict = json.loads(msg_str)
            except json.JSONDecodeError:
                continue
            # if ok...
            # if lost...
            # if reconnected... will need a previous var
            # if failed...

    def send_one(self):
        """Send one packet."""
        # send ping
        packet_id = int((id(self.timeout) * random.random()) / 65535)

        pack = create_packet(packet_id)

        self.sock.sendto(pack, (self.dest, 1))


# https://gist.github.com/pklaus/856268
def checksum(source_string):
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1]) * \
            256+ord(source_string[count])
        sum = sum + this_val
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(id):
    """Create a new echo request packet based on the given "id"."""
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = 192 * 'Q'
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(str(header) + data)
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                         socket.htons(my_checksum), id, 1)
    return str(header) + data
