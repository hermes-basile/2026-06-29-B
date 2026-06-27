from database.DB_connect import DBConnect
from model.album import Album
from model.track import Track


class DAO():

    @staticmethod
    def getAllAlbums():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct a.*
                from album a,
                     track t
                where a.AlbumId = t.AlbumId
                order by a.Title
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Album(row["AlbumId"], row["Title"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTracksForAlbum(album):
        #gli passo un album e lo popolo con i suoi tracks
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select t.*
                from track t
                where t.AlbumId = %s
                order by t.Name
                """

        cursor.execute(query, (album.AlbumId,))

        for row in cursor:
            results.append(Track(**row))
        album.Tracks = results

        cursor.close()
        conn.close()


