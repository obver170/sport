from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
from bs4 import BeautifulSoup


class ParseTeam:
    list_result = []
    team_name = ''

    def __init__(self, url):
        self.url = url
        self.parse_last_events(self.url)

    # Получить все результаты команды
    # url_team - https://24score.pro/basketball/team/usa/milwaukee_bucks_(m)/
    def parse_last_events(self, url_team):
        try:
            html = urlopen(url_team)
        except HTTPError as e:
            print(e)
            return None
        except URLError as e:
            print('Сервер не доступен')
            return None
        try:
            bs = BeautifulSoup(html.read(), 'html.parser')
            reg = '\([0-9]+:.+:.+\)'
            events = bs.find_all('', text=re.compile(reg))
            self.list_result = events
            # Получить название команды
            name = bs.find('h1').text
            name = name.split('команды ')[1]
            name = name.split('. ')[0]
            self.team_name = name
        except AttributeError as e:
            print('Попытка обращения к несуществующему узлу')
            return None


    # Вернуть массив из определенного количества записей (limit)
    def get_limit_row(self, limit):
        res = []
        i = 0
        for row in self.list_result:
            if i < limit:
                res.append(row)
                i += 1
            else:
                return res

    # Вернуть словарь результатов матча из не отформатированной строки
    def get_dict_score(self, dirty_score):
        res = dirty_score.strip()
        res = res.split('(')[1]
        res = res.split(', ')
        score = {
            'chapter1': res[0],
            'chapter2': res[1],
            'chapter3': res[2],
            'chapter4': res[3].strip(')'),
        }

        return score

    # Вернуть сигнатуру четверти (четная - 0, нечетная - 1)
    # dirty_score имеет вид '22:25
    def get_signature_chapter(self, dirty_score):
        score = dirty_score.split(':')
        score = int(score[0]) + int(score[1])
        if score % 2 == 0:
            res = '0'
        else:
            res = '1'

        return res

    # Вернуть сигнатуру матча
    # dict_score имеет вид {'chapter1': '22:25', 'chapter2': '19:31', 'chapter3': '33:34', 'chapter4': '21:29'}
    def get_signature_score(self, dict_score):
        signature = ''
        signature += self.get_signature_chapter(dict_score['chapter1'])
        signature += self.get_signature_chapter(dict_score['chapter2'])
        signature += self.get_signature_chapter(dict_score['chapter3'])
        signature += self.get_signature_chapter(dict_score['chapter4'])

        return signature

    # Вернуть индекс матча - десятичное число построенное на сигнатуре матча.
    # Каждая четверть либо четная (0), либо нечетная (1), потом полученная сигнатура переводится в 10 СС
    # dict_score имеет вид {'chapter1': '22:25', 'chapter2': '19:31', 'chapter3': '33:34', 'chapter4': '21:29'}
    def get_index_score(self, dict_score):
        signature = ''
        signature += self.get_signature_chapter(dict_score['chapter1'])
        signature += self.get_signature_chapter(dict_score['chapter2'])
        signature += self.get_signature_chapter(dict_score['chapter3'])
        signature += self.get_signature_chapter(dict_score['chapter4'])

        return int(signature, 2)

    # Массив последних событий определенной команды
    # url_team имеет вид https://24score.pro/basketball/team/usa/milwaukee_bucks_(m)/
    # limit количество последних матчей, которые попадут в выборку
    def get_last_index_team(self, limit):
        event_limit = self.get_limit_row(limit)
        res = []
        for event in event_limit:
            dict = self.get_dict_score(event)
            index = self.get_index_score(dict)
            res.append(index)
        return res

    # Проверить что все значения в массиве одинаковые
    # True - если так, False - если нет
    def check_index_team(self, index_array):
        count = len(index_array)
        iteration = index_array.count(index_array[0])
        return True if (count == iteration) else False

    # Вернуть True если последние limit матчи сыграны с одинаковой сигнатурой
    def is_overlap(self, limit):
        try:
            last_events = self.get_last_index_team(limit)
            res = self.check_index_team(last_events)
            return res
        except TypeError as e:
            print('Команда имеет меньше сыгранных матчей, чем установлен лимит выборки')


    # Вернуть название команды
    def get_name_team(self):
        return self.team_name


# def experience():
#     url = 'https://24score.pro/basketball/team/usa/milwaukee_bucks_(m)/'
#     parse_team = ParseTeam(url)
#     name = parse_team.get_name_team()
#     print(name)
#     res = parse_team.is_overlap(3)
#     print(res)
#

# experience()
