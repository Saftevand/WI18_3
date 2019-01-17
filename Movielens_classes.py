

class user:
    def __init__(self, id):
        self.ID = id
        self.bias = 0
        self.vector = []
        self.rating_accum = 0
        self.movies_reviewed = []

class movie:
    def __init__(self, id):
        self.ID = id
        self.bias = 0
        self.vector = []
        self.rating_accum = 0
        self.times_reviewed = 0
