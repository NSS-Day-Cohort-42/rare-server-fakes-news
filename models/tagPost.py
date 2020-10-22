class TagPost():

    # Class initializer. 
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, tag_id, post_id):
        self.id = id
        self.tag_id = tag_id
        self.post_id = post_id