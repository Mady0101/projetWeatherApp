class User:
    def __init__(self, id, username, password, email , favorites=[] , historic =[]):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.favorites = favorites
        self.historic = historic

    def __repr__(self):
        return f'<User: {self.username}>'
