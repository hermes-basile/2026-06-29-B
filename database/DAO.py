from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                        select *
                from album a 
                order by a.AlbumId asc 
                
                """

        cursor.execute(query)

        for row in cursor:
            results.append(
                Album(**row)

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.AlbumId 
                    from track t 
                    order by t.AlbumId asc

                """

        cursor.execute(query)

        for row in cursor:
            results.append(
                row["AlbumId"]

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def fillTracce(nodo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.*,g.Name as genreName
                    from track t, genre g 
                    where t.GenreId = g.GenreId 
                    and t.AlbumId = %s
                                   """

        cursor.execute(query, (nodo.AlbumId,))

        for row in cursor:
            results.append(
                {
                    "TrackId" : row["TrackId"],
                    "Name": row["Name"],
                    "AlbumId": row["AlbumId"],
                    "MediaTypeId": row["MediaTypeId"],
                    "GenreId": row["GenreId"],
                    "Composer": row["Composer"],
                    "Milliseconds": row["Milliseconds"],
                    "Bytes": row["Bytes"],
                    "UnitPrice": row["UnitPrice"],
                    "genreName": row["genreName"]

                }
            )

        cursor.close()
        conn.close()
        nodo.lista_tracce= results  # direttore DEVE essere l'oggetto, e deve essere nel DAO scritto
        # proprio così, altro esempio def fillAttori(noDo), noDo.lista_film = result