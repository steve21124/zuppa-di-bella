from bs4 import BeautifulSoup
import requests
from collections import Counter
from collections import Counter, defaultdict
from operator import itemgetter
import pymongo

def make_board_urllist(brand):
### make a list of first 5 pages of URLs based on brand search
	if len(brand) > 1:
		name = "-".join(brand)
		brand_url = "http://pinterest.com/search/?q=%s" %(name)
	else:
		brand_url = "http://pinterest.com/search/?q=%s" %(brand)

	url_list = []
	for i in range(5):
		new_url = ( brand_url+"&page=%d") %i 
		url_list.append(new_url) 
	return url_list


def make_user_list(url_list):
### now having the list of url, get list of users that pinned those pins
	user_list = []
	for url in url_list:
		try:
			page = requests.get(url)
			pinsoup = BeautifulSoup(page.content)
			pinners = get_pinners(pinsoup)
			user_list.extend(pinners)
		except Exception,e:
			pass
	return user_list #list of users that have pinned on this brand


def get_pinners(pinsoup):
### find sources of pins
	all_pinners = pinsoup.find_all("a","ImgLink") # <a href="/ivanaamai/" title="Ivana Amai" class="ImgLink">
	"""	an item in all_pinners

        <a href="/mia7of9/" title="Mia J" class="ImgLink">
          <img src="http://media-cache-ec0.pinterest.com/avatars/mia7of9_1333380083.jpg"
               alt="Profile picture of Mia J" />
        </a>
        <p>
    """
	pinners = []
	""" error message 
		<type 'NoneType'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<class 'bs4.element.Tag'>
		<type 'NoneType'>
	"""
	# i = 0
	for pinner in all_pinners:
	 	if pinner.a == None: #not sure how that works
			continue
		else:
			pinners.append(pinner.a.contents[0])
		# i += 1
	print pinners
	return pinners
	""" sample pin_source
		[u'thefancy.com', u'raspberryandred.blogspot.com', 
		u'rstyle.me', u'25.media.tumblr.com', u'mostbeautifull.net', 
		u'threadflip.com', u'rstyle.me', u'kingsunderlavenderskies.tumblr.com', 
		u'chrisanthemums.tumblr.com', u'laurenconrad.com', 
		u'whyilovetoshop.com', u'iknowhair.com', u'rstyle.me',
		 u'shopbop.com', u'community.boden.co.uk', u'zimbio.com', 
		 u'glamour.com', u'themessesofmen.tumblr.com']
	"""

def count_source(pin_source_list):
### feed all sources and generate a list of tuples with (count, domain)
	output = defaultdict(lambda: 0)
	for source in pin_source_list:
		try:
			domain = source.split(".")[-2]
			output[domain] += 1
		except IndexError:
			pass
	
	source_count = sorted(output.iteritems(),key=lambda (k,v): v,reverse=True)
	# print "source_count", sorted(output.iteritems(),key=lambda (k,v): v,reverse=True)
	return output

def connect_db():
	connect_string = "mongodb://pinterestalgo:pinterest2012@ds035617.mongolab.com:35617/pinterest"
	# mongodb://%s:%s@%s:%d/%s" % \
 #            (user, password, host, port, db_name)
	c = pymongo.connection.Connection(connect_string)
	return c['pinterest']


def main():
	global db
	db = connect_db()
	# db = db['pinterest'] #get collection named pinterest
	t = open("/Users/honeysnow/Desktop/python/beautifulsoup/datafiles/topbrands.txt")
	for line in t.readlines():
		brand = line.strip()
		print brand
		# brand = "gucci"
		all_pinners_list = []	
		url_list = make_board_urllist(brand)
		## need to make it into a loop
		
		user_list = make_user_list(url_list) 
		all_pinners_list.extend(user_list)
		# renamed_list = transform_boardname(board_list)
		# # print "BOARD LIST", renamed_list
		# """ BOARD LIST / renamed_list 
		# 	[u'fitness', u'beauty', u'home-sweet-home', u'words', u'sweetness',
	 # 		u'wanderlust', u'fooodism', u'infographics', u'items', u'nature', 
	 # 		u'love-in-the-bay', u'web-design', u'books ', u'demo-videos']
		# """
		for url in url_list: 
			# print find_board_url(username,board)
			if find_board_url(username, board) == None: 
				continue
			if len(find_board_url(username, board)) == 0:
				continue
			else:
				all_pinners_list.extend(find_board_url(username, board))
		# print "BOARD URL LIST", all_pinners_list
		"""BOARD URL LIST / board_url_list 
			[u'http://pinterest.com/michellelsun/fitness/', u'http://pinterest.com/michellelsun/beauty/', u'http://pinterest.com/michellelsun/beauty/?page=2', 
			u'http://pinterest.com/michellelsun/beauty/?page=3', 
			u'http://pinterest.com/michellelsun/home-sweet-home/', u'http://pinterest.com/michellelsun/home-sweet-home/?page=2', u'http://pinterest.com/michellelsun/words/', u'http://pinterest.com/michellelsun/words/?page=2', 
			u'http://pinterest.com/michellelsun/sweetness/', u'http://pinterest.com/michellelsun/wanderlust/', u'http://pinterest.com/michellelsun/fooodism/', u'http://pinterest.com/michellelsun/infographics/', 
			u'http://pinterest.com/michellelsun/items/', u'http://pinterest.com/michellelsun/nature/', u'http://pinterest.com/michellelsun/love-in-the-bay/', u'http://pinterest.com/michellelsun/web-design/', 
			u'http://pinterest.com/michellelsun/demo-videos/']
		"""
		pin_source_list = make_pin_source_list(board_url_list)
		"""pin_source_list 
			[u'yogurtyoga.tumblr.com', u'tumblr.com', u'loseweight-safe.com', 
			u'danceisuniversal.tumblr.com', u'dare-to-be-healthy.tumblr.com',
			u'fit-not-thin.tumblr.com', u'fitsugar.com', u'flickr.com', 
			u'migas.tumblr.com', u'tumblr.com', u'tumblr.com', u'tumblr.com', 
			u'theathenenoctua.tumblr.com', u'awelltraveledwoman.tumblr.com',
			u'fit-toned4summer.tumblr.com', u'youtube.com', u'tumblr.com', 
			u'sexydangerous.tumblr.com'...] 
			total length : 371 out of 461 total pins
		"""
		output = count_source(pin_source_list)
		# print output
		output_dict = {}
		output_dict['pins'] = output
		output_dict['username'] = username
		print output_dict
	# create mongodb database
		pinners = db.pinners
		pinners.insert(output_dict) #insert 

""" code that was used to update mongodb
for p in db.pinners.find():
     keys = p.keys()
     if "username" in keys:
             continue
     possible_names = [ k for k in keys if k != "_id" ]
     name = possible_names[0]
     p['pins'] = p[name]
     p['username'] = name
     del p[name]
     db.pinners.update({"_id": p["_id"]}, p)
"""

# class Pin(object):
# 	def __init__ (self, link):
# 		soup = get_soup(link)
# 		self.title = etsy_item_title(soup)
# 		self.price = etsy_price(soup)
# 		self.image_link = etsy_img_link(soup)
# 		self.pdt_link = link

if __name__ == '__main__':
	main()

# def find_board_url(username, boardname):
# 	pboard_url = "http://pinterest.com/%s/%s/" %(username,boardname)
# 	pinb = requests.get(pboard_url)
# 	pinsoup = BeautifulSoup(pinb.content)
# 	pin_num_div = pinsoup.find("div",{"id":"BoardStats"})
# 	try: 
# 		pin_num = pin_num_div.contents[3].contents[0]
# 		url_list = make_url_list(pin_num,pboard_url)
# 		return url_list
# 	except Exception,e: 
# 		pass #or print error
### find url_list (page 1-2) by injecting boardname

# def make_url_list(pin_num,pboard_url):
# ### make URL in infinite scrolling 
# ### http://pinterest.com/michellelsun/beauty/?page=3
# 	if int(pin_num) % 50 != 0:
# 		page_num = int(pin_num) / 50 + 1
# 	else:
# 		page_num = int(pin_num) / 50
# 	url_list = [pboard_url]
# 	i = 2
# 	while i <= page_num:
# 		new_url = ( pboard_url+"?page=%d") %i &page=5
# 		url_list.append(new_url) 
# 		i += 1
# 	return url_list