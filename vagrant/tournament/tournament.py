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
    db_query("DELETE FROM matches;")


def delete_players():
    """Remove all the player records from the database.
    """
    db_query("DELETE FROM players;")


def count_players():
    """:returns: the number of players currently registered.
    """
    count = data_pull("SELECT count(*) FROM players;")
    return count[0][0]


def register_player(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    :param name: the player's full name (need not be unique).
    """
    sql = "INSERT INTO players (name) VALUES (%s)"
    data = (name, )
    db_query(sql, data)


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
    standings = data_pull("SELECT * FROM standings_view")
    return standings


def report_match(winner, loser, draw=False):
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
    sql = "INSERT INTO matches (winner, loser, draw) VALUES (%s, %s, %s)"
    data = (winner, loser, draw,)
    db_query(sql, data)


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
    pairs = []
    standing = data_pull(
        """SELECT a.id, a.name, b.id, b.name
           from standings_view as a, standings_view as b
           WHERE NOT EXISTS
             (SELECT winner, loser FROM matches where
             (a.id, b.id) = (winner, loser) or (b.id, a.id) = (winner, loser))
              AND a.id != b.id
              AND a.id < b.id
""")

    for players in standing[0::3]:
        pairs.append(players)

    return pairs


def db_query(query, data=None):
    """Function for querying the database

    Connects to db, selects cursor, passes query to db, commits, and closes
    the connection.

     Args:
        query: String to query the database
        data: The information to be injected to the query. Can be left blank

    """
    conn = connect()
    c = conn.cursor()
    c.execute(query, data)
    conn.commit()
    conn.close()


def data_pull(query, data=None):
    """ Function for querying the database to retrieve data

    Connects to db, selects cursor, passes query to db, saves data, closes
    the connection, then returns the data

    Args:
        query: String to query the database
        data: The information to be injected to the query. Can be left blank

    Returns:
        Data from pulled from the database
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query, data)
    data = c.fetchall()
    conn.close()
    return data

