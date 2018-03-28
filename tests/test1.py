'''
Задание 1

Имеются два файла f1.txt и f2.txt:
В файле f1.txt содержатся уникальные строковые идентификаторы, состоящие из латинских символов разной длины, 
разделенные между собой пробелами.
В файле f2.txt содержатся числовые значения (целочисленные), разделенные между собой пробелами.
Необходимо объединить данные файлы в словарь, где ключами будут строковые идентификаторы (из f1.txt), 
а значениями - числа (из f2.txt), на соответствующих позициях. Если строковому идентификатору не хватило числового 
значения, то значением должно быть None. Числовые значения, которым не хватило строковых идентификаторов, 
нужно игнорировать.
'''
from itertools import zip_longest

result = {}
str1_from_f1 = []
str2_from_f2 = []

with open("f1.txt", 'r') as f1:
    try:
        for s in f1.read().split():
            if not s.isalpha():
                raise Exception("Неверный формат входных данных в файле "+f1.name)
            else:
                str1_from_f1.append(s)
    except Exception as e:
        print (str(e))
        exit(0)

with open("f2.txt", 'r') as f2:
    try:
        str2 = [int(i) for i in f2.read().split()]
    except Exception as e:
        print('Неверный формат входных данных в файле '+f2.name +" "+str(e))
        exit(0)

#zip_longest(*iterables, fillvalue=None) - как zip, но наоыборот берет самый длинный итератор,
# а короткие дополняет fillvalue.
result = {key: values for key, values in zip_longest(str1, str2) if key is not None}

for keys,values in result.items():
    print(str(keys)+":"+str(values))
