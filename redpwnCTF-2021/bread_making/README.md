# bread_making

An interesting misc challenge that doesn't require *too* much technical knowledge, just patience.

Opening the binary with ghidra, we see that there are a few checks we need to pass before we reach the function that prints the flag.


![Image](./images/main.png)
*Screenshot of part of the main function*


![Image](./images/flag.png)
*Screenshot of the flag function*


Running the program, we see something like this
```
$ ./bread
add ingredients to the bowl
aaaaaaaa
we don't have that ingredient at home!
```

Looks like we need to enter some kind of phrase.


We then look at the strings in the binary.

```
$ strings bread
...
pull the tray out with a towel
theres no time to waste
pull the tray out
the window is closed
the fire alarm is replaced
you sleep very well
time to go to sleep
close the window
replace the fire alarm
brush teeth and go to bed
...
```

Looks like we found some actions that we can key in, and it's just a matter of finding the order in which to enter the actions.

It is still a useful challenge to build some pwntools skills :)

`flag{m4yb3_try_f0ccac1a_n3xt_t1m3???0r_dont_b4k3_br3ad_at_m1dnight}`