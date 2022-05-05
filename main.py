# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from sport.parse_list_event import ParseEvents
from sport.parse_team import ParseTeam
from bs4 import BeautifulSoup
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.

class Parse:

    def __init__(self):
        # Объект завтрашних событий
        self.parse_events = ParseEvents()
        # Ссылки на команды участники завтрашних матчей
        self.links_team = self.parse_events.get_links_team()
        # Завтрашняя дата
        self.date = self.parse_events.get_date()
        # Источник данных
        self.base = self.parse_events.get_base()
        # Получить массив повторов
        self.result = self.get_overlap()

    # Устанавливает массив повторов (выполняется с задержкой в 1 секунду)
    def get_overlap(self):
        res = []
        for url in self.links_team:
            team = ParseTeam(url)
            name = team.get_name_team()
            if (team.is_overlap(2)):
                if (team.is_overlap(3)):
                    mess = '3 одинаковых матча'
                    res.append([mess, name])
                else:
                    mess = '2 одинаковых матча'
                    res.append([mess, name])
            time.sleep(1)
        return res

    def get_result(self):
        res = []
        res.append([self.date])
        if (self.result == []):
            res.append(['На указанную дату нет повторов'])
        else:
            res = self.result
            res.append([self.date])
        res.append(['Источник - ' + self.base])

        return res






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p = Parse()
    res = p.get_result()
    for line in res:
        print(line)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
