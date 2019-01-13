class Review:
    def __init__(self, rid, pid, text, sco):
        self.rID = rid
        self.pID = pid
        self.rText = text
        self.score = sco
        self.predicted_score = 0
        self.similarity = 0
        self.rVector = []
