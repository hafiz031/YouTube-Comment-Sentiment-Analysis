from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Firefox()


# Enter url to your youtube video
driver.get("")

retry = r = 30
sleep_time = 1

prev_scroll_height = -1
comment_objects = []

while True:
	'''
	Scrolling 500px in vertical direction in each iteration to load more comments.
	A sleep is introduced to wait for a while to load the comment.
	Finally, the scroll height is calculated in order to keep track if we still scrolling or not.
	If scroll height doesn't get changed it means we are not scrolling anymore and it is time to break the loop.
	'''
	driver.execute_script("window.scrollBy(0, 500);")
	time.sleep(sleep_time)
	scroll_height = driver.execute_script("return document.documentElement.scrollHeight")

	'''
	If the prev_scroll_height and scroll_height are the same, it means we have reached to the end or the driver is having
	trouble while scrolling (possibly for poor internet speed).
	'''
	if prev_scroll_height == scroll_height:
		r -= 1
		print("[INFO] Having problems in scrolling, retry remaining: ", r, "/", retry)
		if r == 0:
			print("[INFO] Cannot scroll more")
			break
	else:
		print("[INFO] Scrolling...retry count is reset to: ", retry)
		prev_scroll_height = scroll_height
		r = retry


print("[INFO] Scrolling finished! Now parsing all visible comments")
try:
	comment_objects = driver.find_elements_by_class_name("style-scope ytd-comment-renderer")
except:
	pass


list_of_yt_comments_dicts = []

for comment_object in comment_objects:
	'''
	All the text items of each of the comments are parsed as comment_object.text
	...and we are interested in only the first 4 fields (generally out of 5 fields) namely:
		 'username', 
		 'timestamp', 
		 'comment (this field can appear as multiple fields because of newline(s) within a single comment)', 
		 'like_count (might not be available if there is no like in that comment)'
		 and REPLY (textual label of reply button is also parsed).
	All these fields are separated by newlines.

	So after splitting them if there are any likes on that comment it should be in the second last position.
	Hence, checking if the second last field is a number or not. If it is a number then it denotes the like_count.
	like_count = 0 otherwise.

	Finally creating a dictionary from each of the comments and appending it to the list.
	'''
	splits = comment_object.text.split('\n')
	username = splits[0]
	timestamp = splits[1]
	comment = ""
	
	try:
		# checking if there is any like on that comment
		if splits[-2].isnumeric():
			like_count = splits[-2]
			# concatenating rest portion as they are from same comment
			comment = ''.join(map(str, splits[2:-2])) 
		else:
			like_count = 0
			# concatenating rest portion as they are from same comment
			comment = ''.join(map(str, splits[2:-1])) 
	except:
		like_count = 0

	list_of_yt_comments_dicts.append({
			"username"   : username,
			"comment"    : comment,
			"timestamp"  : timestamp,
			"like_count" : like_count
		})


print("[INFO] Getting video title and channel name in order to make a meaningful output filename")

import re

try:
	video_title = driver.find_element_by_xpath("//yt-formatted-string[@class = 'style-scope ytd-video-primary-info-renderer']").text + " "
	'''
	Video title may contain illegal character(s) which are not allowed in a filename.
	If any such character(s) are available substituting / replacing them with '-'
	The outermost [] just means char class and we are considering the chars inside of it.
	'''
	channel_name = re.sub(r"[<>:\"\'`/\\|?*]", "-", channel_name)
except:
	video_title = ""

try:
	channel_name = "[" + driver.find_element_by_xpath("//ytd-channel-name[@class = 'style-scope ytd-video-owner-renderer']").text + "] "
	channel_name = re.sub(r"[<>:\"\'`/\\|?*]", "-", channel_name)
except:
	channel_name = ""


import csv
csv_filename = video_title + channel_name + "comments.csv"

print("[INFO] Filename: ", csv_filename)

columns = ["username", "comment", "timestamp", "like_count"]

try:
    with open(csv_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = columns)
        writer.writeheader()
        for data in list_of_yt_comments_dicts:
            writer.writerow(data)
    print("[INFO] All parsed comments are written to disk successfully!")
except IOError:
    print("[INFO] I/O error")