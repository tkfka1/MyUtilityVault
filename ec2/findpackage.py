data = """

"""

# Parsing function to extract server information
def parse_data(data):
    servers = []
    current_server = {}
    
    for line in data.split('\n'):
        if line.startswith("LDZ"):
            if current_server:
                servers.append(current_server)
                current_server = {}
            current_server['name'] = line.split('[')[0].strip()
            current_server['ip'] = line.split('[')[1].strip('[]')
        elif line.startswith("[root@"):
            command = line.split('#')[-1].strip()
            if 'uname -a' in command:
                current_server['kernel_version'] = command
            elif 'cat /etc/*release' in command:
                current_server['release_info'] = command
            elif 'ps -ef | grep' in command:
                current_server['processes'] = command
            elif 'rpm -qa | grep' in command:
                current_server['packages'] = command
                
    # Capture the last server if the loop ends
    if current_server:
        servers.append(current_server)
    return servers

# Format and write the parsed data to a text file
def write_to_file(servers):
    with open('server_info.txt', 'w') as file:
        for server in servers:
            file.write(f"Server Name: {server.get('name', 'N/A')}\n")
            file.write(f"IP Address: {server.get('ip', 'N/A')}\n")
            file.write(f"Kernel Version: {server.get('kernel_version', 'N/A')}\n")
            file.write(f"Release Info: {server.get('release_info', 'N/A')}\n")
            file.write(f"Processes: {server.get('processes', 'N/A')}\n")
            file.write(f"Packages: {server.get('packages', 'N/A')}\n")
            file.write('---------------------------------------------\n')

# Main execution
server_data = parse_data(data)
write_to_file(server_data)