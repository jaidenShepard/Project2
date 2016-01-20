#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  :returns: a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database.
    """
    db_query("DELETE FROM match_ups;")


def delete_players():
    """Remove all the player records from the database.
    """
    db_query("DELETE FROM players;")


def count_players():
    """:returns: the number of players currently registered.
    """
    count = data_pull("SELECT count(*) as num FROM players;")
    return count[0][0]


def register_player(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    :param name: the player's full name (need not be unique).
    """
    db_query("INSERT INTO players (name) VALUES ('{0}'); "
             "INSERT into player_stats (player) SELECT id FROM players "
             "WHERE name = '{0}'".format(name))


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.


    :returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = data_pull("SELECT id, name, wins, matches from "
                          "players, player_stats where id = player"
                          " order by wins desc, o_points desc;")
    return standings


def report_match(winner, loser, draw):
    # TODO add tournament tracking
    """Records the outcome of a single match between two players.

    when draw =  FALSE, both players have the match number incremented, the
    winner increments wins by 1, and the losers's number of wins is added to the
     o_points.
    when draw = TRUE, increments draw and matches in both players, each other's
     wins are added to the other's o_points

    :param winner:  the id number of the player who won
    :param loser:  the id number of the player who lost
    :param draw: boolean determining if the match was a draw.
    """
    if draw:
        db_query("UPDATE player_stats set draws = draws + 1 "
                 "where player = {0} OR name = {1}; "
                 "UPDATE player_stats set o_points = o_points + "
                 "(SELECT o_points from stats "
                 "where player = {1}) "
                 "where player = {0};"
                 "UPDATE player_stats set o_points = o_points + "
                 "(SELECT o_points from player_stats "
                 "WHERE player = {0}) "
                 "WHERE player = {1};".format(winner, loser))

    else:
        db_query("UPDATE player_stats SET wins = wins + 1 "
                 "WHERE player = {0};"
                 "UPDATE player_stats set o_points = o_points + "
                 "(SELECT o_points from player_stats "
                 "WHERE player = {1}) "
                 "WHERE player = {0};".format(winner, loser))

    db_query("UPDATE player_stats SET matches = matches + 1 "
             "WHERE player = {0} OR player = {1};"
             "INSERT INTO match_ups (player1, player2) "
             "VALUES ({0},{1});".format(winner, loser))


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    :returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


def db_query(query):
    """Function for querying the database

    Connects to db, selects cursor, passes query to db, commits, and closes
    the connection.

    :param query: A string to be passed as a query to the database
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def data_pull(query):
    """Function for queries that return data

    Connects to db, selects cursor, passes query to db, saves information, and
    closes the connection.

    :param query: A string to be passed as a query to the database
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    data = c.fetchall()
    conn.close()
    return data
