import windows_mac
import settings
import atexit
from datetime import timedelta


if settings.system == 'mac' or settings.system == 'linux':
    from time import time, strftime, localtime
elif settings.system == 'windows':
    from time import clock, strftime, localtime


def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    if settings.system == 'mac' or settings.system == 'linux':
        end = time()
    elif settings.system == 'windows':
        end = clock()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))
    # print("\nElapsed Time: ", elapsed,"\n")


if settings.system == 'mac' or settings.system == 'linux':
    start = time()
elif settings.system == 'windows':
    start = clock()


atexit.register(endlog)
log("Start Program")