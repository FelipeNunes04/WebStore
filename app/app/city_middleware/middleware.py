#coding: utf-8
from ads.models import Ad
from locations.models import City, State


class DefineCity(object):

    def process_request(self, request):
        l = request.GET.get('l', '')
        s = request.GET.get('s', '')

        city = request.session.get('city')
        if city:
            list_ads = Ad.active.filter(city=city)
        else:
            list_ads = Ad.objects.all()

        if l == '0':
            if list_ads:
                request.session['city'] = None
            else:
                request.session['city'] = City.objects.\
                                    get(city=u'São Paulo', state__state='SP')
        elif l != '':
            request.session['city'] = City.objects.get(id=l)
        elif not 'city' in request.session:
            # ip = request.META['REMOTE_ADDR']
            if City.objects.filter(city=u'São Paulo').exists():
                request.session['city'] = City.objects.\
                                    get(city=u'São Paulo', state__state='SP')
        elif not list_ads:
            request.session['city'] = City.objects.\
                                    get(city=u'São Paulo', state__state='SP')

        if s == '0':
            request.session['state'] = None
        elif s != '':
            request.session['state'] = State.objects.get(id=s)
        elif not 'state' in request.session:
            if State.objects.filter(state=u'SP').exists():
                request.session['state'] = State.objects.get(state=u'SP')
        elif not list_ads:
            request.session['state'] = State.objects.get(state=u'SP')
