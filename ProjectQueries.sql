USE upNxt;

-- Total songs function
DROP PROCEDURE IF EXISTS totalSong;
DELIMITER //

CREATE PROCEDURE totalSong(artID INT)
BEGIN
		DECLARE CONTINUE HANDLER FOR SQLEXCEPTION BEGIN END;
		ALTER TABLE artist ADD COLUMN totalSongs INTEGER;
        
		-- SELECT artist.artistId, COUNT(song.songID) INTO songCount FROM song 
        INSERT INTO songCount SELECT artist.artistId, COUNT(song.songID) FROM song  
        LEFT JOIN album ON song.albumID = album.albumID
        LEFT JOIN artist ON artist.artistID = album.artistID
		GROUP BY artistID;
        
        UPDATE artist SET totalSongs = songCount WHERE artistID = artID;
        
END//

DELIMITER ;

-- Total songs trigger for an Add
DELIMITER //

CREATE TRIGGER totalSongs_after_insert AFTER INSERT ON song FOR EACH ROW
BEGIN
	CALL totalSong(NEW.song);
END//

DELIMITER ;

-- Total songs trigger for an delete
DELIMITER //

CREATE TRIGGER totalSongs_after_insert AFTER DELETE ON song FOR EACH ROW
BEGIN
	
	CALL totalSong(OLD.song);
END//

DELIMITER ;

-- searching by artist provides all song names, album names, socials
DROP PROCEDURE IF EXISTS artistQuery;
DELIMITER //

CREATE PROCEDURE artistQuery(IN nameOfArtist VARCHAR(100))
BEGIN
		SELECT artist.artistID, artist.artistName, song.songName, album.albumName, socials.* FROM song 
        LEFT JOIN album ON song.albumID = album.albumID
        LEFT JOIN artist ON artist.artistID = album.artistID
        LEFT JOIN socials ON socials.artistID = artist.artistID
        WHERE artistName = nameOfArtist GROUP BY artistID;
        
END//

DELIMITER ;

-- returns all the songs on an album when searching for an album
DROP PROCEDURE IF EXISTS albumQuery;
DELIMITER //

CREATE PROCEDURE albumQuery(IN nameOfAlbum VARCHAR(100))
BEGIN
		SELECT album.albumID, album.albumName, song.songName FROM album 
		JOIN song ON song.albumID = album.albumID
        WHERE albumName = nameOfAlbum GROUP BY albumID;
        
END//

DELIMITER ;

-- returns all the info about a song
DROP PROCEDURE IF EXISTS songQuery;
DELIMITER //

CREATE PROCEDURE songQuery(IN nameOfSong VARCHAR(100))
BEGIN
		SELECT song.songID, song.songName, album.albumName, artist.artistName, wrtier.writerName, producer.producerName FROM song 
        LEFT JOIN album ON song.albumID = album.albumID
        LEFT JOIN artist ON artist.artistID = album.artistID
        LEFT JOIN writer ON writer.writerID = song.writerID
        LEFT JOIN producer ON producer.producerID = song.producerID
        WHERE songName = nameOfSong GROUP BY songID;
        
END//

DELIMITER ;

