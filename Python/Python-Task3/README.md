### The script is parsing any file for specific patterns.

usage: task3a [options]

optional arguments:

  -h, --help            show this help message and exit

  -f F                  -f /path/file_name - takes file to parse

  -ipv4 IPV4 [IPV4 ...]
                        {all|priv|cidr}: 

                        {all} - find all ipv4 in the file, 

                        {priv} - find only private ipv4 address, 

                        {cidr} - find only ipv4 addresses with CIDR notation

  -ipv6 IPV6 [IPV6 ...]
                        {all|priv|cidr}: 
                        
                        {all} - find all ipv6 in the file, 
                        
                        {priv} - find only private ipv6 address, 
                        
                        {cidr} - find only ipv6 addresses with CIDR notation

  -mask                 finds all ip masks

  -mac MAC [MAC ...]    {all|gen|lin|win|cis}: 
  
                        {all} - find all MAC addressses in file, 
                        
                        {gen} - only in format XX:XX:XX:XX:XX:XX, 
                        
                        {lin} - only in format XX-XX-XX-XX-XX-XX, 
                        
                        {win} - only in format XXXXXXXXXXXX, 
                        
                        {cis} - only in format XXXX.XXXX.XXXX

  -domain DOMAIN [DOMAIN ...]
                        {first|second}: 
                        
                        {first} - only TLD, 
                        
                        {second} - first and second DL

  -email EMAIL [EMAIL ...]
                        {all|login|domain}: 
                        
                        {all} - find all email addresses, 
                        
                        {login} - get only logins, 
                        
                        {domain} - get only domains

  -url                  find all URLs

  -ssh SSH [SSH ...]    {priv|pub}: 
  
                        {priv} - only private, 
                        
                        {pub} - only public

  -card                 find all card numbers

  -uuid                 find all UUIDs


## Task 3b

The script for parcing csv files

optional arguments:

  -h, --help            
    show this help message and exit

  -H                    
    open with read_csv, with header

  -N                    
    open with read_csv, without header

  -ipv4_n               
    export all ipv4 + netmasks to file 'export_ipv4_netmask.txt'

  -ipv6                 
    export all ipv6 to file 'export_ipv6.txt'

  -name NAME            
    filter by name value, output to terminal

  -c C                  
    works with -value argument only: -c [column name] -value [value] filter by value in column, output to terminal

  -value VALUE          
    works with -c argument only: -c [column name] -value [value] filter by value in column, output to terminal

  -c2 C2                
    with -c -value and -value2 arguments only: -c [column name] -value [value] -c2 [column name] -value2 [value], filter by values in 2 column, output to terminal

  -value2 VALUE2        
    works with -c -value and -value2 -c2 argument only: -c [column name] -value [value] -c2 [column name] -value2, [value] filter by values in 2 column, output to terminal

  -l L [L ...]          
    gets only named lines by number, any quantity of int arguments starting from 1, output to file

  -column COLUMN [COLUMN ...]  
    gets only named columns, by column name, any quantity of arguments, output to file

  -json                 
    converts file to json