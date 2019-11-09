import requests
import telebot
from bs4 import BeautifulSoup
from telebot import apihelper

import config

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAYS_RUSSIAN = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
WEEK_RUSSIAN = ['все недели', 'чётная неделя', 'нечётная неделя']

bot = telebot.TeleBot(config.access_token)
apihelper.proxy = {'https': 'socks5://proxyuser:FapUsErKek@cute.wtf:7777'}


def get_page(group, week=''):
    if week != '0':
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_day(web_page, day_num: int):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": f"{day_num}day"})

    if schedule_table is not None:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text.strip() for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text.strip() for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info.strip().replace('\n', ' ').replace('\t', '') for info in lesson_info if info])
                        for lesson_info in lessons_list]

        return times_list, locations_list, lessons_list
    return None, None, None


@bot.message_handler(commands=DAYS)
def get_schedule(message):
    """ Получить расписание на указанный день """
    command, group, week = message.text.split()
    day_num = DAYS.index(command.lstrip('/')) + 1
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_day(web_page, day_num)
    resp = f'Расписание - {DAYS_RUSSIAN[int(day_num) - 1]} ({WEEK_RUSSIAN[int(week)]}):\n\n'
    if any([x is not None for x in [times_lst, locations_lst, lessons_lst]]):
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time.strip(), location.strip(), lession.strip())
    else:
        resp += f'В {DAYS_RUSSIAN[int(day_num) - 1]} ({WEEK_RUSSIAN[int(week)]}) пар нет.'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    bot.polling()
