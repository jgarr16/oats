#!/usr/bin/env python3
# Oct 20, 2020
# John Garrigues
# projectSetup.py
# This module sets up standarized repository folders for new projects.

import os
import shutil
import windows_mac
import settings

# TODO: set the repos based on work vs. home macos system

login = os.getlogin()
repos = os.listdir(path=settings.base)
ignores = ['.DS_Store']
menu = ['Show Repos', 'Add Repo', 'Delete Repo', 'Exit']
orig_path = os.getcwd()


def removeIgnores():
    for i in range(len(ignores)):
        if ignores[i] in repos:
            repos.remove(ignores[i])
            # print('we want to ignore ',ignores[i])


# TODO: make it print to multiple columns, maybe.
def existingRepos():
    print('\nExisting PY Repositories:')
    sorted_repos = sorted(repos)
    for i in range(len(sorted_repos)):
        print(' - ', sorted_repos[i])
    print('')
    printMenu()


def addRepos():
    while True:
        newProj = input('\nName of new repository: ')
        try:
            reponame = repos+newProj
            os.makedirs(reponame)
            os.chdir(reponame)
            # print(os.getcwd())
            os.makedirs("data")
            os.makedirs("modules")
            os.makedirs("reports")
            # print(os.listdir(os.getcwd()))
            repos.append(newProj)
        except FileExistsError:
            print('Sorry, there\'s already a repository named "%s", try another name?' % (newProj))
            if newProj in ["no", "not", ""]:
                printMenu()
            continue
        print('The "%s" repository has been created.\n' % (newProj))
        printMenu()


def deleteRepos():
    while True:
        # existingRepos()
        delProj = input('\nRepository to delete: ')
        delProjPath = repos + delProj  # dangerous!!!!!!
        print("delProjPath =",delProjPath)
        try:
            # print(os.getcwd())
            os.chdir(repos)
            # print(sorted(os.listdir(os.getcwd())))
            # shutil.rmtree(repos + delProj) # dangerous!!!!!!
            # repos.remove(delProj)
        except:
            print('Sorry, there\'s not a repository named "%s", try another name?' % (delProj))
            if delProj in ["no", "not"]:
                printMenu()
            continue
        print('The "%s" repository has been deleted.\n' % (delProj))
        printMenu()


def makeSelection():
    opt = input('Make selection: ')
    if opt == '1':
        existingRepos()
    elif opt == '2':
        addRepos()
    elif opt == '3':
        deleteRepos()
    elif opt == '4':
        print('\nThanks for dropping by!\n')
        exit()
    # print(opt)


def printMenu():
    print('\nHome \\ Menu Items:')
    for i in range(len(menu)):
        print('[', str(i + 1), '] -', menu[i])
    makeSelection()


removeIgnores()
printMenu()
