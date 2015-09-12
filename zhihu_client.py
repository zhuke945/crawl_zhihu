# -*- coding:utf-8 -*-
__author__='zhuke'
import re,os
import time,datetime
import json
import requests
import importlib
from bs4 import BeautifulSoup
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

def login():

	url_base='http://www.zhihu.com'
	url_captcha=url_base+'captcha.gif'
	s=requests.session()
	login_data={}
	header={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		
		'DNT':'1',
		'Host':'www.zhihu.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
	}
	
	def get_xsrf(url):
		r=s.get(url,headers=header)
		xsrf=re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)',r.text)
		if xsrf==None:
			return ''
		else:
			return xsrf.group(0)

	# xsrf=get_xsrf(url_base)
	# login_data['_xsrf']=xsrf.encode('utf-8')
	# login_data['remember_me']='true'

	# captcha_url='http://www.zhihu.com/captcha.gif'
	# captcha=s.get(captcha_url,stream=True)
	# print captcha
	# f=open('captcha.gif','wb')
	# for line in captcha.iter_content(10):
	# 	f.write(line)
	# f.close()
	# captcha_str=raw_input(r"CheckCode:")
	# login_data['email']=os.environ.get('email_addr')
	# login_data['password']=os.environ.get('email_pass')
	# login_data['captcha']=captcha_str
	# os.remove('captcha.gif')
	# r=s.post('http://www.zhihu.com/login/email',data=login_data,headers=header)
	# print r

	def get_home_page():

		r=s.get(url_base,headers=header)
		#print r.text.encode('utf-8')
		home_page=re.search(r'(?<=a\shref=")[^"]*(?="\sclass="zu-top-nav-userinfo ")',r.text.encode('utf-8'))
		if home_page:
			return url_base+home_page.group(0)
	

	def get_personal_information():
		start_time=time.time()
		homt_page_url=get_home_page()
		print homt_page_url
		r=s.get(homt_page_url,headers=header)
		
		location_arr=re.search(r'(?<=span\sclass="location item"\stitle=")[^"]*(?=">)',r.text.encode('utf-8'))
		if location_arr:
			print 'Personal Details'
			print 'Location = %s' %location_arr.group(0),

		#Business 
		business=re.search(r'(?<=span\sclass="business item"\stitle=")[^"]*(?=">)',r.text.encode('utf-8'))
		if business:
			print 'Business is %s ' %business.group(0)

		with open("data.txt", "wb") as f:
			f.write(location_arr.group(0))
			f.write(',')
			f.write(business.group(0))

		print time.time()-start_time
	get_personal_information()

if __name__=='__main__':
	login()
	




	