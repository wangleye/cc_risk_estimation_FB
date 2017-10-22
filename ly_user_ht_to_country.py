# _*_ coding:utf-8 _*_
import time, pymysql, facebook

# geolocator = Nominatim()


conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="123456",
                  db="fb_posts",
				  charset='utf8')

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
    app_id = '1598399240414220'
    app_secret = '1bb78f1c54c42e0402a2e4127d6c26b6'
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

if __name__ == '__main__':

	# read user ht map
	user_ht_map = {}
	with open('ProfJOC/users_hometown') as inputfile:
		for line in inputfile:
			words = line.strip().split('\t')
			if len(words) == 2:
				user_ht_map[words[0]] = words[1].strip()
			elif len(words) == 1:
				user_ht_map[words[0]] = 'unknown'

	count = 0
	with open ('ProfJOC/u_ht_country', 'w') as outputfile:
		for u in user_ht_map.keys():
			print("user {}: {}".format(count, u))
			count += 1
			ht = user_ht_map[u]
			if ht != 'unknown':
				country = find_country_from_db(ht)
				if country is None:
					country = find_country_from_fb(ht)
				if country is not None:
					outputfile.write("{}\t{}\n".format(u, country))
				else:
					outputfile.write("{}\t{}\n".format(u, 'None'))
			else:
				outputfile.write("{}\t{}\n".format(u, 'None'))
