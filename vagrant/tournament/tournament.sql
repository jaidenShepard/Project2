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

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE matches(
  winner INT REFERENCES players(id) ON DELETE CASCADE,
  loser INT REFERENCES players(id) ON DELETE CASCADE,
  draw BOOLEAN,
  PRIMARY KEY (winner, loser)
);

CREATE VIEW standings_view AS
  SELECT id, name,
    (SELECT count(winner) from matches where id = winner) as wins,
    (SELECT count(*) from matches where id = winner or id = loser) as matches
  FROM players ORDER BY wins DESC
;
