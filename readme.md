# 💀 PHANTOM-IP // ULTIMATE SECURITY AUDITOR SUITE

![Static Badge](https://img.shields.io/badge/Security-Auditor-red?style=for-the-badge&logoChar=white)
![Static Badge](https://img.shields.io/badge/Stack-WSL_Kali-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Status-Active_Recon-green?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Build-Premium_CLI-cyan?style=for-the-badge)

A high-fidelity, professional cybersecurity reconnaissance and auditing toolkit integrated with **WSL Kali Linux**. 

> [!CAUTION]
> **LEGAL DISCLAIMER**: The developer of Phantom-IP is NOT responsible for any illegal use of this toolkit. This tool is intended for educational purposes and authorized security auditing only. The owner assumes no liability for misuse.

## 🚀 Core Features
*   **Network Recon (Nmap)**: High-speed port scanning and service detection.
*   **Vulnerability Scanner**: Advanced directory discovery (Crawl + Fuzz) with wordlists targeting sensitive files (`.env`, backups, database dumps).
*   **Auto-Exploit (SQLMap)**: Automated hand-off from reconnaissance to SQL injection exploitation using batch mode.
*   **IP Geolocation Tracking**: Powered by the **IPGeoLocation** project by **@maldevel**. This component has been integrated and optimized for the Phantom-IP suite.
*   **Protocol Bridge (IPv6 -> IPv4)**: Force IPv4 stack resolution for modern double-stack targets.
*   **Holder Tracer (OSINT)**: Identity discovery using digital footprint mapping to find domain owners.
*   **Precision Geocoder**: Code-based GPS pinpointing for physical addresses.

## ⚖️ Credits & Attribution
Phantom-IP integrates several powerful open-source utilities. Full credit is given to the original authors:
*   **IPGeoLocation**: Originally created by [maldevel](https://github.com/maldevel/IPGeoLocation). The developer of Phantom-IP has curated and integrated this tool into the suite to provide a seamless auditing experience.
*   **Recon Tools**: Standard industry tools like `nmap`, `sqlmap`, and `whois` are utilized via the WSL environment.

## 🛠️ Installation
Ensure you have Python 3 and a WSL Kali Linux environment installed.
```bash
# Clone the repository
git clone https://github.com/[YOUR_USERNAME]/phantom-ip-suite.git
cd phantom-ip-suite

# Install dependencies
pip install requests beautifulsoup4 rich
```

## 🎮 How to Use
Launch the main toolkit using the provided CLI:
```bash
python phantom_cli.py
```

## 💎 Aesthetics & Design
*   **Rich Terminal Console**: Beautifully formatted tables, panels, and progress bars.
*   **Cinematic Logo**: High-impact ASCII art for terminal presence.
*   **Real-time Progress**: Spinner and bar columns for live feedback during scans.

## 🛡️ License
Distributed for educational and research purposes under the MIT License. The owner assumes no liability for misuse.

---
**Tags**: #CyberSecurity #RedTeam #Pentesting #Python #KaliLinux #OSINT #VulnerabilityScanner #InformationSecurity #HackTheBox #EthicalHacking
