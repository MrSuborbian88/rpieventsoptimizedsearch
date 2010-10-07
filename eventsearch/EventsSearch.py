#FA2010
#Event Search

import abc
from SearchBase import SearchBase

class EventsSearch(SearchBase):
    results = None
    keywords = {}
    domains = []
    
    def search(self, query, rpp):
        self.results = super(EventsSearch, self).search(query, rpp)
        self.printResults()

    def printResults(self):
        for res in self.results:
            print res.title#.encode("utf8")
            print res.desc#.encode("utf8")
            print res.url#.encode("utf8")
            print

    def initDomains(self):
	domain_file = open("domains.txt",'r')
	for line in domain_file:
		print line
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
        value = 0
        orders = []
        pair = ()
        
        #search titles and descriptions for keywords
	#this doesn't work, needs to be fixed or removed
        for res in self.results:
            tmpTitle = (res.title.encode('utf-8').lower().strip('().,:-\'\"')).split(" ")
            tmpDesc = (res.desc.encode('utf-8').lower().strip('().,:-\'\"')).split(" ")
            for key in self.keywords.keys():
                for t in tmpTitle:
                    if key == t:
                        value+=self.keywords[key]
                for t in tmpDesc:
                    if key == t:
                        value+=self.keywords[key]
	    value += self.addDomainValue(res)
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
            print

        

