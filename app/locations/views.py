#coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from models import City, State, ZipCode, Area
from ads.models import Ad
from wqti_util.json import to_json_response


class LocationsTemplateView(TemplateView):
    template_name = 'locations/locations.html'

    def get_context_data(self, **kwargs):
        context = super(LocationsTemplateView, self).get_context_data(**kwargs)
        context['locations'] = City.objects.all()
        return context


@csrf_exempt
@to_json_response
def refresh_city(request):
    state = request.POST.get('state', None)
    if state:
        city = Ad.active.filter(state=state).values('city', 'city__city').\
                order_by('city').distinct()
        if city.exists():
            return {'city': list(city)}
        return {'empty': True}
    else:
        return {'empty': True}


@csrf_exempt
@to_json_response
def refresh_address(request):
    zipcode = request.POST.get('zipcode', None)
    if zipcode:
        try:
            zip_code = ZipCode.objects.get(zip_code=zipcode)
            address = zip_code.address
            state = zip_code.city.state
            city = zip_code.city
            area = zip_code.area

            if state:
                state = State.objects.get(state=state)

            if city:
                city = City.objects.get(city=city, state=state)

            if area:
                area = Area.objects.get(area=area, city=city)

            return {
                    'address': address,
                    'state': state.state,
                    'id_state': state.id,
                    'area': area.area,
                    'id_area': area.id,
                    'city': city.city,
                    'id_city': city.id,
                    }
        except ZipCode.DoesNotExist:
            return {
                    'empty': True,
                    'list_state': [(i['id'], i['state'])\
                        for i in State.objects.all().values('id', 'state')],
                    }
    else:
        return {'empty': True}
