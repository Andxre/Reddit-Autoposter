import praw
import random
import re
import time
import os
import config
import idna

# reddit api login and authentication
reddit = praw.Reddit(client_id= config.client_id,
                     client_secret= config.client_secret,
                     username= config.username,
                     password= config.password,
                     user_agent= config.user_agent)


print('   ___        _       ______         _            ")
print('  / _ \      | |      | ___ \       | |           ')
print(' / /_\ \_   _| |_ ___ | |_/ /__  ___| |_ ___ _ __ ')
print(' |  _  | | | | __/ _ \|  __/ _ \/ __| __/ _ \ __|')
print(' | | | | |_| | || (_) | | | (_) \__ \ ||  __/ |   ')
print(' \_| |_/\__,_|\__\___/\_|  \___/|___/\__\___|_|   ')

print("Welcome to Andxre's Autoposter ")
print("You are currently logged in as: " + str(reddit.user.me()))

#What subreddit's to post on
#subreddits = ['cats', 'test']
subreddits = open("sublist.txt").readlines()
pos = 0

#parameters
title = input("Input the Title of your Post: ")
print("Title: " + str(title))
url = input("Input the URL of your Post: ")
print("URL: " + str(url))


#Function to Post on Subreddits
def post():
	global pos
	global subreddits

	try:
		subreddit = reddit.subreddit(subreddits[pos])
		subreddit.submit(title, url=url)
		pos += 1
		if (pos <= len(subreddits) - 1):
			print("Posting..")
			time.sleep(1)
			print("Posted..")
			post()
		else:
			print("Done")
			time.sleep(5)

	except praw.exceptions.APIException as e:
		print(e)
		if (e.error_type == "RATELIMIT"):
			delay = re.search("(\d+) minutes", e.message)

			if delay:
				delay_seconds = float(int(delay.group(1)) * 60)
				print("Sleeping for " + str(delay_seconds) + " seconds..")
				time.sleep(delay_seconds)
				print("Sleep Over, Posting..")
				post()
			else:
				delay = re.search("(\d+) seconds", e.message)
				delay_seconds = float(delay.group(1))
				print("Sleeping for " + str(delay_seconds) + " seconds..")
				time.sleep(delay_seconds)
				print("Sleep Over, Posting..")
				post()

#Execute Post Function
post()
