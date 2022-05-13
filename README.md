# wrath-of-god
Script to recover an internet connection after comcast disables it, thus doing god's bidding by being as irritating as possible w.r.t. comcast. Deus Vult

## How it works
Wrath of God will ping google's nameservers every minute to ensure there is a valid connection to the internet. If there isn't one, it will ping every five seconds for a minute to verify that connection is actually lost. In that event, Wrath of God will change the server's hostname, MAC address, flush the DNS caches and restart the DHCP server to thwart Comcast's attempt to block my server from the internet. In all seriousness, it's just a funny name and I'm making light of a very annoying problem, because after all this server is used for legal and responsible purposes only.

Deus Vult ⚡