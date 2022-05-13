"""Class file for WoG
dokastho@umich.edu"""

from datetime import datetime
from src.hb import hb
import json
import logging
import os
import socket
from threading import Thread

logging.basicConfig(filename='wog.log')
LOGGER = logging.getLogger(__name__)


class WoG:
    def __init__(self, host, port, dest, hb_port):
        """Construct the WoG socket and listen for messages from hb thread."""

        # init the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

        # get port number
        self.port = self.sock.getsockname()[1]

        # log start
        LOGGER.info(
            "Starting Wrath of God host=%s port=%s hb_port=%s pwd=%s",
            host, port, hb_port, os.getcwd(),
        )

        self.host = host
        self.port = port
        self.hb_port = hb_port
        self.signals = {"shutdown": False}

        # instantiate hb obj
        self.dest = dest
        self.hb_obj = hb(self.host, self.hb_port, self.dest, self.signals)

        # start thread to listen for heartbeats
        self.hb_thread = Thread(
            target=self.hb_obj.connection,
            args=())
        self.hb_thread.start()

    def listen(self):
        """Listen for messages from hb thread"""

        # start socket
        self.sock.listen()

        # listen on socket for client connection file descriptors
        while True:
            try:
                connectionfd, address = self.sock.accept()
            except socket.timeout:
                continue
            # debug info
            LOGGER.info("Connection from", address[0])
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

            msg_type = message_dict["message_type"]
            timestamp = datetime.now()

            if msg_type == "connected":
                # connection attempt failed
                LOGGER.warn("connected.", timestamp)
                pass
            if msg_type == "lost":
                # connection attempt failed
                LOGGER.warn("connection temporarily lost...", timestamp)
                pass
            if msg_type == "reconnect":
                # attempting new connection
                LOGGER.info("reconnecting...", timestamp)
                pass
            if msg_type == "fail":
                # reconnections won't work
                LOGGER.warn("connection failed.", timestamp)
                pass
    
    def terminate(self):
        """End the ping thread."""
        # wait for thread to terminate
        self.hb_thread.join()