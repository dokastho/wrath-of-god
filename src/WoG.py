"""Class file for WoG
dokastho@umich.edu"""

import logging
import os
from threading import Thread
from hb import hb
import socket

logging.basicConfig(filename='wog.log', encoding='utf-8', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class WoG:
    def __init__(self, host, port, hb_port):
        """Construct the WoG socket and listen for messages from hb thread."""

        self.sock = socket.socket()
        self.sock.bind((host, port))
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
        hbstart = hb(self.host, self.hb_port, self.signals)

        # start thread to listen for heartbeats
        heartbeatThread = Thread(
            target=hbstart.connection,
            args=())
        heartbeatThread.start()

    def listen():
        """Listen for messages from hb thread"""
