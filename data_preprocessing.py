import pymysql

conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="123456",
                  db="all0504")

# generating a list of user ids with current city published
define 