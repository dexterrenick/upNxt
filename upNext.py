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


global signedIn
signedIn = False

global dbUser
dbUser = ""
global dbPassword 
dbPassword = ""

#sets database username and password to be used everywhere
def initializeDatabase():
    global dbUser
    global dbPassword
    dbUser = input("Enter your database username: ")
    dbPassword = input("Enter your database password: ")
    try:
        mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnextusers')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        print("Program ending. Please try again once you have valid login credentials")
        quit()

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

# Creates account if they do not exist
def createAccount():
    global dbUser
    global dbPassword
    global signedIn
    print(signedIn)
    print("-"*97)
    print(("-"*43) + "Creator Account" + ("-"*42))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnextusers')
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

# Clears screen
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
        

def addArtist():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Artist" + ("-"*40))
    print("-"*97)
    artistName = input("Enter artist name: ")
    # Need spaces because that's how things are in the database
    labelName = input("Enter artist's label name: ")
    mycursor.callproc('createArtist', args=(artistName,labelName))
    userDatabase.commit()
    print("Artist inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def addWriter():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Writer" + ("-"*40))
    print("-"*97)
    writerName = input("Enter writer name: ")
    # Need spaces because that's how things are in the database
    mycursor.callproc('createWriter', args=(writerName,))
    userDatabase.commit()
    print("Writer inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def addProducer():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Producer" + ("-"*40))
    print("-"*97)
    producerName = input("Enter producer name: ")
    # Need spaces because that's how things are in the database
    mycursor.callproc('createProducer', args=(producerName,))
    userDatabase.commit()
    print("Producer inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def addAlbum():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Album" + ("-"*40))
    print("-"*97)
    albumName = input("Enter album name: ")
    # Need spaces because that's how things are in the database
    artistName = input("Enter artist's name: ")
    mycursor.callproc('createAlbum', args=(albumName,artistName))
    userDatabase.commit()
    print("Album inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def addSong():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Song" + ("-"*40))
    print("-"*97)
    songName = input("Enter song name: ")
    artistName = input("Enter artist name: ")
    albumName = input("Enter album name: ")
    producerName = input("Enter producer name: ")
    writerName = input("Enter writer name: ")
    mycursor.callproc('createSong', args=(songName, albumName, producerName, writerName, artistName))
    userDatabase.commit()
    print("Song inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def addArtistSocials():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Add Artist Socials" + ("-"*40))
    print("-"*97)
    artistName = input("Enter artist name: ")
    facebookLink = input("Enter facebook link:")
    twitterLink = input("Enter twitter: ")
    websiteLink = input("Enter website link: ")
    mycursor.callproc('createSocials', args=(facebookLink, twitterLink, websiteLink, artistName))
    userDatabase.commit()
    print("Artist Socials inserted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteArtist():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete Artist" + ("-"*40))
    print("-"*97)
    artistName = input("Enter artist's name: ")
    mycursor.callproc('deleteArtist', args=(artistName, ))
    userDatabase.commit()
    print("Artist deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteWriter():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete Writer" + ("-"*40))
    print("-"*97)
    artistName = input("Enter writer's name: ")
    mycursor.callproc('deleteWriter', args=(artistName, ))
    userDatabase.commit()
    print("Writer deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteProducer():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete Producer" + ("-"*40))
    print("-"*97)
    artistName = input("Enter producer's name: ")
    mycursor.callproc('deleteProducer', args=(artistName, ))
    userDatabase.commit()
    print("Producer deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteAlbum():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete Album" + ("-"*40))
    print("-"*97)
    artistName = input("Enter Album's name: ")
    mycursor.callproc('deleteAlbum', args=(artistName, ))
    userDatabase.commit()
    print("Album deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteSong():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete Song" + ("-"*40))
    print("-"*97)
    artistName = input("Enter song's name: ")
    mycursor.callproc('deleteSong', args=(artistName, ))
    userDatabase.commit()
    print("Song deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def deleteArtistSocials():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Delete socials" + ("-"*40))
    print("-"*97)
    artistName = input("Enter artist's name: ")
    mycursor.callproc('deleteSocials', args=(artistName, ))
    userDatabase.commit()
    print("Socials deleted...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def editArtist():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Edit artist" + ("-"*40))
    print("-"*97)
    oldArtist = input("Enter artist's old name: ")
    newArtist = input("Enter artist's new name: ")
    newLabel = input("Enter artist's new label name: ")
    mycursor.callproc('updateArtist', args=(oldArtist, newArtist, newLabel))
    userDatabase.commit()
    print("Artist updated...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

def editSocials():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Edit artist" + ("-"*40))
    print("-"*97)
    oldArtist = input("Enter artist's name: ")
    newFacebook = input("Enter artist's new facebook link: ")
    newTwitter = input("Enter artist's new twitter link: ")
    newWebsite = input("Enter artist's new website link: ")
    mycursor.callproc('updateArtist', args=(oldArtist, newFacebook, newTwitter, newWebsite))
    userDatabase.commit()
    print("Artist updated...")
    time.sleep(1)
    clearConsole()
    printCreatorMenu()

#Prints Creator Menu
def printCreatorMenu():
    print("-"*97)
    print(("-"*43) + "Creator Menu" + ("-"*42))
    print("-"*97)
    print("1) Add Artist")
    print("2) Add Writer")
    print("3) Add Producer")
    print("4) Add Album")
    print("5) Add Song")
    print("6) Add Artist Socials")
    print("7) Delete Artist")
    print("8) Delete Writer")
    print("9) Delete Producer")
    print("10) Delete Album")
    print("11) Delete Song")
    print("12) Delete Artist")
    print("13) Delete Artist Socials")
    print("14) Edit Artist")
    print("15) Edit Artist Socials")
    print("16) Logout")
    print("17) Close Program")

    option = "-1"
    while (not(option == "1" or option == "2" or option == "3" or option == "4" or option == "5" or option == "6" or option == "7" or option == "8" or option == "9" or option == "10" or option == "11" or option == "12" or option == "13" or option == "14" or option == "15" or option == "16" or option == "17")):
        option = input("Enter your option: ")
        print("Invalid option. Please try again.")

    if (option == "1"):
        clearConsole()
        addArtist()
    elif (option == "2"):
        clearConsole()
        addWriter()
    elif (option == "3"):
        clearConsole()
        addProducer()
    elif (option == "4"):
        clearConsole()
        addAlbum()
    elif (option == "5"):
        clearConsole()
        addSong()
    elif (option == "6"):
        clearConsole()
        addArtistSocials()
    elif (option == "7"):
        clearConsole()
        deleteArtist()
    elif (option == "8"):
        clearConsole()
        deleteWriter()
    elif (option == "9"):
        clearConsole()
        deleteProducer()
    elif (option == "10"):
        clearConsole()
        deleteAlbum()
    elif (option == "11"):
        clearConsole()
        deleteSong()
    elif (option == "12"):
        clearConsole()
        deleteArtist()
    elif (option == "13"):
        clearConsole()
        deleteArtistSocials()
    elif (option == "14"):
        clearConsole()
        editArtist()
    elif (option == "15"):
        clearConsole()
        editSocials()
    elif (option == "16"):
        global signedIn
        signedIn = False
        clearConsole()
        printInitialMenu()
    elif (option == "17"):
        clearConsole()
        quit()

# Prints signup options
def printSignupOptions():
    print("1) Login")
    print("2) Signup")
    print("3) Main Menu")

# Signup menu with controls to login or signup
def signUpMenu():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnextusers')
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


# Displays creator menu
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
        
# Displayes browse menu for common user
def browseMenu():
    print("-"*97)
    print(("-"*40) + "Browse Menu" + ("-"*40))
    print("-"*97)
    print("1) Browse Artists")
    print("2) Browse Writers")
    print("3) Browse Producers")
    print("4) Browse Albums")
    print("5) Browse Songs")
    print("6) Browse Socials")
    print("7) Back")
    print("8) Close Program")

    option = "-1"
    while (not(option == "1" or option == "2" or option == "3" or option == "4" or option == "5" or option == "6" or option == "7" or option == "8")):
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
    elif (option == "4"):
        clearConsole()
        browseAlbums()
    elif (option == "5"):
        clearConsole()
        browseSongs()
    elif (option == "6"):
        clearConsole()
        browseSocials()
    elif (option == "7"):
        clearConsole()
        userMenu()
    elif (option == "8"):
        quit()

# Displays a random artist
def displayRandomArtist():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Random Artist Gen" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('randomArtist', args=())
    mycursor.stored_results()
    print ("%28s  %28s %28s" % ("Artist","Number of Songs","Label"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s %28s" % ((res[0])[:27],res[1],res[2]))
    input("Press Enter to continue...")
    clearConsole()
    userMenu()

def browseArtists():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Artists" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseArtist', args=())
    mycursor.stored_results()
    print ("%28s  %28s %28s" % ("Artist","Number of Songs","Label"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s %28s" % ((res[0])[:27],res[1],res[2]))
    print ("%28s  %28s %28s" % ("Artist","Number of Songs","Label"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def browseWriters():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Writers" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseWriter', args=())
    mycursor.stored_results()
    print ("%28s" % ("Writer"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s " % (res[1]))
    print ("%28s " % ("Writer"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def browseProducers():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Producers" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseProducer', args=())
    mycursor.stored_results()
    print ("%28s" % ("Producer"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s" % (res[1]))
    print ("%28s" % ("Producer"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def browseAlbums():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Albums" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseAlbum', args=())
    mycursor.stored_results()
    print ("%28s  %28s" % ("Artist","Album"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s" % (res[0], res[1]))
    print ("%28s  %28s" % ("Artist","Album"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def browseSongs():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Songs" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseSong', args=())
    mycursor.stored_results()
    print ("%28s  %28s" % ("Artist","Song"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s" % (res[0], res[1]))
    print ("%28s  %28s" % ("Artist","Song"))
    input("Press Enter to continue...")
    clearConsole()
    browseMenu()

def browseSocials():
    global dbUser
    global dbPassword
    print("-"*97)
    print(("-"*40) + "Browse Socials" + ("-"*40))
    print("-"*97)
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.callproc('browseSocials', args=())
    mycursor.stored_results()
    print ("%28s  %28s %28s %28s" % ("Artist","Facebook","Twitter","Website"))
    for result in mycursor.stored_results():
        for res in result:
            print ("%28s  %28s %28s %28s" % (res[0],(res[1])[11:],(res[2])[11:],(res[3])[11:]))
    print ("%28s  %28s %28s %28s" % ("Artist","Facebook","Twitter","Website"))
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
    while (not(option == "1" or option == "2" or option == "3" or option == "4" or option == "5")):
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
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    print("-"*97)
    print(("-"*40) + "Search Artist" + ("-"*40))
    print("-"*97)
    option = input("Enter artist exact name: ")
    # Need spaces because that's how things are in the database
    option = option
    mycursor.callproc('artistQuery', args=(option, ))
    mycursor.stored_results()
    print ("%28s  %28s  %28s %28s %28s %28s" % ("Artist","Song","Album","Facebook","Twitter","Website"))
    for result in mycursor.stored_results():
        for res in result:
            # In case that item is NoneType, don't want an error
            artist = res[0] if (not(type(res[0]) == type(None))) else "None"
            song = res[1] if not(type(res[1]) == type(None)) else "None"
            album = res[2] if not(type(res[2]) == type(None)) else "None"
            facebook = res[3][11:] if not(type(res[3]) == type(None)) else "None"
            twitter = res[4][11:] if not(type(res[4]) == type(None)) else "None"
            website = res[5][11:] if not(type(res[5]) == type(None)) else "None"
            print ("%28s  %28s  %28s %28s %28s %28s" % (artist, song, album, facebook, twitter, website))
    input("Press Enter to continue...")
    clearConsole()
    searchMenu()

def searchAlbum():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
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
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
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

def searchSong():
    global dbUser
    global dbPassword
    userDatabase = mysql.connector.connect(user=dbUser, password=dbPassword, host='127.0.0.1', database='upnxt')
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
    userMenu()

def userMenu():
    print("-"*97)
    print(("-"*42) + "User Menu" + ("-"*42))
    print("-"*97)
    
    print("1) Browse")
    print("2) Search")
    print("3) Discover Random Artist")
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
        displayRandomArtist()
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
    initializeDatabase()
    print("-"*97)
    print(("-"*20) + "Welcome to upNxt, a site to find your new favorite artist" + ("-"*20))
    print("-"*97)
    printInitialMenu()

    

if __name__ == "__main__":
    main()