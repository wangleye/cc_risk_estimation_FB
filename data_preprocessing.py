import pymysql

conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="123456",
                  db="all0504")

def gen_indication_cc_ht_count_table():
    create_tbl_stat = "create table cc_ht_count as (select idcurrentcity, idhometown, count(*) as cnt from user where idcurrentcity != '' and idhometown != '' group by idcurrentcity, idhometown)"
    try:
        x = conn.cursor()
        x.execute(create_tbl_stat)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()

def gen_cc_count_table():
    create_tbl_stat = "create table cc_count as (select idcurrentcity, count(*) as cnt from user where idcurrentcity != '' group by idcurrentcity)"
    try:
        x = conn.cursor()
        x.execute(create_tbl_stat)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()

def gen_ht_with_cc_count_table():
    # generate the total number of users for each hometown, where the users are those who also publish current city
    create_tbl_stat = "create table ht_with_cc_count as (select idhometown, count(*) as cnt from user where idhometown != '' and idcurrentcity != '' group by idhometown)"
    try:
        x = conn.cursor()
        x.execute(create_tbl_stat)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()

# def gen_we_

if __name__ == '__main__':
    # gen_indication_cc_ht_count_table()
    # gen_cc_count_table()
    gen_ht_count_table()