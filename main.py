from src.config import config
from src.api import HeadHunterAPI
from src.DBManager import DBManager


def new_work():
	print('Я выбрал интересные мне компании и хочу получить данные о вакансиях по API.')
	response = HeadHunterAPI()
	database_name = response.database_name  # Имя базы данных
	employers_dict = response.employers_dict  # Словарь компаний
	employers_all_vacancies = response.get_vacancies()  # Список вакансий
	params = config()
	DBManager.create_database(params, database_name)
	DBManager.create_table_employers(params, database_name)
	DBManager.create_table_vacancy(params, database_name)
	DBManager.add_employer_in_bd(params, database_name, employers_dict)
	DBManager.add_vacancy_in_bd(params, database_name, employers_all_vacancies)

	while True:
		user_input = input("""Выберете команду:
Нажмите 1 чтоб получить список всех компаний и количество их вакансий.
Нажмите 2 чтоб получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
Нажмите 3 чтоб получить среднюю зарплату по вакансиям.
Нажмите 4 чтоб получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
Нажмите 5 чтоб получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
Другие команды закончат программу.\n""")
		if user_input not in ['1', '2', '3', '4', '5']:
			print('Программа завершена.')
			break
		elif user_input == '1':
			print(DBManager.get_companies_and_vacancies_count(params, database_name))
			continue
		elif user_input == '2':
			print(DBManager.get_all_vacancies(params, database_name))
			continue
		elif user_input == '3':
			print(DBManager.get_avg_salary(params, database_name))
			continue
		elif user_input == '4':
			print(DBManager.get_vacancies_with_higher_salary(params, database_name))
			continue
		elif user_input == '5':
			word = input('Введите искомое слово.\n')
			print(DBManager.get_vacancies_with_keyword(params, database_name, word))
			continue


if __name__ == '__main__':
	new_work()
