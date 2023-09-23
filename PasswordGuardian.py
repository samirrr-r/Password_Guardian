#this program allows the user to save their passwords to their text file. This text file is also encrpted using the
#cryptography package
#It first asks the user if they are generated a new key
from cryptography.fernet import Fernet
import os
import sys

#this function allows the user to create a new file when given the file name it also encrypts when the user is done
def newUser(fileName, key):
    with open(fileName,"w") as newFile:
        app=input("What is the domain/app name? enter nothing to quit/stop")
        while app!="":
            user = input("What is the username?")
            password = input("What is the password")
            newFile.write(f"Name: {app} Username:{user} Password:{password}\n")

            app = input("What is the next domain/app name? enter nothing to quit")
        newFile.close()

        encryptFile(fileName, key)

#this function checks if the program user is new or returning user
def isUser(response):
    if (response=="y") or (response=="Y"):
        return True
    else:
        return False


#This function creates a key for the user
def geneKey():
    key=Fernet.generate_key()
    return key

#This function encrpyts a file when given a key and the name of the file
def encryptFile(file, key):
    f=open(file, "r")
    fileContent=f.read()
    encContent=Fernet(key).encrypt(bytes(fileContent,'utf-8'))
    f.close()
    with open(file, "w") as overwite:
        overwite.write(str(encContent, "utf_8"))
    f.close()

def decryptFile(fileName, key):
    with open(fileName, "r") as file:
        encFile = file.read()
    try:
        decFile = Fernet(key).decrypt(bytes(encFile, 'utf-8'))
        file.close()
    except:
        print(
            "The toke you have entered is invalid. If you would like to try again pleas re-open Password Guardian.\nGoodbye.")
        file.close()
        sys.exit()

    with open(fileName, "w") as file:
        file.write(str(decFile,"utf-8"))
        file.close()

#this function can only be accessed once the user enters their key for the file
def changePass(fileName, key):
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
            content=content.replace(replaceLine,f"Name:{app} Username:{user} Password:{newPassword}\n")
        except NameError:
            print("Password has not been changed because there has not been a password already made for the app/domain.")
            encryptFile(fileName, key)
            sys.exit()

    with open(fileName, "w") as file:
        file.write(content)
    file.close()
    encryptFile(fileName, key)
    print("Your pass word has been changed and encrypted")

#this function allows the user to remove the password from their Password Manager.
#Almost the same as change password but instead of replacing the content of the line it is removed
def removePassword(fileName, key):
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
            encryptFile(fileName, key)
            sys.exit()

    with open(fileName, "w") as file:
        file.write(content)
    file.close()
    encryptFile(fileName, key)
    print("Your password has been removed and encrypted.")

#This function adds a password to the end of the text file
def addPassword(fileName, key):
    app = input("What is the domain/app name?")
    user = input("What is your username?")
    password = input("What is your password?")

    with open(fileName, "a") as file:
        file.write(f"Name: {app} Username:{user} Password:{password}\n")
        file.close()
    encryptFile(fileName, key)
    print("You have added a new password")

#Thisc function remove the txt file from the device completly
def removeManager(fileName):
    reassure = input("Are you sure that u want to remove all of your passwords?. "
                     "Enter yes to continue and anything else to exit.")
    if reassure.lower()!="yes":
        return None
    os.remove(fileName)
    print("Your password file has been removed")


print("Welcome to Password Guardian!")


response=input("Are you a returning user?(enter \"y\" for yes and any character for no)")
if isUser(response):
    fileName=input("What is your file name")+".txt"
    key=bytes(input("what is your key")+"=", 'utf-8')

    decryptFile(fileName, key)

    with open(fileName, "r") as file:
        decFile=file.read()
        file.close()
    print(decFile)

    changeChoice=input("would you like to \n1. Alter a password\n2. Remove a password\n3. Add a new password"
                       "\n4. Remove all your passwords \nEnter any character to exit program and re-encrypt your file.")
    if changeChoice =="1":
        changePass(fileName, key)
    elif changeChoice=="2":
        removePassword(fileName, key)
    elif changeChoice=="3":
        addPassword(fileName, key)
    elif changeChoice=="4":
        removeManager(fileName)


    print("Thank you for using Password Guardian")



else:
    fileName=input("What would you like to name your password file?")+".txt"
    key=geneKey()
    print(f"This is your new key: {str(key)[2:45]} \nRemember this key because this is the only way you can decrypt your file."
                                                  "\nThere is no way to reset it if you lose it.")
    newUser(fileName, key)