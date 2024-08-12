import os
import subprocess
import sys
import platform
import socket
import requests
from bs4 import BeautifulSoup
import shodan
import colorama
from colorama import Fore, Style

colorama.init()  # Initialize colorama for colored output

# Function to install packages using the appropriate package manager
def install_package(package_name):
    try:
        distro = platform.linux_distribution()[0].lower()
        if "debian" in distro or "ubuntu" in distro:
            subprocess.check_call(["sudo", "apt-get", "install", "-y", package_name])
        elif "arch" in distro or "manjaro" in distro:
            subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm", package_name])
        else:
            print(f"Unsupported distribution: {distro}")
    except Exception as e:
        print(f"Failed to install {package_name}: {e}")

# Function to install external tools
def install_external_tools():
    tools = ["masscan", "nuclei"]

    for tool in tools:
        try:
            subprocess.check_call(["which", tool])
            print(f"{Fore.GREEN}{tool} is already installed.{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.YELLOW}Installing {tool}...{Style.RESET_ALL}")
            install_package(tool)

# Function to install Python dependencies
def install_python_dependencies():
    required_packages = ["requests", "beautifulsoup4", "shodan"]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{Fore.YELLOW}Installing {package}...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to get IP address from domain
def get_ip_address(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}IP Address of {domain}: {ip}{Style.RESET_ALL}")
        return ip
    except socket.error as e:
        print(f"{Fore.RED}Error getting IP address: {e}{Style.RESET_ALL}")
        return None

# Function to search for subdomains using crt.sh
def search_subdomains(domain):
    print(f"{Fore.CYAN}\nSearching for subdomains of {domain} using crt.sh...{Style.RESET_ALL}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            subdomains = {entry['name_value'] for entry in response.json()}
            print(f"{Fore.GREEN}Found {len(subdomains)} subdomains:{Style.RESET_ALL}")
            for subdomain in subdomains:
                print(subdomain)
                with open(f"results/{domain}/subdomains.txt", "a") as f:
                    f.write(subdomain + "\n")
            return subdomains
        else:
            print(f"{Fore.RED}Failed to retrieve subdomains from crt.sh{Style.RESET_ALL}")
            return set()
    except requests.RequestException as e:
        print(f"{Fore.RED}Error querying crt.sh: {e}{Style.RESET_ALL}")
        return set()

# Function to perform a search using Shodan
def search_shodan(ip, shodan_api_key):
    print(f"{Fore.CYAN}\nSearching Shodan for information on {ip}...{Style.RESET_ALL}")
    api = shodan.Shodan(shodan_api_key)
    try:
        result = api.host(ip)
        print(f"{Fore.GREEN}Information from Shodan about {ip}:{Style.RESET_ALL}")
        print(f"Organization: {result.get('org', 'N/A')}")
        print(f"Operating System: {result.get('os', 'N/A')}")
        with open(f"results/{domain}/shodan.txt", "a") as f:
            f.write(f"Organization: {result.get('org', 'N/A')}\n")
            f.write(f"Operating System: {result.get('os', 'N/A')}\n")
        for item in result['data']:
            print(f"Port: {item['port']} - Banner: {item['data']}")
            with open(f"results/{domain}/shodan.txt", "a") as f:
                f.write(f"Port: {item['port']} - Banner: {item['data']}\n")
    except shodan.APIError as e:
        print(f"{Fore.RED}Error searching Shodan: {e}{Style.RESET_ALL}")

# Function to run Masscan
def run_masscan(ip, ports="1-65535"):
    print(f"{Fore.CYAN}\nRunning Masscan on {ip} for ports {ports}...{Style.RESET_ALL}")
    masscan_cmd = f"masscan {ip} -p{ports} --rate 1000"
    try:
        result = subprocess.run(masscan_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        with open(f"results/{domain}/masscan.txt", "a") as f:
            f.write(output)
        return output
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error running Masscan: {e}{Style.RESET_ALL}")
        return None

# Function to run Nuclei on the results from Masscan
def run_nuclei(ip):
    print(f"{Fore.CYAN}\nRunning Nuclei to find vulnerabilities on {ip}...{Style.RESET_ALL}")
    nuclei_cmd = f"nuclei -u {ip} -t /path/to/nuclei-templates"
    try:
        result = subprocess.run(nuclei_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        with open(f"results/{domain}/nuclei.txt", "a") as f:
            f.write(output)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error running Nuclei: {e}{Style.RESET_ALL}")

# Main function to execute the recon process
def perform_recon(domain, shodan_api_key):
    os.makedirs(f"results/{domain}", exist_ok=True)  # Create results directory
    ip = get_ip_address(domain)
    if ip:
        search_subdomains(domain)
        search_shodan(ip, shodan_api_key)
        masscan_output = run_masscan(ip)
        if masscan_output:
            run_nuclei(ip)

if __name__ == "__main__":
    install_python_dependencies()
    install_external_tools()

    # Replace 'your_shodan_api_key' with your actual Shodan API key
    shodan_api_key = "------------------------------------------------"
    
    domain = input(f"{Fore.CYAN}Enter the domain to perform recon on: {Style.RESET_ALL}")
    perform_recon(domain, shodan_api_key)
