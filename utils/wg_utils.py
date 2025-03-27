def get_wireguard_status():
    import subprocess
    import re

    try:
        # Execute `wg show` command locally
        output = subprocess.check_output(['wg', 'show'], universal_newlines=True)

        allowed_ips_info = re.findall(r'allowed ips: ([\d.]+/\d+)', output)
        endpoint_info = re.findall(r'endpoint: ([\d.]+):', output)
        handshake_info = re.findall(r'latest handshake: (.+)', output)

        ip_isp_info = []
        for allowed_ips, endpoint_ip, last_handshake in zip(allowed_ips_info, endpoint_info, handshake_info):
            online_status = is_online(last_handshake)
            ip_isp_info.append((allowed_ips.split('/')[0], endpoint_ip, online_status))

        return ip_isp_info

    except Exception as e:
        return str(e)

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