import time
import sys
import argparse
import subprocess
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class SecurityAuditor:
    def __init__(self, target_ip, distro="kali-linux", hack_mode=False):
        self.target_ip = target_ip
        self.distro = distro
        self.hack_mode = hack_mode
        self.base_cmd = ["wsl", "-d", self.distro, "bash", "-c"]

    def log(self, msg, style="green"):
        timestamp = time.strftime("%H:%M:%S")
        console.print(f"[{timestamp}] [bold {style}]>[/] {msg}")

    def run_wsl(self, cmd, interactive=False):
        """Runs a safe diagnostic WSL command."""
        self.log(f"EXECUTING IN KALI: {cmd}", "bold yellow")
        try:
            if interactive:
                subprocess.run(self.base_cmd + [cmd])
            else:
                process = subprocess.Popen(
                    self.base_cmd + [cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                for line in iter(process.stdout.readline, ""):
                    if line:
                        console.print(f"  [dim green]{line.strip()}[/]")
                process.wait()
        except Exception as e:
            self.log(f"WSL_ERROR: {str(e)}", "red")

    def module_nmap(self):
        console.print("\n[bold cyan]--- NETWORK RECON (NMAP) ---[/]")
        console.print("  [1] Fast Port Scan (-F)")
        console.print("  [2] Standard Scan (-sV)")
        mode = Prompt.ask("Select Scan Type", choices=["1", "2"], show_choices=False, default="1")
        
        args = {
            "1": f"nmap -F {self.target_ip}",
            "2": f"nmap -sV {self.target_ip}"
        }.get(mode, f"nmap {self.target_ip}")

        self.run_wsl(args)

    def module_ping(self):
        console.print("\n[bold cyan]--- CONNECTIVITY TEST ---[/]")
        self.run_wsl(f"ping -c 4 {self.target_ip}")

    def module_dns(self):
        console.print("\n[bold cyan]--- DNS / WHOIS INFO ---[/]")
        self.run_wsl(f"whois {self.target_ip} || nslookup {self.target_ip}")

    def module_geolocate(self):
        console.print("\n[bold cyan]--- IP GEOLOCATION TRACKING ---[/]")
        try:
            target = self.target_ip

            import os
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IPGeoLocation", "ipgeolocation.py")
            cmd = [sys.executable, script_path]
            if target:
                cmd.extend(["-t", target])
            else:
                cmd.append("-m")
                
            self.log(f"Running IPGeoLocation...", "yellow")
            subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def module_raw_shell(self):
        console.print("\n[bold cyan]--- RAW KALI SHELL ---[/]")
        console.print("[dim]You are now entering a true interactive Kali Linux terminal.[/]")
        console.print("[dim]Type 'exit' to return to the Phantom Toolkit.[/]")
        try:
            # Spawn a true pseudo-terminal directly bridging to the WSL Kali subsystem
            subprocess.run(["wsl", "-d", self.distro, "bash", "-i"])
        except Exception as e:
            console.print(f"  [red]ERROR launching shell: {str(e)}[/]")

    def module_sqlmap(self):
        console.print("\n[bold cyan]--- VULNERABILITY SCAN (SQLMAP) ---[/]")
        console.print("  [1] Basic Injection Test")
        console.print("  [2] Automated Form Crawl")
        
        mode = Prompt.ask("Select Scan Type", choices=["1", "2"], show_choices=False, default="1")
        
        url = Prompt.ask("[bold green]Enter Target URL (e.g. http://example.com/page?id=1)[/]")
        
        if mode == "1":
            self.run_wsl(f"sqlmap -u '{url}' --dbs --random-agent", interactive=True)
        elif mode == "2":
            self.run_wsl(f"sqlmap -u '{url}' --forms --crawl=2 --random-agent", interactive=True)

    def module_nat_converter(self):
        console.print("\n[bold cyan]--- NAT IP CONVERTER (PRIVATE TO PUBLIC) ---[/]")
        try:
            import socket
            import requests

            # Get Private IP (even if it's the target, but if it is not LAN, skip or just get the system's)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('10.255.255.255', 1))
                private_ip = s.getsockname()[0]
            except Exception:
                private_ip = '127.0.0.1'
            finally:
                s.close()

            # The user might have entered a private IP, so let's honor that if they did. 
            target = self.target_ip
            if target.startswith("192.168.") or target.startswith("10.") or target.startswith("127."):
                private_ip = target

            self.log(f"Mapping Private IP ({private_ip}) to Public Gateway...", "yellow")
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            if response.status_code == 200:
                public_ip = response.json().get('ip')
                console.print(f"\n  [bold green]PRIVATE LAN IP:[/]   [bold yellow]{private_ip}[/]")
                console.print(f"         [bold magenta]|[/]")
                console.print(f"         [bold magenta]v[/] [italic dim]NAT Translation[/]")
                console.print(f"  [bold green]PUBLIC WAN IP:[/]    [bold cyan]{public_ip}[/]\n")
            else:
                console.print("  [red]Failed to reach public API.[/]")
        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def module_vulnerability_scanner(self):
        console.print("\n[bold cyan]--- VULNERABILITY SCANNER (STORAGE DISCOVERY) ---[/]")
        url = Prompt.ask("[bold green]Enter Target Website URL (e.g. chess.com)[/]")
        
        if not url:
            return

        try:
            import os
            # Run the newly created vulnerability_scanner.py
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vulnerability_scanner.py")
            cmd = [sys.executable, script_path, url]
            
            self.log(f"Initializing Storage Discovery for {url}...", "yellow")
            
            # Clear previous findings
            if os.path.exists("last_findings.txt"):
                os.remove("last_findings.txt")
                
            subprocess.run(cmd)
            
            # Check for findings to offer "Hack All"
            if os.path.exists("last_findings.txt"):
                with open("last_findings.txt", "r") as f:
                    vulnerable_urls = [line.strip() for line in f if line.strip()]
                
                if vulnerable_urls:
                    console.print(f"\n[bold red][!] DISCOVERED {len(vulnerable_urls)} POTENTIAL TARGETS[/]")
                    confirm = Prompt.ask("[bold cyan]Try hack all? (Runs SQLMap on every finding) [y/N][/]", default="n")
                    
                    if confirm.lower() == 'y':
                        for v_url in vulnerable_urls:
                            console.print(Panel(f"[bold red]AUTOHACK INITIATED:[/] {v_url}", border_style="red"))
                            self.run_wsl(f"sqlmap -u '{v_url}' --batch --random-agent --dbms=mysql --level=1", interactive=True)
                        console.print("[bold green]Automated exploit sequence completed.[/]")
                else:
                    self.log("No high-priority targets found for automated hacking.", "dim white")

        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def module_protocol_converter(self):
        console.print("\n[bold cyan]--- PROTOCOL CONVERTER (IPv6 -> IPv4) ---[/]")
        target = Prompt.ask("[bold green]Enter IPv6 Address or Hostname[/]")
        
        if not target:
            return

        self.log(f"Translating {target} to IPv4 stack...", "yellow")
        
        try:
            import socket
            
            # 1. Handle Hostname Resolution (Forcing A record)
            try:
                ipv4 = socket.gethostbyname(target)
                console.print(Panel(
                    f"[bold white]Target:[/] {target}\n"
                    f"[bold green]Resolved IPv4:[/] [bold cyan]{ipv4}[/]",
                    title="[bold magenta]DNS RE-ROUTE[/]",
                    border_style="cyan"
                ))
                self.target_ip = ipv4 # Update target for subsequent modules
                self.log(f"Target stack successfully switched to IPv4: {ipv4}", "green")
                return
            except socket.gaierror:
                pass

            # 2. Check for IPv4-mapped IPv6 (::ffff:1.2.3.4)
            if ":" in target and "." in target:
                ipv4 = target.split(":")[-1]
                console.print(f"  [bold green][+][/] Extracted Mapped IPv4: [bold cyan]{ipv4}[/]")
                self.target_ip = ipv4
                return

            # 3. Fallback: Reverse DNS then resolve
            self.log("Attempting Deep Protocol Translation...", "dim white")
            try:
                host_info = socket.gethostbyaddr(target)
                if host_info:
                    hostname = host_info[0]
                    ipv4 = socket.gethostbyname(hostname)
                    console.print(f"  [bold green][+][/] Protocol Bridge Established via {hostname}")
                    console.print(f"  [bold green][+][/] Extracted IPv4: [bold cyan]{ipv4}[/]")
                    self.target_ip = ipv4
                else:
                    console.print("  [red][!] Failed to bridge protocol. Target may be IPv6-only.[/]")
            except:
                console.print("  [red][!] Reverse DNS failed. No IPv4 bridge found.[/]")

        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def module_holder_tracer(self):
        console.print("\n[bold red]--- HOLDER TRACER (IDENTITY / OSINT) ---[/]")
        target = Prompt.ask("[bold green]Enter Target Website (e.g. molverse.tech)[/]")
        
        if not target:
            return

        try:
            import os
            import sys
            import subprocess
            # Run the newly created holder_tracer.py
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "holder_tracer.py")
            cmd = [sys.executable, script_path, target]
            
            self.log(f"Establishing OSINT baseline for {target}...", "yellow")
            subprocess.run(cmd)
        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def module_geocoder(self):
        console.print("\n[bold magenta]--- PRECISION GEOCODER (ADDRESS -> GPS) ---[/]")
        address = Prompt.ask("[bold green]Enter Physical Address[/]")
        
        if not address:
            return

        try:
            import os
            import sys
            import subprocess
            # Run the newly created geocoder_tool.py
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geocoder_tool.py")
            cmd = [sys.executable, script_path, address]
            
            self.log(f"Initiating Geocoding Protocol for target address...", "yellow")
            subprocess.run(cmd)
        except Exception as e:
            console.print(f"  [red]ERROR: {str(e)}[/]")

    def run(self):
        self.print_logo()
        console.print(Panel(
            Text("LEGAL DISCLAIMER: The developer of Phantom-IP is NOT responsible for any illegal use of this toolkit.\n"
                 "This tool is for educational and authorized security auditing purposes only.", 
                 justify="center", style="bold red"), 
            border_style="red"
        ))
        
        console.print(Panel(Text(f"PHANTOM SECURITY AUDITOR // TARGET: {self.target_ip}", justify="center", style="bold green"), border_style="green"))
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description=f"Testing route to {self.target_ip}...", total=None)
            self.run_wsl(f"ping -c 1 -W 2 {self.target_ip} > /dev/null && echo '[+] Host is Online' || echo '[-] Host Unreachable'")

        while True:
            console.print("\n[bold white]AVAILABLE DIAGNOSTICS:[/]")
            console.print("  [bold green][1][/] Network Recon (Nmap)")
            console.print("  [bold green][2][/] Connectivity Test (Ping)")
            console.print("  [bold green][3][/] IP Query (Whois/NSLookup)")
            console.print("  [bold green][4][/] Diagnostic Shell (Direct Kali Input)")
            console.print("  [bold magenta][5][/] Geolocation Tracking (Lat/Lon/ISP)")
            console.print("  [bold yellow][6][/] Vulnerability Scan (SQLMap)")
            console.print("  [bold blue][7][/] Private->Public IP Converter (NAT)")
            console.print("  [bold red][8][/] Vulnerability Scanner (Storage/Endpoints)")
            console.print("  [bold cyan][9][/] Protocol Converter (IPv6 -> IPv4)")
            console.print("  [bold yellow][10][/] Holder Tracer (Identity/OSINT)")
            console.print("  [bold magenta][11][/] Precision Geocoder (Address -> GPS)")
            console.print("  [bold red][0][/] Exit Toolkit")
            
            choice = Prompt.ask("\n[bold cyan]Select Module[/]", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"], show_choices=False)

            if choice == "1":
                self.module_nmap()
            elif choice == "2":
                self.module_ping()
            elif choice == "3":
                self.module_dns()
            elif choice == "4":
                self.module_raw_shell()
            elif choice == "5":
                self.module_geolocate()
            elif choice == "6":
                self.module_sqlmap()
            elif choice == "7":
                self.module_nat_converter()
            elif choice == "8":
                self.module_vulnerability_scanner()
            elif choice == "9":
                self.module_protocol_converter()
            elif choice == "10":
                self.module_holder_tracer()
            elif choice == "11":
                self.module_geocoder()
            elif choice == "0":
                self.log("Terminating session...", "yellow")
                sys.exit(0)

    def print_logo(self):
        logo = """
     ,===========================,
    ||       PHANTOM-IP         ||
    ||    SECURITY AUDITOR      ||
    '==========================='
          \\   .  .   /
           \\ |    | /
            ||====||
            ||====||
            \\      /
             '====' 
        """
        console.print(f"[bold green]{logo}[/]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Accept arbitrary leftover args from the .bat script so it doesn't crash on 'pc' or 'toolkit'
    parser.add_argument("dummy_args", nargs="*", help=argparse.SUPPRESS)
    parser.add_argument("--ip", help="Target IP Address")
    parser.add_argument("--hack", action="store_true", help="Enable offensive modules")
    args = parser.parse_args()
    
    target = args.ip
    if not target and args.dummy_args:
        # User might have passed IP as a positional argument
        target = args.dummy_args[-1] 
    
    if not target:
        target = Prompt.ask("[bold green]ENTER TARGET IP[/]")
    
    cli = SecurityAuditor(target, hack_mode=args.hack)
    cli.run()
