import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import sys

console = Console()

class PrecisionGeocoder:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            "User-Agent": "Phantom-IP-Security-Auditor/1.0 (Educational/Security Research)"
        }

    def geocode(self, address):
        console.print(Panel(f"[bold cyan]PRECISION GEOCODING ENGINE[/]\n[dim]Target Address: {address}[/]", border_style="cyan"))
        
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            data = response.json()
            
            # Smart Retry: If precise address fails, try stripping first part (like House No)
            if not data and "," in address:
                simplified_address = ",".join(address.split(",")[1:])
                console.print(f"[dim]Refining search...[/]")
                params["q"] = simplified_address
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                data = response.json()

            if data:
                res = data[0]
                lat = res.get("lat")
                lon = res.get("lon")
                display_name = res.get("display_name")
                
                table = Table(title="GEOCODING RESULTS", border_style="bold green")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("Address Found", display_name)
                table.add_row("Latitude", f"[bold yellow]{lat}[/]")
                table.add_row("Longitude", f"[bold yellow]{lon}[/]")
                table.add_row("Map Link", f"https://www.google.com/maps/search/{lat},{lon}")
                
                console.print(table)
                console.print(f"\n[bold green][+][/] PINPOINT ACCURANCY ESTABLISHED.")
                return lat, lon
            else:
                console.print("[bold red][!] No coordinates found for this specific address.[/]")
                return None, None
                
        except Exception as e:
            console.print(f"[bold red][!] Geocoding error: {str(e)}[/]")
            return None, None

if __name__ == "__main__":
    geocoder = PrecisionGeocoder()
    if len(sys.argv) > 1:
        # Join all args as the address
        address = " ".join(sys.argv[1:])
        geocoder.geocode(address)
    else:
        addr = input("Enter Address to Geocode: ")
        geocoder.geocode(addr)
