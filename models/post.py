
class Post():

    # Class initializer. 
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, title, content, category_id, date, user_id, approved):
        self.id = id
        self.title = title
        self.content = content
        self.category_id = category_id
        self.date = date
        self.user_id = user_id
        self.approved = approved
