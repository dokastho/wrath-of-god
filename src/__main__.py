"""Driver for WoG"""

from src.WoG import WoG


def main():
    """Main script for WoG"""
    host = "localhost"
    port = 0  # let os decide
    dest = "google.com"
    hb_port = 10582

    retribution = WoG(host, port, dest, hb_port)
    retribution.listen()
    retribution.terminate()
