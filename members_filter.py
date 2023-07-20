import typing

class Member_filter:
    def __init__(self, user):
        self.user = user

    def exclude(self):
        with open ('exclude_list.txt', 'r', encoding='utf-8') as f:
            name_list = []
            black_list = f.readlines ()
            for i in black_list:
                name_list.append (i.rstrip ('\n').lower ())
        for i in name_list:
            if self.user.first_name is None or self.user.last_name is None:
                return False
            if (i in self.user.first_name.lower()) or (i in self.user.last_name.lower()):
                return True





