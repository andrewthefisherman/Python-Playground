# Ethical-Hacking
This is a collection of python projects and python scripts for various . They are simple, but they cover some of the fundamentals of the technology and the concepts behind modern hacking.


## 🛜 Network Scanner (ARP Reconnaissance)
This script is a basic but functional (only on Windows) network mapping tool built with Python and scapy. It performs a Layer 2 network sweep by broadcasting Address Resolution Protocol (ARP) requests across a specified subnet. By parsing the responses, it dynamically maps active hosts and their corresponding MAC addresses on the local network.
While simple, this project serves as a practical application of foundational computer networking concepts. It demonstrates a theoretical and applied understanding of the following areas:
* Network Protocols: Mechanics of Layer 2 (Ethernet/ARP) and Layer 3 (IPv4) of the OSI model.
* Addressing Architecture: The structural differences between public and private IP ranges and MAC addressing.
* Protocol Fundamentals: Theoretical knowledge of transport layer protocols (TCP/UDP) and application layer resolution systems (DNS).
* Traffic Analysis: Basic knowledge with the operational logic behind professional network analysis and reconnaissance tools, such as Wireshark and Nmap.
* Security Architecture Awareness: Understanding how local network broadcasting and ARP resolution function is the prerequisite for comprehending Layer 2 vulnerabilities, such as ARP-Spoofing, which   forms the basis of Man-in-the-Middle (MITM) attacks.

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

