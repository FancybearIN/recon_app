# Recon App

This Python script performs reconnaissance on a given domain, gathering information about its subdomains, IP address, and potential vulnerabilities.

## Features

- **Domain to IP Resolution:** Resolves the domain name to its corresponding IP address.
- **Subdomain Enumeration:** Uses crt.sh to search for subdomains associated with the target domain.
- **Shodan Search:** Queries Shodan for information about the target IP address, including organization, operating system, and open ports.
- **Port Scanning:** Uses Masscan to scan the target IP address for open ports.
- **Vulnerability Scanning:** Employs Nuclei to scan for known vulnerabilities on the target IP address.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `shodan`
- `masscan`
- `nuclei`

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install requests beautifulsoup4 shodan
Install external tools:

Debian/Ubuntu:
sudo apt-get update
sudo apt-get install masscan nuclei
Arch/Manjaro:
sudo pacman -S masscan nuclei
CentOS/RHEL:
sudo yum install masscan nuclei
Fedora:
sudo dnf install masscan nuclei
Other distributions: Check your distribution's package manager documentation for instructions on installing masscan and nuclei.
Obtain a Shodan API key: Sign up for a free Shodan account at https://www.shodan.io/ and get your API key.

Usage
Replace the placeholder Shodan API key: In the shodan_api_key variable, replace "n24dpMs1SK8bWCFhZEz6JriVdxxw1tza" with your actual Shodan API key.

Run the script:

python fg.py
Enter the target domain: When prompted, enter the domain you want to perform reconnaissance on.

Output
The script will output the following information:

IP address of the target domain
List of subdomains found
Shodan information about the target IP address
Results of the Masscan port scan
Results of the Nuclei vulnerability scan
The output of masscan and nuclei will also be written to a file named recon_results.txt.

Notes
Ensure that you have the necessary permissions to run the script and install packages.
The script uses the nuclei command with the -t /path/to/nuclei-templates flag. Replace /path/to/nuclei-templates with the actual path to your Nuclei templates directory.
The script uses the masscan command with the --rate 1000 flag. You can adjust this rate to control the speed of the port scan.
Disclaimer
This script is for educational purposes only. Use it responsibly and ethically. Do not use it for illegal activities.

Contributing
Contributions are welcome! Feel free to submit pull requests or open issues.