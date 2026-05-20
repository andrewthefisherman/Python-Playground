# Ethical-Hacking
This is a collection of python projects and python scripts for various . They are simple, but they cover some of the fundamentals of the technology and the concepts behind modern hacking.

## 🚪 Backdoor - Educational Test Malware
This script is a educational and completely inoffensive version of the modern malware known as a backdoor. It displays the basic functionality of the virus establishing a reverse shell connection and giving the attacker root access to terminal and directories. Its features are:
* Socket Connection Datastream: The most interesting and hardest feature of the script was figuring out how to use the socket python library to send commands and receive supposedly "sensitive" information about the target machine. Data is sliced into chunks of a kilobyte of either string datatype or binary data specifically marked with "End-of" markers.
* Basic Remote Commands: Basic OS commands can be executed remotely on the target machine such as echo (debug), cd, dir
* Download: Possibility to download files from the target machine
* WI-FI Passwords Retrieval: The backdoor uses terminal access on the target machine to retrieve saved WI-FI SSID-Password entries to help the attacker map and gain access inside the private network of the victim or learn more about the machine's network's history
* Google Passwords Extraction: Using exploits of Google Chrome's flawed password storage and autocompletion feature, the script crawls through the target machine to retrieve a specific .db file and send it to the attacker, allowing him to fetch all passwords saved on Chrome
* Machine Information Retrieval: Uses root access to transmit several pieces of information about the target machine such as username and user directory or full network configuration
* Listener Customization: Implemented settings and preferences system
As aforementioned, the script is completely harmless as it is lacking any malware obfuscation and replication technique and it is easily detectable by any modern antivirus software. Just for educational purpose.

## 🔐 Encrypted Communication (Encryption & Decryption)
A pair of CLI scripts (Encryption.py and Decryption.py) that implement a multi-layered, custom encryption algorithm. Rather than relying on simple character substitution, these scripts combine data format conversions with a date-dependent book cipher approach.
Features:
* Dynamic Date-Based Keys: The password used for array shifting dynamically changes based on the current day and month. The decryption module includes specific logic to calculate the offset, allowing the retrieval of messages ciphered on previous days.
* Data Manipulation: The plaintext undergoes sequential transformations, converting into binary and then hexadecimal formats before the main encryption phase.
* Book Cipher Implementation: The primary obfuscation maps characters to an external reference text file (bok.txt). It generates the cipher by adding numeric values derived from the dynamic daily password to the index of the reference text.
* Array Shifting: As a final layer, the encrypted data list undergoes a circular array shift. The magnitude of this shift is determined by the sum of the digits present in the daily password.
* Clipboard Integration: Utilizes the subprocess module to automatically copy the final ciphertext to the Windows clipboard. The terminal interface is visually enhanced using the termcolor library.

## 🎙️ Finn - Voice Assistant
An early-stage, experimental voice assistant named "Finn." Built to operate continuously in the background, this script captures microphone input, parses the text to identify intents, and provides audio feedback. It serves as a practical exploration of speech-to-text (STT) and text-to-speech (TTS) pipelines in Python.
Features:
* Wake Word Activation: Implements an active listening loop (speech_recognition) that triggers command execution only when the wake word ("Finn" or phonetic variations) is detected.
* TTS Audio Feedback: Utilizes pyttsx3 to initialize a local speech engine, allowing the assistant to speak responses, confirm commands, and ask for missing inputs (like message content).
* WhatsApp Automation: Integrates pywhatkit to send instant WhatsApp messages to a predefined dictionary of contacts through pure voice commands.
* Time and Date Parsing: Uses the datetime module to parse specific temporal queries (e.g., "what time is it", "which day is today") and return formatted audio responses.

## ⌨️ Keylogger - Educational Test Malware
This script is a educational and completely inoffensive version of the modern malware known as a keylogger. It displays the basic functionality of the virus recording key presses and transmitting reports to its operator via email. Its features are:
* Keystroke recording: makes use of the pynput.keyboard library to record the key pressed by the target device and stores them
* Text Parsing and Processing: Implemented callback function that preprocesses the text before sending it, adjusting format, ignoring characters that can't be encoded in ASCII code and replaces other pieces of text with a placeholder propting the attacker that a key was pressed but that it wasn't possible to send it
* Automated Reporting: Compiles logs which are sent to the operator at fixed time intervals using the smtplib library and thus transmitting via email
As aforementioned, the script is completely harmless as it is lacking any malware obfuscation and replication technique and it is easily detectable by any modern antivirus software. Just for educational purpose.

## 🛜 Network Scanner (ARP Reconnaissance)
This script is a basic but functional (only on Windows) network mapping tool built with Python and scapy. It performs a Layer 2 network sweep by broadcasting Address Resolution Protocol (ARP) requests across a specified subnet. By parsing the responses, it dynamically maps active hosts and their corresponding MAC addresses on the local network.
While simple, this project serves as a practical application of foundational computer networking concepts. It demonstrates a theoretical and applied understanding of the following areas:
* Network Protocols: Mechanics of Layer 2 (Ethernet/ARP) and Layer 3 (IPv4) of the OSI model.
* Addressing Architecture: The structural differences between public and private IP ranges and MAC addressing.
* Protocol Fundamentals: Theoretical knowledge of transport layer protocols (TCP/UDP) and application layer resolution systems (DNS).
* Traffic Analysis: Basic knowledge with the operational logic behind professional network analysis and reconnaissance tools, such as Wireshark and Nmap.
* Security Architecture Awareness: Understanding how local network broadcasting and ARP resolution function is the prerequisite for comprehending Layer 2 vulnerabilities, such as ARP-Spoofing, which   forms the basis of Man-in-the-Middle (MITM) attacks.

## ⏱️ PC Usage Manager & Remote Email Access and Control
A dual-script system (PCUsage.py and mailistener.py) designed to monitor, limit, and remotely manage local machine access. Built as a practical access control mechanism for shared hardware, it operates as a background service that enforces daily session limits and processes administrative commands asynchronously via an email bridge.
The features are:
* Session Enforcement & State Management: Tracks active usage time by constantly reading and updating a local state file (usage_log.txt). When the daily time quota is reached, it automatically minimizes all windows and forces an OS-level shutdown.
* Remote IMAP Control: The mailistener.py script acts as a daemon, continuously polling a designated inbox using the imaplib library. By sending an email with the subject "PCUsage Command", an administrator can parse arguments to remotely extend, reduce, or set the time limit, force an immediate timeout (drain), or request specific log data.
* Automated Reporting (SMTP): Uses smtplib to parse the local log data and automatically compile and email weekly usage statistics, or push on-demand daily/weekly/monthly reports when queried remotely.
* Native OS Notifications: Integrates the plyer library to push system-level desktop warnings at specific countdown intervals (e.g., 45m, 30m, 1m remaining) or to display custom text messages sent remotely via the msg email command.
This project relies on Windows-specific terminal commands for system operations (os.system("shutdown /s /t 1")) and window management (pyautogui.hotkey('win','d')). It requires the plyer and pyautogui libraries. To deploy, valid SMTP/IMAP credentials (using App Passwords for secure authentication) must be configured within the global variables of both scripts.
