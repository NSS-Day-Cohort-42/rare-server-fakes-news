class Reaction():

    # Class initializer. 
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, reaction, reaction_description):
        self.id = id
        self.reaction = reaction
        self.reaction_description = reaction_description
