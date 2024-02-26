class PointDto:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def mapping(json):
        return PointDto(id=str(json['_id']), name=json['name'])
