# m3-Linux-Task1

## Task1
Знайти всі системні групи й отримати тільки їхні унікальні імена та id. Зберегти у файл

Commands: 
1. find all system groups: getent group
2. get only names and ids: cut -d: -f1,3
3. save to the file: > task1.txt

**Solution:**

    getent group | cut -d: -f1,3 > task1.txt

## Task2
Знайти всі файли і директорії, які мають права для доступу відповідних user і group

**Solution:**
    
    find /path -user username -group groupname

## Task3
Знайти всі скрипти в зазначеній директорії та її піддиректоріях

Commands for main solution: 
1. find all executable files: find /path/to/dig -executable
2. additionaly, we can take previous as input and choose only files with shebang: xargs grep -l '^#!/'

**Solution:**
    
    main solution:
    find /path/to/dig -type f -executable

    OR with shebang:
    find /path/to/dig -type f -executable | xargs grep -l '^#!/'

## Task4
Виконати пошук файлів скриптів з-під певного користувача

**Solution:**

    find /path/to/dig -type f -executable -user username

## Task5
Виконати рекурсивний пошук слів або фрази для певного типу файлів

**Solution:**
    for example, in .txt files

    find /path -type f -name "*.txt" -exec grep -H "text_to_find" {} +

## Task6
Знайти дублікати файлів у заданих каталогах. Спочатку порівнювати за розміром, потім за варіантом (вибрати хеш функцію: CRC32, MD5, SHA-1, sha224sum). Результат має бути відсортований за ім'ям файлу

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
Знайти за іменем файлу та його шляхом усі символьні посилання на нього.

**Solution:**

    find /path/to/dig -lname '/path/to/file'

## Task8
Знайти за іменем файлу та його шляхом усі жорсткі посилання на нього.

**Solution:**

    find /path/to/dig -samefile /path/to/file

## Task9
Є тільки inode файлу знайти всі його імена.

Commands for first option of solution: 
1. find the inode by number: find . -type f -inum <inode-number>
2. execute the stat command for each found file (the -c "%N" option tells the stat command to output the file name): -exec stat -c "%N" {} +

**Solution:**

    #first option, finds regular file type:
    find /path/to/dig -type f -inum <inode-number> -exec stat -c "%N" {} +
    
    #other option, to match any type of file: 
    find /path/to/dig -inum <inode-number>  

## Task10
Є тільки inode файлу знайти всі його імена. Врахуйте, що може бути примонтовано кілька розділів 

If use / as path, find command will look though all mounted points

**Solution:**

    find / -inum <inode_number> 

## Task11
Коректно видалити файл з урахуванням можливості існування символьних або жорстких посилань

Commands: 
1. find all soft links and delete: find /path/to/dig -lname '/path/to/file' -delete
2. find all hard links and delete: find /path/to/dig -samefile /path/to/file -delete

**Solution:**

    find /path/to/dig -lname '/path/to/file' -delete | find /path/to/dig -samefile /path/to/file -delete

## Task12
Рекурсивно змінити права доступу до файлів (задано маску файлу) у заданій директорії

**Solution:**
    
    find /path/to/dig -type f -name "file mask" -exec chmod -R [permissions] {} +
    
    for example, make all .sh files in current directory executable:
    find . -type f -name "*.sh" -exec chmod -R +x {} +

## Task13
* Порівняти рекурсивно дві директорії і відобразити тільки ті файли, що відрізняються. * (вивести до 2 рядка і після 3 рядка відносно рядка, в якому знайдено відмінність).

Commands: 
1. compare two directories recursively, output 3 (by default) lines before and after difference: diff -r -c dir1 dir2
2. grep 2 lines before and 3 lines after difference: grep -B 2 -A 3 '!' 

**Solution:**

    diff -r -c task13 task13_copy | grep -B 2 -A 3 '!' 

## Task14
Отримати MAC-адреси мережевих інтерфейсів

**Solution:**

    ip link

## Task15
Вивести список користувачів, авторизованих у системі на поточний момент

**Solution:**

    who

    w

## Task16
Вивести список активних мережевих з'єднань у вигляді таблиці: тип стану з'єднання та їх кількість

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
Перепризначити наявне символьне посилання.

**Solution:**

    ln -sf /path/to/existing/slink /path/to/new/slink

## Task18
Є список фалів з відносним шляхом і шляхом до каталогу, в якому має зберігатися символьне посилання на файл. Створити символьні посилання на ці файли

Commands: 
1. cat the file with files list: cat file_list 
2. read line by line split each line into two fields - file and path_to_dir: while read -r file path_to_dir
3. make symbolic link after reading each line: do ln -s "$file" "$path_to_dir"; done

**Solution:**

    cat file_list | while read -r file path_to_dir; do ln -s "$file" "$path_to_dir"; done

## Task19
Скопіювати директорію з урахуванням, що в ній існують як прямі, так відносні символьні посилання на файли та директорії. Передбачається, що копіювання виконується for backup on a removable storage. (зробити в двох варіантах, без rsync і з rsync)

Commands: 
1. cp command with -R - recursive and -L - follow symbolic links and copy the target of each link instead of the link itself
2. rsync command with -a which enables recursive copying and -L to follow symbolic links and copy the target of each link

**Solution:**

    with cp:
    cp -RL source_dir destination_dir
    
    with rsync:
    rsync -aL source_dir/ destination_dir

## Task20
Скопіювати директорію з урахуванням, що в ній існують прямі символьні відносні символьні посилання

Commands: 
1. cp command with -R - recursive and -P - preserves the symbolic links as symbolic links, without following them

**Solution:**

    cp -RP source_dir destination_dir

## Task21
Скопіювати всі файли та директорії із зазначеної директорії в нове розташування зі збереженням атрибутів і прав

Commands: 
1. cp command with -a enables archive mode, which ensures recursive copying of all files and subdirectories from the specified directory to the destination directory while preserving attributes and permissions

**Solution:**

    cp -a source_directory destination_directory

## Task22
У директорії проекту перетворити всі відносні посилання на прямі.

Commands: 
1. search for all symbolic links within the project directory: find /path/to/project -type l
2. print their paths separated by null characters: -print0
3. read each null-separated link path: while read -r -d '' link; do ... done
4. create a symbolic link with the -f option (to replace existing links) and the target path obtained from readlink -f "$link". Replace the existing symbolic link "$link" with a new one that has an absolute path target: ln -sf "$(readlink -f "$link")" "$link"

**Solution:**

    find /path/to/project -type l -print0 | while read -r -d '' link; do ln -sf "$(readlink -f "$link")" "$link"; done

## Task23
У директорії проекту перетворити всі прямі посилання у відносні, відносно директорії проекту.

Commands: 
1. -3. same as in previous task
4. assigns the target and directory path of the symbolic link to the variables: target=$(readlink "$link"), target_dir=$(dirname "$link"), 
5. compute the relative path from the symbolic link's directory to its target: relative_path=$(realpath --relative-to="$target_dir" "$target")
6. create a relative symbolic link using the ln command. The -s option indicates it's a symbolic link, the -f option replaces existing links, and the -n option avoids dereferencing the target if it's a symbolic link: ln -sfn

**Solution:**

    find /path/to/project -type l -print0 | while read -r -d '' link; do target=$(readlink "$link"); target_dir=$(dirname "$link"); relative_path=$(realpath --relative-to="$target_dir" "$target"); ln -sfn "$relative_path" "$link"; done

## Task24
У зазначеній директорії знайти всі зламані посилання і видалити їх

Commands: 
1. find all symbolic links: find /path/to/dig -type l
2. check if link exists and print its /path/to/file if the link does not exist: ! -exec test -e {} \; -print
3. pass /path/to/file to while loop: while read -r link; 
4. delete the file: do rm "$link"; done

**Solution:**

    find /path/to/dig -type l ! -exec test -e {} \; -print | while read -r link; do rm "$link"; done

## Task25
Розпакувати з архіву tar, gz, bz2, lz, lzma, xz, Z певний каталог/файл у вказане місце.

**Solution:**

    tar -xf /path/to/archive.tar -C /path/to/target/dir
    
    tar -xzf /path/to/archive.gz -C /path/to/target/dir

    tar -xjf /path/to/archive.bz2 -C /path/to/target/dir

    tar --lzip -xf /path/to/archive.lz -C /path/to/target/dir

    tar --lzma -xf /path/to/archive.lzma -C /path/to/target/dir

    tar -xJf /path/to/archive.xz -C /path/to/target/dir

    tar -xZf /path/to/archive.Z -C /path/to/target/dir

## Task26
Упакувати структуру директорію з файлами зі збереженням усіх прав і атрибутів

Commands: 
1. tar command with -p flag to preserve rights and attributes

**Solution:**

    tar -cpf file.tar /path/to/directory

## Task27
Рекурсивно скопіювати структуру каталогів із зазначеної директорії. (без файлів)

Commands: 
1. go to source directory you need to copy
2. find all directories: find . -type d
3. to execute command for each found item use -exec ... \;
4. create directories, including parent directories. The -p option ensures that the command does not produce an error if the directory already exists: mkdir -p

**Solution:**

    cd /path/to/sourece/dir && find . -type d -exec mkdir -p /path/to/destination/{} \;

## Task28
Вивести список усіх користувачів системи (тільки імена) за алфавітом

Commands: 
1. from /etc/passwd cut with deliminator ":", take first field: cut -d: -f1
2. sort

**Solution:**

    cut -d: -f1 /etc/passwd | sort

## Task29
Вивести список усіх системних користувачів системи відсортованих за id, у форматі: login id

Commands: 
1. from /etc/passwd cut with deliminator ":", take first and third field: cut -d: -f1,3
2. exclude non-system users (ids with values 1000+): grep ':[0-9]\{1,3\}$'
3. sort numeric by second field, using ":" as the delimiter: sort -n -t: -k2

**Solution:**

    cut -d: -f1,3 /etc/passwd | grep ':[0-9]\{1,3\}$' | sort -n -t: -k2

## Task30
Вивести список усіх користувачів системи (тільки імена) відсортовані за id у зворотному порядку

Commands: 
1. from /etc/passwd cut with deliminator ":", take first and third field: cut -d: -f1,3
2. sort numeric reverse by second field, using ":" as the delimiter: sort -n -t: -k2
3. cut only first field: cut -d: -f1

**Solution:**

    cut -d: -f1,3 /etc/passwd | sort -nr -t: -k2 | cut -d: -f1

## Task31
Вивести всіх користувачів, які не мають права авторизовуватися або не мають права авторизовуватися в системі. (дві команди)

**Solution:**

    grep 'nologin' /etc/passwd | cut -d: -f1

    grep 'false' /etc/passwd | cut -d: -f1

## Task32
Вивести всіх користувачів, які (мають/не мають) терміналу (bash, sh, zsh and etc, which are installed on the system) (дві команди)

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
Зі сторінки з інтернету закачати всі посилання на ресурси href, які на сторінці. a) Використовувати curl або wget (зробити обидва варіанти). Закачувати паралельно.  b) Дати рекомендації щодо використання. 

Commands: 
1. make request to site without displaying progress meter, but show error if it fails: curl -sS
2. get only href with grep, only matched parts, extended regexp: grep -oE 'href="([^"]+)"'
3. extract the URLs from the href links: cut -d'"' -f2
4. take links as input with xargs, do it in parallel (-P 0) and download links with wget: xargs -P 0 wget

**Solution:**

    curl -s "URLaddressishere" | grep -oE 'href="([^"]+)"'| cut -d'"' -f2 | xargs -P 0 wget

## Task34
Зупинити процеси, які працюють понад 5 днів.  a) використовувати killall; b) команду ps / killall не використовувати. 

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
Є директорія, в якій існують папки та файли (*.txt & *.jpeg). Файли *.txt і *.jpeg однозначно пов'язані між собою за префіксом імені. Файли можуть перебувати в різному місці цієї директорії. Потрібно видалити всі *.jpeg для яких не існує файлу *.txt. 

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
Отримати всі ip-адреси з текстового файлу 

**Solution:**

    grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' filename.txt

## Task38
Знайти всі активні хости в: - заданій мережі,  - списку IP (hosts-server.txt) використовуючи/не використовуючи nMAP; 

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
Використовуючи результат таска 36 (as I understood, it meant task 38 results). Отримати ip піднятих інтерфейсів

**Solution:**

    nmap -sn 192.168.1.0/24 | grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'

## Task40
Отримати всі піддомени з SSL сертифіката. 

##### будь який сайт що підтримує SSL: підключитися, отримати сертифікати (в ньому будуть перераховані усі домени), видати список усіх доменів

Commands: 
1. connect to the specified domain on port 443: openssl s_client -connect example.com:443
2. redirect any error output to null to avoid cluttering the output: 2>/dev/null
3. output the textual representation of the SSL certificate: openssl x509 -noout -text
4. filter out only the lines that contain subdomains (DNS): grep "DNS:"

**Solution:**

    echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -text | grep "DNS:"

## Task41
Витягти шлях, ім'я та розширення файлу в Bash зі строки. (трикоманди)

**Solution:**
    get path:
    dirname "/path/to/file/file.txt"

    get name:
    basename "/path/to/file/file.txt"

    get extention:
    basename "/path/to/file/file.txt" | grep -o '\.[^.]*$'


## Task42
Як видалити файли вказаної довжини та шаблону імені з відповідного каталогу? (Підкаталоги також можуть існувати)

**Solution:**
    for all .txt files more than 10k:
    find /path/to/directory -type f -name "*.txt" -size +10k -delete

## Task43
Є файл в якому існує 2 стовпчика, що розділені пробілом: ім’я файлу та ідентифікатор у вигляді хеш-значення (4 байта). Створити усі файли та записати до них відповідні ідентифікатори. 

Commands: 
1. read the file by lines and split line into fields "file_name" and "hash" usig space as delimiter (IFS=' '): while IFS=' ' read -r file_name hash; do ...; done
2. write "hash" to "file_name": echo "$hash" > "$file_name"

**Solution:**

    while IFS=' ' read -r file_name hash; do echo "$hash" > "$file_name"; done < /path/to/file


