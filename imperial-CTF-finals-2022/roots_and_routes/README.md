# Web - Roots and Routes

## Initial Investigation
This challenge starts by providing us with a Dockerfile and the source file. The Dockerfile just states the Python version number, which will be important later on.

From the source file, it seems like we need to access the `/give_flag` page - but the catch is that it must be accessed locally, since there is this check:
```python
if flask.request.remote_addr not in ['127.0.0.1', '::1', '::ffff:127.0.0.1']:
```

There is also a `/fetch` page, which fetches a webpage for us and displays it. Obviously, we need to somehow trick the `/fetch` page to fetch the `/give_flag` page of itself to get the flag. There are however more traps.

Before actually fetching the page, the server will check if the hostname of the link provided `/fetch` is a global hostname, if not it will not fetch the page. So the question becomes: 
> How can we fetch a local page, while still specifying a global hostname?

## urlparse vulnerability
Initially, we tried to exploit a [known bug](https://bugs.python.org/issue35748) with how hostnames are parsed by the urllib module. A provided page like `http://127.0.0.1\@example.com` would trick the server into thinking the hostname is example.com (and is hence a global hostname), and fetch the main url. However, this didn't work, since we could not access the `/give_flag` page like this.

## DNS Rebinding
After many hours of googling, we found [this](https://sec.stealthcopter.com/htb-ctf-writeup-cached-web/) writeup which looked very similar to our challenge. Essentially, we provide a single website, but it can resolve to two different IP address randomly. By using a [rebinder website](https://lock.cmpxchg8b.com/rebinder.html), we could pass this to the server.There is a good chance that when it checks the hostname, it is global, but when it actually visits the page, it is a local page.

The final exploit looks like this:
> http://<server-ip>:5000/fetch?page=7f000001.5db8d822.rbndr.us:5000/give_flag

And many refreshes later we get:
>Welcome back, admin!
Your flag has been stored safely below.
Flag: ICTF{dns_r3b1nd1ng_sh0uld_b3_1ll3g4l}

```
ICTF{dns_r3b1nd1ng_sh0uld_b3_1ll3g4l}
```