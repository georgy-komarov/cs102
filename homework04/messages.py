import datetime
from collections import defaultdict
from typing import List, Tuple

import plotly.graph_objs as go

from api import messages_get_history
from api_models import Message

Dates = List[datetime.date]
Frequencies = List[int]


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    result = defaultdict(lambda: 0)
    for message in messages:
        result[fromtimestamp(message.date)] += 1
    return list(result.keys()), list(result.values())


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param dates: список дат
    :param freq: число сообщений в соответствующую дату
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=freq, mode='lines+markers', name='lines+markers'))
    fig.show()


if __name__ == '__main__':
    msgs = messages_get_history(223712375, count=401)
    plotly_messages_freq(*count_dates_from_messages(msgs))
