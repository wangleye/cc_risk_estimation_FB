# _*_ coding:utf-8 _*_
from incf.countryutils import transformations
import pycountry

if __name__ == '__main__':
	# print transformations.cn_to_ctn('United States')
	# country = pycountry.countries.get(name='United States')
	# print transformations.cc_to_cn(country.alpha2)
	u_continent_map = {}
	with open ('ProfJOC/u_ht_country') as inputfile:
		for line in inputfile:
			words = line.strip().split('\t')
			u = words[0]
			if len(words)==2 and words[1] != 'None':
				try:
					country = pycountry.countries.get(name=words[1])
					u_continent_map[u] = transformations.cn_to_ctn(transformations.cc_to_cn(country.alpha_2))
				except:
					u_continent_map[u] = 'unknown'
			else:
				u_continent_map[u] = 'unknown'
	with open ('ProfJOC/u_ht_continent', 'w') as outputfile:
		for u in u_continent_map:
			outputfile.write("{}\t{}\n".format(u, u_continent_map[u]))