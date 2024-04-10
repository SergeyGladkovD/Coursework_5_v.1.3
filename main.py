from src.config import config
from src.api import HeadHunterAPI
from src.DBManager import DBManager


def new_work():
	print('Я выбрал интересные мне компании и хочу получить данные о вакансиях по API.')
	response = HeadHunterAPI()
	database_name = response.database_name  # Имя базы данных
	employers_dict = response.employers_dict  # Словарь компаний
	employers_all_vacancies = response.get_vacancies()  # Список вакансий
	params = config()  # Конфигом достаем параметры
	DBManager.create_database(params, database_name)  # Статик методом создаем базу данных
	conn = DBManager(database_name, params)  # Создаем экземпляр, класса открываем подключение
	DBManager.create_table_employers(conn)  # Создаем таблицу компаний
	DBManager.create_table_vacancy(conn)  # Создаем таблицу вакансий
	DBManager.add_employer_in_bd(conn, employers_dict)  # Заполняем таблицу компаний
	DBManager.add_vacancy_in_bd(conn, employers_all_vacancies)  # Заполняем таблицу вакансий

	while True:
		user_input = input("""Выберете команду:
Нажмите 1 чтоб получить список всех компаний и количество их вакансий.
Нажмите 2 чтоб получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
Нажмите 3 чтоб получить среднюю зарплату по вакансиям.
Нажмите 4 чтоб получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
Нажмите 5 чтоб получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
Другие команды закончат программу.\n""")
		match user_input:

			case '1':
				print(DBManager.get_companies_and_vacancies_count(conn))
				continue
			case '2':
				print(DBManager.get_all_vacancies(conn))
				continue
			case '3':
				print(DBManager.get_avg_salary(conn))
				continue
			case '4':
				print(DBManager.get_vacancies_with_higher_salary(conn))
				continue
			case '5':
				word = input('Введите искомое слово.\n')
				print(DBManager.get_vacancies_with_keyword(conn, word))
				continue
			case _:
				print('Программа завершена.')
				DBManager.quit(conn)
				break


if __name__ == '__main__':
	new_work()
