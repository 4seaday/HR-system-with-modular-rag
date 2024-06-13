import pymysql
from employee_info import data

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
cur = conn.cursor()

# 추가 테이블 생성
create_table_query = """
CREATE TABLE IF NOT EXISTS employees_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    department VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100)
);
"""

cur.execute(create_table_query)

insert_query = """
INSERT INTO employees_info (name, age, department, phone, email)
VALUES (%s, %s, %s, %s, %s);
"""

for employee in data:
    cur.execute(insert_query, (employee['name'], 
                               employee['age'], 
                               employee['department'],
                               employee['phone'],
                               employee['email']
                               ))

conn.commit()
cur.close()
conn.close()