#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'http://www.qiushibaike.com'
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
			  Chrome/31.0.1650.63 Safari/537.36'
headers = {'User-Agent': user_agent}


class Qiubai(object):
	def __init__(self):
		self.url_prefix = 'http://www.qiushibaike.com'
		self.url = self.url_prefix
		self.user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/31.0.1650.63 Safari/537.36'
		self.headers = {'User-Agent': user_agent}

	def get_item(self, part):
		"""
			根据一段html, 返回一个字典
		"""
		item = {}
		# content
		content = part.find(class_ = 'content')
		if content:
			item['content'] = content.get_text().encode('utf-8')
		else:
			item['content'] = ''
		# author
		author = part.find(class_ = 'author')
		if author:
			item['author'] = author.get_text().encode('utf-8')
		else:
			item['author'] = ''
		# vote
		vote = part.find(class_ = 'number')
		if vote:
			item['vote'] = vote.get_text().encode('utf-8')
		else:
			item['vote'] = ''
		return item

	def parse(self, page):
		"""
			解析页面内容, 返回此页的列表, 并更新url
		"""
		# 糗百列表
		items = []

		soup = BeautifulSoup(page)
		for part in soup.find_all(class_ = 'article block untagged mb15'):
			# 处理每一条糗百
			item = self.get_item(part)
			items.append(item)
		# next page url
		url_postfix = soup.find(class_='next').get('href')
		self.url = self.url_prefix + url_postfix
		return items
	
	def get_url(self):
		"""
			根据url, 返回获取的页面, 编码方式为utf-8
		"""
		reponse = requests.get(self.url, headers = self.headers)
		reponse.encoding = 'utf-8'
		return reponse.content
	
	def print_item(self, item):
		"""
			打印一条糗百
		"""
		print 'content : ', item['content']
		print 'author : ', item['author']
		print 'vote : ', item['vote']

	def process(self):
		"""
			控制整个流程
		"""
		while self.url:
			# 得到html页面
			page = self.get_url()
			# 对html页面进行解析
			items = self.parse(page)
			
			# 显示出来
			for item in items:
				self.print_item(item)
			# wait for input
			input = raw_input()


if __name__ == '__main__':
	# reponse = requests.get(url, headers = headers)
	# soup = BeautifulSoup(reponse.content)
	# # 每一条糗百
	# for part in soup.find_all(class_ = 'article block untagged mb15'):
	# 	content = part.find(class_ = 'content')
	# 	print content.get_text().encode('utf-8')
	# 	# author
	# 	author = part.find(class_ = 'author')
	# 	print author.get_text().encode('utf-8')
	# 	# vote
	# 	vote = part.find(class_ = 'number')
	# 	print  vote.get_text().encode('utf-8')

	# next_url = soup.find(class_='next')
	# print url + next_url.get('href')
	q = Qiubai() 
	q.process()









