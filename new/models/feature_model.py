import uuid

class feature():
    def __init__(self, name: str, description: str = ""):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description
        }
class dependency():
    def __init__(self, feature1: feature, feature2: feature, dependency_type: str = "optional"):
        self.feature1 = feature1
        self.feature2 = feature2
        self.feature_type = dependency_type

    def to_dict(self):
        return {
            "feature1": self.feature1.to_dict(),
            "feature2": self.feature2.to_dict(),
            "dependency_type": self.feature_type
        }
