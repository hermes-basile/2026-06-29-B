from dataclasses import dataclass


@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: float

    def __hash__(self):
        return hash(self.AlbumId)

    def __eq__(self, other):
        return self.AlbumId == other.AlbumId

    def __str__(self):
        return f"{self.Title}"





