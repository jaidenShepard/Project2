-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

DROP TABLE IF EXISTS players, player_stats, tournament, match_ups;


CREATE TABLE tournament(
  id SERIAL PRIMARY KEY
);

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT,
  tour_id SERIAL REFERENCES tournament(id) ON DELETE CASCADE
);

CREATE TABLE player_stats(
  player SERIAL REFERENCES players(id) ON DELETE CASCADE ,
  wins INT DEFAULT 0,
  draws INT DEFAULT 0,
  matches INT DEFAULT 0,
  o_points INT DEFAULT 0
);

CREATE TABLE match_ups(
  tour_id SERIAL REFERENCES tournament(id) ON DELETE CASCADE ,
  player1 SERIAL REFERENCES players(id),
  player2 SERIAL REFERENCES players(id)
);
