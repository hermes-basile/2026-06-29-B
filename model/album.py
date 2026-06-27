from dataclasses import dataclass

from model.track import Track


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    Tracks: list[Track] = None

    def __hash__(self):
        return hash(self.AlbumId)

    def __eq__(self, other):
        return self.AlbumId == other.AlbumId

    def __str__(self):
        return f"{self.Title}"

