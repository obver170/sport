from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
from bs4 import BeautifulSoup
import time
import datetime
from sport.parse_team import ParseTeam


# Класс позволяет найти ссылки на баскетбольные команды, участвующие в завтрашних матчах
class ParseEvents:

    tomorrow = ''
    base = 'https://24score.pro/'
    url = ''

    def __init__(self):
        self.set_url()
        self.links = self.get_link_teams()

    # Установить ссылку на матчи следующего дня
    # Ссылка должна иметь вид - https://24score.pro/basketball/?date=2022-04-28
    def set_url(self):
        today = datetime.date.today()
        self.tomorrow = str(today + datetime.timedelta(days=1))
        self.url = self.base + 'basketball/?date=' + self.tomorrow


    def get_date(self):
        return self.tomorrow

    def get_base(self):
        return self.base


    # Получить ссылки на команды со страницы
    # url_date - https://24score.pro/basketball/?date=2022-04-28
    def get_link_teams(self):
        try:
            html = urlopen(self.url)
        except HTTPError as e:
            print(e)
            return None
        except URLError as e:
            print('Сервер не доступен')
            return None
        try:
            bs = BeautifulSoup(html.read(), 'html.parser')
            reg = 'basketball/team/'
            res = bs.find_all('a', href=re.compile(reg))

        except AttributeError as e:
            print('Попытка обращения к несуществующему узлу')
            return None
        return res


    # Вернуть полную ссылку на команду
    # base - 'https://24score.pro/'
    # dirty_url - объект bs
    def get_pure_link(self, dirty_url):
        return self.base + dirty_url['href']


    # Вернуть ссылки на команды
    def get_links_team(self):
        urls = self.get_link_teams()
        res = []
        for url in urls:
            res.append(self.get_pure_link(url))
        return res


# def experience():
#     parse_events = ParseEvents()
#     links_team = parse_events.get_links_team()
#     limit = 2
#     print(parse_events.get_date())
#     for url in links_team:
#         team = ParseTeam(url)
#         time.sleep(2)
#         print(url)
#         print('2 одинаковых матча :')
#         name = team.get_name_team()
#         res = team.is_overlap(limit)
#         print(name + ' - ' + str(res))
#
#
# experience()
