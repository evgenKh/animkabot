"""
Just sketches load and write
"""


class CommentUser:
    def __init__(self, first_name, last_name, username):
        if not first_name: first_name = ''
        if not last_name: last_name = ''
        if not username: username = ''
        self.first_name = first_name
        self.last_name = last_name
        self.username = '@' + username
        self.comment = ''
        self.mark = 0

    def add_comment(self, comment):
        self.comment = comment

    def add_mark(self, mark):
        self.mark = mark

    def show(self):
        res = """
Username: {0}
Имя: {1}
Фамилия: {2}

коммент: {3}
оцiночка: {4}
""".format(self.username, self.first_name, self.last_name,
           self.comment, self.mark)

        return res


class RegistrationUser:
    def __init__(self, first_name, last_name, username):
        if not first_name: first_name = ''
        if not last_name: last_name = ''
        if not username: username = ''
        self.first_name = first_name
        self.last_name = last_name
        self.username = '@' + username
        self.wish = ''

    def add_wish(self, wish):
        self.wish = wish

    def show(self):
        res = """
Username: {0}
Ім'я: {1}
Прізвище: {2}

Побажання: {3}
""".format(self.username, self.first_name, self.last_name,
           self.wish)

        return res
