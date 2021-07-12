from pwn import *

HOST, PORT = "mc.ax", 31796
BINARY = './bread'
context.log_level = 'critical'

def start():
    if not args.REMOTE:
        print("LOCAL PROCESS")
        return process(BINARY)
    else:
        print("REMOTE PROCESS")
        return remote(HOST, PORT)

def solve():
    p = start()

    sequence = ['add flour', 'add salt', 'add yeast', 'add water', 'hide the bowl inside a box', 'wait 3 hours', 'work in the basement', 'preheat the toaster oven', 'set a timer on your phone', 'watch the bread bake', 'pull the tray out with a towel', 'open the window', 'unplug the fire alarm', 'unplug the oven', 'clean the counters', 'wash the sink', 'flush the bread down the toilet', 'get ready to sleep', 'replace the fire alarm', 'close the window', 'brush teeth and go to bed']
    
    # Add ingredients
    for item in sequence:
        p.recvline()
        p.sendline(item)

    p.interactive()

solve()

# options
'leave the bowl on the counter'
'put the bowl on the bookshelf'
'hide the bowl inside a box'

'work in the kitchen'
'work in the basement'

'wait 2 hours'
'wait 3 hours'

'preheat the oven'
'preheat the toaster oven'

'use the oven timer'
'set a timer on your phone'

'return upstairs'
'watch the bread bake'

'pull the tray out'
'pull the tray out with a towel'

'open the window'
'close the window'

'unplug the oven'
'unplug the fire alarm'

'wash the sink'
'clean the counters'
'flush the bread down the toilet'

'get ready to sleep'
'replace the fire alarm'
'brush teeth and go to bed'