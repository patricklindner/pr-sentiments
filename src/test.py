from threading import Thread
from time import sleep

from tqdm import tqdm


bar1 = tqdm(range(20), position=0)
bar2 = tqdm(range(30), position=1)

def loop():
    for i in range(30):
        sleep(1)
        bar1.update()
        bar2.update()

loop()

#
# t1 = Thread(target=loop, args=(0,))
# t2 = Thread(target=loop, args=(1,))
#
# t1.start()
# t2.start()
