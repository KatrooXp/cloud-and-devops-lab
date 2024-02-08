"""working with csv file"""
import re
import argparse
import csv
import json
import pandas

parser = argparse.ArgumentParser(prog="task3b", usage='%(prog)s [options]')

parser.add_argument("-H", default=False, action="store_true", help="open with read_csv, with header")
parser.add_argument("-N", default=False, action="store_true", help="open with read_csv, without header")
parser.add_argument("-ipv4_n", default=False, action="store_true",
                    help="export all ipv4 + netmasks to file 'export_ipv4_netmask.txt'")
parser.add_argument("-ipv6", default=False, action="store_true", help="export all ipv6 to file 'export_ipv6.txt'")
parser.add_argument("-name", type = str, help="filter by name value, output to terminal")
parser.add_argument("-c", type = str, help="""works with -value argument only: -c [column name]
                    -value [value] filter by value in column, output to terminal""")
parser.add_argument("-value", type = str, help="""works with -c argument only: -c [column name]
                    -value [value] filter by value in column, output to terminal""")
parser.add_argument("-c2", type = str, help="""with -c -value and -value2 arguments only: -c [column name]
                    -value [value] -c2 [column name] -value2 [value] filter by values in 2 column, output to terminal""")
parser.add_argument("-value2", type = str, help="""works with -c -value and -value2 -c2 argument only: -c [column name]
                    -value [value] -c2 [column name] -value2 [value] filter by values in 2 column, output to terminal""")
parser.add_argument("-l", nargs="+", type = int, help="""gets only named lines by number,
                    any quantity of int arguments starting from 1, output to file""")
parser.add_argument("-column", nargs="+", type = str,
                    help="gets only named columns, by column name, any quantity of arguments, output to file")
parser.add_argument("-json", default=False, action="store_true", help="converts file to json")

args = parser.parse_args()

# whith/without header
if args.N:
    df = pandas.read_csv("example.csv", header=None)
    print(df)
elif args.H:
    df = pandas.read_csv("example.csv")
    print(df)
else:
    df = pandas.read_csv("example.csv")


def readfile():
    """read csv file"""
    with open("example.csv") as f:
        global file
        file = f.read()


def find_all(pat_name, file):
    """findall function"""
    find_name = re.findall(pat_name, file)
    return find_name


def export(export_file, export_info):
    """export in file function"""
    with open(f"{export_file}", "a") as f:
        f.write(export_info)

# find all ipv6
if args.ipv6:
    readfile()
    pat_ipv6 = r"(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]):){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]):){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?:,)"

    export_file_ipv6 = "export_ipv6.txt"
    export_info_ipv6 = find_all(pat_ipv6, file)
    export_info_ipv6 = " ".join(export_info_ipv6)
    export(export_file_ipv6, export_info_ipv6)

# find all ipv4 and netmask
if args.ipv4_n:
    readfile()
    pat_ipv4 = r'((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:,))'
    pat_netmask = r"(?:(?:(?:(?:25[2,4,5]|24[0,8]|224|192|128|0)\.){3})(?:(?:25[2,4,5]|24[0,8]|224|192|128|0))(?:,))"

    export_info_ipv4 = find_all(pat_ipv4, file)
    export_info_netmask = find_all(pat_netmask, file)
    export_info_ipv4_netmask = [i + j for i, j in zip(export_info_ipv4, export_info_netmask)]
    export_info_ipv4_netmask = " ".join(export_info_ipv4_netmask)
    export_file_ipv4_netmask = "export_ipv4_netmask.txt"
    export(export_file_ipv4_netmask, export_info_ipv4_netmask)

# filter by column data
if args.name:

    output_name = df.name.str.contains(args.name)
    print(df[output_name])

if args.c and args.value and not args.c2 and not args.value2:

    output = df[f"{args.c}"].str.contains(args.value)
    print(df[output])

# filter by several columns
if args.c and args.value and args.c2 and args.value2:

    output = df[f"{args.c}"].str.contains(args.value)
    output_line = df[f"{args.c2}"].str.contains(args.value2)
    print(df[output & output_line])

# get specific lines
if args.l:

    # specify rows to import
    specific_rows = [0, ]
    arg_rows = args.l
    for x in arg_rows:
        specific_rows.append(x)

    # import specific rows from CSV into DataFrame
    df = pandas.read_csv('example.csv', skiprows = lambda x: x not in specific_rows)

    # design the file name  
    args_from_int = map(str, args.l)
    args_to_str = "_".join(args_from_int)
    file_name = f"rows_{args_to_str}.csv"

    # export to the file
    df.to_csv(f'{file_name}')
    print(f"Find the specified rows in {file_name}")

# get specific columns
if args.column:

    # choose specified columns
    specific_columns = df[args.column]

    # design the file name
    args_to_str = "_".join(args.column)
    file_name = f"columns_{args_to_str}.csv"

    # export to the file
    specific_columns.to_csv(f'{file_name}')
    print(f"Find the specified columns in {file_name}")


def make_json(csv_file_path, json_file_path):
    """Function to convert a CSV to JSON
    Takes the file paths as arguments"""

    # create a dictionary
    data = {}

    # open a csv reader called DictReader
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        # convert each row into a dictionary and add it to data
        for rows in csv_reader:

            key = rows['name']
            data[key] = rows

    # open a json writer, and use the json.dumps() function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# convert to json
if args.json:

    my_csv_file_path = r'example.csv'
    my_json_file_path = r'example.json'

    make_json(my_csv_file_path, my_json_file_path)

