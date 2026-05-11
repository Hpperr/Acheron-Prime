import os
import time
import threading
import subprocess
import random
import requests
import signal
import sys
import platform
from stem import Signal
from stem.control import Controller

# --- TACTICAL CONFIGURATION ---
INTERFACE = "eth0"        
TOR_CONTROL_PORT = 9051
ROTATION_DELAY = 1.0      
DASHBOARD_REFRESH = 2
MAX_HISTORY = 8

# --- ANSI COLORS ---
G = '\033[92m'  # Green
R = '\033[91m'  # Red
Y = '\033[93m'  # Yellow
B = '\033[94m'  # Blue
C = '\033[96m'  # Cyan
W = '\033[0m'   # White
BOLD = '\033[1m'

class AcheronPrime:
    def __init__(self):
        self.is_active = True
        self.current_ip = "Connecting..."
        self.current_country = "Scanning..."
        self.history = []
        self.lock = threading.Lock()
        self.start_time = time.time()

    def print_banner(self):
        os.system('clear' if platform.system() != "Windows" else 'cls')
        banner = f"""
{C}{BOLD}    ___   ______ __  __ ______ ____   ____   _   __
   /   | / ____// / / // ____// __ \ / __ \ / | / /
  / /| |/ /    / /_/ // __/  / /_/ // / / //  |/ / 
 / ___ / /___ / __  // /___ / _, _// /_/ // /|  /  
/_/  |_\____//_/ /_//_____//_/ |_| \____//_/ |_/   
                                                   
          {G}PRIME EDITION v3.0 - BY HPPERR{W}
{Y}    [ Ghost Protocol | Stealth Network Pivoting ]{W}
        """
        print(banner)
        print(f"{B}[*]{W} Verifying Network Interface: {INTERFACE}...")
        time.sleep(1)

    def _exec(self, cmd):
        return subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def panic_handler(self, signum, frame):
        self.is_active = False
        print(f"\n\n{R}{BOLD}[!!!] PANIC SIGNAL: RESTORING DEFAULT NETWORK STATE...{W}")
        self._exec("iptables -F")
        self._exec("iptables -t nat -F")
        self._exec("iptables -P OUTPUT ACCEPT")
        print(f"{G}[+] Cleanup Complete. System Ghosted.{W}")
        sys.exit(0)

    def spoof_mac(self):
        """Thay đổi định danh Layer 2 (MAC Address)"""
        new_mac = f"08:00:27:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}"
        self._exec(f"ip link set dev {INTERFACE} down")
        self._exec(f"ip link set dev {INTERFACE} address {new_mac}")
        self._exec(f"ip link set dev {INTERFACE} up")

    def setup_routing(self):
    
        self._exec("iptables -F")
        self._exec("iptables -t nat -F")
        self._exec("iptables -P OUTPUT ACCEPT")

    def get_network_info(self):
        while self.is_active:
            try:
                proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                res = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=10).json()
                with self.lock:
                    self.current_ip = res.get("ip", "Unknown")
                    self.current_country = res.get("country_name", "Unknown")
                    if not self.history or self.current_ip != self.history[0].split(" - ")[1].split(" (")[0]:
                        entry = f"{time.strftime('%H:%M:%S')} - {self.current_ip} ({self.current_country})"
                        self.history.insert(0, entry)
                        self.history = self.history[:MAX_HISTORY]
            except:
                with self.lock:
                    self.current_ip = "Tor Not Ready"
                    self.current_country = "Check Bridges"
            time.sleep(DASHBOARD_REFRESH)

    def rotate_identity(self):
        while self.is_active:
            try:
                with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
                    controller.authenticate(password="") 
                    controller.signal(Signal.NEWNYM)
            except:
                pass
            time.sleep(ROTATION_DELAY)

    def draw_ui(self):
    
        while self.is_active:
            os.system('clear' if platform.system() != "Windows" else 'cls')
            uptime = int(time.time() - self.start_time)
            
            print(f"{C}┌" + "─"*62 + f"┐{W}")
            print(f"{C}│{W}  {BOLD}ACHERON PRIME v3.0{W} | {G}STEALTH NETWORK PIVOTING{W}               {C}│{W}")
            print(f"{C}├" + "─"*62 + f"┤{W}")
            print(f"{C}│{W}  STATUS     : {G}[ OPERATIONAL ]{W}          UPTIME: {uptime:<6}s      {C}│{W}")
            print(f"{C}│{W}  INTERFACE  : {Y}{INTERFACE:<10}{W}               MODE  : {R}GHOST{W}      {C}│{W}")
            print(f"{C}│{W}  CURRENT IP : {G}{self.current_ip:<15}{W}          LOC   : {C}{self.current_country[:10]:<10}{W} {C}│{W}")
            print(f"{C}├" + "─"*62 + f"┤{W}")
            print(f"{C}│{W}  {BOLD}REAL-TIME IP ROTATION LOG (BY HPPERR):{W}                     {C}│{W}")
            
            with self.lock:
                for entry in self.history:
                    print(f"{C}│{W}  {G}[+]{W} {entry:<54} {C}│{W}")
                for _ in range(MAX_HISTORY - len(self.history)):
                    print(f"{C}│{W}  {' ': <58} {C}│{W}")
            
            print(f"{C}├" + "─"*62 + f"┤{W}")
            print(f"{C}│{W}  {Y}[!]{W} INTEGRATED PROXY ACTIVE (ISOLATED MODE)                 {C}│{W}")
            print(f"{C}│{W}  {R}[*]{W} PRESS CTRL+C FOR EMERGENCY EXIT                         {C}│{W}")
            print(f"{C}└" + "─"*62 + f"┘{W}")
            time.sleep(1)

    def run(self):
        if os.getuid() != 0:
            print(f"{R}[!] ERROR: Root privileges required for MAC Spoofing.{W}")
            return

        self.print_banner()
        signal.signal(signal.SIGINT, self.panic_handler)

        self.spoof_mac()     # Layer 2
        self.setup_routing() # Layer 3 Rs
        
        threads = [
            threading.Thread(target=self.rotate_identity, daemon=True),
            threading.Thread(target=self.get_network_info, daemon=True),
            threading.Thread(target=self.draw_ui, daemon=True)
        ]
        
        for t in threads: t.start()
        
        while self.is_active:
            time.sleep(1)

if __name__ == "__main__":
    AcheronPrime().run()
