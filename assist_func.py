import typing
import csv


def get_txt_len(filename: str):
    with open(filename, 'r', encoding='UTF-8') as f:
        return len(f.readlines())

def convert_to_csv(filename, csv_filename, what_to_write):
    list_file = []
    with open (filename, 'r', encoding='UTF-8') as f:
        for line in f.readlines ():
            list_file.append (line.rstrip ('\n').split(':'))
    add_to_csv (csv_filename, list_file, what_to_write)


def add_to_csv(filename: str, users: typing.List, what_to_write):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        write = csv.writer(f, delimiter=':')
        if what_to_write == 'users':
            write.writerow(['user_id', 'first_name', 'username', 'access_hash'])
            for user in users:
                write.writerow([user[0], user[1], user[2], user[3]])
        elif what_to_write == 'accounts':
            for user in users:
                try:
                    write.writerow ([user[0], user[1], user[2], user[3]])
                except IndexError:
                    continue
        elif what_to_write == 'tg_ac':
            write.writerow (['name', 'api_id', 'api_hash', 'phone'])
            for user in users:
                write.writerow ([user[0], user[1], user[2], user[3]])
        elif what_to_write == 'proxy':
            for user in users:
                try:
                    write.writerow ([user[0], user[1], user[2], user[3], user[4]])
                except IndexError:
                    continue



def yield_users(filename, start, stop):
    user_list = []
    with open(filename, 'r', encoding='UTF-8') as f:
        csvreader = csv.reader (f)
        for row in csvreader:
            if start < csvreader.line_num <= stop:
                try:
                    user_list.append((list (row)[0].split (':')[0], list (row)[0].split (':')[1], list (row)[0].split (':')[2], list (row)[0].split (':')[3]))
                except IndexError:
                    continue
            elif csvreader.line_num > stop:
                return user_list


def split_ac(clients_num: int, users_via_ac: int):
    start = 1
    num = users_via_ac
    for i in range(clients_num):
        user_list = yield_users ('users.csv', start, users_via_ac + 1)
        add_to_csv(f'users{i}.csv', user_list, 'users')
        start += num
        users_via_ac += num
    user_list = yield_users ('users.csv', users_via_ac, get_csv_len('users.csv'))
    add_to_csv (f'users.csv', user_list, 'users')


def get_from_csv(filename: str, what_to_get: str, line_num=1):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if what_to_get == 'users':  # если брать юзеров из файла
                if csvreader.line_num > line_num:
                    try:
                        yield list(row)[0].split(':')[0], list(row)[0].split(':')[1], list(row)[0].split(':')[2], list(row)[0].split(':')[3]
                    except IndexError:
                        continue
            elif what_to_get == 'accs':  # если брать аки из файла
                if csvreader.line_num > line_num:
                    try:
                        yield list(row)[0].split(':')[0], list(row)[0].split(':')[1], list(row)[0].split(':')[2], list(row)[0].split(':')[3]
                    except IndexError:
                        continue
            elif what_to_get == 'prox':  # если брать прокси из файла
                if csvreader.line_num > line_num:
                    yield list(row)[0].split(':')[0], list(row)[0].split(':')[1], list(row)[0].split(':')[2], \
                      list(row)[0].split(':')[3], list(row)[0].split(':')[4]


def get_csv_len(filename: str):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        i = 0
        for row in csvreader:
            i += 1
        return i - 1

def add_to_existing_file(users: typing.List):
    if get_csv_len('users.csv') > 1:
        with open('users.csv', 'a', newline='', encoding='UTF-8') as f:
            write = csv.writer (f, delimiter=':')
            for user in users:
                write.writerow ([user[0], user[1], user[2], user[3]])
    else:
        add_to_csv('users.csv', users, 'users')


# for proxy use only
def get_list(filename: str) -> typing.List:
    with open(filename, 'r', encoding='UTF-8') as f:
        file_list = []
        lines = f.readlines()
        for line in lines[1:]:
            file_list.append(line.rstrip('\n').split(':'))
    return file_list


def convert_proxy_to_dict():
    proxy_list = []
    for line in get_list('proxy.csv'):
        proxy_dict = {
            'proxy_type': line[0],
            'addr': line[1],
            'port': int(line[2]),
            'username': line[3],
            'password': line[4],
            'rdns': True}
        proxy_list.append(proxy_dict)
    return proxy_list


def divide_proxy():
    proxy_list = convert_proxy_to_dict()
    client_list = get_list('tg_accs.csv')
    if len(proxy_list) >= len(client_list):
        for num, i in enumerate(proxy_list):
            try:
                client_list[num].append(i)
            except IndexError:
                print(f"since {num + 2} inclusive, proxies haven't been used")
                break
    elif len(proxy_list) < len(client_list):
        proxy_num = 0
        rounds = 0
        for i in client_list:
            try:
                if rounds > 0:
                    proxy_num += 1
                    i.append (proxy_list[proxy_num])
                else:
                    i.append(proxy_list[proxy_num])
                    proxy_num += 1
            except IndexError:
                rounds += 1
                proxy_num = 0
                i.append (proxy_list[proxy_num])

    return client_list


if __name__ == '__main__':
    print(get_csv_len('tg_accs.csv'))
