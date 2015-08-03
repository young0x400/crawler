#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'http://www.qiushibaike.com'
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
			  Chrome/31.0.1650.63 Safari/537.36'
headers = {'User-Agent': user_agent}


if __name__ == '__main__':
	reponse = requests.get(url, headers = headers)
	soup = BeautifulSoup(reponse.content)
	# 每一条糗百
	for item in soup.find_all(class_ = 'article block untagged mb15'):
		content = item.find(class_ = 'content')
		print content.get_text().encode('utf-8')

	next_url = soup.find(class_='next')
	print url + next_url.get('href')
