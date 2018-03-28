'''
Задание 4
В базе данных содержатся 3 сущности — users, courses и saves:
users [ id, name ]
courses [ id, name ]
saves [ id, user_id, course_id, lesson_no, exercise_no, data ]
Таблица users содержит информацию о пользователях.
Таблица courses содержит информацию об обучающих курсах.
Таблица saves содержит информацию о результатах прохождения различных упражнений пользователями в определенных курсах. 
Пользователи могут выполнять каждое упражнение в каждом курсе более 1 раза.
Используя sqlite3 создайте базу данных и соответствующие сущности (напишите SQL для создания таблиц). 
Напишите SQL-запрос, результатом которого будет выборка из двух полей: "Имя пользователя" и 
"Кол-во пройденных курсов". Курс считается пройденным, если суммарно по урокам выполнено 100 различных упражнений.

'''

import sqlite3
#Подключение к базе
great_table_user = ''' CREATE TABLE 'users' (
	'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
	'name'	TEXT
);'''

great_table_courses =  '''CREATE TABLE 'courses' (
	'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
	'name'	TEXT
);'''

great_table_saves = '''CREATE TABLE 'saves' (
	'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
	'user_id'	INTEGER,
	'course_id'	INTEGER,
	'lesson_no'	INTEGER,
	'exercise_no'	INTEGER,
	'data'	TEXT
);'''
conn = sqlite3.connect('my.sqlite')
#Создание курсора
c = conn.cursor()
#Создание таблицы
c.execute(great_table_user)
c.execute(great_table_courses)
c.execute(great_table_saves)
#Наполнение таблицы
#c.execute("INSERT INTO users (name,password) VALUES ('admin','123')")
#Подтверждение отправки данных в базу
conn.commit()
#Завершение соединения
'''
SELECT course_id, lesson_no, count(DISTINCT exercise_no) FROM saves WHERE user_id = 1
GROUP BY course_id
'''

'''
select user_id, course_id, lesson_no, count(DISTINCT exercise_no) 
from saves group by user_id
''' 

c.close()
conn.close()
