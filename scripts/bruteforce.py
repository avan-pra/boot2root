#!/usr/bin/python3

import subprocess

c_sol = "Public speaking is very easy.\n1 2 6 24 120 720\n2 b 755\n9\no05km1\n"

for i in range(400000, 500000):
	l = list(str(i))
	j = 1
	while True:
		if (j == 11):
			break
		l.insert(j, ' ');
		j = j + 2
	file = open("./defuse", "w");
	file.write(c_sol + ''.join(l) + '\n')
	file.close()
	try:
		if 'Congratulations' in subprocess.check_output(["./bomb", "defuse"]).decode('utf-8'):
			print(''.join(l))
			exit()
	except subprocess.CalledProcessError:
		pass
