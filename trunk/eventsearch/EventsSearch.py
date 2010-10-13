#FA2010
#Event Search

import abc
from SearchBase import SearchBase
from xgoogle.search import SearchResult
from RSS import ns, CollectionChannel, TrackingChannel

import time
import datetime
class EventsSearch(SearchBase):
    results = None
    keywords = {}
    domains = []
    locations = []
    query = None
    def search(self, query, rpp):
        self.results = super(EventsSearch, self).search(query, rpp)
        #self.printResults()
	self.query = query
    def printResults(self):
        for res in self.results:
            print res.title#.encode("utf8")
            print res.desc#.encode("utf8")
            print res.url#.encode("utf8")
            print
    def createURL(self, start, end):
	
	url = "http://events.rpi.edu/webcache/v1.0/rssRange/"+ str(start.year) + str(start.month)+ str(start.day)+"/"+ str(end.year)+str(end.month)+ str(end.day)+"/list-rss/no--filter.rss"
	print url
	return url
    def addRSS(self):
	#Indexes RSS data by item URL
	tc = TrackingChannel()
	TodayDate = datetime.date.today()
	StartDate = TodayDate - datetime.timedelta(days=3)
	EndDate = TodayDate + datetime.timedelta(days=5)
	
	#Returns the RSSParser instance used, which can usually be ignored
	tc.parse(self.createURL(StartDate,EndDate))

	RSS10_TITLE = (ns.rss10, 'title')
	RSS10_DESC = (ns.rss10, 'description')

	#You can also use tc.keys()
	items = tc.listItems()
	for item in items:
	    #Each item is a (url, order_index) tuple
	    url = item[0]
	    #print "URL:", url
	    #Get all the data for the item as a Python dictionary
	    item_data = tc.getItem(item)
	    title = item_data.get(RSS10_TITLE, "(none)")
	    desc = item_data.get(RSS10_DESC, "(none)").replace("<br/>","").replace("\n","").replace("\r","")
	    #print "Title:", item_data.get(RSS10_TITLE, "(none)")
	    #print "Description:", item_data.get(RSS10_DESC, "(none)")
	    for q in self.query.split():
		if(title.lower().find(q.lower()) >= 0 or desc.lower().find(q.lower())):
			self.results.append(SearchResult(title, url, desc))
			print q
			break

    def initLocations(self):
	#one location per line
	location_file = open("locations.txt",'r')
	for line in location_file:
		self.locations.append(line.strip('\r\n'))

    def addLocationValue(self, res):
	for location in self.locations:
		if self.query.find(location) >= 0:
			return 2
		if res.desc.find(location) >= 0:
			return 1
	return 0

    def initDomains(self):
	domain_file = open("domains.txt",'r')
	for line in domain_file:
		for domain in line.split():
			self.domains.append(domain)

    def addDomainValue(self, res):
	for domain in self.domains:
		if res.url.find(domain) >= 0:
			return 1
	return 0

    def initDictionary(self):
        key_file = open("keywords.txt",'r')
        count = 1
        for line in key_file:
            for word in line.split():
                self.keywords[word]=count
                count = count+1

    def reorder(self):
        self.initDictionary()
	self.initDomains()
	self.initLocations()
	self.addRSS()
        value = 0
        orders = []
        pair = ()
        
        #search titles and descriptions for keywords
	#this doesn't work, needs to be fixed or removed
        for res in self.results:
	    value += self.addDomainValue(res)
	    value += self.addLocationValue(res)
            pair = res, value
            orders.append(pair)
            pair = ()
            value = 0

        #order results based on values
        def cmpfun(a,b):
            return cmp(b[1],a[1])
        orders.sort(cmpfun)

        for i in orders:
            print i[0].title, "RANK = ", i[1]
            print i[0].desc
	    print i[0].url
            print

        

