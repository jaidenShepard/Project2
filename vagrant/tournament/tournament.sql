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

DROP TABLE IF EXISTS players, /*player_wins,*/ matches;

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE matches(
  number SERIAL PRIMARY KEY
);

/*CREATE TABLE player_wins(
*player SERIAL REFERENCES players(id),
 * matches INT REFERENCES matches(number)
);*/

