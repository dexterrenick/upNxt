"""
upNext.py
Dexter Renick and Brian Cahill
Final project to simulate a website where users can connect with up and coming artists
Version 0.0.1
"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import smtplib
import time
import os
from prettytable import PrettyTable


global signedIn
signedIn = False

# Sends email confirmation
def sendEmailConfirmation(username, password):
    myEmail = 'upnext@dexterrenick.com'
    myPassword = 'upN3xt'

    msg = MIMEMultipart()
    msg["From"] = myEmail
    msg["To"] = username
    msg["Subject"] = "UpNext Sign Up Verification"
    body_text = "Thank you for signing up for your upNext account! \n \n Account details: \n username: " + username + "\n password: " + password
    body_part = MIMEText(body_text, 'plain')
    msg.attach(body_part)

    try:
        print("Verifying information...")
        smtp_server = smtplib.SMTP_SSL('smtp.dexterrenick.com', port=465)
        smtp_server.ehlo()
        # smtp_server.starttls()
        smtp_server.login(myEmail, myPassword)
        smtp_server.sendmail(msg['From'], [msg['To'],], msg.as_string())
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong. Did you enter a valid email?")
        print("Please try again later")

#Send email recovery


# Creates account if they do not exist
def createAccount():
    print("-"*97)
    print(("-"*43) + "Creator Account" + ("-"*42))
    print("-"*97)
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnextusers')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    validEmail = False
    while (not validEmail):
        us = input("Enter your signup email: ")
        if "." in us and "@" in us:
            validEmail = True
        else:
            print("Invalid email. Try again.")

    ps = input("Enter your password: ")

    #Check if user already has an account
    mycursor.execute("SELECT userUserName FROM users WHERE userUserName = '%s'"%us)
    # gets the number of rows affected by the command executed
    row_count = mycursor.rowcount
    #if they don't have an account already
    if row_count == 0:
        sql = "INSERT INTO users (userUserName, userPassword) VALUES (%s, %s)"
        val = (us, ps)
        mycursor.execute(sql, val)
        print("items inserted")
        sendEmailConfirmation(us, ps)
        userDatabase.commit()
        print("Thank you for signing up, you received a confirmation email to the email you signed up with confirming your signup")
    else:
        cursor = userDatabase.cursor()
        print("It looks like that account already exists. Login details have been send to the account.")
        cursor.execute("SELECT userPassword FROM users WHERE userUserName = '%s'"%us)
        password = cursor.fetchall()
        print(password[0][0])
        sendEmailConfirmation(us, password[0][0])
        print("Your sign in information was just resent to the email you previously entered")
    userDatabase.close()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
        

def printCreatorMenu():
    print("-"*97)
    print(("-"*43) + "Creator Menu" + ("-"*42))
    print("-"*97)
    print("1) Add Artist")
    print("2) Add Writer")
    print("3) Add Producer")
    print("4) Add Album")
    print("5) Add Song")
    print("6) Add Artist")
    print("7) Add Artist Socials")
    print("8) Delete Artist")
    print("9) Delete Writer")
    print("10) Delete Producer")
    print("11) Delete Album")
    print("12) Delete Song")
    print("13) Delete Artist")
    print("14) Delete Artist Socials")
    print("15) Logout")
    print("16) Close Program")


def printSignupOptions():
    print("1) Login")
    print("2) Signup")
    print("3) Main Menu")

def signUpMenu():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnextusers')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)

    validEmail = False
    global signedIn
    while not signedIn:
        print("-"*97)
        print(("-"*42) + "Sign in Menu" + ("-"*42))
        print("-"*97)
        print()
        while (not validEmail):
            us = input("Enter your account email: ")
            if "." in us and "@" in us:
                validEmail = True
            else:
                print("Invalid email. Try again.")

        ps = input("Enter your account password: ")

        mycursor.execute("SELECT * FROM upnextusers.users")
        numrows = mycursor.rowcount
        for x in range(0,numrows):
            row = mycursor.fetchone()
            if (row[0] == us and row[1] == ps):
                print("login success!")
                signedIn = True
                userDatabase.close()
                clearConsole()
                print(signedIn)
                # Logged in at this point
                return
        print("Invalid credentials.")
        print("1) Sign in again")
        print("2) back")
        option = "3"
        validEmail = False
        while (not(option == "1" or option == "2")):
            option = input("Enter your option: ")
            print("Invalid option. Please try again.")
        clearConsole()
        if (option == "1"):
            print()
        if (option == "2"):
            creatorMenu()



def creatorMenu():
    while not signedIn:
        print("-"*97)
        print(("-"*43) + "Creator Menu" + ("-"*42))
        print("-"*97)
        printSignupOptions()
        option = "4"
        while (not(option == "1" or option == "2" or option == "3")):
            option = input("Enter your option: ")
            print("Invalid option. Please try again.")
        clearConsole()
        if (option == "1"):
            signUpMenu()
        if (option == "2"):
            createAccount()
        if (option == "3"):
            printInitialMenu()
    # They have successfully signed in
    clearConsole()
    printCreatorMenu()
        

def browseMenu():
    print("-"*97)
    print(("-"*40) + "Browse Menu" + ("-"*40))
    print("-"*97)
    print("1) Browse Artists")
    print("2) Browse Writers")
    print("3) Browse Producers")
    print("4) Browse Albums")
    print("5) Browse Songs")
    print("7) Browse Socials")
    print("8) Back")
    print("9) Close Program")

    option = "-1"
    while (not(option == "1" or option == "2" or option == "3" or option == "4" or option == "5" or option == "6" or option == "7" or option == "8" or option == "9")):
        option = input("Enter your option: ")
        print("Invalid option. Please try again.")

    if (option == "1"):
        clearConsole()
        browseArtists()
    elif (option == "2"):
        clearConsole()
        browseWriters()
    elif (option == "3"):
        clearConsole()
        browseProducers()
    elif (option == "5"):
        clearConsole()
        browseAlbums()
    elif (option == "6"):
        clearConsole()
        browseSongs()
    elif (option == "8"):
        clearConsole()
        browsSocials()
    elif (option == "8"):
        clearConsole()
        userMenu()
    elif (option == "9"):
        quit()

def browseArtists():
    print("-"*97)
    print(("-"*40) + "Browse Artists" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Search Artist" + ("-"*40))
    print("-"*97)
    mycursor.callproc('browseArtist', args=())
    mycursor.stored_results()
    print ("%28s  %28s" % ("Artist","Number of Songs"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s" % ((res[1])[:27],res[3]))
    print ("%28s  %28s" % ("Artist","Number of Songs"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def searchMenu():
    print("-"*97)
    print(("-"*40) + "Search Menu" + ("-"*40))
    print("-"*97)
    print("1) Search Artist")
    print("2) Search Album")
    print("3) Search Song")
    print("4) Back")
    print("5) Close Program")
    option = "-1"
    while (not(option == "1" or option == "2" or option == "3" or option == "4" or option == "5" or option == "6" or option == "7" or option == "8" or option == "9")):
        option = input("Enter your option: ")
        print("Invalid option. Please try again.")
    
    if (option == "1"):
        clearConsole()
        searchArtist()
    elif (option == "2"):
        clearConsole()
        searchAlbum()
    elif (option == "3"):
        clearConsole()
        searchSong()
    elif (option == "4"):
        clearConsole()
        userMenu()
    elif (option == "5"):
        quit()


def searchArtist():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Search Artist" + ("-"*40))
    print("-"*97)
    option = input("Enter artist exact name: ")
    # Need spaces because that's how things are in the database
    option = " " + option + " "
    mycursor.callproc('artistQuery', args=(option, ))
    mycursor.stored_results()
    print ("%28s  %28s  %28s %28s %28s %28s" % ("Artist","Song","Album","Facebook","Twitter","Website"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s  %28s %28s %28s %28s" % (res[0],res[1],res[2],(res[3])[11:],(res[4])[11:],(res[5])[11:]))
    input("Press Enter to continue...")
    clearConsole()
    searchMenu()

def searchAlbum():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Search Album" + ("-"*40))
    print("-"*97)
    option = input("Enter album exact name: ")
    # Need spaces because that's how things are in the database
    option = option 
    mycursor.callproc('albumQuery', args=(option, ))
    mycursor.stored_results()
    print ("%28s  %28s  %28s %28s %28s " % ("Album","Artist","Song","Producer","Label"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s  %28s %28s %28s" % (res[1],res[0],res[2],res[3],res[4]))
    input("Press Enter to continue...")
    clearConsole()
    searchMenu()

def searchSong():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Search Song" + ("-"*40))
    print("-"*97)
    option = input("Enter song exact name: ")
    # Need spaces because that's how things are in the database
    option = option 
    mycursor.callproc('songQuery', args=(option, ))
    mycursor.stored_results()
    print ("%28s  %28s  %28s %28s %28s " % ("Song","Album","Artist","Writer","Producer"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s  %28s %28s %28s" % (res[1],res[0],res[2],res[3],res[4]))
    input("Press Enter to continue...")
    clearConsole()
    searchMenu()



def userMenu():
    print("-"*97)
    print(("-"*42) + "User Menu" + ("-"*42))
    print("-"*97)
    
    print("1) Browse")
    print("2) Search")
    print("3)Discover Random Artist")
    print("4) Main Menu")
    print("5) Close Program")

    option = "-1"
    while (not(option == "1" or option == "2" or option == "3" or option == "4")):
        option = input("Enter your option: ")
        print("Invalid option. Please try again.")
    
    clearConsole()
    if (option == "1"):
        browseMenu()
    if (option == "2"):
        searchMenu()
    if (option == "3"):
        # TODO: Add random artist functionality
        print()
    if (option == "4"):
        printInitialMenu()
    if (option == "5"):
        quit()


def printInitialMenu():
    print("-"*97)
    print(("-"*40) + "Main Menu" + ("-"*40))
    print("-"*97)
    print("Select from the following: ")
    print("1) Explore the site")
    print("2) Creator sign in")
    print("3) Close Program")
    print()
    option = "4"
    while (not(option == "1" or option == "2" or option == "3")):
        option = input("Enter your option: ")
        print("Invalid option. Please try again.")

    clearConsole()
    if (option == "1"):
        userMenu()
    if (option == "2"):
        creatorMenu()
    if (option == "3"):
        quit()

def main():
    print("-"*97)
    print(("-"*20) + "Welcome to upNxt, a site to find your new favorite artist" + ("-"*20))
    print("-"*97)
    time.sleep(1)
    printInitialMenu()
    # createAccount(userDatabase)

    

if __name__ == "__main__":
    main()