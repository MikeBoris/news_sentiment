"""
	Read RSS feeds for 5 news sources
	For each feed:
		Calc sentiment polarity
		print summary ordered by polarity like

		Source 	Polarity
		------	--------
		news3	0.52232
		news1	0.12345
		news4	0.02312
		news5	-0.0192
		news2	-0.1432
"""
import feedparser
from textblob import TextBlob

RSS_FEEDS = {
	'bbc': 'http://feeds.bbci.co.uk/news/rss.xml?edition=us',
	'cnn': 'http://rss.cnn.com/rss/edition.rss%20',
	'abc': 'http://feeds.abcnews.com/abcnews/topstories',
	'nyt': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
	'fox': 'http://feeds.foxnews.com/foxnews/latest',
	'reu': 'http://feeds.reuters.com/Reuters/domesticNews',
	'eco': 'http://www.economist.com/feeds/print-sections/71/united-states.xml',
	'wpo': 'http://feeds.washingtonpost.com/rss/national',
	'hap': 'http://hosted.ap.org/lineups/USHEADS-rss_2.0.xml?SITE=SCAND&SECTION=HOME',
	'npr': 'http://www.npr.org/rss/rss.php?id=1001',
	'usa': 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories'

}

def fetch_parse(rss_feed):
	d = feedparser.parse(rss_feed)
	return d

def get_block_of_text(d):
	"""function to combine title, summary, description, tag text from feedparser obj
	d is feedparser parsed object"""
	entry_lst = []
	if len(d.entries) > 0:
		for j in range(len(d.entries)):
			# select each entries object
			e = d.entries[j]
			# for each entry get ti, cont, desc, tags
			try:
				entry_lst.append(d.entries[j].title)
			except:
				print('No object \'title\' found')
			try:
				entry_lst.append(d.entries[j].description)
			except:
				pass #print('No object \'descritpion\' found')
			#try:
			#	entry_lst.append(d.entries[j].content[0]['value'])
			#except:
			#	print('No object \'summary\' found')
			# collect all tags
			try:
				for i in range(len(e.tags)):
					entry_lst.append(e.tags[i].term)
			except:
				pass #print('No object \'e.tags\'')
		# return list concatenated as block of text
		return ' '.join(entry_lst)
	else:
		print('d.entries object is length 0 or doesn\'t exist')

def get_text_polarity(block_of_text):
	blob = TextBlob(block_of_text)
	return blob.sentiment.polarity

def byFreq(pair):
	""" utility function for sorting score_dict"""
	return pair[1]

def print_results(RSS_FEEDS):
	news_score_dict = {}
	for k in RSS_FEEDS:
		t = fetch_parse(RSS_FEEDS[k])
		textBlock = get_block_of_text(t)
		pol = get_text_polarity(textBlock)
		# assign polarity score to news source in score_dict
		news_score_dict[k] = pol
	# sort by highest to lowest polarity
	items = list(news_score_dict.items())
	items.sort(key=byFreq, reverse=True)
	for key, value in items:
		print('Polarity for {0} is {1}'.format(key, round(value, 3)))

if __name__=='__main__':
	try:
		print_results(RSS_FEEDS)
	except:
		print('didn\'t do it')


