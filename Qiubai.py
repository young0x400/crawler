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
		# initial
		item['content'] = u''	#本条糗百内容
		item['pubtime'] = u''	#本条糗百发布时间
		item['author'] = u''		#作者
		item['vote_num'] = u'' #投票数
		item['comment_num'] = u'' #评论数
		item['tag'] = []		 # 标签
		item['video_src'] = u''  # 视频链接, 无则为空
		item['img_src'] = u''    # 图片链接, 无则为空

		# content
		content = part.find(class_ = 'content')
		if content:
			item['content'] = content.get_text(strip = True)
			#publish time
			item['pubtime'] = content.contents[1]

		# author
		author = part.find(class_ = 'author')
		if author:
			item['author'] = author.get_text(strip = True)

		# vote number
		vote = part.find(class_ = 'stats-vote')
		if vote:
			item['vote_num'] = vote.find(class_ = 'number').string

		# comment number
		comment = part.find(class_ = 'stats-comments')
		if comment:
			item['comment_num'] = comment.find(class_ = 'number').string

		# tag
		tag = part.find(class_ = 'stats-tag')
		if tag:
			item['tag'] = [s for s in tag.stripped_strings]
		
		# video
		video = part.find(class_ = 'video_holder')
		if video:
			video_src = video.source
			item['video_src'] = video_src.get('src')

		# image
		image = part.find(class_ = 'thumb')
		if image:
			img_src = image.img
			item['img_src'] = img_src.get('src')

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
		print 'author : ', item['author']
		print 'content : ', item['content']
		print 'pubtime : ', item['pubtime']
		print 'vote_num : ', item['vote_num']
		print 'comment_num : ', item['comment_num']
		print 'tag : ', ','.join(item['tag'])
		if item['img_src']:
			print 'img_src : ', item['img_src']
		if item['video_src']:
			print 'video_src : ', item['video_src'] 
		print ''

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
	q = Qiubai() 
	q.process()









