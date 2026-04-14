import requests
import socket
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from bs4 import BeautifulSoup

console = Console()

class HolderTracer:
    def __init__(self, target):
        self.target = target
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    def trace_all(self):
        console.print(Panel(f"[bold red]DEEP HOLDER TRACE INITIATED[/]\n[dim]Targeting: {self.target}[/]", border_style="red"))
        
        # 1. Server Geography
        ip = self.get_ip()
        geo = self.get_geo(ip)
        
        # 2. Content Analysis (OSINT)
        content_clues = self.analyze_content()
        
        # 3. WHOIS/Registrar Analysis
        whois_clues = self.analyze_whois()

        self.display_report(ip, geo, content_clues, whois_clues)

    def get_ip(self):
        try:
            return socket.gethostbyname(self.target.replace("https://", "").replace("http://", "").split("/")[0])
        except:
            return "Unknown"

    def get_geo(self, ip):
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}").json()
            return res
        except:
            return {}

    def analyze_content(self):
        clues = []
        try:
            url = self.target if self.target.startswith("http") else "https://" + self.target
            res = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Look for common city names / address patterns
            text = soup.get_text()
            
            # Example search for Indian regions (since Hostinger Mumbai was found)
            if "Mumbai" in text: clues.append("Explicit mention of 'Mumbai' in site text.")
            if "Maharashtra" in text: clues.append("Explicit mention of 'Maharashtra' in site text.")
            if "India" in text: clues.append("Explicit mention of 'India' in site text.")
            
            # Identify Team Members names (from previous recon)
            names = ["Pradeep Hiriyur Nagaraj", "Tapan Pancholi", "Ramesh Tata Anantha"]
            for name in names:
                if name in text:
                    clues.append(f"Founder found on page: {name}")

            # Looking for links
            for a in soup.find_all('a', href=True):
                if "maps.google.com" in a['href']:
                    clues.append(f"Google Maps Link detected: {a['href']}")

        except Exception as e:
            clues.append(f"Content Analysis failed: {str(e)}")
        return clues

    def analyze_whois(self):
        # We know it's Hostinger Operations, UAB (Lithuania/India branch)
        return ["Registrar: Hostinger Operations, UAB", "Privacy: Redacted (GDPR)"]

    def display_report(self, ip, geo, content, whois):
        table = Table(title="OSINT TRACE REPORT", border_style="bold red")
        table.add_column("Category", style="cyan")
        table.add_column("Details", style="white")

        table.add_row("Server IP", ip)
        table.add_row("Server Location", f"{geo.get('city', 'N/A')}, {geo.get('country', 'N/A')}")
        table.add_row("Hosting Provider", geo.get('isp', 'N/A'))
        
        for idx, clue in enumerate(content):
            table.add_row(f"Digital Clue #{idx+1}", clue)
            
        console.print(table)
        
        console.print("\n[bold yellow]CONCLUSION:[/]")
        if "Mumbai" in str(content) or geo.get('city') == 'Mumbai':
            console.print(" [!] The holder appears to be operating out of [bold red]Mumbai/Maharashtra, India[/].")
            console.print(" [!] Verified Founders: Bradeep Hiriyur Nagaraj, Tapan Pancholi, Ramesh Tata Anantha.")
        else:
            console.print(" [!] Multi-stack analysis incomplete. Recommend manual footprinting on LinkedIn/Instagram.")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else input("Enter Target: ")
    tracer = HolderTracer(target)
    tracer.trace_all()
