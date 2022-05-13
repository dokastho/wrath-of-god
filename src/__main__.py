"""Driver for WoG"""

import os
from WoG import WoG

def main():
    """Main script for WoG"""
    host = "localhost"
    port = 0  # let os decide
    
    retribution = WoG()