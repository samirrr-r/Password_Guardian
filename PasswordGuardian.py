#this program allows the user to save their passwords to their text file. This text file is also encrpted using the
#cryptography package
#It first asks the user if they are generated a new key
import cryptography.fernet
from cryptography.fernet import Fernet
import os
import sys


#this function checks if the program user is new or returning user
def isUser(response):
    if (response=="y") or (response=="Y"):
        return True
    else:
        return False


#This function creates a key for the user
def geneKey():
    key=Fernet.generate_key()
    return str(key)+"="

#This function encrpyts a file when given a key and the name of the file
def encryptFile(key, file):
    f=open(file, "r")
    fileContent=f.read()
    encContent=Fernet(key).encrypt(bytes(fileContent,'utf-8'))
    with open(file, "w") as overwite:
        overwite.write(str(encContent))
    f.close()

#this function can only be accessed once the user enters their key for the file
def changePass(fileName):
    app = input("What is the domain/app name?")
    user = input("What is your username?")
    newPassword = input("What is your new password?")

    with open(fileName, "r") as file:
        for x in file:
            if app in x:
                replaceLine=x

        file.seek(0)
        content=file.read()

        try:
            content=content.replace(replaceLine,f"{app}: Username:{user} Password:{newPassword}\n")
        except NameError:
            print("Password has not been changed because there has not been a password already made for the app/domain.")
            return None

    with open(fileName, "w") as file:
        file.write(content)
    file.close()
    print("Your pass word has been changed")

#this function allows the user to remove the password from their Password Manager.
#Almost the same as change password but instead of replacing the content of the line it is removed
def removePassword(fileName):
    app=input("what is the domain/app of the password that you want to remove")
    reassure=input("Are you sure that u want to remove this password. Enter yes to continue and anything else to exit.")
    if reassure.lower()!="yes":
        return None
    with open(fileName, "r") as file:
        for x in file:
            if app in x:
                replaceLine=x

        file.seek(0)
        content=file.read()

        try:
            content=content.replace(replaceLine,"")
        except NameError:
            print("Password has not been removed because there has not been a password already made for the app/domain.")
            return None

    with open(fileName, "w") as file:
        file.write(content)
    file.close()

def addPassword(fileName):
    app = input("What is the domain/app name?")
    user = input("What is your username?")
    password = input("What is your password?")

    with open(fileName, "a") as file:
        file.write(f"{app}: Username:{user} Password:{password}\n")
        file.close()

def removeManager(fileName):
    reassure = input("Are you sure that u want to remove all of your passwords?. "
                     "Enter yes to continue and anything else to exit.")
    if reassure.lower()!="yes":
        return None



response=input("Are you a returning user?(enter \"y\" for yes and any character for no)")
if isUser(response):
    fileName=input("What is your file name")
    key=bytes(input("what is your 43 character key")+"=", 'utf-8')

    with open(fileName, "r") as file:
        encFile = file.read()
    try:
        decFile = Fernet(key).decrypt(bytes(encFile, 'utf-8'))
    except cryptography.fernet.InvalidToken:
        print(
            "The toke you have entered is invalid. If you would like to try again pleas re-open Password Guardian.\nGoodbye.")
        file.close()
        sys.exit()

    print(decFile)

    changeChoice=int(input("would you like to 1. Alter a password\n2. Remove a password\n3. 3. Add a new password"
                       "4. Remove all your passwords \n enter any character to exit program and re-encrypt your file."))
    if changeChoice ==1:
        changePass(fileName)
    elif changeChoice==2:
        removePassword(fileName)
    elif changeChoice==3:
        addPassword(fileName)
    elif changeChoice==4:
        removeManager(fileName)

    print("Thank you for using Password Guardian")
    encryptFile(key,fileName)
    file.close()
    sys.exit()







else:
    fileName=input("What would you like to name your password file?")
    key=geneKey()
    print("This is your new key: "+str(key)[2:45]+" \nRemember this key because this is the only way you can decrypt your file."
                                                  "There is no way to reset it if you lose it.")


