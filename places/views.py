from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *

# Create your views here.
class CityView(generic.ListView):
    #Search bar and list of categories
    model = Place
    paginate_by = 20
    template_name = 'places/city_view.html'
    http_method_names = ['get']
    context_object_name = 'places'
    
    def get_queryset(self):
        city = get_object_or_404(City,pk=self.request.session['city'])
        return Place.objects.filter(city=city).order_by('-name')
    def get_context_data(self,*args, **kwargs):
        data = super(CityView,self).get_context_data(**kwargs)
        id = self.request.session['city']
        if id:
            data['city'] = get_object_or_404(City, pk=id)
            data['category_list'] = Category.objects.all()
        data['search_form'] = SearchForm(self.request.GET)
        return data

def redirect_to_city(request):
    if request.method=='GET':
        city_id = request.GET.get('city')
        request.session['city'] = city_id
        city = get_object_or_404(City,pk=city_id)
        return HttpResponseRedirect(reverse('places:city',args=[city.slug]))


class PlaceView(generic.TemplateView):
    template_name = 'places/place_view.html'
    http_method_names = ['get']
    def get_context_data(self,*args,**kwargs):
        from django.utils import timezone
        context = super(PlaceView, self).get_context_data(**kwargs)
        context['city'] = get_object_or_404(City, pk= self.request.session['city'])
        print(self.kwargs)
        place = get_object_or_404(Place, pk=self.kwargs.get('id'))
        context['place'] = place
        context['search_form'] = SearchForm(self.request.GET)
        try:
            tmp = Schedule.objects.get(place=place).to_list()
            context['schedule']=[(x[0],get_str_interval(x[1],x[2])) for x in tmp]
            print(context['schedule'])
            context['opened'] = Schedule.is_opened(place,timezone.now())
        except ObjectDoesNotExist:
            context['opened'] = None
            context['schedule']=[]
        try:
            context['phones'] = PlacePhoneNumber.objects.get(place=place);
        except ObjectDoesNotExist:
            context['phones'] = []
        return context
    

