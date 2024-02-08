### password generator that takes several arguments for different password configurations

usage: password generator [options]

optional arguments:

  -h, --help  
    show this help message and exit

  -n N        [int]
    set the length of password. If no character set (-S) is given, generate random password from set {small lateral ASCII, big lateral ASCII, digit}

  -S S        [str] 
    character set to generate random password from

  -t T        [str] 
    set template for generate passwords

  -f F        [path to the file] 
    getting list of patterns from file and generate for each random password

  -c C        [int] 
    number of passwords

  -v          
    verbose mode-1

  -vv         
    verbose mode-2

  -vvv        
    verbose mode-3