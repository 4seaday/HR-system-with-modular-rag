import pymysql
from employee_data import data

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
cur = conn.cursor()

# 테이블 생성
create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            age INT,
            position VARCHAR(20),
            department VARCHAR(20),
            skill VARCHAR(50),
            education VARCHAR(20),
            years_at_company INT,
            hobby VARCHAR(50),
            marital_status VARCHAR(10),
            certification VARCHAR(50),
            award VARCHAR(50),
            address VARCHAR(100)
        )"""

cur.execute(create_table_query)

# 데이터 insert

insert_query = """INSERT INTO employees (name, age, position, department, skill, education, years_at_company, hobby, marital_status, certification, award, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
for employee in data:
    cur.execute(insert_query, (
                employee['name'],
                employee['age'],
                employee['position'],
                employee['department'],
                employee['skill'],
                employee['education'],
                employee['years_at_company'],
                employee['hobby'],
                employee['marital_status'],
                employee['certification'],
                employee['award'],
                employee['address']
            ))
conn.commit()
conn.close()