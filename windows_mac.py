import os
import platform
import settings


login = os.getlogin()


def printPlatform():
    print('System: %s@%s' % (settings.system.title(),settings.locale.title()))
    print(settings.system.title(), 'base:', settings.base)


def sys_check():
    if platform.system() == 'Windows':
        settings.system = 'windows'
        settings.base = "\\\\server\\folder\\subfolder\\"
        settings.locale = "needs_to_be_assigned"
    elif platform.system() == 'Linux':
        settings.system = 'linux'
        settings.base = "/home/%s/ws/" % (login)
        settings.locale = "needs_to_be_assigned"
    elif platform.system() == 'Darwin':
        settings.system = 'mac'
        netname=platform.node()
        if netname == 'ARLAL0119090173':
            settings.base = "/Users/%s/OneDrive-NASA/py/repos/" % (login)
            settings.locale = "work"
        elif netname.startswith('Johns-MBP'):
            settings.base = "/Users/%s/Library/Mobile Documents/com~apple~CloudDocs/py/repos/" % (login)
            settings.locale = "home"
    else:
        print('Not sure what system you are on; please check out settings in the infra.py module.')


sys_check()
printPlatform()
