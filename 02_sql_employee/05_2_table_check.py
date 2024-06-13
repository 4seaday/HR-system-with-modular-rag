import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
cur = conn.cursor()

select_query = "SELECT * FROM employees_info"

cur.execute(select_query)

result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()