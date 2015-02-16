import psycopg2 # Handles our postgres connection
import os
import urlparse

def getDbConnection():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.getenv("DATABASE_URL"))
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)


def readTokens():
    tokens = None
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """SELECT * FROM TOKENS;"""
            curs.execute(SQL)
            tokens = curs.fetchall()
    return tokens

def createToken(name):
    with getDbConnection() as conn:
        with conn.cursor() as curs:
            SQL = """INSERT INTO TOKENS (NAME) VALUES (%s);"""
            curs.execute(SQL, [name])
            conn.commit

def deleteTokens(tokenIds):
    with getDbConnection() as conn:
        with conn.cursor() as curs:

            # Alternativly, instead of constructing the SQL delete string with a 
            # for loop we could have used psycopg2's "executemany" function
            # however this would have required reformatting our tokenIds list
            # and would have just done multiple deletes as oppossed to just one
            # with proper WHERE clauses

            SQL = """DELETE FROM TOKENS WHERE"""
            for tIds in tokenIds:
                if tokenIds.index(tIds) != 0:
                    SQL += " OR"
                SQL += " ID = %s"
            SQL += ';'
            
            curs.execute(SQL, tokenIds)
            conn.commit
