import paramiko
import secrets
import string
import time
import socket
import sys


ip = input (' Введите IP сервера:\n')
try:
    socket.inet_aton(ip)
    # legal
except socket.error:
    print('Адрес введен неверно!')
    exit(0)
username = input (' Введите логин:\n')
password = input(' Введите пароль:\n')



uname = 'uname -a'
animation = "|/-\\"

VestaCP = 'cd /opt | curl -O http://vestacp.com/pub/vst-install.sh'
bash = 'yes | bash vst-install.sh'


try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username,password=password)
    print(" Подключение к %s" % ip)
except paramiko.AuthenticationException:
    print(" Неудалось подключиться к %s неверный логин/пароль" %ip)
    exit(1)
except Exception as e:
    print(e.message)
    exit(2)

try:
    stdin, stdout, stderr = ssh.exec_command(uname)
except Exception as e:
    print(e.message)

err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
osversion = str(out)+str(err)

print('\n Проверяем версию ОС...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

if 'el' not in osversion:
    osversion='Debian'
else:
    osversion='RedHat'


if osversion=='RedHat':
    update='yum -y update'
    inst = 'sed -i s/^SELINUX=.*$/SELINUX=disabled/ /etc/selinux/config'
    curl='yum -y install curl'
else:
    update='yes | sudo apt-get update'
    inst='yes | sudo apt-get upgrade'
    curl='yes | sudo apt-get install curl'

print('\n Обновляем ОС...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(update)
except Exception as e:
    print(e.message)

err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
updated=str(out)+str(err)
print(updated)

try:
    stdin, stdout, stderr = ssh.exec_command(inst)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
instd=str(out)+str(err)
print(instd)

print('\n Проверка наличия curl...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(curl)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
curld=str(out)+str(err)
print(curld)

print('\n Скачивание скрипта VestaCP...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(VestaCP)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
vestad=str(out)+str(err)
print(vestad)


choose = input(' Какой веб-сервер установить? \n1. Nginx + Apache (По-умолчанию)\n2. Nginx+PHP-FPM\n3. Apache\n4. Никакого\n')
if choose=='1':
    bash=bash+' --nginx yes --apache yes --phpfpm no'
elif choose=='2':
    bash=bash+' --nginx yes --phpfpm yes --apache no'
elif choose=='3':
    bash=bash+' --nginx no --apache yes --phpfpm no'
elif choose=='4':
    bash=bash+' --nginx no --apache no --phpfpm no'
else:
    bash=bash+' --nginx yes --apache yes --phpfpm no'

choose = input(' Установить Named? \n1. Да (По-умолчанию)\n2. Нет\n')
if choose=='1':
    bash=bash+' --named yes'
elif choose=='2':
    bash=bash+' --named no'
else:
    bash=bash+' --named yes'

choose = input(' Установить Remi? \n1. Да (По-умолчанию)\n2. Нет\n')
if choose=='1':
    bash=bash+' --remi yes'
elif choose=='2':
    bash=bash+' --remi no'
else:
    bash=bash+' --remi yes'

choose = input(' Какой FTP установить? \n1. VSftpd \n2. PROftpd (По-умолчанию)\n3. Никакого\n')
if choose=='1':
    bash=bash+' --vsftpd yes --proftpd no'
elif choose=='2':
    bash=bash+' --vsftpd no --proftpd yes'
elif choose=='3':
    bash=bash+' --vsftpd no --proftpd no'
else:
    bash=bash+' --vsftpd no --proftpd yes'

choose = input(' Какой Firewall установить? \n1. iptables + fail2ban \n2. iptables (По-умолчанию)\n3. Никакого\n')
if choose=='1':
    bash=bash+' --iptables yes --fail2ban yes'
elif choose=='2':
    bash=bash+' --iptables yes --fail2ban no'
elif choose=='3':
    bash=bash+' --iptables no --fail2ban no'
else:
    bash=bash+' --iptables yes --fail2ban no'

choose = input(' Установить Quota? \n1. Да\n2. Нет (По-умолчанию)\n')
if choose=='1':
    bash=bash+' --quota yes'
elif choose=='2':
    bash=bash+' --quota no'
else:
    bash=bash+' --quota no'

choose = input(' Какой почтовый сервер установить? \n1. Exim + Dovecot + Spamassassin + Clamav\n2. Exim + Dovecot + Spamassassin\n3. Exim + Dovecot (По-умолчанию)\n4. Exim\n5. Никакого\n')
if choose=='1':
    bash=bash+' --exim yes --dovecot yes --spamassassin yes --clamav yes'
elif choose=='2':
    bash=bash+' --exim yes --dovecot yes --spamassassin yes --clamav no'
elif choose=='3':
    bash=bash+' --exim yes --dovecot yes --spamassassin no --clamav no'
elif choose=='4':
    bash=bash+' --exim yes --dovecot no --spamassassin no --clamav no'
elif choose=='5':
    bash=bash+' --exim no --dovecot no --spamassassin no --clamav no'
else:
    bash=bash+' --exim yes --dovecot yes --spamassassin no --clamav no'

choose = input(' Установить Softaculus? \n1. Да\n2. Нет (По-умолчанию)\n')
if choose=='1':
    bash=bash+' --softaculous yes'
elif choose=='2':
    bash=bash+' --softaculous no'
else:
    bash=bash+' --softaculous no'

choose = input(' Установить Mysql? \n1. Да (По-умолчанию)\n2. Нет\n')
if choose=='1':
    bash=bash+' --mysql yes'
elif choose=='2':
    bash=bash+' --mysql no'
else:
    bash=bash+' --mysql yes'

choose = input(' Установить PostgreeSQL? \n1. Да\n2. Нет (По-умолчанию)\n')
if choose=='1':
    bash=bash+' --postgresql yes'
elif choose=='2':
    bash=bash+' --postgresql no'
else:
    bash=bash+' --postgresql no'

hostname = input(' Введите hostname (По-умолчанию - localhost): \n')
if not hostname:
    hostname='localhost'
bash = bash + ' --hostname ' + hostname

email = input(' Введите email (По-умолчанию - mail@localhost.com): \n')
if not email:
    email='mail@localhost.com'
bash = bash + ' --email ' + email
alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(16))
bash = bash + ' --password ' + password

try:
    stdin, stdout, stderr = ssh.exec_command(bash)
except Exception as e:
    print(e.message)


print(' VestaCP успешно установлен\nАдрес: http://'+ip+':8083\nLogin: admin\nПароль: '+password+'\n\nУспешной работы.')