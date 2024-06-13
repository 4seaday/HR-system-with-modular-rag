import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
cur = conn.cursor()

cur.execute("SHOW COLUMNS FROM employees;")

for column in cur.fetchall():
    print(column)

cur.close()
conn.close()