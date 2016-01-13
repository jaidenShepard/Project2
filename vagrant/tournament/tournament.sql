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

DROP TABLE IF EXISTS players, player_stats, matches, round_match_ups;

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT,
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  matches INT DEFAULT 0
);

CREATE TABLE matches(
  player1 SERIAL REFERENCES players(id),
  player2 SERIAL REFERENCES players(id)
);
/*
CREATE TABLE player_stats(
  player SERIAL REFERENCES players(id),
  match_id SERIAL REFERENCES matches(id),
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  matches INT DEFAULT 0
);
CREATE TABLE round_match_ups(
  match SERIAL REFERENCES matches(id),
  player1 SERIAL REFERENCES players(id),
  player2 SERIAL REFERENCES players(id)
);
*/
