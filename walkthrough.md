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
