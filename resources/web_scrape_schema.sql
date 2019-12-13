CREATE TABLE song_instance_t (
	playlist_song_timestamp timestamp NOT NULL,
	song_id integer NOT NULL,
	web_station_id integer NOT NULL,
	row_create_date timestamp NOT NULL DEFAULT now()
);
ALTER TABLE song_instance_t ADD CONSTRAINT pk_song_instance PRIMARY KEY(playlist_song_timestamp,song_id,web_station_id);
CREATE INDEX song_instance_t_FK1 ON song_instance_t (song_id);
CREATE INDEX song_instance_t_FK2 ON song_instance_t (web_station_id);
CREATE TABLE artist_t (
	artist_id serial NOT NULL,
	artist_name character varying(255) NOT NULL,
	create_row_timestamp timestamp NOT NULL DEFAULT now()
);
ALTER TABLE artist_t ADD CONSTRAINT pk_artist PRIMARY KEY(artist_id);
CREATE TABLE album_t (
	album_id serial NOT NULL,
	artist_id integer NOT NULL,
	album_name character varying(255) NOT NULL,
	album_release_year smallint,
	album_release_date date,
	create_row_timestamp timestamp NOT NULL DEFAULT now()
);
ALTER TABLE album_t ADD CONSTRAINT pk_album PRIMARY KEY(album_id);
CREATE INDEX album_t_FK1 ON album_t (artist_id);
CREATE TABLE song_t (
	song_id serial NOT NULL,
	album_id integer NOT NULL,
	artist_id integer NOT NULL,
	song_name character varying(255) NOT NULL,
	song_release_year smallint,
	song_release_date date,
	row_create_timestamp timestamp NOT NULL DEFAULT now()
);
ALTER TABLE song_t ADD CONSTRAINT pk_song PRIMARY KEY(song_id);
CREATE INDEX song_t_FK1 ON song_t (album_id);
CREATE INDEX song_t_FK2 ON song_t (artist_id);
CREATE TABLE song_scrapes.web_station_t
(
    web_station_id integer NOT NULL,
    web_station_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    web_station_url character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    create_row_timestamp timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT pk_web_station PRIMARY KEY (web_station_id)
);
ALTER TABLE album_t ADD CONSTRAINT fk_artist_id_to_album FOREIGN KEY (artist_id) REFERENCES artist_t(artist_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE song_t ADD CONSTRAINT fk_album_id_to_song FOREIGN KEY (album_id) REFERENCES album_t(album_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE song_t ADD CONSTRAINT fk_artist_id_to_song FOREIGN KEY (artist_id) REFERENCES artist_t(artist_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE song_instance_t ADD CONSTRAINT fk_song_id_to_song_instance FOREIGN KEY (song_id) REFERENCES song_t(song_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE song_instance_t ADD CONSTRAINT fk_web_station_id_to_song_instance FOREIGN KEY (web_station_id) REFERENCES web_station_t(web_station_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
