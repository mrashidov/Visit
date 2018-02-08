from django.views.generic import TemplateView
from places.models import Category,City,Place
def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
	return out
	
from places.forms import CityForm
from places.forms import SearchForm
class IndexView(TemplateView):
	template_name='_home.html'
	http_methods_name=['get']
	def get_context_data(self, **kwargs):
		from places.models import City
		if self.request.method =='GET':
			form = CityForm(self.request.GET)
			context = super(IndexView, self).get_context_data(**kwargs)
			search_form = SearchForm(self.request.GET)
		context['city_form']=form
		context['search_form'] = search_form
		return context

class AboutView(TemplateView):
	template_name='_about.html'
	http_methods_name=['get']
	def get_context_data(self, **kwargs):
		context = super(AboutView, self).get_context_data(**kwargs)
		context['search_form'] = SearchForm(self.request.GET)
		return context



def is_not_stopword(string):
	stopwords = {"a","about","above","across","after","afterwards","again","against","all","almost","alone",
	"along","already","also","although","always","am","among","amongst","amoungst","amount","an","and","another",
	"any","anyhow","anyone","anything","anyway","anywhere","are","around","as","at","back","be","became",
	"because","become","becomes","becoming","been","before","beforehand","behind","being","below","beside",
	"besides","between","beyond","bill","both","bottom","but","by","call","can","cannot","cant","co","computer",
	"con","could","couldnt","cry","de","describe","detail","do","done","down","due","during","each","eg","eight",
	"either","eleven","else","elsewhere","empty","enough","etc","even","ever","every","everyone","everything",
	"everywhere","except","few","fifteen","fify","fill","find","fire","first","five","for","former","formerly",
	"forty","found","four","from","front","full","further","get","give","go","had","has","hasnt","have","he",
	"hence","her","here","hereafter","hereby","herein","hereupon","hers","herse","him","himse","his","how",
	"however","hundred","i","ie","if","in","inc","indeed","interest","into","is","it","its","itse","keep",
	"last","latter","latterly","least","less","ltd","made","many","may","me","meanwhile","might","mill",
	"mine","more","moreover","most","mostly","move","much","must","my","myse","name","namely","neither",
	"never","nevertheless","next","nine","no","nobody","none","noone","nor","not","nothing","now",
	"nowhere","of","off","often","on","once","one","only","onto","or","other","others","otherwise","our",
	"ours","ourselves","out","over","own","part","per","perhaps","please","put","rather","re","same","see",
	"seem","seemed","seeming","seems","serious","several","she","should","show","side","since","sincere",
	"six","sixty","so","some","somehow","someone","something","sometime","sometimes","somewhere","still",
	"such","system","take","ten","than","that","the","their","them","themselves","then","thence","there",
	"thereafter","thereby","therefore","therein","thereupon","these","they","thick","thin","third","this",
	"those","though","three","through","throughout","thru","thus","to","together","too","top","toward",
	"towards","twelve","twenty","two","un","under","until","up","upon","us","very","via","was","we","well",
	"were","what","whatever","when","whence","whenever","where","whereafter","whereas","whereby","wherein",
	"whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","whose","why",
	"will","with","within","without","would","yet","you","your","yours","yourself","yourselves"}
	return string.lower() not in stopwords;

class SearchView(TemplateView):
	template_name = "_search.html"
	http_methods_name=['get']

	def get_context_data(self, **kwargs):
		from django.db.models import Q
		from functools import reduce
		context = super(SearchView, self).get_context_data(**kwargs)
		context['search_form'] = SearchForm(self.request.GET)
		query = self.request.GET.get('query')
		try:
			cityId = self.request.session['city'];
			city = City.objects.get(pk=cityId)
		except KeyError:
			city=None;
		if query:
			queries = list(filter(is_not_stopword,query.split()))
			print(queries)
			bigQuery = reduce(lambda q, f: q | Q(description__contains=f)|Q(name__contains=f), queries, Q())
			context['result'] = Place.objects.filter(bigQuery)
		else:
			context['result'] = Place.objects.filter()
		if city:
			context['result'] = context['result'].filter(city=city)
		context['search_form'] = SearchForm(self.request.GET)
		return context
