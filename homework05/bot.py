import datetime

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import apihelper

import config

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAYS_RUSSIAN = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
WEEK_RUSSIAN = ['все недели', 'чётная неделя', 'нечётная неделя']
MONTHS_RUSSIAN = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}

bot = telebot.TeleBot(config.access_token)
apihelper.proxy = getattr(config, 'proxy', None)


def get_current_day(group):
    url = '{domain}/{group}/raspisanie_zanyatiy_{group}.htm'.format(domain=config.domain, group=group)
    response = requests.get(url)
    web_page = response.text

    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу датой и неделей
    schedule_week = soup.find("h2", attrs={"class": "schedule-week"})

    date_list = schedule_week.contents[0].lower().split()[:-2]
    date_list[1] = str(MONTHS_RUSSIAN[date_list[1]])
    date_str = ' '.join(date_list)
    date = datetime.datetime.strptime(date_str, '%d %m %Y')

    day = date.weekday()

    if 'нечетная' in schedule_week.text:
        schedule_week = 2
    else:
        schedule_week = 1

    return schedule_week, day


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
        locations_list = [room.text.split('\n\n') for room in locations_list]
        locations_list = [
            ', '.join([info.strip().replace('\n', ' ').replace('\t', '') for info in location_info if info])
            for location_info in locations_list]

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
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time.strip(), location.strip(), lesson.strip())
    else:
        resp += f'В {DAYS_RUSSIAN[int(day_num) - 1]} ({WEEK_RUSSIAN[int(week)]}) пар нет.'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


def get_current_lesson(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    for day_num in range(1, 8):
        # Получаем таблицу с расписанием на день
        schedule_table = soup.find("table", attrs={"id": f"{day_num}day"})
        if schedule_table:
            day_lessons = list(filter(lambda lesson: lesson.text, schedule_table.find_all("tr")))
            for lesson_i, lesson in enumerate(day_lessons):
                if 'today' in lesson.contents[0].attrs['class'][0]:
                    return day_num, lesson_i
    return None, None


def get_next_lesson(web_page, day, lesson):
    soup = BeautifulSoup(web_page, "html5lib")

    if day is None and lesson is None:
        day_range = range(1, 8)
    else:
        day_range = range(day, 8)

    for day_num in day_range:
        # Получаем таблицу с расписанием на день
        schedule_table = soup.find("table", attrs={"id": f"{day_num}day"})
        day_lessons = list(filter(lambda l: l.text, schedule_table.find_all("tr")))
        if day is None and lesson is None and day_lessons:  # Если занятие на следующей неделе
            return day_lessons[0]  # то выводим первое же, если в этот день есть занятия
        for lesson_i, lesson_obj in day_lessons:
            if day_num == day and lesson_i > lesson or day_num > day:
                return lesson_obj


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    week, day = get_current_day(group)
    web_page = get_page(group, str(week))

    current_day, current_lesson = get_current_lesson(web_page)
    next_lesson = get_next_lesson(web_page, current_day, current_lesson)
    if next_lesson is None:
        week = int(not bool(week - 1)) + 1
        web_page = get_page(group, str(week))
        next_lesson = get_next_lesson(web_page, None, None)

    # Время проведения занятий
    time = next_lesson.find("td", attrs={"class": "time"}).span.text.strip()

    # Место проведения занятий
    location = next_lesson.find("td", attrs={"class": "room"}).text.strip().split('\n\n')
    location = ', '.join([info.strip().replace('\n', ' ').replace('\t', '') for info in location if info])

    # Название дисциплин и имена преподавателей
    lesson = next_lesson.find("td", attrs={"class": "lesson"}).text.strip().split('\n\n')
    lesson = ', '.join([info.strip().replace('\n', ' ').replace('\t', '') for info in lesson if info])

    resp = 'Ближайшее занятие:\n<b>{}</b>, {}, {}\n'.format(time.strip(), location.strip(), lesson.strip())
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    week, day = get_current_day(group)
    if day == 7:
        week = int(not bool(week - 1)) + 1
        day = 1
    else:
        day += 1

    web_page = get_page(group, str(week))
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_day(web_page, day)
    resp = f'Расписание - {DAYS_RUSSIAN[int(day) - 1]} ({WEEK_RUSSIAN[week]}):\n\n'
    if any([x is not None for x in [times_lst, locations_lst, lessons_lst]]):
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time.strip(), location.strip(), lesson.strip())
    else:
        resp += f'В {DAYS_RUSSIAN[int(day) - 1]} ({WEEK_RUSSIAN[week]}) пар нет.'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    command, group, week = message.text.split()
    web_page = get_page(group, week)
    resp = f'Расписание ({WEEK_RUSSIAN[int(week)]}):\n\n'
    for day in range(1, 8):
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_day(web_page, day)
        resp += f'{DAYS_RUSSIAN[int(day) - 1].capitalize()}:\n'
        if any([x is not None for x in [times_lst, locations_lst, lessons_lst]]):
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time.strip(), location.strip(), lesson.strip())
        else:
            resp += f'Пар нет.\n'
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling()
