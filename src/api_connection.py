from abc import ABC, abstractmethod
import requests


class BaseParser(ABC):
    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    @abstractmethod
    def _connection(self, *args):
        pass


class EmployerHH(BaseParser):
    """
    Класс для работы с API HeadHunter.
    """

    def _connection(self, keyword) -> list:
        """
        Метод, который подключается к API hh.ru и получает работодателей по ключевому слову.
        """
        url = f"{self.base_url}employers?text={keyword}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []

    def get_employer_ids(self, keyword) -> list:
        employers = self._connection(keyword)

        ids = []
        for employer in employers:
            data = {employer['id']: employer['name']}
            ids.append(data)
        if ids:
            return ids
        else:
            print('Айди не найдены')


class Vacancy(BaseParser):
    """
    Класс для работы с API HeadHunter.
    """

    def _connection(self, employer_id):
        """
        Метод, который подключается к апи hh.ru и получает вакансии по айди работодателя в формате json словарей
        """
        url = f"{self.base_url}vacancies?employer_id={employer_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["items"]

        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []


if __name__ == '__main__':
    data = EmployerHH()
    for e in data.get_employer_ids('Т-банк'):
        print(e)
    for e in data._connection('78638'):
        print(e)

    vacancies = Vacancy()
    print(vacancies._connection('78638'))
