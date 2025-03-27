from flask import Flask, render_template, jsonify
import subprocess
import re
import time
import os
import csv
import requests

app = Flask(__name__)

# creates csv file if it doesn't exist
def init_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ip', 'isp'])

# gets ISP data from CSV file
def get_isp_from_csv(ip, file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ip'] == ip:
                return row['isp']
    return None

# saves ISP data to CSV file
def save_isp_to_csv(ip, isp, file_path):
    # Verifica si la IP ya existe en el archivo
    if get_isp_from_csv(ip, file_path) is not None:
        return  # No hace nada si la IP ya existe

    # if the IP doesn't exist, adds it to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip, isp])

# cleans the CSV file by removing duplicate IPs
def clean_csv(file_path):
    if not os.path.exists(file_path):
        return

    seen_ips = set()
    rows = []

    # read the CSV file and remove duplicate IPs
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ip'] not in seen_ips:
                seen_ips.add(row['ip'])
                rows.append(row)

    # write the cleaned data back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ip', 'isp'])
        writer.writeheader()
        writer.writerows(rows)

# gets ISP data from the API or CSV file
def get_isp(ip, file_path):
    if ip.startswith("10.20"):
        return "INTERNAL"
    
    # Busca en el archivo CSV primero
    isp = get_isp_from_csv(ip, file_path)
    if isp:
        return isp
    
    # Si no está en el CSV, consulta la API
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        isp = data.get('org', 'Unknown ISP')
        save_isp_to_csv(ip, isp, file_path)  # Guarda el resultado en el CSV
        return isp
    except:
        return "Unknown ISP"

# gets WireGuard status
def get_wg_status():
    csv_file_path = 'isp_data.csv'
    init_csv(csv_file_path)

    try:
        output = subprocess.check_output(['wg', 'show'], universal_newlines=True)
        allowed_ips_info = re.findall(r'allowed ips: ([\d.]+/\d+)', output)
        endpoint_info = re.findall(r'endpoint: ([\d.]+):', output)
        handshake_info = re.findall(r'latest handshake: (.+)', output)

        ip_isp_info = []
        for allowed_ips, endpoint_ip, last_handshake in zip(allowed_ips_info, endpoint_info, handshake_info):
            isp = get_isp(endpoint_ip, csv_file_path)
            online_status = is_online(last_handshake)
            ip_isp_info.append({
                'ip': allowed_ips.split('/')[0],
                'endpoint_ip': endpoint_ip,
                'isp': isp,
                'online_status': online_status
            })

        # Ordenar las IPs
        ip_isp_info.sort(key=lambda x: [int(part) for part in x['ip'].split('.')])
        return ip_isp_info
    except Exception as e:
        return {'error': str(e)}

def is_online(last_handshake):
    last_handshake = last_handshake.split(', ')
    hours, minutes, seconds = 0, 0, 0

    for part in last_handshake:
        if 'hour' in part:
            hours = int(part.split()[0])
        elif 'minute' in part:
            minutes = int(part.split()[0])
        elif 'second' in part:
            seconds = int(part.split()[0])

    total_minutes = hours * 60 + minutes + seconds / 60
    return total_minutes <= 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify(get_wg_status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)