from dataclasses import dataclass


@dataclass
class ArtObject:
    object_id: int
    classification: str
    continent: str
    country: str
    curator_approved: str
    dated: str
    department: str
    medium: str
    nationality: str
    object_name: str
    restricted: int
    rights_type: str
    role: str
    room: str
    style: str
    title: str

    def __hash__(self):
        return hash(self.object_id)

    def __eq__(self, other):
        return self.object_id == other.object_id

    def __str__(self):
        return f"{self.object_id} - {self.title} - {self.dated} - {self.classification}"