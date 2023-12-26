"""task 4 - log file parsing"""
import argparse
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
import parse

parser = argparse.ArgumentParser(prog="task4", usage='%(prog)s [options]')
parser.add_argument(
    "-a", type=int, help="[N, int] find N the most used ip addresses -output1-")
parser.add_argument(
    "-b", type=int, help="[N, int] find quantity of requests in time period, N minutes -output2-")
parser.add_argument(
    "-c", type=int, help="[N, int] find N the most often used user agents -output3-")
parser.add_argument(
    "-d", type=int, help="[N, int] find N quantity of error code in time period -output4-")
parser.add_argument("-e", nargs='+',
                    help="""[N, int] [s, optional] find N the longest (by default) requests (in millis).
                    If add argument [s], finds N the shortest requests  - format:
                    Get, time when, ip address - millis -output5-""")
parser.add_argument(
    "-f", nargs='+', help="[N, int] [K, int] find N the most often requests up to K slash -output6-")
parser.add_argument("-g", default=False, action="store_true",
                    help="show quantity of requests per node (worker) -output7-")
parser.add_argument("-i", default=False, action="store_true",
                    help="show quantity of same references to webpage, sort by domain -output8-")
parser.add_argument("-j", type=int, help="""[int, N] find quantity of request in time period,
                    N minutes, by nodes (workers) -output9-""")
parser.add_argument("-k", type=int, help="""[int, N] find quantity of requests in time period,
                    N minutes, sorted by quantity of requests -output10-""")

args = parser.parse_args()

"""
1(-a) - ip addresses of clients (x.x.x.x) or (x.x.x.x, x.x.x.x, ...),
             find N of the most often used
2(-b) - quantity of request in time period (minutes):
             from 09.01.41 - 09.02.41 min - x requests, 09.02.41 - 09.03.41 min - y requests etc
3(-c) - most often user agents
4(-d) - quantity of code S 304 / 404 in time period
5(-e) - find N the longest / the shortest requests (in millis) - format: Get, time when, ip address - millis
6(-f) - find N most often requests up to 2nd / 3rd / ... slash
7(-g) - quantity of requests per node (worker)
8(-i) - quantity of same references to webpage, sort by domain
9(-j) - quantity of request in time period by nodes (workers)
10(-k) - task 2, sorted by quantity (N of the most loaded time periods)
"""

# read file
file = open('access_log', 'r', encoding="utf-8")
lines = file.readlines()


def write_to_file (filename, output_file):
    """writes result to the file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_file)
    print(f"See results in file {filename}")


def write_to_file_by_lines(filename, print_to_file):
    """writes results to file by lines with sys.stdout"""
    with open(filename, 'a', encoding="utf-8") as sys.stdout:
        print(print_to_file)
    sys.stdout = sys.__stdout__  # reset stdout


def most_often_used_ip(quantity):
    """1(-a) - ip addresses of clients (x.x.x.x) or (x.x.x.x, x.x.x.x, ...),
    find N of the most often used"""

    # find all ip addresses, convert to list
    all_ip_list = []

    for line_a in lines:
        ip_address_a = "".join(list(parse.search("({})", line_a).fixed))
        all_ip_list.append(ip_address_a)
    # count most frequent used
    most_common_ip = Counter(all_ip_list).most_common(quantity)
    # convert to string
    result_a = '\n'.join([str(elem) for i, elem in enumerate(most_common_ip)])

    return result_a

# 1(-a) - ip addresses of clients (x.x.x.x) or (x.x.x.x, x.x.x.x, ...),
# find N of the most often used
if args.a:
    filename_1 = f"output_logs/output_1_{args.a}_elements"
    output_1 = most_often_used_ip(args.a)

    write_to_file(filename_1, output_1)

# 2(-b) - quantity of request in time period (minutes):
# from 09.01.41 - 09.02.41 min - x requests, 09.02.41 - 09.03.41 min - y requests etc"""
if args.b:
    filename_2 = f'output_logs/output_2_{args.b}_min_interval'
    first_run = True
    count = 0

    for line in lines:
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        # assign delta
        delta = timedelta(minutes=args.b)

        # first run to find end_time for time period
        if first_run == True:
            first_run = False
            end_time = current_time + delta

        # find all times in time interval and write to file
        if current_time >= end_time:    # write count to file, renew count to 1, renew end time
            start_time = end_time - delta
            print_to_file_2 = f"from {start_time} to {end_time} - {count} requests"
            write_to_file_by_lines (filename_2,  print_to_file_2)
            count = 1
            end_time += delta
        else:                           # count the itteration
            count += 1

    # write the last time interval to file, if it is less than given interval:
    if (end_time - delta) == current_time:
        pass
    else:
        print_to_file_2_last = f"""from {end_time - delta} to {current_time} - {count} requests.
                   !!! the last time interval is less then {args.b} min """
        write_to_file_by_lines (filename_2,  print_to_file_2_last)

    print(f"See results in file {filename_2}")


def most_often_user_agents (number):
    """finds n most often user agents"""

    # get all user agents
    agents_list = []

    for line_c in lines:
        in_quotes_c = line_c.split('"')[1::2]
        agents = "".join(in_quotes_c[2::4])
        agents_list.append(agents)

    # count most frequent used
    most_common_agent = Counter(agents_list).most_common(number)
    # convert to string
    result_c = '\n'.join([str(elem) for i, elem in enumerate(most_common_agent)])

    return result_c

# 3(-c) - most often user agents
if args.c:
    filename_3 = f"output_logs/output_3_{args.c}_elements"
    output_3 = most_often_user_agents(args.c)

    write_to_file(filename_3, output_3)

# 4(-d) - quantity of code S 304 / 404 in time period
if args.d:
    filename_4 = f'output_logs/output_4_{args.d}_minutes_interval'
    first_run = True
    count = 0

    for line in lines:
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        # assign delta
        delta = timedelta(minutes=args.d)
        # find error code
        error = re.search(r"[34]04", line)

        # first run to find end_time for time period
        if first_run == True:
            first_run = False
            end_time = current_time + delta

        # find all times in time interval and write to file
        if current_time >= end_time:    # write count to file, renew count to 1, renew end time
            start_time = end_time - delta
            print_to_file_4 = f"from {end_time - delta} to {end_time} - {count} errors"
            write_to_file_by_lines (filename_4,  print_to_file_4)
            count = 1
            end_time += delta
        else:                           # count the itteration
            if error:
                count += 1
            else:
                continue

    # write the last time interval to file, if it is less than given interval:
    if (end_time - delta) == current_time:
        pass
    else:
        print_to_file_4_last = f"""from {start_time} to {current_time} - {count} errors.
                  !!! the last time interval is less then {args.d} min """
        write_to_file_by_lines (filename_4,  print_to_file_4_last)

    print(f"See results in file {filename_4}")

# 5(-e) - find N the longest / the shortest requests (in millis) - format: Get, time when, ip address - millis
if args.e:
    millis_list = []
    arg_1 = int(args.e[0])

    # append list with needed values line by line
    for line in lines:
        request = "".join(re.findall(r'[A-Z]* \/(?:[^\/]*\/)', line))
        time = "".join(list(parse.search("[{}]", line).fixed))
        ip_address = "".join(list(parse.search("({})", line).fixed))
        millis = """request time in
                 millis: """ + (re.search(r"(?:\d+|-) (?:\d+|-) (?:\d+|-) (?:\d+|-)", line).group(0)).rsplit(' ', 1)[-1]
        tmp_list = []
        tmp_list.append(request)
        tmp_list.append(time)
        tmp_list.append(ip_address)
        tmp_list.append(millis)
        millis_str = " ".join(tmp_list)
        millis_list.append(millis_str)

    # sort list and convert result to readable string, try if there is second optional argument
    result = '\n'.join([str(elem)
                       for i, elem in enumerate(millis_list[:arg_1])])

    # write results to the output file, try if there is second optional argument
    try:
        if args.e[1] == "s":
            with open(f'output_logs/output_5_{arg_1}_shortest_requests', 'a', encoding="utf-8") as sys.stdout:
                print(result)
        else:
            print("you can only use argument 's' - shortest")
            sys.exit()
    except IndexError:
        with open(f'output_logs/output_5_{arg_1}_longest_requests', 'a', encoding="utf-8") as sys.stdout:
            print(result)
    sys.stdout = sys.__stdout__  # reset stdout

    # print to the console:
    try:
        if args.e[1] == "s":
            print(f"See results in file 'output_logs/output_5_{arg_1}_shortest_requests'")
        else:
            print("you can only use argument 's' - shortest")
    except IndexError:
        print(f"See results in file 'output_logs/output_5_{arg_1}_longest_requests'")


def n_most_often_requests (number, to_slash):
    """find N most often requests up to 2nd / 3rd / ... slash"""

    # check requested number of slash (second argument) and use in re.findall to find needed string
    slash_number = int(to_slash) - 1
    up_to_k_slash = []

    for line_f in lines:
        up_to_k_slash_string = "".join(re.findall(
            rf'[A-Z]* \/(?:[^\/]*\/){{{slash_number}}}', line_f))
        up_to_k_slash.append(up_to_k_slash_string)

    # count most frequent used
    most_common_request = Counter(up_to_k_slash).most_common(int(number))
    # convert to string
    result_f = '\n'.join([str(elem)
                       for i, elem in enumerate(most_common_request)])

    return result_f

# 6(-f) - find N most often requests up to 2nd / 3rd / ... slash
if args.f:
    filename_6 = f"output_logs/output_6_{args.f[0]}_elements_to_{args.f[1]}_slash"
    output_6 = n_most_often_requests(args.f[0], args.f[1])

    write_to_file(filename_6, output_6)


def requests_per_node():
    """quantity of requests per node (worker)"""

    # get all nodes
    node_list_g = []

    for line_g in lines:
        node = "".join(re.findall(r'ajp:[^"]*', line_g))
        node_list_g.append(node)

    # count frequency of usage
    per_node_g = Counter(node_list_g).most_common()
    # convert to string
    result_g = '\n'.join([str(elem) for i, elem in enumerate(per_node_g)])

    return result_g

# 7(-g) - quantity of requests per node (worker)
if args.g:
    filename_7 = "output_logs/output_7"
    output_7 = requests_per_node()

    write_to_file(filename_7, output_7)


def same_ref_to_page():
    """quantity of same references to webpage, sort by domain"""
    webpage_list = []

    # get all webpages
    for line_i in lines:
        in_quotes = line_i.split('"')[1::2]
        webpage = "".join(in_quotes[1::4])
        webpage_list.append(webpage)

    # count frequency of usage
    per_webpage = Counter(webpage_list).most_common()
    # sort by domain
    per_webpage.sort(key=lambda x: x[0])
    result_i = '\n'.join([str(elem) for i, elem in enumerate(per_webpage)])

    return result_i

# 8(-i) - quantity of same references to webpage, sort by domain
if args.i:
    filename_8 = "output_logs/output_8"
    output_8 = same_ref_to_page()

    write_to_file(filename_8, output_8)

# 9(-j) - quantity of request in time period by nodes (workers)
if args.j:
    filename_9 = f'output_logs/output_9_{args.j}_minutes_interval'
    first_run = True

    for line in lines:
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        # assign time delta
        delta = timedelta(minutes=args.j)

        # first run to find end_time for time period
        if first_run == True:
            first_run = False
            end_time = current_time + delta
            # assign node list
            node_list = []

        # find all times in time interval and write to file
        if current_time >= end_time:  # write count to file, renew count to 1, renew end time
            start_time = end_time - delta
            # count frequency of usage for each node
            per_node = Counter(node_list).most_common()
            # convert to readable string format
            per_node_str = '\n'.join([str(elem) for i, elem in enumerate(per_node)])
            print_to_file_9 = f"from {end_time - delta} to {end_time}, requests per node: \n {per_node_str}"
            write_to_file_by_lines (filename_9,  print_to_file_9)
            node_list = []
            end_time += delta
        else:
            # find node and add it to the node list
            node_current = re.search(r'ajp:[^"]*', line)
            if not node_current:
                pass
            else:
                node_str_current = node_current.group(0)
                node_list.append(node_str_current)

    # write the last time interval to file, if it is less than given interval:
    if (end_time - delta) == current_time:
        pass
    else:
        print_to_file_9_last = f"""from {end_time - delta} to {current_time}, requests per node: \n {per_node_str}
                !!! the last time interval is less then {args.j} min """
        write_to_file_by_lines (filename_9,  print_to_file_9_last)

    print(
        f"See results in file {filename_9}")

# 10(-k) - task 2, sorted by quantity (N of the most loaded time periods)
if args.k:
    filename_10 = f'output_logs/output_10_{args.k}_minutes_interval'
    first_run = True
    count = 0

    for line in lines:
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        # assign delta
        delta = timedelta(minutes=args.k)

        # first run to find end_time for time period
        if first_run == True:
            first_run = False
            end_time = current_time + delta
            count_list = []

        # find all times in time interval and write to file
        if current_time >= end_time:  # write count to list, renew count to 1, renew end time
            start_time = end_time - delta
            count_list.append(f"from {start_time} to {end_time} - {count} requests")
            count = 1
            end_time += delta
        else:  # count the itteration
            count += 1

    # write the last time interval to list, if it is less than given interval:
    if (end_time - delta) == current_time:
        pass
    else:
        count_list.append(
            f"""from {end_time - delta} to {current_time} - {count} requests. 
            !!! the last time interval is less then {args.k} min """)

    # sort the list and convert to readable string format
    count_list.sort(key=lambda x: x.split()[7], reverse=True)
    print_to_file_10 = '\n'.join([str(elem) for i, elem in enumerate(count_list)])

    write_to_file_by_lines (filename_10,  print_to_file_10)

    print(
        f"See results in file {filename_10}")


file.close()
