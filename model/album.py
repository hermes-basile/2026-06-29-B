from dataclasses import dataclass, field


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    #se devo creare una lista interna che all'inizio è vuota
    # e non conta nel rees.append delle query
    lista_tracce: list = field(default_factory=list)



    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title}"

    def __eq__(self, other):
        return self.AlbumId == other.AlbumId