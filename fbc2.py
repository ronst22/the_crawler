#!/usr/bin/python

import time
import urllib2,urllib, cookielib, shelve
from tornado_client import Client
from HTMLParser import HTMLParser
from argparse import ArgumentParser
from smtplib import SMTP

SELF_MAIL_SERVICE = "smtp.gmail.com"
SELF_MAIL_PORT = 25
SELF_MAIL_ADDRESS = "hacker4good1@gmail.com"
SELF_MAIL_PASSWORD = "blashit123"

DB_FILE = "fbc.db"
LOG_FILE = "fbc.log"

class FacebookCrawlerMailNotifier:
	def __init__(self, other_mail):
	    self.__other_mail = other_mail
            self.server = SMTP("%s:%d" % (SELF_MAIL_SERVICE, SELF_MAIL_PORT))

	def create_mail_connection(self):
	    self.server.ehlo()
	    self.server.starttls()
            self.server.login(SELF_MAIL_ADDRESS, SELF_MAIL_PASSWORD)

        def send_link(self, link):
	    msg = "\r\n".join([
  		"From: %s" % (SELF_MAIL_ADDRESS),
  		"To: %s" % self.__other_mail,
  		"Subject: Offensive behavior detected on your profile watch",
  		"",
  		link
  		])
	    self.server.sendmail(SELF_MAIL_ADDRESS, self.__other_mail, msg)

# create a subclass and override the handler methods
class FullStoryGetterHTMLParser(HTMLParser):
    def __init__(self):
	HTMLParser.__init__(self)
	self.counter = 0
	self.in_post = False
	self.last_href = ""
	self.post_links = []

    def handle_starttag(self, tag, attrs):

	if self.in_post:
            self.counter += 1
	    if "a" == tag:
		for i in attrs:
		    if i[0] == "href":
			self.last_href = i[1]

	if "div" in tag and True in ["u_0" in i[1] and "id" in i[0] for i in attrs]:
            self.in_post = True

    def handle_endtag(self, tag):

	if self.counter == 0 and self.in_post:
            self.in_post = False

        if self.in_post:
            self.counter -= 1

    def handle_data(self, data):
	if self.in_post:
	    if data == "Full Story":
		self.post_links.append(self.last_href)

class GetDataHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
	self.is_style = False
	self.in_post = False
        self.post_data = ""
	self.counter = 0

    def handle_starttag(self, tag, attrs):
        if self.in_post:
            self.counter += 1

        if "div" in tag and True in ["u_0" in i[1] and "id" in i[0] for i in attrs]:
            self.in_post = True

	if "style" in tag:
	    self.is_style = True
	pass

    def handle_endtag(self, tag):
	self.is_style = False

        if self.counter == 0 and self.in_post:
            self.in_post = False

        if self.in_post:
            self.counter -= 1

	pass

    def handle_data(self, data):
	if not self.is_style:
            self.post_data += data + " "


class FacebookCrawler:

    jar = cookielib.CookieJar()
    cookie = urllib2.HTTPCookieProcessor(jar)
    opener = urllib2.build_opener(cookie)

    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "ISO-8859-1",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "m.facebook.com"
    }

    def login(self, user, password):
        try:
            params = urllib.urlencode({'email':user,'pass':password,'login':'Log+In'})
            req = urllib2.Request('http://m.facebook.com/login.php?m=m&refsrc=m.facebook.com%2F', params, self.headers)
            res = self.opener.open(req)
            html = res.read()

        except urllib2.HTTPError, e:
            print e.msg
        except urllib2.URLError, e:
            print e.reason[1]
        return True

    def fetch(self,url):
        req = urllib2.Request(url,None,self.headers)
        res = self.opener.open(req)
        return res.read()

def main():
	arg_parser = ArgumentParser()
	arg_parser.add_argument("username", metavar="username", type=str)
	arg_parser.add_argument("password", metavar="password", type=str)
	arg_parser.add_argument("profile_link", metavar="profile_link", type = str)
	arg_parser.add_argument("user_email", metavar="user_email", type=str)
	args = arg_parser.parse_args()

	offensive_detector = Client()

	fb_crawler = FacebookCrawler()
	fb_crawler.login(args.username, args.password)
        log_file = open(LOG_FILE,"w+")
                        
	while True:
                mail_notifyer = FacebookCrawlerMailNotifier(args.user_email)
                mail_notifyer.create_mail_connection()
                
                fb_db = shelve.open(DB_FILE)

                if not fb_db.has_key("link_list"):
                        fb_db["link_list"] = []

                current_link_list = fb_db["link_list"]
                
		link_parser = FullStoryGetterHTMLParser()
		link_parser.feed(fb_crawler.fetch("https://m.facebook.com/" + args.profile_link.split("/")[-1]))

                cutted_list = []
                for link in link_parser.post_links:
                        cutted_list.append(link.split("&refid")[0])

                for post_link in cutted_list:
			data_parser = GetDataHTMLParser()
			data_parser.feed(fb_crawler.fetch("https://m.facebook.com/" + post_link))
			if offensive_detector.is_offensive(data_parser.post_data):
				if not post_link in current_link_list:
                                        log_file.write(data_parser.post_data + "\n")
                                        log_file.write("sending mail...\n")
                                        log_file.flush()
					current_link_list.append(post_link)
					mail_notifyer.send_link("https://m.facebook.com/" + post_link)

                fb_db["link_list"] = current_link_list
                fb_db.close()
                
                mail_notifyer.server.quit()

if __name__ == "__main__":
	main()
