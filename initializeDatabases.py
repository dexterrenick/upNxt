"""
initializeDatabases.py
Dexter Renick and Brian Cahill
Initializes databases with data scraped from internet
Version 0.0.1
"""
import random
import csv

import mysql.connector
import barnum
import names
import namegenerator


def dumpLabels():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    with open('./databaseData/record_labels.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            label = row[0]
            location = barnum.create_city_state_zip()
            city = location[1]
            state = location[2]
            locationString = (city + ", " + state)
            name = names.get_full_name()
            sql = "INSERT IGNORE INTO label (labelName, location, president) VALUES (%s, %s, %s)"
            val = (label, locationString, name)
            mycursor.execute(sql, val)
    userDatabase.commit()
    userDatabase.close()

def dumpArtist(file):
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    numLabels = mycursor.execute("SELECT * FROM label")
    # gets the number of rows affected by the command executed
    numLabels = mycursor.rowcount 
    with open("./databaseData/" + file + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            artistString = row[0]
            # Add one so we don't get 0
            labelNum = (random.randrange(numLabels-1))+1
            sql = "INSERT IGNORE INTO artist (artistName, labelId) VALUES (%s, %s)"
            val = (artistString, int(labelNum))
            mycursor.execute(sql, val)
    userDatabase.commit()
    userDatabase.close()

def dumpSocials(file):
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    with open("./databaseData/" + file + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        artistCount = 1
        for row in csv_reader:
            facebook = (row[1])[:119]
            twitter = (row[2])[:119]
            website = (row[3])[:119]
            sql = "INSERT IGNORE INTO socials (facebook, twitter, website, artistId) VALUES (%s, %s, %s, %s)"
            val = (facebook, twitter, website, int(artistCount))
            mycursor.execute(sql, val)
            artistCount+=1
    userDatabase.commit()
    userDatabase.close()

def dumpWriters():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    for x in range(4000):
        name = names.get_full_name()
        sql = "INSERT IGNORE INTO writer (writerName) VALUES (%s)"
        val = (name,)
        mycursor.execute(sql, val)
    userDatabase.commit()
    userDatabase.close()

def dumpProducers():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    for x in range(4000):
        name = names.get_full_name()
        sql = "INSERT IGNORE INTO producer (producerName) VALUES (%s)"
        val = (name,)
        mycursor.execute(sql, val)
    userDatabase.commit()
    userDatabase.close()

# Creates albums and songs on given album
def dumpAlbums():
    userDatabase = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='upNxt')
    mycursor = userDatabase.cursor()
    mycursor= userDatabase.cursor(buffered=True)
    mycursor.execute("SELECT * FROM label")
    # gets the number of rows affected by the command executed
    numArtists = mycursor.rowcount 

    mycursor.execute("SELECT * FROM producer")
    # gets the number of rows affected by the command executed
    numProducers = mycursor.rowcount 

    mycursor.execute("SELECT * FROM writer")
    # gets the number of rows affected by the command executed
    numWriters = mycursor.rowcount 

    currentAlbum = 1

    for x in range(numArtists):
        numAlbumsForArtist = random.randrange(5)
        # Add albums for artist
        for y in range(numAlbumsForArtist) :
            albumName = namegenerator.gen().replace("-", " ").title()
            sql = "INSERT IGNORE INTO album (albumName, artistId) VALUES (%s, %s)"
            val = (albumName, int(x+1))
            mycursor.execute(sql, val)
            # Add songs for album
            numSongsOnAlbum = random.randrange(15)
            for z in range(numSongsOnAlbum):
                songName = namegenerator.gen().replace("-", " ").title()
                sql = "INSERT IGNORE INTO song (songName, albumId, producerId, writerId, artistId) VALUES (%s, %s, %s, %s, %s)"
                randProducer = (random.randrange(numProducers)) + 1
                randWriter = (random.randrange(numWriters)) + 1
                val = (songName, currentAlbum, randProducer, randWriter, x+1)
                mycursor.execute(sql, val)
            currentAlbum+=1

    userDatabase.commit()
    userDatabase.close()

def main():

    dumpLabels()
    dumpWriters()
    dumpProducers()

    files = ["10000-MTV-Music-Artists-page-1", "10000-MTV-Music-Artists-page-2", "10000-MTV-Music-Artists-page-3", "10000-MTV-Music-Artists-page-4"]
    for file in files:
        dumpArtist(file)
        dumpSocials(file)

    dumpAlbums()


if __name__ == "__main__":
    main()