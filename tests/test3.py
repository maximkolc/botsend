'''Задание 3
В базе данных содержится сущность something:
something [ id, ..., date ]
Необходимо написать SQL-запрос, который удалит из данной сущности все записи, кроме 5-ти записей, имеющих самую свежую дату (date).
'''
import sqlite3

conn = sqlite3.connect('test3.sqlite')
cursor = conn.cursor()
cursor.execute("""
 DELETE  FROM 'something' WHERE 
    id IN (SELECT id FROM 
            (
			SELECT 'something'.'id' FROM 'something' ORDER BY 'something'.'date' DESC LIMIT -1 OFFSET 5
		  ));
""")
conn.commit()
results = cursor.fetchall()
conn.close()
