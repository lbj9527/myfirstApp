import random
import string
import mysql.connector

#gene 26+26 letters and 10 digits
forSelect = string.ascii_letters + string.digits

def generate_code(count, length):
    for x in range(count):
        re = ""
        for y in range(length):
            re += random.choice(forSelect)
        yield re

def save_code():
    conn = mysql.connector.connect(user='root', password='123456',database='test')
    cursor = conn.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS veriTable")

    # 创建数据表SQL语句
    sql = """CREATE TABLE IF NOT EXISTS veriTable(
                id INT NOT NULL AUTO_INCREMENT,
                code VARCHAR(32) NOT NULL,
                PRIMARY KEY(id)
                )"""

    cursor.execute(sql)

    codes = generate_code(200,20)
    for code in codes:
        print("data:%s" % code)
        cursor.execute("INSERT INTO `veriTable`(`code`) VALUES(%s)", params=[code])
        conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    save_code()