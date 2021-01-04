class BoundaryForm(dict):
    def __init__(self):
        dict.__init__(self)

    def add(self, bc_type, value):
        self.update({bc_type: value})



