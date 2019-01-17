class Item:
    def __init__(self, pid):
        self.pID = pid
        self.reviews = []
        self.scores = []
        self.reviewers = []
        self.predicted_score = 0
        self.similarity = 0
        self.rVectors = []
