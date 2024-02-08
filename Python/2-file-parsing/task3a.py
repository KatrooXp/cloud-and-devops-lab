"""This script is parsing any file for specific patterns. 
Patterns are described in parser.add.argument in this script
and can be displayed in the terminal with -h"""

import re
import argparse
import sys

parser = argparse.ArgumentParser(prog="task3a", usage='%(prog)s [options]')

parser.add_argument("-f", type = str, help="-f /path/file_name - takes file to parse")
parser.add_argument("-ipv4", nargs="+", type = str, help="""{all|priv|cidr}:
                    {all} - find all ipv4 in the file,
                    {priv} - find only private ipv4 address,
                    {cidr} - find only ipv4 addresses with CIDR notation""")
parser.add_argument("-ipv6", nargs="+", type = str, help="""{all|priv|cidr}:
                    {all} - find all ipv6 in the file,
                    {priv} - find only private ipv6 address,
                    {cidr} - find only ipv6 addresses with CIDR notation""")
parser.add_argument("-mask", default=False, action="store_true",
                    help="finds all ip masks")
parser.add_argument("-mac", nargs="+", type = str,
                    help="""{all|gen|lin|win|cis}:
                    {all} - find all MAC addressses in file
                    {gen} - only in format XX:XX:XX:XX:XX:XX,
                    {lin} - only in format XX-XX-XX-XX-XX-XX,
                    {win} - only in format XXXXXXXXXXXX,
                    {cis} - only in format XXXX.XXXX.XXXX""")
parser.add_argument("-domain", nargs="+", type = str, help="""{first|second}:
                    {first} - only TLD,
                    {second} - first and second DL""")
parser.add_argument("-email", nargs="+", type = str, help="""{all|login|domain}:
                    {all} - find all email addresses
                    {login} - get only logins,
                    {domain} - get only domains""")
parser.add_argument("-url", default=False, action="store_true", help="find all URLs")
parser.add_argument("-ssh", nargs="+", type = str, help="""{priv|pub}:
                    {priv} - only private,
                    {pub} - only public""")
parser.add_argument("-card", default=False, action="store_true", help="""find all card numbers""")
parser.add_argument("-uuid", default=False, action="store_true", help="""find all UUIDs""")

args = parser.parse_args()

# read the file function
def readfile(path_to_file):
    """read file from input"""
    with open(f"{path_to_file}", encoding="utf-8") as file_to_read:
        return file_to_read.read()

# ipv4 functions
def ipv4_all(file_to_parse):
    """finds all ipv4 addresses, returns list"""
    pattern_ipv4 = r"""(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|
                    [1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]){1,3}"""
    find_ipv4 = re.findall(pattern_ipv4, file_to_parse)
    all_ipv4 = [ x for x in find_ipv4 if "255.255" not in x ]
    return all_ipv4


def ipv4_priv(file_to_parse):
    """finds only private ipv4 addresses, returns list"""
    pattern_ipv4_priv = r"(?:10|172\.(?:1[6-9]|2[0-9]|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}(?:.\d{1,3})?"
    find_ipv4_priv = re.findall(pattern_ipv4_priv, file_to_parse)
    return find_ipv4_priv


def ipv4_cidr(file_to_parse):
    """finds all ipv4 addresses with CIDR notation, returns list"""
    pattern_ipv4_cidr = r"""(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|
    [1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]){1,3}(?:[\/][3][0-2]|[\/][1-2][0-9]|[\/][0-9])"""
    find_ipv4_cidr = re.findall(pattern_ipv4_cidr, file_to_parse)
    return find_ipv4_cidr

#ipv6 functions
def ipv6_all(file_to_parse):
    """finds all ipv6 addresses, returns list"""
    pattern_ipv6 = r"""(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)"""
    find_ipv6 = re.findall(pattern_ipv6, file_to_parse)
    return find_ipv6


def ipv6_priv(file_to_parse):
    """finds only private ipv6 addresses, returns list"""
    pattern_ipv6 = r"""(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)"""
    find_ipv6 = re.findall(pattern_ipv6, file_to_parse)
    pattern_ipv6_priv = r"(?:(?:fc00:[^\s]+)|(?:fd00:[^\s]+)|(?:fe80:[^\s]+))"
    find_ipv6_priv = re.findall(pattern_ipv6_priv, " ".join(find_ipv6))
    return find_ipv6_priv


def ipv6_cidr(file_to_parse):
    """finds all ipv6 addresses with CIDR notation, returns list"""
    pattern_ipv6_cidr = r"""(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?:[\/][1][0-2][0-8]|[\/][1-9][0-9]|[\/][0-9])"""
    find_ipv6_cidr = re.findall(pattern_ipv6_cidr, file_to_parse)
    return find_ipv6_cidr

# ip mask function
def ip_mask(file_to_parse):
    """finds all ip masks, returns list"""
    pattern_mask = r"""(?:(?:(?:(?:25[2,4,5]|24[0,8]|224|192|128|0)\.){3})(?:(?:25[2,4,5]|24[0,8]|224|192|128|0)))"""
    find_mask = re.findall(pattern_mask, file_to_parse)
    return find_mask

# mac address functions
def mac_gen(file_to_parse):
    """finds mac addresses in general format, returns list"""
    pattern_mac_gen = r"""(?:(?:[0-9a-fA-F]{2}:){5})(?:[0-9a-fA-F]{2})"""
    find_mac_gen = re.findall(pattern_mac_gen, file_to_parse)
    return find_mac_gen


def mac_lin(file_to_parse):
    """finds mac addresses in linux format, returns list"""
    pattern_mac_lin = r"""(?:(?:[0-9a-fA-F]{2}-){5})(?:[0-9a-fA-F]{2})"""
    find_mac_lin = re.findall(pattern_mac_lin, file_to_parse)
    return find_mac_lin


def mac_win(file_to_parse):
    """finds mac addresses in windows format, returns list"""
    pattern_mac_win = r"""(?:[0-9a-fA-F]{12})"""
    find_mac_win = re.findall(pattern_mac_win, file_to_parse)
    return find_mac_win


def mac_cis(file_to_parse):
    """finds mac addresses in cisco format, returns list"""
    pattern_mac_cis = r"""(?:(?:[0-9a-fA-F]{4}\.){2}(?:[0-9a-fA-F]{4}))"""
    find_mac_cis = re.findall(pattern_mac_cis, file_to_parse)
    return find_mac_cis

# domain functions
def domain_first(file_to_parse):
    """finds TDL addresses, returns list"""
    pattern_domain_first = r"""\b(?:https?://|www\.)\S+\.([A-Za-z]{2,})\b"""
    find_domain_first = re.findall(pattern_domain_first, file_to_parse)
    return find_domain_first


def domain_second(file_to_parse):
    """finds second and more DL addresses, returns list"""
    pattern_domain_second = r"""\b(?:https?://|www\.)((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})\b"""
    find_domain_second = re.findall(pattern_domain_second, file_to_parse)
    return find_domain_second

# email functions
def email_all(file_to_parse):
    """finds all email addresses, returns list"""
    pattern_email_all = r"""\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"""
    find_email_all = re.findall(pattern_email_all, file_to_parse)
    return find_email_all


def email_login(file_to_parse):
    """finds only logins from email addresses, returns list"""
    pattern_email_login = r"""\b([A-Za-z0-9._%+-]+)@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"""
    find_email_login = re.findall(pattern_email_login, file_to_parse)
    return find_email_login


def email_domain(file_to_parse):
    """finds only domains from email addresses, returns list"""
    pattern_email_domain = r"""\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b"""
    find_email_domain = re.findall(pattern_email_domain, file_to_parse)
    return find_email_domain

# url function
def url_all(file_to_parse):
    """finds URL addresses, returns list"""
    pattern_url_all = r"""\b(?:https?://|www\.)\S+\b"""
    find_url_all = re.findall(pattern_url_all, file_to_parse)
    return find_url_all

# ssh functions
def ssh_priv(file_to_parse):
    """finds private ssh keys, returns list"""
    pattern_ssh_priv = r"""-----BEGIN [^\n]+ PRIVATE KEY-----\n(?:[A-Za-z0-9+/=\n]+)+-----END[^\n]+ PRIVATE KEY-----"""
    find_ssh_priv = re.findall(pattern_ssh_priv, file_to_parse)
    return find_ssh_priv


def ssh_pub(file_to_parse):
    """finds public ssh keys, returns list"""
    pattern_ssh_pub = r"""ssh-[a-z0-9]+ [\w+/=]+(?: [\w.+/:=]+)*@[a-z]+"""
    find_ssh_pub = re.findall(pattern_ssh_pub, file_to_parse)
    return find_ssh_pub

# card function
def card_num(file_to_parse):
    """finds card numbers, returns list"""
    pattern_card = r"""(?:\d{4}(?:[-\s]?\d{4}){3})|(?:\d{4}[- ]?\d{6}[- ]?\d{5})"""
    find_card = re.findall(pattern_card, file_to_parse)
    return find_card

# uuid function
def uuid(file_to_parse):
    """finds UUID, returns list"""
    pattern_uuid = r"""[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"""
    find_uuid = re.findall(pattern_uuid, file_to_parse)
    return find_uuid

# script starts working here
if not args.f:
    print("please, enter path to the file you want to parse: -f /path/to/file")
    sys.exit()

if args.ipv4:
    file = readfile(args.f)
    permitted_args = ['all', 'priv', 'cidr']

    if any(arg not in permitted_args for arg in args.ipv4):
        print("-ipv4 takes only arguments: [all], [priv] or [cidr]")
        sys.exit()

    if 'all' in args.ipv4:
        print("all ipv4 addresses found in the file:\n", "\n".join(ipv4_all(file)))

    if 'priv' in args.ipv4:
        print("private ipv4 addresses found in the file:\n", "\n".join(ipv4_priv(file)))

    if 'cidr' in args.ipv4:
        print("ipv4 with CIDR notation found in the file:\n", "\n".join(ipv4_cidr(file)))

if args.ipv6:
    file = readfile(args.f)
    permitted_args = ['all', 'priv', 'cidr']

    if any(arg not in permitted_args for arg in args.ipv6):
        print("-ipv6 takes only arguments: [all], [priv] or [cidr]")
        sys.exit()

    if 'all' in args.ipv6:
        print("all ipv6 addresses found in the file:\n", "\n".join(ipv6_all(file)))

    if 'priv' in args.ipv6:
        print("private ipv6 addresses found in the file:\n", "\n".join(ipv6_priv(file)))

    if 'cidr' in args.ipv6:
        print("ipv6 with CIDR notation found in the file:\n", "\n".join(ipv6_cidr(file)))

if args.mask:
    file = readfile(args.f)
    print("IP masks found in the file:\n", "\n".join(ip_mask(file)))

if args.mac:
    file = readfile(args.f)
    permitted_args = ['all', 'gen', 'lin', 'win', 'cis']

    if any(arg not in permitted_args for arg in args.mac):
        print("-mac takes only arguments: [all], [gen], [lin], [win] or [cis]")
        sys.exit()

    if 'all' in args.mac:
        mac_all = []
        mac_all.append(mac_gen(file))
        mac_all.append(mac_lin(file))
        mac_all.append(mac_win(file))
        mac_all.append(mac_cis(file))
        mac_all = [item for sublist in mac_all for item in sublist]
        print("all mac addresses found in the file:\n", "\n".join(mac_all))

    if 'gen' in args.mac:
        print("mac addresses in general format found in the file:\n", "\n".join(mac_gen(file)))

    if 'lin' in args.mac:
        print("mac addresses in linux format found in the file:\n", "\n".join(mac_lin(file)))

    if 'win' in args.mac:
        print("mac addresses in windows format found in the file:\n", "\n".join(mac_win(file)))

    if 'cis' in args.mac:
        print("mac addresses in cisco format found in the file:\n", "\n".join(mac_cis(file)))

if args.domain:
    file = readfile(args.f)
    permitted_args = ['first', 'second']

    if any(arg not in permitted_args for arg in args.domain):
        print("-domain takes only arguments: [first] or [second]")
        sys.exit()

    if 'first' in args.domain:
        print("TDL addresses found in the file:\n\n", "\n".join(sorted(domain_first(file))))

    if 'second' in args.domain:
        print("first and second DL addresses found in the file:\n\n", "\n".join(sorted(domain_second(file))))

if args.email:
    file = readfile(args.f)
    permitted_args = ['all', 'login', 'domain']

    if any(arg not in permitted_args for arg in args.email):
        print("-email takes only arguments: [all], [login] or [domain]")
        sys.exit()

    if 'all' in args.email:
        print("all email addresses found in the file:\n\n", "\n".join(sorted(email_all(file))))

    if 'login' in args.email:
        print("only logins from email addresses found in the file:\n\n", "\n".join(sorted(email_login(file))))

    if 'domain' in args.email:
        print("only domains from email addresses found in the file:\n\n", "\n".join(sorted(email_domain(file))))

if args.url:
    file = readfile(args.f)
    print("all URL addresses found in the file:\n\n", "\n".join(sorted(url_all(file))))

if args.ssh:
    file = readfile(args.f)
    permitted_args = ['priv', 'pub']

    if any(arg not in permitted_args for arg in args.ssh):
        print("-domain takes only arguments: [priv] or [pub]")
        sys.exit()

    if 'priv' in args.ssh:
        print("private ssh keys found in the file:\n\n", "\n\n".join(ssh_priv(file)))

    if 'pub' in args.ssh:
        print("public ssh keys found in the file:\n\n", "\n\n".join(ssh_pub(file)))

if args.card:
    file = readfile(args.f)
    print("credit cards numbers found in the file:\n\n", "\n".join(card_num(file)))

if args.uuid:
    file = readfile(args.f)
    print("UUID found in the file:\n\n", "\n".join(uuid(file)))
