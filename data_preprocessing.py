import pymysql

conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="123456",
                  db="all0504")

def gen_indication_cc_ht_count_table():
    create_tbl_stat = "create cc_ht_count as select idcurrentcity, idhometown, count(*) from user where cc != '' and ht != '' group by idcurrentcity, idhometown"
    try:
        x = conn.cursor()
        x.execute(create_tbl_stat)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()

if __name__ == '__main__':
    gen_indication_cc_ht_count_table()