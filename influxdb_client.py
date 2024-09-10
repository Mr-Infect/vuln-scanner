from influxdb import InfluxDBClient

# Initialize InfluxDB client
client = InfluxDBClient(host='localhost', port=8088, database='vuln_scanner')

def send_to_influxdb(scan_results):
    json_body = []
    
    for result in scan_results:
        data_point = {
            "measurement": "vulnerability_scan",
            "tags": {
                "host": result['host'],
                "port": result['port'],
                "service": result['name']
            },
            "fields": {
                "state": result['state'],
                "product": result['product'],
                "version": result['version'],
            },
            "time": result['time']
        }
        json_body.append(data_point)
    
    # Write data to InfluxDB
    client.write_points(json_body)

if __name__ == "__main__":
    client.create_database('vuln_scanner')
