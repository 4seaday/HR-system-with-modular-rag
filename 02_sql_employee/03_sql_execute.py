import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
cur = conn.cursor()

sql = """
SELECT COUNT(*) AS num_employees
FROM employees
WHERE department <> '경영'
AND (skill = 'PPT' OR skill = '엑셀');
"""

cur.execute(sql)
result = cur.fetchall()

for data in result:
    print(data)

cur.close()
conn.close()