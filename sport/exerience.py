# import datetime
#
#
# def get_url(base):
#     today = datetime.date.today()
#     tomorrow = today + datetime.timedelta(days=1)
#     url = base + 'basketball/?date=' + str(tomorrow)
#     return url
#
#
# base = 'https://24score.pro/'
#
# print(get_url(base))