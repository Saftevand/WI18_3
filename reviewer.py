class Reviewer:
    def __init__(self, rid):
        self.rID = rid
        self.reviews = []
        self.pIDs = []
        self.scores = []
        self.predicted_score = 0
        self.similarity = 0
        self.rVectors = []
