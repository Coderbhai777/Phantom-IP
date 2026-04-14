import time
import sys
import argparse
import subprocess
import threading
import requests
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text

console = Console()

class PhantomTUI:
    def __init__(self, target_ip="192.168.1.1", mode="standard", distro="kali-linux"):
        self.target_ip = target_ip
        self.mode = mode
        self.distro = distro
        self.logs = []
        self.geo_data = {}
        self.start_time = time.time()
        self.is_running = True

    def fetch_ip_metadata(self):
        try:
            import os, sys
            plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IPGeoLocation")
            if plugin_path not in sys.path:
                sys.path.append(plugin_path)
            
            from IpGeoLocation import IpGeoLocationLib
            from core.Logger import Logger
            
            logger = Logger(nolog=True, verbose=False)
            # Suppress terminal prints to prevent breaking Rich TUI Layout
            logger.Print = lambda *a, **k: None  
            logger.PrintError = lambda *a, **k: None
            
            lib = IpGeoLocationLib(self.target_ip, logger, noprint=True, nolog=True)
            ip_obj = lib._IpGeoLocationLib__retrieveGeolocation(self.target_ip)
            
            if ip_obj:
                self.geo_data = {
                    "status": "success",
                    "country": ip_obj.Country,
                    "countryCode": ip_obj.CountryCode,
                    "regionName": ip_obj.RegionName,
                    "city": ip_obj.City,
                    "zip": ip_obj.Zip,
                    "lat": ip_obj.Latitude,
                    "lon": ip_obj.Longtitude,
                    "timezone": ip_obj.Timezone,
                    "isp": ip_obj.ISP,
                    "org": ip_obj.Organization,
                    "as": ip_obj.ASN
                }
        except Exception as e:
            self.add_log(f"GEO_ERROR: {str(e)}")

    def make_layout(self) -> Layout:
        layout = Layout()
        layout.split(Layout(name="header", size=3), Layout(name="main", ratio=1), Layout(name="footer", size=8))
        layout["main"].split_row(Layout(name="side", size=35), Layout(name="body", ratio=1))
        layout["side"].split(Layout(name="stats", ratio=1), Layout(name="location", ratio=1))
        return layout

    def get_header(self) -> Panel:
        color = "green"
        title = f"PHANTOM-IP // {self.mode.upper()} MODE // RECON ONLY"
        return Panel(Text(title, style=f"bold {color}", justify="center"), style=color)

    def get_stats(self) -> Panel:
        table = Table.grid(padding=1)
        table.add_column(style="dim"); table.add_column(style="bold green")
        table.add_row("TARGET:", self.target_ip)
        table.add_row("MODE:", self.mode.upper())
        table.add_row("WSL:", self.distro.upper())
        return Panel(table, title="[bold]SYSTEM STATS[/]", border_style="green")

    def get_location_panel(self) -> Panel:
        table = Table.grid(padding=1)
        table.add_column(style="dim"); table.add_column(style="bold cyan")
        if self.geo_data and self.geo_data.get("status") != "fail":
            table.add_row("COUNTRY:", f"{self.geo_data.get('country', 'N/A')} ({self.geo_data.get('countryCode', '')})")
            table.add_row("REGION:", self.geo_data.get("regionName", "N/A"))
            table.add_row("CITY:", f"{self.geo_data.get('city', 'N/A')} ({self.geo_data.get('zip', '')})")
            
            lat = self.geo_data.get("lat", "N/A")
            lon = self.geo_data.get("lon", "N/A")
            table.add_row("COORDS:", f"{lat}, {lon}")
            table.add_row("TIMEZONE:", self.geo_data.get("timezone", "N/A"))

            table.add_row("ISP:", self.geo_data.get("isp", "N/A"))
            table.add_row("ORG:", self.geo_data.get("org", "N/A"))
            table.add_row("ASN:", str(self.geo_data.get("as", "N/A")).split(" ")[0])
            
            if lat != "N/A" and lon != "N/A":
                table.add_row("MAPS:", f"https://google.com/maps?q={lat},{lon}")
        else:
            table.add_row("STATUS:", "TARGET OFFLINE OR LOCAL")
        return Panel(table, title="[bold]GEOINT TRACKING[/]", border_style="cyan")

    def get_terminal(self) -> Panel:
        log_text = Text()
        for log_line in self.logs[-20:]:
            log_text.append(log_line + "\n")
        return Panel(log_text, title="[bold]CONSOLEX[/]", border_style="green")

    def add_log(self, msg):
        self.logs.append(msg.strip())

    def run_wsl_command(self, cmd):
        wsl_cmd = ["wsl", "-d", self.distro, "bash", "-c", cmd]
        try:
            process = subprocess.Popen(wsl_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(process.stdout.readline, ""):
                if line: self.add_log(line)
            process.wait()
        except Exception as e:
            self.add_log(f"BRIDGE_ERROR: {str(e)}")

    def execute_mode_sequence(self):
        """Standard sequence before user interaction."""
        self.add_log(f"--- INITIATING {self.mode.upper()} PROTOCOL ---")
        if self.mode == "phone":
            self.run_wsl_command(f"nmap -v {self.target_ip}")
        elif self.mode == "pc":
            self.run_wsl_command(f"nmap -v -sV {self.target_ip}")
        elif self.mode == "server":
            self.run_wsl_command(f"nmap -v -A -p- {self.target_ip}")
        elif self.mode == "iot":
            self.run_wsl_command(f"nmap -v -p 80,443,23,22,21,554 {self.target_ip}")
        elif self.mode == "sqlmap":
            pass # SQLMap is handled outside the non-interactive thread
        else:
            self.run_wsl_command(f"nmap -F {self.target_ip}")

    def run(self):
        if self.mode == "sqlmap":
            console.print("\n[bold cyan]--- VULNERABILITY SCAN (SQLMAP) ---[/]")
            console.print("[yellow]SQLMap requires interactive confirmation prompts.[/]")
            console.print("[yellow]Launching in Pure Terminal Mode...[/]")
            target_url = self.target_ip if self.target_ip.startswith("http") else f"http://{self.target_ip}"
            
            # Run without TUI capturing stdout so we can type
            wsl_cmd = ["wsl", "-d", self.distro, "bash", "-c", f"sqlmap -u '{target_url}' --random-agent --crawl=1"]
            subprocess.run(wsl_cmd)
            sys.exit(0)

        layout = self.make_layout()
        threading.Thread(target=self.fetch_ip_metadata, daemon=True).start()
        
        # Initial scan thread
        scan_thread = threading.Thread(target=self.execute_mode_sequence, daemon=True)
        scan_thread.start()

        self.add_log("--- SCANNING TARGET IN PROGRESS... ---")

        try:
            with Live(layout, refresh_per_second=10, screen=True):
                while scan_thread.is_alive():
                    layout["header"].update(self.get_header()); layout["stats"].update(self.get_stats())
                    layout["location"].update(self.get_location_panel()); layout["body"].update(self.get_terminal())
                    time.sleep(0.1)
                
                self.add_log("--- RECONNAISSANCE SCAN COMPLETE. ---")
                self.add_log("--- PRESS CTRL+C TO EXIT THE CONSOLE. ---")
                
                # Keep updating the UI until user interrupts
                while True:
                    layout["header"].update(self.get_header()); layout["stats"].update(self.get_stats())
                    layout["location"].update(self.get_location_panel()); layout["body"].update(self.get_terminal())
                    time.sleep(0.1)
        except KeyboardInterrupt:
            console.clear()
            console.print("[bold green]EXITTING PHANTOM TUI...[/]")

from rich.prompt import Prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("positional_args", nargs="*", help="Mode or IP")
    parser.add_argument("--ip", help="Target IP")
    parser.add_argument("--hack", action="store_true", help="Enable offensive modules")
    args = parser.parse_args()

    mode = None
    target = args.ip

    valid_modes = ["phone", "pc", "internet", "standard", "server", "iot", "sqlmap"]
    
    for arg in args.positional_args:
        if arg in valid_modes:
            mode = arg
        elif not target:
            target = arg

    if not mode:
        console.print("\n[bold cyan]--- TARGET PROFILING ---[/]")
        console.print("[1] PC       - Local network computer (SMB/RDP scans)")
        console.print("[2] Server   - Remote server (Full port & OS scans)")
        console.print("[3] Phone    - Mobile device mapping")
        console.print("[4] IoT      - Smart device scan (Cameras, Routers)")
        console.print("[5] Internet - Standard fast network recon")
        console.print("[6] SQLMap   - Vulnerability detection via SQLMap")
        
        mode_choices = {"1": "pc", "2": "server", "3": "phone", "4": "iot", "5": "internet", "6": "sqlmap"}
        choice = Prompt.ask("\n[bold green]SELECT TARGET TYPE[/]", choices=["1", "2", "3", "4", "5", "6"], default="5")
        mode = mode_choices[choice]

    # Select IP
    if not target:
        target = Prompt.ask("\n[bold green]ENTER TARGET IP OR DOMAIN[/]", default="127.0.0.1")
    
    tui = PhantomTUI(target, mode)
    tui.run()
