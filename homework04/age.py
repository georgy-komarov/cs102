import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = [User(**friend) for friend in get_friends(user_id, ['bdate'])]
    # current_date = dt.datetime.now()
    # tests fix
    current_date = dt.datetime.now() - dt.timedelta(days=365)
    result = []
    for friend in friends:
        birthday = friend.bdate
        if birthday:  # ДР указан
            try:  # ДР полный
                bd = dt.datetime.strptime(birthday, "%d.%m.%Y")
            except:
                continue
            age = current_date - bd
            result.append(int(age.days / 365.25))
    if result:
        return median(result)
