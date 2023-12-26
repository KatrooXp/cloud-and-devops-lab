### 6.1.a. Analysing network interfaces

### 1. Дослідити мережеві налаштування на вашому комп'ютері. Виконати перевірку щодо всіх
доступних мережевих інтерфейсів у системі. (ifconfig / ip)

![Alt text](<pictures/Screenshot from 2023-07-19 17-23-08.png>)

![Alt text](<pictures/Screenshot from 2023-07-19 17-24-20.png>)

![Alt text](<pictures/Screenshot from 2023-07-19 17-24-47.png>)

    There're 4 network interfaces - 2 active (LOWER_UP) and 2 not connected (NO-CARRIER), all are in default group and has standart mtu (maximum for loopback and 1500 for others)

    1. Loopback interface
    2. Ethernet interface - not active (NO-CARRIER), has no ip address
    3. WiFi interfase - has ipv4 and ipv6 addresses attached, ipv4 is valid for 5731 sec (ip a command)
    4. Docker interface - not active, has been assigned the ipv4 address, valid forever


    - Ifconfig additionally provides statistics on received and transmitted packets, bytes, errors, drops, overruns, carrier status, and collisions on the wireless interface

### 2. Перевірити якість зв'язку (на домени ukr.net, google.com, 8.8.8.8, та інші), пояснити виведення команди ping.

![Alt text](<pictures/Screenshot from 2023-07-19 18-12-03.png>)

    bytes from: response was received from the ... IP address

    icmp_sec: number of the received packet

    ttl: the number of hops that the packet can travel before it is dropped. at the screenshot we see that on the way to 8.8.8.8 and google.com the packet can travel through more routers before reaching the destination than on the way to ukr.net

    time: the round-trip time for the packet

![Alt text](<pictures/Screenshot from 2023-07-19 18-46-59.png>)

    ping with larger size of data shows that avg and max time was increased, thus it did not affected in country traffic as much as abroad


### 3. Перевірити якість зв'язку (на host студента), максимально навантажити host. (використовувати команду ping, mtr, tracert)

![Alt text](<pictures/Screenshot from 2023-07-20 18-08-28.png>)

    Maximum size of data we can transfer is 1500 bytes

![Alt text](<pictures/Screenshot from 2023-07-20 18-15-44.png>)

    The farther server is located, the more hops we see with tracerout command. Some hops are not responding to the traceroute requests - most often in aws.com, due to routers settings

![Alt text](<pictures/Screenshot from 2023-07-20 18-31-23.png>)

    Traceroute cat perform with higher load vs. ping, because in linux this command uses UDP packets, not ICMP

![Alt text](<pictures/Screenshot from 2023-07-20 18-34-37.png>)
![Alt text](<pictures/Screenshot from 2023-07-20 18-35-02.png>)
![Alt text](<pictures/Screenshot from 2023-07-20 18-35-30.png>)

    mtr command uses ICMP by default and shows different results for aws.com than traceroute, but same for ukr.net and google.com

![Alt text](<pictures/Screenshot from 2023-07-20 18-50-03.png>)

    but unlike ping, mtr works with abroad traffic up to 1500 bytes 

![Alt text](<pictures/Screenshot from 2023-07-20 18-57-22.png>)

    we can choose protocol in mtr command to enlarge test load and tcp lets test the biggest load (200 Mbit on the screen, as example)

### 4. Вивчення MTU:

a. Отримати значення MTU локальних інтерфейсів;

    With ifconfig or ip a command (task 1)
    In this task I use virual machicne with Ubuntu 22.04.2. Default MTU on enp0s3 interface is 1500 bytes.

b. Змінити значення MTU локальних інтерфейсів. Визначити допустимі значення MTU. Як це позначиться на каналі зв'язку?

    First, I tried to ping 8.8.8.8 with 1500 and 1501 bytes packetsize:

![Alt text](<pictures/Screenshot from 2023-07-21 12-47-07.png>)

    Then, I change MTU to 15000 bytes (10 times more than default):

![Alt text](<pictures/Screenshot from 2023-07-21 13-08-21.png>)

    Still can't ping with 1501 bytes. Than tried to do the same on my main machine:

![Alt text](<pictures/Screenshot from 2023-07-21 13-25-26.png>)

    Wifi module doesn't let to up the mtu this much, but 2000 is ok. Still, ping did not work, because of router settings.
    Than, let's try to lower mtu, go back to virtual machine:

![Alt text](<pictures/Screenshot from 2023-07-21 13-36-57.png>)

    Still, it does not affect the performance of ping command, because the packet has been fragmented by system. To avoid packet fragmentation I used -M flag:

![Alt text](<pictures/Screenshot from 2023-07-21 14-07-13.png>)

c. Увімкніть режим Jumbo Frame. Промоделювати переваги та недоліки. Налаштувати між двома віртуальними машинами.

    I have changed mtu to 9000, but packet size I can send between virtual machines remains the same

![Alt text](<pictures/Screenshot from 2023-07-21 15-11-55.png>)

    To be able to send the packets I have to enable jumbo frame at the other vm as well.
    On my first try to enable jumbo frame at the second virtual machine, it had lost the ip address. After reboot it worked and big packets can be sent now:

![Alt text](<pictures/Screenshot from 2023-07-21 15-27-43.png>)

    So, the main benefit of jumbo frame is possibility to send large packets between machines, the main drowbacks are - too bit load to the machine and limitation of usage (can only be used if both machines are controlled by admin)

d. обчислити MTU каналу зв'язку,оОписати процес обчислення

    To find mtu of the other machine's interface I would enlarge mtu on my machine and then ping the other machine with flags -s and -M, until find the limit 

e. Змініть довжину черги передачі та промоделюйте її роботу після змін. Зробіть кілька змін.

    I changed qlen from 1 to 100000 and didn't find any changes using ping, traceroute or mtr commands

### 5.Вивчення MAC:
a. Знайти всі доступні MAC-адреси у вашій мережі (хости колег, ресурсів)
b. використовуйте команди arp і ip.

![Alt text](<pictures/Screenshot from 2023-07-23 15-02-15.png>)

c. Придумайте реалізацію системи автоматичного виявлення змін (появи або вимкнення пристрою/VM і т.д.) у локальній мережі.

    It should be script that monitors changes in the ARP table of my router. The ARP table contains the mapping between IP addresses and MAC addresses of devices on the network. A change in the MAC address or IP address indicates the appearance or disappearance of a device. As monitoring tool I choosed arp-scan command (see device-online-monitor.sh):
        1. scan the local network
        2. whith while loop continiously scan the network again and compare with first scan
        3. if changed output the diff and rewrite first scan
        4. compare every 5 seconds
    
    the result screenshot (I turned on, off and on devices for test):

![Alt text](<pictures/Screenshot from 2023-07-23 23-08-24.png>)

### 6. Network Administration in Linux
a. Perform static configuration of the network interface (for Ubuntu 22.04, Debian 12, Oracle Linux 9, CentOS 9).

i. Set a temporary static IP address.

![Alt text](<pictures/Screenshot from 2023-07-28 22-59-54.png>)

![Alt text](<pictures/Screenshot from 2023-07-28 22-51-52.png>)

ii. Встановити перманентну статичну IP-адресу.

    sudo vim /etc/netplan/00-installer-config.yaml

![Alt text](<pictures/Screenshot from 2023-07-28 22-33-57.png>)

    sudo netplan apply

iii. Встановити статичну IP-адресу з мінімально допустимою маскою для мережі з кількістю комп'ютерів 2^(<останнє число вашого ID-пропуску> або <дати народження>, 
якщо число дорівнює 0, або 1 то брати наступне)

    my date of birth is 27
    quantity of computers - 128
    we need 128 ip addresses, so it should be minimum 130 number of hosts (including network address and broadcast address) - the mask is /24

    the process is the same as in previous task: sudo vim /etc/netplan/00-installer-config.yaml - configuration - sudo netplan apply

iv. Призначити кілька IP адрес на один інтерфейс канального рівня.

![Alt text](<pictures/Screenshot from 2023-07-28 23-41-37.png>)

![Alt text](<pictures/Screenshot from 2023-07-28 23-43-27.png>)

v. Способи зміни MAC-адреси в операційних системах. Встановити локально адміністровану MAC-адресу, що адмініструється. (Знайдіть де це використовується)

    for Linux:
    sudo ifconfig <interface> hw ether <new_MAC>
    or
    sudo ip link set <interface> address <new_MAC>

![Alt text](<pictures/Screenshot from 2023-08-08 23-08-29-1.png>)

    it is used for network anonymity, security, troubleshooting, and bypassing certain network restrictions

vi. Get the list of MAC addresses for multicast.

![Alt text](<pictures/Screenshot from 2023-07-28 23-25-09.png>)

vii. Verify what has been done with the ip and ipconfig (ifconfig) command.

b. Налаштувати адресу шлюзу. У разі використання кількох інтерфейсів пояснити, як працюватимуть шлюзи.

![Alt text](<pictures/Screenshot from 2023-07-29 17-55-46.png>)

    When using multiple network interfaces, each interface can have its own gateway, a routing table defines which route should be used to forward packets to specific networks or IP addresses. The operating system assigns priorities to different network interfaces. Typically, one interface has a higher priority and is considered the primary or default interface. Traffic that doesn't have a specific routing rule will be sent through the primary interface and its gateway

c. Призначення маски для host і для router

    /24 mask for router

![Alt text](<pictures/Screenshot from 2023-08-28 12-25-47.png>)

    host: process is the same as in task 6a.ii: sudo vim /etc/netplan/00-installer-config.yaml - configuration - sudo netplan apply

d. Отримати список мережевих протоколів та їхніх версій, які підтримуються ядром системи.

![Alt text](<pictures/Screenshot from 2023-07-29 22-59-26.png>)

### 6.1.b. Traffic analysis

### Perform installation in Windows and Linux operating systems:
a. Wireshark / b. tcpdump

### 2. Capture traffic on your host:

![Alt text](<pictures/Screenshot from 2023-07-29 23-45-23.png>)

a. Find Ethernet frames

i. Find unicast frame (identify whose)

Unicast TCP frame:

    23:35:56.171159 IP katroocomp.44336 > 45.60.65.216.https: Flags [P.], seq 2479317202:2479319581, ack 3411839469, win 12333, options [nop,nop,TS val 1448085905 ecr 1321105067], length 2379

    the source IP address is katroocomp and the destination IP address is 45.60.65.216

Unicast UDP frame:

    23:35:58.142664 IP katroocomp.51308 > 172.67.139.179.443: UDP, length 1250

    the source IP address is katroocomp, and the destination IP address is 172.67.139.179

ii. Find the broadcast frame (identify the service that receives/sends it)

    23:59:43.587458 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 68:63:59:bd:a0:ec (oui Unknown), length 300

    This packet is a DHCP request (BOOTP/DHCP)

iii. Перехопити трафік, що моделює роботу протоколу ARP.

![Alt text](<pictures/Screenshot from 2023-07-30 00-09-50.png>)

b. Find IP packets:

i. Determine the application layer service it belongs to and what type of traffic.

    23:35:56.171159 IP katroocomp.44336 > 45.60.65.216.https: Flags [P.], seq 2479317202:2479319581, ack 3411839469, win 12333, options [nop,nop,TS val 1448085905 ecr 1321105067], length 2379

    - Application layer service: https
    - Type of traffic: secure web browsing

    23:35:56.376987 IP katroocomp.49112 > vdns2.vectranet.pl.domain: 14703+ [1au] PTR? 216.65.60.45.in-addr.arpa. (54)

    - Application layer service: DNS
    - Type of traffic: DNS query

ii. Знайти вхідний і вихідний IP пакети. Пояснити захоплений трафік.

    Outgoing packet, sent from katroocomp to 45.60.65.216:

    23:35:56.171159 IP katroocomp.44336 > 45.60.65.216.https: Flags [P.], seq 2479317202:2479319581, ack 3411839469, win 12333, options [nop,nop,TS val 1448085905 ecr 1321105067], length 2379

    - [P.] - indicate that this packet carries application data (payload) 
    - the sequence number of the first byte in this packet's payload is 2479317202, and the sequence number of the last byte is 2479319581
    - acknowledgment number: 3411839469
    - win 12333: the receiver can accept up to 12333 bytes of data without further acknowledgment
    - length 2379: the total length of the IP packet, including the header and payload

    Incoming packet, sent from the source 45.60.65.216 to katroocomp in response to the previous packet:

    23:35:56.187659 IP 45.60.65.216.https > katroocomp.44336: Flags [.], ack 1448, win 3917, options [nop,nop,TS val 1321111063 ecr 1448085905], length 0

    - [.] - this is an acknowledgment packet, and there is no new data payload in this packet.
    - acknowledgment Number: 1448
    - win 3917: the receiver can accept up to 3917 bytes of data without further acknowledgment.
    - length 0: there is no payload data in this packet

iii. Find packets that are (unicast, broadcast, multicast).

    - Unicast packets are those that are sent from one source to one specific destination. Example:

    23:35:56.188419 IP 45.60.65.216.https > katroocomp.44336: Flags [.], seq 1:5793, ack 2379, win 3940, options [nop,nop,TS val 1321111065 ecr 1448085905], length 5792    

    - Broadcast packet example (the destination is broadcast address 255.255.255.255):

    23:59:43.587458 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 68:63:59:bd:a0:ec (oui Unknown), length 300

    - Multicast packet example (destination IP address 224.0.0.251 is a multicast address used for Multicast DNS services):

    23:35:58.139608 IP 224.0.0.251.mdns > katroocomp.57556: 0 PTR (QM)? 45.65.60.45.in-addr.arpa. (43)


iv. Знайти пакети, які підтверджують виконання фрагментації IP на Ethernet (визначити які розміри пакетів прийшли одержувачу і яка кількість).

    command: sudo tcpdump -r capture.pcap '((ip[6:2] > 0) and (not ip[6] = 64))'

c. Find segments:

i. TCP segments that confirm the connection establishment process (handshaking).

    filter syn and ack packets from captured traffic with the command: 
    tcpdump -r capture.pcap 'tcp[tcpflags] == tcp-syn|tcp-ack'


![Alt text](<pictures/Screenshot from 2023-08-01 19-33-10.png>)

ii. TCP segments that confirm the connection data transfer process (ESTABLISHED).

    tcpdump -r capture.pcap 'tcp[tcpflags] & (tcp-ack) != 0 and tcp[tcpflags] & (tcp-syn|tcp-fin) == 0'

![Alt text](<pictures/Screenshot from 2023-08-01 20-14-59.png>)

iii. TCP segments that confirm client and server communication in the state of connection established (ESTABLISHED), but without data transfer. 

![Alt text](<pictures/Screenshot from 2023-08-28 12-48-44.png>)

iv. TCP segments that confirm the connection termination process.

    tcpdump -r capture.pcap 'tcp[tcpflags] & (tcp-fin|tcp-rst) != 0'

![Alt text](<pictures/Screenshot from 2023-08-01 20-31-01.png>)

v. Виконати передачу великих сегментів TCP/UDP. Обчислити MSS. Переглянути весь трафік передачі великого сегмента на нижніх рівнях моделі TCP/IP. 

    on receiving host

![Alt text](<pictures/Screenshot from 2023-08-28 14-46-42.png>)

    on sending host

![Alt text](<pictures/Screenshot from 2023-08-28 14-46-55.png>)

    MSS = 1500 - 20 (TCP Header) - 20 (IP Header) = 1460 bytes

    traffic captured:

![Alt text](<pictures/Screenshot from 2023-08-28 15-12-43.png>)

d. Find these protocols (adjust the filter):

i. DNS (UDP/TCP datagrams)

    tcpdump -r capture.pcap 'port 53'

![Alt text](<pictures/Screenshot from 2023-08-01 22-58-00.png>)

ii. DHCP (UDP/TCP datagrams)

    tcpdump -r capture.pcap udp port 67 or udp port 68

iii. HTTP (TCP’s segments)

    tcpdump -r capture.pcap tcp port 80

iv. * HTTPS (TCP’s segments)

    tcpdump -r capture.pcap tcp port 443

![Alt text](<pictures/Screenshot from 2023-08-01 23-02-12.png>)

### 3. Виконати пошук логінів і паролів у трафіку HTTP і FTP

    sudo tcpdump port http or port ftp -l -A | egrep -i -B5 'pass=|pwd=|log=|login=|user=|username=|pw=|passw=|passwd=|password=|pass:|user:|username:|password:|login:|pass |user'

![Alt text](<pictures/Screenshot from 2023-08-08 23-52-41.png>)

### 4. Виконати тестування пропускної спроможності мережі за протоколами TCP, UDP і SCTP* з використанням Iperf3

    TCP
    server:

![Alt text](<pictures/Screenshot from 2023-08-01 23-37-59.png>)

    client:

![Alt text](<pictures/Screenshot from 2023-08-01 23-38-04.png>)

    UDP
    server:

![Alt text](<pictures/Screenshot from 2023-08-01 23-42-10.png>)

    client:

![Alt text](<pictures/Screenshot from 2023-08-01 23-42-24.png>)

### 6.1.c. Host diagnostics

### 1. Monitor network activity of the local system (commands: netstat, ss, iptraf, nc)
a. Виявлення активних з'єднань

![Alt text](<pictures/Screenshot from 2023-08-07 22-55-28.png>)

![Alt text](<pictures/Screenshot from 2023-08-07 22-58-49.png>)

b. проаналізувати відкриті порти (UDP, TCP). Дати їхню класифікацію

    TCP Ports:

    27017 - commonly used by MongoDB as its default listening port

    22 - used for SSH service

    5432 - used by PostgreSQL as its default listening port

    8080 - used for web servers or web applications, serving HTTP traffic.

    UDP Ports:

    5353 = used for Multicast DNS service, typically used for device discovery on local networks

    TCP and UDP ports:

    53 - used for DNS service

    631 - used by the CUPS for printer service

c. пояснити в якому стані перебувають мережеві з'єднання

    LISTEN: The connection is actively listening for incoming connections on a specified port
    UNCONN: the socket is not actively connected to any remote endpoint

d. визначити основні, запущені мережеві служби (процеси). Які з них працюють у режимі сервера

    SSH, DNS, MongoDB, PostgreSQL, CUPS, HTTP - working in server mode (LISTEN)

e. пояснити в якому стані перебуває сполука

    did not understood the question - what is meant by "сполука". Please, rephrase in English

f. використовуючи команду ping побудувати маршрут пакетів через роутери до одержувача. Написати скрипт (python).

    I used ping command with new TTL value for each successive ping request. As the TTL increased, the packets traversed further through the network and reached different routers along the path

![Alt text](<pictures/Screenshot from 2023-08-07 23-48-13.png>)    

    The python script that does the same: ping.py

![Alt text](<pictures/Screenshot from 2023-08-08 00-14-13.png>)


### 2. Виконати перевірку відкритих портів за протоколами TCP/UDP (netstat, ss, iptraf, nc, lsof):

a. на локальному хості;

![Alt text](<pictures/Screenshot from 2023-08-08 20-45-07.png>)    

b. на віддаленому хості;

    we can use commands:    
    nmap -sT destination_host - if there's no firewall
    nmap -Pn destination_host - if there's firewall

    nc -zv destination_host port_number

![Alt text](<pictures/Screenshot from 2023-08-08 21-14-58.png>)

c. пояснити принцип перевірки, на чому він заснований (a, b)

    a) netstat and ss:
    these tools are interacting with the operating system's kernel to gather information about the network's state and connections
    ss is a more modern replacement for netstat and also retrieves information from the operating system's kernel but offers faster and more efficient operation.

    b) iptraf:
    iptraf is an interactive tool for monitoring network activity.
    it is listening to network traffic and analyzing it to determine active connections and open ports

    c) nc:
    nc attempting to establish a connection to the specified host and port. If the connection is successful, it means the port is open. If the connection fails, it means the port is closed or unreachable

    d) lsof:
    lsof analyzing the system's open file log, which includes network ports being listened to by processes on the system

d. запропонувати utils для перевірки відкритих портів (для ОС Linux, containers).

    all utils that are used before - same for Linux and containers



