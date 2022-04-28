CREATE DATABASE upnxt;
USE upnxt;

CREATE TABLE label
(
	labelId INT AUTO_INCREMENT PRIMARY KEY,
	labelName VARCHAR(50),
    location VARCHAR(100),
    president VARCHAR(50)
);

CREATE TABLE artist
(
	artistId INT AUTO_INCREMENT PRIMARY KEY,
    artistName VARCHAR(100),
    labelId INT,
    songCount INT DEFAULT 0,
    FOREIGN KEY (labelId) REFERENCES label(labelId)
      ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE socials
(
	facebook VARCHAR(120),
    twitter VARCHAR(120),
    website VARCHAR(120),
    artistId INT PRIMARY KEY,
    FOREIGN KEY (artistId) REFERENCES artist(artistId)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE album
(
	albumId INT AUTO_INCREMENT PRIMARY KEY,
    albumName VARCHAR(100),
    artistId INT,
    FOREIGN KEY (artistId) REFERENCES artist(artistId)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE writer
(
	writerId INT AUTO_INCREMENT PRIMARY KEY,
    writerName VARCHAR(100)
);

CREATE TABLE producer
(
	producerId INT AUTO_INCREMENT PRIMARY KEY,
    producerName VARCHAR(100)
);

CREATE TABLE song
(
	songID INT AUTO_INCREMENT PRIMARY KEY,
    songName VARCHAR(100),
    albumId INT,
    producerId INT,
    writerId INT,
    artistId INT,
    FOREIGN KEY (albumId) REFERENCES album(albumId)
      ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (producerId) REFERENCES producer(producerId)
	  ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (writerId) REFERENCES writer(writerId)
	  ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (artistId) REFERENCES artist(artistId)
	  ON UPDATE CASCADE ON DELETE CASCADE
);


