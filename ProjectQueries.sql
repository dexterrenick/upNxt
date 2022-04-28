USE upnxt;

select * from artist;

-- Total songs function
DROP PROCEDURE IF EXISTS totalSong;
DELIMITER //

CREATE PROCEDURE totalSong(artID INT)
BEGIN
		DECLARE numSongs INT;
        
        SELECT count(*) FROM song LEFT JOIN artist ON song.artistId = artist.artistId WHERE artist.artistId = artID GROUP BY artist.artistId INTO numSongs;
		        
		-- Set to 0 if it is null 
        UPDATE artist SET songCount = IFNULL(numSongs, 0) WHERE artistId = artID;
        
        
END//
DELIMITER ;

Drop trigger if exists totalSongs_after_insert;
-- Total songs trigger for an Add
DELIMITER //
CREATE TRIGGER totalSongs_after_insert AFTER INSERT ON song FOR EACH ROW
BEGIN
	CALL totalSong(NEW.artistId);
END//
DELIMITER ;

Drop trigger if exists totalSongs_after_delete;
-- Total songs trigger for an delete
DELIMITER //
CREATE TRIGGER totalSongs_after_delete AFTER DELETE ON song FOR EACH ROW
BEGIN
	CALL totalSong(OLD.artistId);
END//

DELIMITER ;

-- searching by artist provides all song names, album names, socials
DROP PROCEDURE IF EXISTS artistQuery;
DELIMITER //
CREATE PROCEDURE artistQuery(IN nameOfArtist VARCHAR(100))
BEGIN
		SELECT artist.artistName, song.songName, album.albumName, socials.facebook, socials.twitter, socials.website FROM artist 
        LEFT JOIN album ON album.artistId = artist.artistId
        LEFT JOIN socials ON socials.artistId = artist.artistId
        LEFT JOIN song ON song.artistId = artist.artistId
        WHERE artist.artistName = nameOfArtist;
END//
DELIMITER ;

-- returns all the songs on an album when searching for an album
DROP PROCEDURE IF EXISTS albumQuery;
DELIMITER //

CREATE PROCEDURE albumQuery(IN nameOfAlbum VARCHAR(100))
BEGIN
		SELECT artist.artistName, album.albumName, song.songName, producer.producerName, writer.writerName, label.labelName FROM album 
		JOIN song ON song.albumID = album.albumID
        JOIN artist ON song.artistId = Artist.artistID
        Join label ON artist.labelId = label.labelId
        join writer ON song.writerId = writer.writerID
        join producer ON song.writerId = producer.producerId
		WHERE album.albumName = nameOfAlbum;
END//
DELIMITER ;

-- returns all the info about a song
DROP PROCEDURE IF EXISTS songQuery;
DELIMITER //

CREATE PROCEDURE songQuery(IN nameOfSong VARCHAR(100))
BEGIN
		SELECT song.songName, album.albumName, artist.artistName, writer.writerName, producer.producerName FROM song 
        LEFT JOIN album ON song.albumID = album.albumID
        LEFT JOIN artist ON artist.artistID = album.artistID
        LEFT JOIN writer ON writer.writerID = song.writerID
        LEFT JOIN producer ON producer.producerID = song.producerID
        WHERE songName = nameOfSong;
        
END//
DELIMITER ;

-- Add an artist
DELIMITER //

CREATE PROCEDURE createArtist(artstName VARCHAR(100), lbelName VARCHAR(100))
BEGIN
    DECLARE label_p INT;
    
    SELECT label.labelId INTO label_p FROM label WHERE lbelName = label.labelName;
    IF label_p IS NULL THEN INSERT INTO label(labelName)
    VALUES (lbelName);
    SELECT label.labelId INTO label_p FROM label WHERE lbelName = label.labelName;
    END IF;
    
	INSERT IGNORE INTO artist( artistName, labelId)
    VALUES (artstName, label_p);
        
END//
DELIMITER ;

Select * from song;
Trinity Gospel Singers


-- Add a Writer
DELIMITER //
CREATE PROCEDURE createWriter(wrterName VARCHAR(100))
BEGIN
    
	INSERT IGNORE INTO writer(writerName)
    VALUES (wrterName);
        
END//

DELIMITER ;

-- Add a Producer
DELIMITER //

CREATE PROCEDURE createProducer(prducerName VARCHAR(100))
BEGIN
    
	INSERT IGNORE INTO producer(producerName)
    VALUES (prducerName);
        
END//

DELIMITER ;

-- Add an album
DELIMITER //

CREATE PROCEDURE createAlbum(albmName VARCHAR(100), artstName VARCHAR(100))
BEGIN
    DECLARE artist_p INT;
    
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    IF artist_p IS NULL THEN INSERT INTO artist(artistName)
    VALUES (artstName);
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    END IF;
    
	INSERT IGNORE INTO album(albumName, artistId)
    VALUES (albmName, artist_p);
        
END//

DELIMITER ;

-- Add a song
DELIMITER //
CREATE PROCEDURE createSong(sngName VARCHAR(100), albmName VARCHAR(100), prducerName VARCHAR(100), wrterName VARCHAR(100), artstName VARCHAR(100))
BEGIN
    DECLARE album_p INT;
    DECLARE producer_p INT;
    DECLARE writer_p INT;
    DECLARE artist_p INT;

    
	SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    IF artist_p IS NULL THEN INSERT INTO artist(artistName)
    VALUES (artstName);
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    END IF;
    
    SELECT album.albumId INTO album_p FROM album WHERE albmName = album.albumName;
    IF album_p IS NULL THEN INSERT INTO album(albumName, ArtistId)
    VALUES (albmName, artist_p);
    SELECT album.albumId INTO album_p FROM album WHERE albmName = album.albumName;
    END IF;
    
    SELECT producer.producerId INTO producer_p FROM producer WHERE prducerName = producer.producerName;
    IF producer_p IS NULL THEN INSERT INTO producer(producerName)
    VALUES (prducerName);
    SELECT producer.producerId INTO producer_p FROM producer WHERE prducerName = producer.producerName;
    END IF;
    
    SELECT writer.writerId INTO writer_p FROM writer WHERE wrterName = writer.writerName;
    IF writer_p IS NULL THEN INSERT INTO writer(writerName)
    VALUES (wrterName);
    SELECT writer.writerId INTO writer_p FROM writer WHERE wrterName = writer.writerName;
    END IF;
    
    
	INSERT IGNORE INTO song(songName, albumId, producerId, writerId, artistId)
    VALUES (sngName, album_p, producer_p, writer_p, artist_p);
    COMMIT ;
END//

DELIMITER ;

-- Add socials
DELIMITER //

CREATE PROCEDURE createSocials(facebk VARCHAR(100), twtter VARCHAR(100), wbsite VARCHAR(100), artstName VARCHAR(100))
BEGIN
    DECLARE artist_p INT;
    
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    IF artist_p IS NULL THEN INSERT INTO artist(artistName)
    VALUES (artstName);
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    END IF;
    
	INSERT IGNORE INTO socials(facebook, twitter, website, artistId)
    VALUES (facebk, twtter, wbsite, artist_p);
        
END//

DELIMITER ;

-- Delete Artist
DELIMITER //

CREATE PROCEDURE deleteArtist(artstName VARCHAR(100))
BEGIN
	DECLARE artist_p INT;
    SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
    
	DELETE FROM artist WHERE artist_p = artistId;
        
END//

DELIMITER ;

-- Delete writer
DELIMITER //

CREATE PROCEDURE deleteWriter(wrterName VARCHAR(100))
BEGIN
	DECLARE writer_p INT;
    SELECT writer.writerId INTO writer_p FROM writer WHERE wrterName = writer.writerName;
    
	DELETE FROM writer WHERE writer_p = writerId;
        
END//

DELIMITER ;

-- Delete producer
DELIMITER //

CREATE PROCEDURE deleteProducer(prducerName VARCHAR(100))
BEGIN
	DECLARE producer_p INT;
    SELECT producer.producerId INTO producer_p FROM producer WHERE prducerName = producer.producerName;
    
	DELETE FROM producer WHERE producer_p = producerId;
        
END//

DELIMITER ;

-- Delete Album
DELIMITER //

CREATE PROCEDURE deleteAlbum(albmName VARCHAR(100))
BEGIN
	DECLARE album_p INT;
    SELECT album.albumId INTO album_p FROM album WHERE albmName = album.albumName;
    
	DELETE FROM album WHERE album_p = albumId;
        
END//

DELIMITER ;

-- Delete song
DELIMITER //

CREATE PROCEDURE deleteSong(sngName VARCHAR(100))
BEGIN
	DECLARE song_p INT;
    SELECT song.songId INTO song_p FROM song WHERE sngName = song.songName;
    
	DELETE FROM song WHERE song_p = songId;

END//

DELIMITER ;


-- Delete socials
DELIMITER //
CREATE PROCEDURE deleteSocials(artstName VARCHAR(100))
BEGIN
	DECLARE artist_p INT;
    SELECT socials.artistId INTO artist_p FROM socials join artist on socials.artistId = artist.artistId WHERE artstName = artist.artistName;
    
	DELETE FROM socials WHERE artist_p = artistId;
        
END//
DELIMITER ;

-- Search Artist, filtered by Name because i figured a user would never know the primary key
DELIMITER //

CREATE PROCEDURE searchArtist(artstName VARCHAR(100))
BEGIN
		SELECT * FROM artist WHERE artstName = artstName;
END//

DELIMITER ;

-- Search Writer
DELIMITER //

CREATE PROCEDURE searchWriter(wrterName VARCHAR(100))
BEGIN
		SELECT * FROM writer WHERE wrterName = writerName;
END//

DELIMITER ;

-- Search producer
DELIMITER //

CREATE PROCEDURE searchProducer(prducerName VARCHAR(100))
BEGIN
		SELECT * FROM producer WHERE prducerName = producerName;
END//

DELIMITER ;

-- Search Album
DELIMITER //

CREATE PROCEDURE searchAlbum(albmName VARCHAR(100))
BEGIN
		SELECT * FROM album WHERE albmName = albumName;
END//

DELIMITER ;

-- Search song
DELIMITER //

CREATE PROCEDURE searchSong(sngName VARCHAR(100))
BEGIN
		SELECT * FROM song WHERE sngName = songName;
END//

DELIMITER ;

-- Search socials
DELIMITER //

CREATE PROCEDURE searchsocials(artstName VARCHAR(100))
BEGIN
		DECLARE artist_p INT;
        SELECT artist.artistId INTO artist_p FROM artist WHERE artstName = artist.artistName;
        
		SELECT * FROM socials WHERE artist_p = artistId;
END//

DELIMITER ;

-- Browse Artist, filtered by Name because i figured a user would never know the primary key
DELIMITER //

CREATE PROCEDURE browseArtist()
BEGIN
		SELECT artist.artistName, artist.songCount, label.labelName from artist join label on artist.labelId = label.labelId;
END//

DELIMITER ;

-- Browse Writer
DELIMITER //

CREATE PROCEDURE browseWriter()
BEGIN
		SELECT * FROM writer;
END//

DELIMITER ;

-- Browse producer
DELIMITER //

CREATE PROCEDURE browseProducer()
BEGIN
		SELECT * FROM producer;
END//

DELIMITER ;

-- Browse Album
DELIMITER //

CREATE PROCEDURE browseAlbum()
BEGIN
		select artist.artistname, album.albumname from upNxt.artist join upNxt.album on artist.artistId = album.artistId;
END//

DELIMITER ;

-- Browse song
DELIMITER //

CREATE PROCEDURE browseSong()
BEGIN
		select artist.artistname, song.songName from upNxt.song join upNxt.artist on song.artistId = artist.artistId;
END//

DELIMITER ;

-- Browse socials
DELIMITER //

CREATE PROCEDURE browseSocials()
BEGIN
		select artist.artistName, socials.facebook, socials.twitter, socials.website from upNxt.artist join upNxt.socials on artist.artistId = socials.artistId;

END//

DELIMITER ;

-- Random Artist
DELIMITER //

CREATE PROCEDURE randomArtist()
BEGIN
		SELECT artist.artistName, artist.songCount, label.labelName from artist join label on artist.labelId = label.labelId ORDER BY rand() limit 1;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS updateArtist;
DELIMITER //
CREATE PROCEDURE updateArtist(oldName VARCHAR(100), newName VARCHAR(100), newLabel VARCHAR(100))
BEGIN        
		DECLARE artstId INT;
        DECLARE artstLabel INT;
        
        Select artist.artistId from artist where artist.artistName = oldName INTO artstId;
        Select label.labelId from artist left join label on artist.labelId = label.labelId WHERE label.labelName = newLabel LIMIT 1 INTO artstLabel;
		
        
        IF(artstId IS NOT NULL) THEN
			UPDATE artist SET artist.labelId = artstLabel WHERE artistId = artstId;
			UPDATE artist SET artistName = newName WHERE artistId = artstId;
		END IF;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS updateSocials;
DELIMITER //
CREATE PROCEDURE updateSocials(artistName VARCHAR(100), newFacebook VARCHAR(100), newTwitter VARCHAR(100), newWebsite VARCHAR(100))
BEGIN        
		DECLARE artstId INT;
	
        Select artist.artistId from artist where artist.artistName = artistName INTO artstId;
		
        
        IF(artstId IS NOT NULL) THEN
			UPDATE socials SET socials.facebook = newFacebook WHERE socials.artistId = artstId;
			UPDATE socials SET socials.twitter = newTwitter WHERE socials.artistId = artstId;
            UPDATE socials SET socials.website = newWebsite WHERE socials.artistId = artstId;
		END IF;
END//
DELIMITER ;