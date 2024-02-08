# m3-Linux-Task1

## Task1
Find all system groups and get only their unique names and ids. Save to file

Commands: 
1. find all system groups: getent group
2. get only names and ids: cut -d: -f1,3
3. save to the file: > task1.txt

**Solution:**

    getent group | cut -d: -f1,3 > task1.txt

## Task2
Find all files and directories that have access rights for the corresponding user and group

**Solution:**
    
    find /path -user username -group groupname

## Task3
Find all scripts in the specified directory and its subdirectories

Commands for main solution: 
1. find all executable files: find /path/to/dig -executable
2. additionaly, we can take previous as input and choose only files with shebang: xargs grep -l '^#!/'

**Solution:**
    
    main solution:
    find /path/to/dig -type f -executable

    OR with shebang:
    find /path/to/dig -type f -executable | xargs grep -l '^#!/'

## Task4
Search for script files from a specific user

**Solution:**

    find /path/to/dig -type f -executable -user username

## Task5
Perform a recursive word or phrase search for a specific file type

**Solution:**
    for example, in .txt files

    find /path -type f -name "*.txt" -exec grep -H "text_to_find" {} +

## Task6
Find duplicate files in specified directories. First, compare by size, then by option (choose a hash function: CRC32, MD5, SHA-1, sha224sum). The result should be sorted by filename

Commands: 
1. find all not empty files: find /path/to/dig ! -empty -type f
2. print files size: -printf "%s\n"
3. Sort numerically (-n), in reverse order (-r): | sort -rn
4. Look for duplicate consecutive rows and keep only those: | uniq -d
5. For each line of input (i.e. each size that occurs more than once), execute the following command, but replace {} by the size: | xargs -I{} -n1
6. Find files in the current directory which match that size, given in characters (c): find -type f -size {}c
7. Print all the matching file names, separated by null bytes instead of newlines so filenames which contain newlines are treated correctly: -print0
8. For each of these null-separated names, compute the MD5 checksum of said file: | xargs -0 md5sum
9. Sort: | sort

**Solution:**

    find /path/to/dig ! -empty -type f -printf "%s\n" | sort -rn | uniq -d | xargs -I{} -n1 find -type f -size {}c -print0 | xargs -0 md5sum | sort

    Only by MD5:
    find /path/to/dig ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD

## Task7
Find all symlinks to a file by file name and path.

**Solution:**

    find /path/to/dig -lname '/path/to/file'

## Task8
Find all hard links to a file by file name and path.

**Solution:**

    find /path/to/dig -samefile /path/to/file

## Task9
There is only the inode of the file to find all its names.

Commands for first option of solution: 
1. find the inode by number: find . -type f -inum <inode-number>
2. execute the stat command for each found file (the -c "%N" option tells the stat command to output the file name): -exec stat -c "%N" {} +

**Solution:**

    #first option, finds regular file type:
    find /path/to/dig -type f -inum <inode-number> -exec stat -c "%N" {} +
    
    #other option, to match any type of file: 
    find /path/to/dig -inum <inode-number>  

## Task10
There is only the inode of the file to find all its names. Note that multiple partitions may be mounted

If use / as path, find command will look though all mounted points

**Solution:**

    find / -inum <inode_number> 

## Task11
Correctly delete the file, taking into account the possibility of the existence of symbolic or hard links

Commands: 
1. find all soft links and delete: find /path/to/dig -lname '/path/to/file' -delete
2. find all hard links and delete: find /path/to/dig -samefile /path/to/file -delete

**Solution:**

    find /path/to/dig -lname '/path/to/file' -delete | find /path/to/dig -samefile /path/to/file -delete

## Task12
Recursively change access rights to files (given file mask) in the given directory

**Solution:**
    
    find /path/to/dig -type f -name "file mask" -exec chmod -R [permissions] {} +
    
    for example, make all .sh files in current directory executable:
    find . -type f -name "*.sh" -exec chmod -R +x {} +

## Task13
* Recursively compare two directories and display only those files that differ. * (output up to the 2nd line and after the 3rd line relative to the line in which the difference is found).

Commands: 
1. compare two directories recursively, output 3 (by default) lines before and after difference: diff -r -c dir1 dir2
2. grep 2 lines before and 3 lines after difference: grep -B 2 -A 3 '!' 

**Solution:**

    diff -r -c task13 task13_copy | grep -B 2 -A 3 '!' 

## Task14
Get MAC addresses of network interfaces

**Solution:**

    ip link

## Task15
Display the list of users currently authorized in the system

**Solution:**

    who

    w

## Task16
Display a list of active network connections in the form of a table: the type of connection status and their number

Commands:
1. show all active connections: ss -nat / netstat -nat
2. find lines and calculate: grep -c LISTEN
3. output result: xargs -I {} echo "LISTEN: {}"

**Solution:**

    usig ss:
    ss -nat | grep -c LISTEN | xargs -I {} echo "LISTEN: {}" && ss -nat | grep -c ESTAB | xargs -I {} echo "ESTAB: {}" && ss -nat | grep -c TIME_WAIT | xargs -I {} echo "TIME_WAIT: {}"

    using netstat:
    netstat -nat | grep -c LISTEN | xargs -I {} echo "LISTEN: {}" && netstat -nat | grep -c ESTABLISHED | xargs -I {} echo "ESTABLISH: {}" && netstat -nat | grep -c TIME_WAIT | xargs -I {} echo "TIME_WAIT: {}"

## Task17
Reassign an existing symbolic link.

**Solution:**

    ln -sf /path/to/existing/slink /path/to/new/slink

## Task18
There is a list of files with a relative path and a path to the directory in which the symbolic link to the file should be stored. Create symbolic links to these files

Commands: 
1. cat the file with files list: cat file_list 
2. read line by line split each line into two fields - file and path_to_dir: while read -r file path_to_dir
3. make symbolic link after reading each line: do ln -s "$file" "$path_to_dir"; done

**Solution:**

    cat file_list | while read -r file path_to_dir; do ln -s "$file" "$path_to_dir"; done

## Task19
Copy the directory, taking into account that it contains both direct and relative symbolic links to files and directories. It is assumed that copying is performed for backup on a removable storage. (do it in two versions, without rsync and with rsync)

Commands: 
1. cp command with -R - recursive and -L - follow symbolic links and copy the target of each link instead of the link itself
2. rsync command with -a which enables recursive copying and -L to follow symbolic links and copy the target of each link

**Solution:**

    with cp:
    cp -RL source_dir destination_dir
    
    with rsync:
    rsync -aL source_dir/ destination_dir

## Task20
Copy the directory, taking into account that there are direct symbolic relative symbolic links in it

Commands: 
1. cp command with -R - recursive and -P - preserves the symbolic links as symbolic links, without following them

**Solution:**

    cp -RP source_dir destination_dir

## Task21
Copy all files and directories from the specified directory to the new location, preserving attributes and rights

Commands: 
1. cp command with -a enables archive mode, which ensures recursive copying of all files and subdirectories from the specified directory to the destination directory while preserving attributes and permissions

**Solution:**

    cp -a source_directory destination_directory

## Task22
In the project directory, convert all relative links to direct links.

Commands: 
1. search for all symbolic links within the project directory: find /path/to/project -type l
2. print their paths separated by null characters: -print0
3. read each null-separated link path: while read -r -d '' link; do ... done
4. create a symbolic link with the -f option (to replace existing links) and the target path obtained from readlink -f "$link". Replace the existing symbolic link "$link" with a new one that has an absolute path target: ln -sf "$(readlink -f "$link")" "$link"

**Solution:**

    find /path/to/project -type l -print0 | while read -r -d '' link; do ln -sf "$(readlink -f "$link")" "$link"; done

## Task23
In the project directory, convert all direct links to relative, relative to the project directory.

Commands: 
1. -3. same as in previous task
4. assigns the target and directory path of the symbolic link to the variables: target=$(readlink "$link"), target_dir=$(dirname "$link"), 
5. compute the relative path from the symbolic link's directory to its target: relative_path=$(realpath --relative-to="$target_dir" "$target")
6. create a relative symbolic link using the ln command. The -s option indicates it's a symbolic link, the -f option replaces existing links, and the -n option avoids dereferencing the target if it's a symbolic link: ln -sfn

**Solution:**

    find /path/to/project -type l -print0 | while read -r -d '' link; do target=$(readlink "$link"); target_dir=$(dirname "$link"); relative_path=$(realpath --relative-to="$target_dir" "$target"); ln -sfn "$relative_path" "$link"; done

## Task24
Find all broken links in the specified directory and delete them

Commands: 
1. find all symbolic links: find /path/to/dig -type l
2. check if link exists and print its /path/to/file if the link does not exist: ! -exec test -e {} \; -print
3. pass /path/to/file to while loop: while read -r link; 
4. delete the file: do rm "$link"; done

**Solution:**

    find /path/to/dig -type l ! -exec test -e {} \; -print | while read -r link; do rm "$link"; done

## Task25
Extract a specific directory/file from the tar, gz, bz2, lz, lzma, xz, Z archive to the specified location.

**Solution:**

    tar -xf /path/to/archive.tar -C /path/to/target/dir
    
    tar -xzf /path/to/archive.gz -C /path/to/target/dir

    tar -xjf /path/to/archive.bz2 -C /path/to/target/dir

    tar --lzip -xf /path/to/archive.lz -C /path/to/target/dir

    tar --lzma -xf /path/to/archive.lzma -C /path/to/target/dir

    tar -xJf /path/to/archive.xz -C /path/to/target/dir

    tar -xZf /path/to/archive.Z -C /path/to/target/dir

## Task26
Pack the directory structure with files while preserving all rights and attributes

Commands: 
1. tar command with -p flag to preserve rights and attributes

**Solution:**

    tar -cpf file.tar /path/to/directory

## Task27
Recursively copy the directory structure from the specified directory. (without files)

Commands: 
1. go to source directory you need to copy
2. find all directories: find . -type d
3. to execute command for each found item use -exec ... \;
4. create directories, including parent directories. The -p option ensures that the command does not produce an error if the directory already exists: mkdir -p

**Solution:**

    cd /path/to/sourece/dir && find . -type d -exec mkdir -p /path/to/destination/{} \;

## Task28
List all system users (names only) alphabetically

Commands: 
1. from /etc/passwd cut with deliminator ":", take first field: cut -d: -f1
2. sort

**Solution:**

    cut -d: -f1 /etc/passwd | sort

## Task29
Display a list of all system users of the system sorted by id, in the format: login id

Commands: 
1. from /etc/passwd cut with deliminator ":", take first and third field: cut -d: -f1,3
2. exclude non-system users (ids with values 1000+): grep ':[0-9]\{1,3\}$'
3. sort numeric by second field, using ":" as the delimiter: sort -n -t: -k2

**Solution:**

    cut -d: -f1,3 /etc/passwd | grep ':[0-9]\{1,3\}$' | sort -n -t: -k2

## Task30
List all system users (names only) sorted by id in reverse order

Commands: 
1. from /etc/passwd cut with deliminator ":", take first and third field: cut -d: -f1,3
2. sort numeric reverse by second field, using ":" as the delimiter: sort -n -t: -k2
3. cut only first field: cut -d: -f1

**Solution:**

    cut -d: -f1,3 /etc/passwd | sort -nr -t: -k2 | cut -d: -f1

## Task31
Remove all users who do not have the right to log in or do not have the right to log in to the system. (two commands)

**Solution:**

    grep 'nologin' /etc/passwd | cut -d: -f1

    grep 'false' /etc/passwd | cut -d: -f1

## Task32
Display all users who (have/do not have) a terminal (bash, sh, zsh and etc, which are installed on the system) (two commands)

Commands: 
1. find all in /etc/passwd with grep, -f option to read the patterns from the output of the command inside <(command)
2. while loop that reads each line (shell) from the output of grep: while read -r shell; do echo "$shell\$"; done | cat /etc/shells
3. combine the modified login shells from step 2 with the contents of /etc/shells
4. cut first field

**Solution:**

    with shell:
    grep -f <(while read -r shell; do echo "$shell\$"; done | cat /etc/shells) /etc/passwd | cut -d: -f1 

    without shell:
    grep -v -f <(while read -r shell; do echo "$shell\$"; done | cat /etc/shells) /etc/passwd | cut -d: -f1 

## Task33
Download all links to href resources on the page from the Internet. Use curl or wget (make both options). Download in parallel. 

Commands: 
1. make request to site without displaying progress meter, but show error if it fails: curl -sS
2. get only href with grep, only matched parts, extended regexp: grep -oE 'href="([^"]+)"'
3. extract the URLs from the href links: cut -d'"' -f2
4. take links as input with xargs, do it in parallel (-P 0) and download links with wget: xargs -P 0 wget

**Solution:**

    curl -s "URLaddressishere" | grep -oE 'href="([^"]+)"'| cut -d'"' -f2 | xargs -P 0 wget

## Task34
Stop processes that have been running for more than 5 days. a) use killall; b) do not use the ps / killall command.

Commands for option b: 
1. list the elapsed time and process ID of running processes in Linux: ps -eoetime=,pid= 
2. get only those running more than 5 days: grep -E '(0[5-9]|[1-9][0-9])-[0-9]{2}:[0-9]{2}:[0-9]{2}'
3. cut process id: cut -d' ' -f2 
4. kill all from the input: xargs -I{} kill {}

**Solution:**
    a:
    killall --older-than 5d

    b:
    ps -eoetime=,pid= | grep -E '(0[5-9]|[1-9][0-9])-[0-9]{2}:[0-9]{2}:[0-9]{2}' | cut -d' ' -f2 | xargs -I{} kill {}

## Task35
There is a directory in which folders and files (*.txt & *.jpeg) exist. The *.txt and *.jpeg files are uniquely linked by the name prefix. The files can be in different places in this directory. You need to delete all *.jpegs for which there is no *.txt file.

Commands: 
1. find all find all .jpg and .txt names: find . -type f \( -name "*.txt" -o -name "*.jpg" \) -exec basename {} \;
2. take only name before .: grep -o '^[^.]*'
3. sort and leave only names that is listed once: sort | uniq -u
4. find all .jpg names with path from the input and delete: xargs -I{}find . -type f -name "{}.jpg" -delete

**Solution:**

    find . -type f \( -name "*.txt" -o -name "*.jpg" \) -exec basename {} \; | grep -o '^[^.]*' | sort | uniq -u | xargs -I{}find . -type f -name "{}.jpg" -delete

## Task36
Find your IP address using the command line 

**Solution:**
    local IP:
    hostname -I 

    external IP:
    curl -s https://ipinfo.io/ip

## Task37
Get all ip addresses from a text file

**Solution:**

    grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' filename.txt

## Task38
Find all active hosts in: - given network, - IP list (hosts-server.txt) using/not using nMAP;

Commands: 
1. nmap: -sn serforms a ping scan (ICMP echo request) to determine host availability, -iL specifies that the input for scanning should be read from a file
2. without nmap: using ping -c 1 (single echo request)

**Solution:**

    nmap -sn 192.168.1.0/24

    nmap -sn -iL hosts-server.txt

    without nmap:

    for i in {1..255}; do ping -c 1 192.168.1.$i | grep "bytes from"; done

    xargs -I {} ping -c 1 {} < hosts-server.txt | grep "bytes from"

## Task39
Using the result of task 38, get the IP of the raised interfaces

**Solution:**

    nmap -sn 192.168.1.0/24 | grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'

## Task40
Get all subdomains with SSL certificate.

##### any site that supports SSL: connect, get certificates (it will list all domains), issue a list of all domains

Commands: 
1. connect to the specified domain on port 443: openssl s_client -connect example.com:443
2. redirect any error output to null to avoid cluttering the output: 2>/dev/null
3. output the textual representation of the SSL certificate: openssl x509 -noout -text
4. filter out only the lines that contain subdomains (DNS): grep "DNS:"

**Solution:**

    echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -text | grep "DNS:"

## Task41
Extract the path, name and extension of a file in Bash from a string. (three teams)

**Solution:**
    get path:
    dirname "/path/to/file/file.txt"

    get name:
    basename "/path/to/file/file.txt"

    get extention:
    basename "/path/to/file/file.txt" | grep -o '\.[^.]*$'


## Task42
How to remove files of specified length and name pattern from the corresponding directory? (Subdirectories can also exist)

**Solution:**
    for all .txt files more than 10k:
    find /path/to/directory -type f -name "*.txt" -size +10k -delete

## Task43
There is a file in which there are 2 columns separated by a space: the name of the file and the identifier in the form of a hash value (4 bytes). Create all files and write the corresponding identifiers to them.

Commands: 
1. read the file by lines and split line into fields "file_name" and "hash" usig space as delimiter (IFS=' '): while IFS=' ' read -r file_name hash; do ...; done
2. write "hash" to "file_name": echo "$hash" > "$file_name"

**Solution:**

    while IFS=' ' read -r file_name hash; do echo "$hash" > "$file_name"; done < /path/to/file


