"""modules for import"""
import argparse
import random
import ast
import string
import re
import sys
import logging
from logging import StreamHandler, Formatter

parser = argparse.ArgumentParser(
    prog="password generator", usage='%(prog)s [options]')

parser.add_argument("-n", type=int, help="""[int] set the length of password.
                    If no character set (-S) is given, generate
                    random password from set
                    {small lateral ASCII, big lateral ASCII, digit}""")
parser.add_argument("-S", type=str,
                    help="""[str] character set
                    to generate random password from""")
parser.add_argument("-t", type=str,
                    help="[str] set template for generate passwords")
parser.add_argument("-f", type=str,
                    help="""[path to the file] getting list of patterns
                    from file and generate for each random password""")
parser.add_argument("-c", type=int, help="[int] number of passwords")
parser.add_argument("-v", default=False, action="store_true",
                    help="verbose mode-1")
parser.add_argument("-vv", default=False, action="store_true",
                    help="verbose mode-2")
parser.add_argument("-vvv", default=False, action="store_true",
                    help="verbose mode-3")

args = parser.parse_args()

# logging level
if args.v:
    LOG_LEVEL = "ERROR"
elif args.vv:
    LOG_LEVEL = "WARNING"
elif args.vvv:
    LOG_LEVEL = "INFO"
else:
    LOG_LEVEL = "CRITICAL"

# logging initialization
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

logger.info("task2 started")


def check_string(text):
    """function to check string for unicode characters"""

    # define the regex pattern
    regex_pattern = re.compile(r'[\u0001-\uD7FF\uE000-\uFFFF]')
    # characters to exclude
    excluded_characters = ['\u0009', '\u000A', '\u000D']
    # find all matches in the string
    matches = regex_pattern.findall(text)
    # exclude specific characters
    matches = [match for match in matches if match not in excluded_characters]

    # check if matches was found
    if len(matches) > 0:
        pass
    else:
        print("Some characters you used are not allowed. Please, try again")
        logger.warning("not allowed characters were used")
        sys.exit()


def n_s_argument():
    """function for -n and -S arguments"""

    if not args.S:

        # rand passwd from set {small lateral ASCII, big lateral ASCII, digit}
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password_n = ''.join(random.choice(chars) for i in range(args.n))

        print(password_n)
        logger.info("""random password from set
                   {small lateral ASCII, big lateral ASCII, digit}
                   has been generated""")

    else:
        # check string for unicode characters
        check_string(args.S)

        # random password from characters set in -S argument
        line = "".join(set(args.S))  # remove duplicate characters
        password_s = ''.join(random.choice(line) for i in range(args.n))

        print(password_s)
        logger.info("random password from the -S characters set is generated")


# functions for -t argument

def multiply_previous_character(text):
    """find number in curly brackets
    and multiply previous character by this number"""

    # find numbers in {}
    pattern = r"([^]]\{[^}]*\})"
    matches = re.findall(pattern, text)

    # find previous char and * by number from {}
    for match in matches:
        preceding_char = match[0]
        number = int(match[2:-1])
        new_char = preceding_char * number
        text = text.replace(match, new_char)
    return text


def generate_from_set(template):
    """generate random characters from set"""

    password = ''
    i = 0
    # itterate though template just once
    while i < len(template):
        # find text between [] and add to password string
        if template[i] == '[':
            j = template.find(']', i)
            if j == -1:
                raise ValueError('Invalid template: missing closing bracket')
            options = template[i+1:j]
            option_list = ast.literal_eval(options)
            # check if there's {} after []
            if '{' in template[j+1:]:
                k = template.find('}', j+1)
                if k == -1:
                    raise ValueError(
                        'Invalid template: missing closing curly bracket')
                repeat_count = int(template[j+2:k])
                for _ in range(repeat_count):
                    password += random.choice(option_list)
                i = k + 1
            else:
                password += random.choice(option_list)
                i = j + 1
        else:
            password += template[i]
            i += 1
    return password


def remove_next_char(text):
    """remove character after ^"""

    pattern = r"(\^.)"
    matches = re.findall(pattern, text)

    for match in matches:
        text = text.replace(match, "")
    return text


def t_argument(argument):
    """function for t argument - generate random password from template"""

    # remove haracter after ^
    argument = remove_next_char(argument)

    # multiply prev char by number from {}
    argument = multiply_previous_character(argument)

    # custom char sets to string conversion
    pattern = r"(\[[^]]*\])"
    matches = re.findall(pattern, argument)  # find the sets in []

    # transform set to needed list (random choice, n times)
    # and replace in argument string
    for match in matches:
        char_list = []
        i = 0
        while i < len(match):
            if match[i] == '\\' and i + 1 < len(match):
                char_list.append(match[i] + match[i+1])
                i += 2
            else:
                char_list.append(match[i])
                i += 1

        str_a = f"{char_list[1:-1]}"
        argument = re.sub(re.escape(match), str_a, argument, count=1)

    # generate random string from list
    argument = generate_from_set(argument)

    # Replace placeholders
    result = ""

    i = 0
    while i < len(argument):
        char = argument[i]
        if char == "\\" and i < len(argument) - 1:
            result += char + argument[i+1]
            i += 1
        elif char == "d":
            random_num = str(random.randint(0, 9))
            result += random_num
        elif char == "l":
            random_low_letter = random.choice(string.ascii_lowercase)
            result += random_low_letter
        elif char == "L":
            random_any_letter = random.choice(string.ascii_letters)
            result += random_any_letter
        elif char == "u":
            random_up_letter = random.choice(string.ascii_uppercase)
            result += random_up_letter
        elif char == "p":
            sign_set = [',', '.', ';', ':']
            random_set = random.choice(sign_set)
            result += random_set
        else:
            result += char

        i += 1

    # delete extra backslashes
    for i in result:
        result = re.sub(r'(?<!\\)\\', "", result)
        break

    print(result)


def f_argument():
    """function for -f argument"""

    with open(args.f, encoding="utf-8") as f:
        file = f.read()
        t_argument(file)


if args.n:

    if args.n < 0:
        logger.error("you can not use negative integers or 0")

    n_s_argument()

if args.S and not args.n:

    print("please, add -n [int] to set the lengh of password")
    logger.warning("-S option without -n option were initialized")

if args.t:

    t_argument(args.t)
    logger.info("random password from the -t template was generated")

if args.f:

    f_argument()
    logger.info("random password(s) from the -f file templates was generated")

if args.c:

    if args.c < 0:
        logger.error("you can not use negative integers or 0")

    pass_quant = args.c

    if args.t:
        for x in range(pass_quant-1):
            t_argument(args.t)
    elif args.n:
        for x in range(pass_quant-1):
            n_s_argument()
    elif args.f:
        for x in range(pass_quant-1):
            f_argument()
    else:
        print("""-c defines only the quantity of passwords. \n
              Please, use one of the arguments [-t|-f|-n|-S -n]
              to define the password type""")

    logger.info('%d more same password sets were generated', args.c-1)

logger.info("task2 is finished")
