"""task 5 python"""
import argparse
import os
import re
from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import psycopg2
from pymongo import MongoClient

parser = argparse.ArgumentParser(prog="task5", usage='%(prog)s [options]')

parser.add_argument("-ms", default=False, action="store_true", help="choose MySQL database")
parser.add_argument("-pos", default=False, action="store_true", help="choose PostgreSQL database")
parser.add_argument("-mon", default=False, action="store_true", help="choose PostgreSQL database")
parser.add_argument("-a", type=int, help="[N, int] find N the most used ip addresses -output1-")
parser.add_argument("-b", type=int,
                    help="[N, int] find quantity of requests in time period, N minutes -output2-")
parser.add_argument("-c", type=int,
                    help="[N, int] find N the most often used user agents -output3-")
parser.add_argument("-d", type=int,
                    help="[N, int] find N quantity of error code in time period -output4-")
parser.add_argument("-e", nargs='+',
                    help="""[N, int] [s, optional] find N the longest (by default) requests (in millis).
                    If add argument [s], finds N the shortest requests  - format:
                    Get, time when, ip address - millis -output5-""")
parser.add_argument("-f", nargs='+',
                    help="[N, int] [K, int] find N the most often requests up to K slash -output6-")
parser.add_argument("-g", default=False, action="store_true",
                    help="show quantity of requests per node (worker) -output7-")
parser.add_argument("-i", default=False, action="store_true",
                    help="show quantity of same references to webpage, sort by domain -output8-")
parser.add_argument("-j", type=int,
                    help="[int, N] find quantity of request in time period, N minutes, by nodes (workers) -output9-")
parser.add_argument("-k", type=int,
                    help="""[int, N] find quantity of requests in time period, N minutes,
                    sorted by quantity of requests -output10-""")

args = parser.parse_args()

# variables for connection details
mysql_user = os.environ.get('MYSQL_DB_USER')
mysql_pass = os.environ.get('MYSQL_DB_PASS')
postgre_user = os.environ.get('POSTGRESQL_DB_USER')
postgre_pass = os.environ.get('POSTGRESQL_DB_PASS')
postgre_database = os.environ.get('POSTGRESQL_DB_DATABASE')
# variables for databases input
data_base= "access_log"
table = "access_log_table"
columns = """balancer_ip varchar(255), client_ip varchar(255), username varchar(255), user_auth varchar(255),
date_and_time varchar(255), request varchar(2000), status_code varchar(255), bytes_sent varchar(255),
proc_time_sec varchar(255), proc_time_mil varchar(255), site_refered varchar(2000), 
user_agent varchar(255), worker_node_ip varchar(255)"""
#print(postgre_values)
values = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
output_file = "output_logs/output_file"
# arguments and dbs list
all_arguments = [args.a, args.b, args.c, args.d, args.e, args.f, args.g, args.i, args.j, args.k]
all_databases = [args.ms, args.pos, args.mon]
#variables for column names
client_ip_column = "client_ip"
date_time_column = "date_and_time"
request_column = "request"
status_code_column = "status_code"
millis_column = "proc_time_mil"
webpage_column = "site_refered"
agents_column = "user_agent"
nodes_column = "worker_node_ip"
#date format
date_format = '%d/%b/%Y:%H:%M:%S'

with open('access_log', 'r') as file:
    lines = file.readlines()

# parse logfile
balancer_ip = []
for line in lines:
    balancer_ip_select = line.split(" ")[0]
    balancer_ip.append(balancer_ip_select)

client_ip = []
for line in lines:
    match = re.search(r'\((.+?)\)', line)
    if match:
        client_ip.append(match.group(1))

username = []
user_auth = []
for line in lines:
    after_parentheses = line.split(')')[1]
    after_parentheses = after_parentheses.strip()
    username_select = after_parentheses.split(" ")[0]
    username.append(username_select)
    user_auth_select = after_parentheses.split(" ")[1]
    user_auth.append(user_auth_select)

date_and_time = []
for line in lines:
    time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
    time_str = time.group(0)
    time_str = time_str.strip()
    date_and_time.append(time_str)

request = []
status_code = []
bytes_sent = []
proc_time_sec = []
proc_time_mil = []
for line in lines:
    after_square = line.split(']')[1]
    after_square = after_square.strip()
    request_select = after_square.split("\"")[1]
    request.append(request_select)
    after_request = after_square.split("\"")[2]
    after_request = after_request.strip()
    status_code_select = after_request.split(" ")[0]
    status_code.append(status_code_select)
    bytes_sent_select = after_request.split(" ")[1]
    bytes_sent.append(bytes_sent_select)
    proc_time_sec_select = after_request.split(" ")[2]
    proc_time_sec.append(proc_time_sec_select)
    proc_time_mil_select = after_request.split(" ")[3]
    proc_time_mil.append(proc_time_mil_select)

site_refered = []
for line in lines:
    in_quotes_site = line.split('"')[1::2]
    site_refered_select = "".join(in_quotes_site[1::4])
    site_refered.append(site_refered_select)

user_agent = []
for line in lines:
    in_quotes_ua = line.split('"')[1::2]
    user_agent_select = "".join(in_quotes_ua[2::4])
    user_agent.append(user_agent_select)

worker_node_ip = []
for line in lines:
    worker_node_ip_select = "".join(re.findall(r'ajp:[^"]*', line))
    worker_node_ip.append(worker_node_ip_select)

# data frame for mysql database
df = pd.DataFrame(
    {
        "balancer_ip": balancer_ip,
        "client_ip": client_ip,
        "username": username,
        "user_auth": user_auth,
        "date_and_time": date_and_time,
        "request": request,
        "status_code": status_code,
        "bytes_sent": bytes_sent,
        "proc_time_sec": proc_time_sec,
        "proc_time_mil": proc_time_mil,
        "site_refered": site_refered,
        "user_agent": user_agent,
        "worker_node_ip": worker_node_ip, 
    }
)

# data for mongodb
data_dict = {
        "balancer_ip": balancer_ip,
        "client_ip": client_ip,
        "username": username,
        "user_auth": user_auth,
        "date_and_time": date_and_time,
        "request": request,
        "status_code": status_code,
        "bytes_sent": bytes_sent,
        "proc_time_sec": proc_time_sec,
        "proc_time_mil": proc_time_mil,
        "site_refered": site_refered,
        "user_agent": user_agent,
        "worker_node_ip": worker_node_ip, 
    }

# Functions
# MySQL db and table creation
def mysql_connect_create_db(data_base):
    """connect to mysql and create database"""

    try:
        conn_db = msql.connect(host='localhost', user=mysql_user,
                            password=mysql_pass)
        if conn_db.is_connected():
            cursor = conn_db.cursor()
            cursor.execute(f"CREATE DATABASE {data_base}")
            print("Database is created")

    except Error as e:
        print("Error while connecting to MySQL", e)


def mysql_create_table(data_base, table, columns, values):
    """create table under base db in mysql"""
    try:
        conn_db = msql.connect(host='localhost',
                            database=data_base, user=mysql_user,
                            password=mysql_pass)
        if conn_db.is_connected():
            cursor = conn_db.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute(f'DROP TABLE IF EXISTS {table};')
            print('Creating table....')
            cursor.execute(f"CREATE TABLE {table} ({columns})")
            print(f"{table} table is created....")
            for i,row in df.iterrows():
                sql = f"INSERT INTO {data_base}.{table} VALUES ({values})"
                cursor.execute(sql, tuple(row))
                conn_db.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    
    print("The table was successfully updated")


# PostgreSQL db and table creation
def postgres_connect_create_db(data_base):
    """connect to postresql and create database"""

    try:
        conn = psycopg2.connect(database=postgre_database,
                                user=postgre_user, password=postgre_pass,
                                host='127.0.0.1', port='5432'
        )
        conn.autocommit = True

        # create a base if not exist
        if not data_base:
            cursor = conn.cursor()

            # Creating a database
            cursor.execute(f'''CREATE database {data_base};''')
            print(f"database {data_base} created successfully...")

        # Closing the connection
        conn.close()

    except Error as e:
        print("Error while connecting to PostgreSQL", e)


def postgres_create_table(data_base, table, columns, values):
    """connect to postgresql base db and create table""" 

    try:
        conn = psycopg2.connect(database=data_base,
                                user=postgre_user, password=postgre_pass,
                                host='127.0.0.1', port='5432')
        cursor = conn.cursor()

        # drop table if already exists
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

        # create table
        cursor.execute(f'''CREATE TABLE {table}({columns})''')
        print(f"table {table} created successfully...")
        for i,row in df.iterrows():
            sql = f"INSERT INTO {table} VALUES ({values})"
            cursor.execute(sql, tuple(row))
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()

        # Closing the connection
        conn.close()

    except Error as e:
        print("Error while connecting to PostgreSQL", e) 

    print("The table was successfully updated")

# Mongo DB and collection creation
def mongo_connect_create_db_collection(data_base, table):
    """connect to mongo db and create collection"""

    client = MongoClient('localhost', 27017)

    # getting the database instance
    db = client[f'{data_base}']

    # drop collection if exists
    try:
        coll_exists = db.validate_collection(f"{table}")
        if coll_exists:
            db[f'{table}'].drop()
            coll = db[f'{table}']
    except:
        #creating a collection
        coll = db[f'{table}'] 
    
    # inserting document into a collection
    coll.insert_one(data_dict)

    print("The collection was successfully updated")


# export from databases
def get_list_from_MySQL(data_base, column_name):
    """returns values from from MySQL as list"""
    try:
        conn_db = msql.connect(host='localhost',
                            database=data_base, user=mysql_user,
                            password=mysql_pass)

        if conn_db.is_connected:
            cursor = conn_db.cursor()
            cursor.execute(f'SELECT {column_name} FROM {table};')
            result_set = cursor.fetchall()
            column_values = [row[0] for row in result_set]
            return column_values

    except Error as e:
        print("Error while connecting to MySQL", e)


def get_list_from_Postgre(data_base, column_name):
    """returns values from from PostgreSQL as list"""
    try:
        conn = psycopg2.connect(database=data_base,
                                user=postgre_user, password=postgre_pass,
                                host='127.0.0.1', port='5432')
        cursor = conn.cursor()

        cursor.execute(f'SELECT {column_name} FROM {table};')
        result_set = cursor.fetchall()
        column_values = [row[0] for row in result_set]
        return column_values

    except Error as e:
        print("Error while connecting to PostgreSQL", e) 


def get_list_from_Mongo(data_base, column_name):
    """returns values from from MongoDB as list"""
    client = MongoClient('localhost', 27017)
    db = client[f'{data_base}']
    coll = db[f'{table}']

    column_values = coll.distinct(column_name)
    return column_values

# write to output file
def write_to_file(input_list, output_file):

    with open(f'{output_file}', 'w') as file:
        for element in input_list:
            file.write(element + '\n')

    print(f"Output from \"{table}\" table \"{data_base}\" db is written to \"{output_file}\"")


# functions for arguments
def argument_a(ip_list_from_db):
    """1(-a) - ip addresses of clients (x.x.x.x) or (x.x.x.x, x.x.x.x, ...), find N of the most often used"""

    # convert to string separated by comma and convert to list back, to separate ip addresses
    all_ip_string = ",".join(ip_list_from_db)
    all_ip_list = all_ip_string.split(",")
    # count most frequent used
    most_common_ip = Counter(all_ip_list).most_common(args.a)
    most_common_ip = [', '.join(str(item) for item in tpl) for tpl in most_common_ip]

    return most_common_ip


def argument_b(date_time_list_from_db, diff):
    """2(-b) - quantity of request in time period (minutes): 
           from 09.01.41 - 09.02.41 min - x requests, 09.02.41 - 09.03.41 min - y requests etc"""
    #diff = args.b
    first_run = True
    count = 0
    time_intervals = []

    for line in date_time_list_from_db:  
        current_time = datetime.strptime(line, date_format)
        # assign delta
        delta = timedelta(minutes=diff)

        # first run to find end_time for time period
        if first_run == True:
            first_run = False
            end_time = current_time + delta

        # find all times in time interval and write to file
        if current_time >= end_time:    # write count to file, renew count to 1, renew end time
            time_from = str(end_time - delta)
            time_to = str(current_time)
            time_from_to = f"{time_from} - {time_to}"
            time_intervals_list = [time_from_to, str(count)]
            time_intervals.append(time_intervals_list)
            count = 1
            end_time += delta
        else:                           # count the itteration
            count += 1
  
    # write the last time interval to file, if it is less than given interval:
    if (end_time - delta) <= current_time:
        time_from = str(end_time - delta)
        time_to = str(current_time)
        time_from_to = f"{time_from} - {time_to}"
        time_intervals_list = [time_from_to, str(count)]
        time_intervals.append(time_intervals_list)

    time_intervals = [', '.join(sublist) for sublist in time_intervals]

    return time_intervals


def argument_c(agents_list_from_db):
    """3(-c) - most often user agents"""

    # count most frequent used
    most_common_agent = Counter(agents_list_from_db).most_common(args.c)
    most_common_agent = [', '.join(str(item) for item in tpl) for tpl in most_common_agent]

    return most_common_agent


def argument_d(date_time_status_code_from_db):
    """4(-d) - quantity of code S 304 / 404 in time period"""
    first_run = True
    count = 0
    time_intervals = []
    
    for line in date_time_status_code_from_db:       
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, date_format)
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
            time_from = str(end_time - delta)
            time_to = str(current_time)
            time_from_to = f"{time_from} - {time_to}"
            time_intervals_list = [time_from_to, str(count)]
            time_intervals.append(time_intervals_list)
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
        time_from = str(end_time - delta)
        time_to = str(current_time)
        time_from_to = f"{time_from} - {time_to}"
        time_intervals_list = [time_from_to, str(count)]
        time_intervals.append(time_intervals_list)

    time_intervals = [', '.join(sublist) for sublist in time_intervals]
    return time_intervals


def argument_e(get_date_ip_millis_from_db):
    """5(-e) - find N the longest / the shortest requests (in millis) - format: Get, time when, ip address - millis"""
    
    arg_1 = int(args.e[0])

    millis_list = get_date_ip_millis_from_db

    # sort list, try if there is second optional argument    
    try: 
        if args.e[1] == "s":    
            millis_list = sorted(millis_list, key=lambda x: int(x[-1]), reverse=False)
    except:
        millis_list = sorted(millis_list, key=lambda x: int(x[-1]), reverse=True)

    result = [elem for i, elem in enumerate(millis_list[:arg_1])]
    result = ['; '.join(sublist) for sublist in result]
    return result


def argument_f(requests_from_db):
    """6(-f) - find N most often requests up to 2nd / 3rd / ... slash"""

    slash_number = int(args.f[1]) - 1
    up_to_k_slash = []

    for line in requests_from_db:
        up_to_k_slash_string = "".join(re.findall(rf'[A-Z]* \/(?:[^\/]*\/){{{slash_number}}}', line))
        up_to_k_slash.append(up_to_k_slash_string)

    # count most frequent used
    most_common_request = Counter(up_to_k_slash).most_common(int(args.f[0]))
    most_common_request = [', '.join(str(item) for item in tpl) for tpl in most_common_request]

    return most_common_request


def argument_g(nodes_list_from_db):
    """7(-g) - quantity of requests per node (worker)"""
    
    # count most frequent used
    per_node = Counter(nodes_list_from_db).most_common()
    per_node = [', '.join(str(item) for item in tpl) for tpl in per_node]

    return per_node


def argument_i(webpages_from_db):
    """8(-i) - quantity of same references to webpage, sort by domain"""
    
    # count most frequent used
    per_webpage = Counter(webpages_from_db).most_common()
    per_webpage.sort(key=lambda x: x[0])
    per_webpage = [', '.join(str(item) for item in tpl) for tpl in per_webpage]
    
    return per_webpage


def argument_j(date_time_nodes_from_db):
    """9(-j) - quantity of request in time period by nodes (workers)"""
    
    first_run = True
    time_intervals = []
    
    for line in date_time_nodes_from_db:       
        # find time record and convert to datetime object
        time = re.search(r"(?:[\d]{2}\/[a-zA-Z]{3}\/[\d]{4}:.*?) ", line)
        time_str = time.group(0)
        time_str = time_str.strip()
        current_time = datetime.strptime(time_str, date_format)
        # assign time delta
        delta = timedelta(minutes=args.j)
                
        # first run to find end_time for time period        
        if first_run == True:
            first_run = False
            end_time = current_time + delta
            # assign node list
            node_list = []
            
        # find all times in time interval and write to file
        if current_time >= end_time:    # write count to file, renew count to 1, renew end time   
            start_time = end_time - delta
            per_node = Counter(node_list).most_common() # count frequency of usage for each node  
            time_from = str(end_time - delta)
            time_to = str(current_time)
            time_from_to = f"{time_from} - {time_to}"
            if args.ms or args.pos:     # format for SQL dbs
                for i in per_node:
                    time_intervals_list = [time_from_to, str(i)]
                    time_intervals.append(time_intervals_list)
            elif args.mon:              # format for non-SQL dbs
                time_intervals_list = [time_from_to, str(per_node)]
                time_intervals.append(time_intervals_list)
                
            # reset node list and end time
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
    
    # write the last time interval to list, if it is less than given interval:      
    if (end_time - delta) == current_time:
        pass
    else:
        per_node = Counter(node_list).most_common() # count frequency of usage for each node
        time_from = str(end_time - delta)
        time_to = str(current_time)
        time_from_to = f"{time_from} - {time_to}"
        if args.ms or args.pos:     # format for SQL dbs
            for i in per_node:
                time_intervals_list = [time_from_to, str(i)]
                time_intervals.append(time_intervals_list)
        elif args.mon:              # format for non-SQL dbs
            time_intervals_list = [time_from_to, str(per_node)]
            time_intervals.append(time_intervals_list)
            
    time_intervals = [', '.join(sublist) for sublist in time_intervals]
    return time_intervals


def argument_k(date_time_from_db):
    """10(-k) - task 2(b), sorted by quantity (N of the most loaded time periods)"""
    
    count_list = argument_b(date_time_from_db, diff=args.k)
    count_list = [string.split(', ') for string in count_list]
    count_list = sorted(count_list, key=lambda x: int(x[-1]), reverse=True)
    time_intervals_sorted = [', '.join(sublist) for sublist in count_list]
    return time_intervals_sorted


# IF conditions

if args.ms and not any (all_arguments):
    mysql_connect_create_db(data_base)
    mysql_create_table(data_base, table, columns, values)

if args.pos and not any (all_arguments):
    postgres_connect_create_db(data_base)
    postgres_create_table(data_base, table, columns, values)

if args.mon and not any (all_arguments):
    mongo_connect_create_db_collection(data_base, table)

if all_arguments and not any (all_databases):
    print("Please, choose database (see -help)")

if args.a and any (all_databases):
    if args.ms:
        ip_from_db = get_list_from_MySQL(data_base, client_ip_column)
    elif args.pos:
        ip_from_db = get_list_from_Postgre(data_base, client_ip_column)
    elif args.mon:
        ip_from_db = get_list_from_Mongo(data_base, client_ip_column)

    file_1 = "output_logs/output_file_1"
    write_to_file(argument_a(ip_from_db), file_1)

if args.b and any (all_databases):
    if args.ms:
        date_time_from_db = get_list_from_MySQL(data_base, date_time_column)
    elif args.pos:
        date_time_from_db = get_list_from_Postgre(data_base, date_time_column)
    elif args.mon:
        date_time_from_db = get_list_from_Mongo(data_base, date_time_column)

    file_2 = "output_logs/output_file_2"
    write_to_file(argument_b(date_time_from_db, diff=args.b), file_2)

if args.c and any (all_databases):
    if args.ms:
        agents_from_db = get_list_from_MySQL(data_base, agents_column)
    elif args.pos:
        agents_from_db = get_list_from_Postgre(data_base, agents_column)
    elif args.mon:
        agents_from_db = get_list_from_Mongo(data_base, agents_column)

    file_3 = "output_logs/output_file_3"
    write_to_file(argument_c(agents_from_db), file_3)

if args.d and any (all_databases):
    if args.ms:
        date_time_from_db = get_list_from_MySQL(data_base, date_time_column)
        status_code_from_db = get_list_from_MySQL(data_base, status_code_column)
    elif args.pos:
        date_time_from_db = get_list_from_Postgre(data_base, date_time_column)
        status_code_from_db = get_list_from_Postgre(data_base, status_code_column)
    elif args.mon:
        date_time_from_db = get_list_from_Mongo(data_base, date_time_column)
        status_code_from_db = get_list_from_Mongo(data_base, status_code_column)

    date_time_status_code_from_db = [s1 + " " + s2 for s1, s2 in zip(date_time_from_db, status_code_from_db)]
    file_4 = "output_logs/output_file_4"
    write_to_file(argument_d(date_time_status_code_from_db), file_4)

if args.e and any (all_databases):
    if args.ms:
        request_from_db = get_list_from_MySQL(data_base, request_column)
        date_time_from_db = get_list_from_MySQL(data_base, date_time_column)
        ip_from_db = get_list_from_MySQL(data_base, client_ip_column)
        millis_from_db = get_list_from_MySQL(data_base, millis_column)
    elif args.pos:
        request_from_db = get_list_from_Postgre(data_base, request_column)
        date_time_from_db = get_list_from_Postgre(data_base, date_time_column)
        ip_from_db = get_list_from_Postgre(data_base, client_ip_column)
        millis_from_db = get_list_from_Postgre(data_base, millis_column)
    elif args.mon:
        request_from_db = get_list_from_Mongo(data_base, request_column)
        date_time_from_db = get_list_from_Mongo(data_base, date_time_column)
        ip_from_db = get_list_from_Mongo(data_base, client_ip_column)
        millis_from_db = get_list_from_Mongo(data_base, millis_column)

    get_date_ip_millis_from_db = [[s1, s2, s3, s4] for s1, s2, s3, s4 
                                     in zip(request_from_db, date_time_from_db, ip_from_db, millis_from_db)]
    file_5 = "output_logs/output_file_5"
    write_to_file(argument_e(get_date_ip_millis_from_db), file_5)

if args.f and any(all_databases):
    if args.ms:
        request_from_db = get_list_from_MySQL(data_base, request_column)
    elif args.pos:
        request_from_db = get_list_from_Postgre(data_base, request_column)
    elif args.mon:
        request_from_db = get_list_from_Mongo(data_base, request_column)

    file_6 = "output_logs/output_file_6"
    write_to_file(argument_f(request_from_db), file_6)

if args.g and any(all_databases):
    if args.ms:
        nodes_from_db = get_list_from_MySQL(data_base, nodes_column)
    elif args.pos:
        nodes_from_db = get_list_from_Postgre(data_base, nodes_column)
    elif args.mon:
        nodes_from_db = get_list_from_Mongo(data_base, nodes_column)

    file_7 = "output_logs/output_file_7"
    write_to_file(argument_g(nodes_from_db), file_7)

if args.i and any(all_databases):
    if args.ms:
        webpages_from_db = get_list_from_MySQL(data_base, webpage_column)
    elif args.pos:
        webpages_from_db = get_list_from_Postgre(data_base, webpage_column)
    elif args.mon:
        webpages_from_db = get_list_from_Mongo(data_base, webpage_column)

    file_8 = "output_logs/output_file_8"
    write_to_file(argument_i(webpages_from_db), file_8)

if args.j and any(all_databases):
    if args.ms:
        date_time_from_db = get_list_from_MySQL(data_base, date_time_column)
        nodes_from_db = get_list_from_MySQL(data_base, nodes_column)
    elif args.pos:
        date_time_from_db = get_list_from_Postgre(data_base, date_time_column)
        nodes_from_db = get_list_from_Postgre(data_base, nodes_column)
    elif args.mon:
        date_time_from_db = get_list_from_Mongo(data_base, date_time_column)
        nodes_from_db = get_list_from_Mongo(data_base, nodes_column)

    date_time_nodes_from_db = [s1 + " " + s2 for s1, s2 in zip(date_time_from_db, nodes_from_db)]
    file_9 = "output_logs/output_file_9"
    write_to_file(argument_j(date_time_nodes_from_db), file_9)

if args.k and any(all_databases):
    if args.ms:
        date_time_from_db = get_list_from_MySQL(data_base, date_time_column)
    elif args.pos:
        date_time_from_db = get_list_from_Postgre(data_base, date_time_column)
    elif args.mon:
        date_time_from_db = get_list_from_Mongo(data_base, date_time_column)

    file_10 = "output_logs/output_file_10"
    write_to_file(argument_k(date_time_from_db), file_10)