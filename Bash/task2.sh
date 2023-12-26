#!/bin/bash

# Check if the script is executed with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

if [ $# -eq 0 ]; then
  echo "Please, provide email address as an argument. If you don't need to send email use argument [no]"
  exit 1
fi

# Function to generate a random username
generate_username() {
    random_number=$(shuf -i 1000-9999 -n 1)
    echo "iptables_user_$random_number"
}

# Function to generate a random password
generate_password() {
    password=$(head /dev/urandom | tr -dc 'A-Za-z0-9!@#$%^&*_+-' | fold -w 10 | head -n 1)
    echo "$password"
}

# Function to check if the password meets the policies
is_password_strong() {
    local password=$1
    if [[ ${#password} -lt 8 ]]; then
        return 1
    fi
    if [[ !($password =~ [[:lower:]]) ]]; then
        return 1
    fi
    if [[ !($password =~ [[:upper:]]) ]]; then
        return 1
    fi
    if [[ !($password =~ [[:digit:]]) ]]; then
        return 1
    fi
    if [[ !($password =~ [[:punct:]]) ]]; then
        return 1
    fi
    return 0
}

# Configure the password policy requirements
configure_password_policy() {
    # Install the libpam-pwquality package
    apt-get install -y libpam-pwquality

    # Configure the password policy requirements
    pwquality_conf="/etc/security/pwquality.conf"

    # Enable password policy checks in the common-password file
    common_password="/etc/pam.d/common-password"
    pam_pwquality_line="password  required pam_pwquality.so \
    retry=4 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1 minlen=8 enforce_for_root"

    if grep -q "$pam_pwquality_line" $common_password; then
        echo "Password policy enforcement already configured."
    else
        echo "$pam_pwquality_line" >> $common_password
        sed  -i '/pam_unix.so/ipassword required pam_pwhistory.so remember=3' $common_password
        echo "Password policy enforcement configured."
    fi
}

configure_password_policy

# Generate a username iptables_user_xxxx
username=$(generate_username)

# Check if the username already exists
while id -u $username >/dev/null 2>&1; do
    username=$(generate_username)
done

# Generate a random password
password=$(generate_password)

# Check if the password meets the policies
while ! is_password_strong "$password"; do
    password=$(generate_password)
done

# Create the user with the random username
useradd -m -s /bin/bash $username

# Set the password for the user
echo "$username:$password" | chpasswd

# Print user creation success message
echo "User '$username' has been created with a random password"

# Force the user to change the password upon first login
chage -d 0 $username

# success message
echo "User '$username' will be forced to change the password upun first longin"

# Set password expiration policies
chage -M 90 -m 0 -W 7 $username

# success message
echo "Password set by User '$username' will expire in 90 days"

# Deny executing 'sudo su -' and 'sudo -s'
echo -e "Cmnd_Alias DENY_SHELL_CMNDS = /bin/su -, /bin/su -s\n%$username ALL=(ALL:ALL) !DENY_SHELL_CMNDS" > /etc/sudoers.d/iptables_user

# Prevent accidental removal of /var/log/auth.log
chattr +a /var/log/auth.log

# Add user access to iptables in sudoers file
echo "$username ALL=(root) NOPASSWD: /usr/sbin/iptables" >> /etc/sudoers

# Print success message
echo "User '$username' has been granted access to iptables"

# Create alias for iptables command
echo "alias iptables='sudo iptables'" >> /home/$username/.bashrc

# Print success message
echo "User '$username' has been granted alias to access to iptables without printing sudo"

# Grant read access to /var/log/syslog
chmod +r /var/log/syslog
chown $username:$username /var/log/syslog

# Print success message
echo "User '$username' has been granted read access to /var/log/syslog"

# Print user creation details
echo "The user will be required to change the password upon first login."
echo "The password should be at least 8 characters long and include: upper letter, lower letter, digit and special char"
echo "Generated Username: $username"
echo "Generated Password: $password"

# Send mail
mail_receiver=$1
mail_message="The user $username was created with password $password.
The user will be required to change the password upon first login.
The password should be at least 8 characters long and include: upper letter, lower letter, digit and special char
The password should be changed every 3 months, it is not allowed to repeat 3 last passwords
The user can execute ‘iptables’ with any command line arguments, no need to type sudo
The user was granted read access to /var/log/syslog without using sudo
The user can not executing 'sudo su -' and 'sudo -s'
Accidental removal of /var/log/auth.log is prevented
"

if [ "$1" = "no" ]; then
  exit 0
else
  echo "$mail_message" | msmtp $mail_receiver
  echo "message was sent to $mail_receiver"
fi
