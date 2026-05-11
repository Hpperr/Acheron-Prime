**ETHICAL USE & LEGAL DISCLAIMER**
Acheron Prime is developed strictly for educational purposes, authorized security auditing, and offensive security research.

-Purpose: This framework is designed to help organizations test the resilience of their IDS/IPS systems against high-frequency IP rotation and behavior obfuscation techniques.

-Prohibition: Unauthorized use of this tool against systems without prior written consent is illegal and strictly prohibited.

-Responsibility: The author Hpperr assumes no liability and is not responsible for any misuse or damage caused by this program. Users are solely responsible for complying with local and international laws.

-Compliance: This tool aligns with the principles of Ethical Hacking and professional Red Teaming operations.



**Key Features**
*Layer 2 Obfuscation: Automatic MAC Address spoofing on startup.

*Layer 3 Enforcement: Kernel-level iptables routing (Transparent Proxy).

*Identity Fluidity: High-velocity Tor circuit rotation (NEWNYM signal).

*Traffic Padding: Generates background noise to bypass AI-based behavioral analysis.

*Panic Protocol: One-click emergency shutdown and trace purging.

Installation
1. Prereq:
Ensure you are running Kali Linux and have the following tools installed:
---------------------------sudo apt update && sudo apt install -y tor iptables curl python3-pip | sudo apt update && sudo apt install -y obfs4proxy-----------------------------------------------------------------
2. Configure Tor Backbone
Edit your Tor configuration file to allow control signals:
---------------------------sudo nano /etc/tor/torrc-------------------------------------------------------------------------------------------------------------
Append these lines to the end of the file:
#UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
#Bridge obfs4 38.229.33.83:80 0BAB3FFC63749298495A5B64E30292E4F064C46A cert=V2vDRnS6Xp9Y6S79F7mR9fS9r8fS9S6/p9Y6S79F7mR9fS9r8fS9S6/p9Y6S79 iat-mode=0
#Bridge obfs4 192.95.36.142:443 CDF2E8525FF362A4AD361CA627F648939746C958 cert=766SreYdAnWv7idA3sh/ZlU9P7vX18C8B5GCH3X7zKInpZ0yv52hILeOIZLid6E7fS9p9g iat-mode=0
And then,restart Tor service:
-------------------------sudo systemctl restart tor-------------------------------------------------------------------------------------------------------------
3. Setup Acheron Prime
Clone the repository and install Python dependencies:
-------------------------git clone https://github.com/Hpperr/Acheron-Prime.git | cd Acheron-Prime | sudo pip3 install -r requirements.txt ----------------------
Usage Guide
Starting the Ghost Protocol
Run the script with root privileges (required for iptables and MAC manipulation):
-------------------------sudo python3 acheron_prime.py----------------------------------------------------------------------------------------------------------

Dashboard Overview
Current IP: Displays your real-time exit node IP.
Recent IP Pivots: A live log of your identity history.
Uptime: Tracks the duration of your stealth session.
*****************************************************************************************************************************************************************
Emergency Exit
+Press CTRL + C at any time to trigger the Panic Handler. This will:
+Flush all iptables rules.
+Restore default network routing.
+Clear DNS cache.
+Purge all system traces of the tool.

{Author}
**Hpperr - Cybersecurity Researcher & Red Team Enthusiast**
   

   
