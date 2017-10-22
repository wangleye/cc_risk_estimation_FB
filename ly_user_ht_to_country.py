# _*_ coding:utf-8 _*_
import time, pymysql, facebook

conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="123456",
                  db="all0504",
                  charset='utf8')

def read_api_key():
    lines = []
    with open('secret') as s:
        lines = s.readlines()
    return lines[0].strip(), lines[1].strip()


def find_country_from_db(location_id):
    query_statement = "SELECT country FROM fb_location WHERE location_id = '{}'".format(location_id)
    x = conn.cursor()
    x.execute(query_statement)
    results = x.fetchall()
    if len(results) == 0:
        return None
    return results[0][0]

def store_FB_loc(loc_id, loc_lat, loc_long, city, country):
    insert_statement = "INSERT INTO fb_location (location_id, city, country, location_lat, location_long) VALUES (%s,%s,%s,%s,%s)"
    try:
        # print(city.encode(), country.encode(), loc_lat, loc_long)
        # insert_sql = insert_statement.format(loc_id, city, country, loc_lat, loc_long)
        # print(insert_sql)
        x = conn.cursor()
        x.execute(insert_statement, (loc_id, city, country, loc_lat, loc_long))
        conn.commit()
        print(x._last_executed.encode())
    except pymysql.Error as e:
        print(e)
        # print("insert ERROR!")
        conn.rollback()

def find_country_from_fb(cc):
    app_id, app_secret = read_api_key()
    graph = facebook.GraphAPI(access_token='{}|{}'.format(app_id, app_secret), version='2.3')
    time.sleep(1) # not query too frequently
    city_id = cc
    while True:
        try:
            response = graph.get_object(id=city_id, fields='location')
            if 'location' in response:
                location = response['location']
                if 'latitude' in location:
                    loc_lat = location['latitude']
                    loc_long = location['longitude']
                    city = location['city'] if 'city' in location else ''
                    country = location['country'] if 'country' in location else ''
                    store_FB_loc(cc, loc_lat, loc_long, city, country)
                    return country
            print("Wrong city id {}".format(cc))
            return None
        except facebook.GraphAPIError as e:
            message = str(e)
            if message.find("was migrated to page ID") != -1:
                city_id = message.split(' ')[8][:-1]
            else:
                print(e)
                break
    print("SHOULD NOT ARRIVE HERE!! cc id: {}".format(cc))

def get_all_hometown_ids():
    query_statement = "SELECT distinct(idhometown) FROM user where idhometown != ''"
    x = conn.cursor()
    x.execute(query_statement)
    results = x.fetchall()
    return results

def get_all_cc_ids():
    query_statement = "SELECT distinct(idcurrentcity) FROM user where idcurrentcity != ''"
    x = conn.cursor()
    x.execute(query_statement)
    results = x.fetchall()
    return results

if __name__ == '__main__':

    all_hometown_ids = get_all_hometown_ids()
    for idx, result_line in enumerate(all_hometown_ids):
        ht_id = result_line[0]
        country = find_country_from_db(ht_id)
        if country is None:
            print('{}/{}'.format(idx, len(all_hometown_ids)))
            print('retreive city {} from Facebook...'.format(ht_id))
            country = find_country_from_fb(ht_id)
