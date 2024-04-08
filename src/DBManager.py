import psycopg2


class DBManager:

	@staticmethod
	def create_database(params: dict, database_name):
		""" Создает базу данных. """
		conn = psycopg2.connect(dbname='postgres', **params)
		conn.autocommit = True
		cur = conn.cursor()
		cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
		cur.execute(f'CREATE DATABASE {database_name}')
		conn.close()

	@staticmethod
	def create_table_employers(params: dict, database_name):
		""" Создает таблицу компаний. """
		conn = psycopg2.connect(dbname=database_name, **params)
		with conn.cursor() as cur:
			cur.execute("""
			CREATE TABLE employers (
			company_id SERIAL PRIMARY KEY,
			employer_name VARCHAR UNIQUE
			)
			""")
		conn.commit()
		conn.close()

	@staticmethod
	def create_table_vacancy(params: dict, database_name):
		""" Создает таблицу вакансий. """
		conn = psycopg2.connect(dbname=database_name, **params)
		with conn.cursor() as cur:
			cur.execute("""
			CREATE TABLE vacancies (
			vacancy_id serial,
			vacancy_name text not null,
			salary int,
			company_name text REFERENCES employers(employer_name) NOT NULL,
			vacancy_url varchar not null,
			foreign key(company_name) references employers(employer_name)
			)
			""")
		conn.commit()
		conn.close()

	@staticmethod
	def add_employer_in_bd(params: dict, database_name: str, employers_dict: dict):
		"""Скрипт для заполнения данными компаний таблицы в БД. """
		conn = psycopg2.connect(dbname=database_name, **params)
		cur = conn.cursor()
		for employer in employers_dict:
			cur.execute(
				f"INSERT INTO employers (employer_name) VALUES ('{employer}')")
		conn.commit()
		conn.close()

	@staticmethod
	def add_vacancy_in_bd(params: dict, database_name: str, employers_all_vacancies: dict):
		"""Скрипт для заполнения данными вакансий таблицы в БД."""
		conn = psycopg2.connect(dbname=database_name, **params)
		cur = conn.cursor()
		for vacancy in employers_all_vacancies:
			cur.execute(
				f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
				f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
				f"'{vacancy['employer']}', '{vacancy['url']}')")
		conn.commit()
		conn.close()

	@staticmethod
	def get_companies_and_vacancies_count(params, database_name):
		""" Получает список всех компаний и количество вакансий у каждой компании. """
		with psycopg2.connect(dbname=database_name, **params)as conn:
			with conn.cursor()as cur:
				cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
				answer = cur.fetchall()
		conn.close()
		return answer

	@staticmethod
	def get_all_vacancies(params, database_name):
		""" Получает список всех вакансий с указанием названия компании,
		названия вакансии и зарплаты и ссылки на вакансию. """
		with psycopg2.connect(dbname=database_name, **params) as conn:
			with conn.cursor() as cur:
				cur.execute('SELECT * FROM  vacancies')
				answer = cur.fetchall()
		conn.close()
		return answer

	@staticmethod
	def get_avg_salary(params, database_name):
		""" Получает среднюю зарплату по вакансиям. """
		with psycopg2.connect(dbname=database_name, **params) as conn:
			with conn.cursor() as cur:
				cur.execute('SELECT AVG(salary) FROM  vacancies')
				answer = cur.fetchall()
		conn.close()
		return answer

	@staticmethod
	def get_vacancies_with_higher_salary(params, database_name):
		""" Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
		with psycopg2.connect(dbname=database_name, **params) as conn:
			with conn.cursor() as cur:
				cur.execute('SELECT * FROM  vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
				answer = cur.fetchall()
		conn.close()
		return answer

	@staticmethod
	def get_vacancies_with_keyword(params, database_name, word):
		"""  Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. """
		with psycopg2.connect(dbname=database_name, **params) as conn:
			with conn.cursor() as cur:
				cur.execute(f"SELECT * FROM  vacancies WHERE vacancy_name LIKE '%{word}%'")
				answer = cur.fetchall()
		conn.close()
		return answer
