class Order:
    def __init__(self):
        self.state = 'PENDING'
    def transition(self, state):
        self.state = state
