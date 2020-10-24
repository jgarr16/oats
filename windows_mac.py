import os
import platform
import settings


login = os.getlogin()


def printPlatform():
    print('System: %s' % (settings.system.title()))
    print(settings.system.title(), 'base:', settings.base)


def sys_check():
    if platform.system() == 'Windows':
        settings.system = 'windows'
        settings.base = "\\\\sf18mms1\\dcps\\Reports\\"
    elif platform.system() == 'Linux':
        settings.system = 'linux'
        settings.base = "/home/%s/ws/" % (login)
    elif platform.system() == 'Darwin':
        settings.system = 'mac'
        settings.base = "/Users/%s/Library/Mobile Documents/com~apple~CloudDocs/py/repos/caprs/" % (
            login)
    else:
        print('Not sure what system you are on; please check out settings in the infra.py module.')


sys_check()
printPlatform()
