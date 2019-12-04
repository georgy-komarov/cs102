import time
from typing import List, Dict

import requests

import config


def get(url: str, params: dict = None, timeout: int = 5, max_retries: int = 5,
        backoff_factor: float = 0.3) -> requests.models.Response:
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for retry in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if retry == max_retries - 1:
                raise
            time.sleep(backoff_factor * (2 ** retry))


def get_friends(user_id: int, fields: List[str]) -> Dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    params = config.VK_CONFIG.copy()
    params.update({"user_id": user_id, "fields": fields})
    url = f"{params['domain']}/friends.get"

    response = get(url, params)
    return response.json()


def messages_get_history(user_id: int, offset: int = 0, count: int = 20) -> List:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "offset must be positive integer"
    assert count >= 0, "count must be positive integer"

    params = config.VK_CONFIG.copy()
    params.update({"user_id": user_id, "offset": offset, "count": 200})
    url = f"{params['domain']}/messages.getHistory"

    full_requests_num = count // 200
    result = []
    for i in range(full_requests_num + 1):
        if i == full_requests_num:
            params["count"] = count - params["offset"]

        response = get(url, params).json()
        if response.get("response") and (messages := response["response"].get("items")):
            result.extend(messages)

        params["offset"] += 200
    return result
