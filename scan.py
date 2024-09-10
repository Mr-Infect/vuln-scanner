import nmap
import time
from influxdb_client import send_to_influxdb

# Initialize nmap scanner
nm = nmap.PortScanner()

# Function to scan a target for open ports and services
def scan_target(target):
    print(f"Scanning {target}...")
    nm.scan(target, '1-65535')
    
    scan_results = []
    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                result = {
                    'host': host,
                    'port': port,
                    'state': nm[host][proto][port]['state'],
                    'name': nm[host][proto][port]['name'],
                    'product': nm[host][proto][port]['product'],
                    'version': nm[host][proto][port]['version'],
                    'time': int(time.time())
                }
                scan_results.append(result)
                print(f"Port: {port}, State: {nm[host][proto][port]['state']}")
    
    return scan_results

if __name__ == "__main__":
    target_ip = '192.168.1.1/24'  # Replace with your target network
    results = scan_target(target_ip)
    
    # Send results to InfluxDB
    send_to_influxdb(results)
