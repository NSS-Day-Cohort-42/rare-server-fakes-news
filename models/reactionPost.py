class ReactionPost():

    # Class initializer. 
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, reaction_id, post_id, user_id):
        self.id = id
        self.reaction_id = reaction_id
        self.post_id = post_id
        self.user_id = user_id