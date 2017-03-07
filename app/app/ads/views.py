# coding: utf-8
import os
from uuid import uuid4
from PIL import Image
from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.comments.models import Comment
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, CreateView, FormView
from wqti_util.json import to_json_response
from category.models import Activity, OptionGroup
from locations.models import City, Area, ZipCode
from voucher.models import Promotion
from forms import AdContactForm, AdIndicateForm, EditAdForm, EditImageAdForm,\
    PhotoFormSet, EditVideoAdForm, SignatureForm, NewAdForm, PhotoHiddenFormSet
from models import Ad, Photo, Signature


class EditAdUpdateView(UpdateView):
    template_name = 'ads/edit_ad.html'
    form_class = EditAdForm
    context_object_name = 'ad'

    def get_context_data(self, *args, **kwargs):
        context = super(EditAdUpdateView, self).get_context_data(*args,
                                                                    **kwargs)
        context['image_form'] = EditImageAdForm(instance=self.object)
        context['video_form'] = EditVideoAdForm(instance=self.object)
        context['photo_form'] = PhotoFormSet(instance=self.object)
        context['state'] = City.objects.values('state').distinct()
        context['city'] = City.objects.filter(state=self.object.state)
        context['area'] = Area.objects.filter(city=self.object.city)
        context['photos'] = Photo.objects.filter(ad=self.object)
        for activities in Activity.objects.filter(ad=self.object):
            context['activities'] = activities.id
        return context

    def get_object(self, queryset=None):
        signatures = self.request.user.get_profile().get_final_profile().\
                                                            signature_set.all()
        return Ad.objects.get(signature__in=signatures,\
                                                    slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('my_ads')


class EditImageUpdateView(UpdateView):
    template_name = 'ads/edit_ad.html'
    form_class = EditImageAdForm
    context_object_name = 'ad'

    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(EditImageUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = Ad.objects.get(slug=self.kwargs['slug'])
        return obj

    def get_success_url(self):
        return reverse('edit_ad', kwargs=self.kwargs)


class EditVideoUpdateView(UpdateView):
    template_name = 'ads/edit_ad.html'
    form_class = EditVideoAdForm
    context_object_name = 'ad'

    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(EditVideoUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = Ad.objects.get(slug=self.kwargs['slug'])
        return obj

    def get_success_url(self):
        return reverse('edit_ad', kwargs=self.kwargs)


class NewSignatureFormView(CreateView):
    template_name = 'ads/new_signature.html'
    form_class = SignatureForm

    def get_form_kwargs(self):
        kwargs = super(NewSignatureFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request,
            u'Sua assinatura foi criada com sucesso, aguarde e  você'
                                        u' receberá o boleto para pagamento.')
        return reverse('new_ad', kwargs={'signature_id': self.object.pk})


class NewAdFormView(FormView):
    form_class = NewAdForm

    def get_initial(self):
        return {'signature': self.kwargs['signature_id']}

    def get_template_names(self):
        signature = get_object_or_404(Signature, pk=self.\
                    kwargs['signature_id'], customer__user=self.request.user)
        if signature.calculate_ads_available() > 0:
            return 'ads/new_ad.html'
        return 'ads/new_ad_unavailable.html'

    def get_form_kwargs(self):
        kwargs = super(NewAdFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['signature'] = self.kwargs['signature_id']
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(NewAdFormView, self)\
            .get_context_data(*args, **kwargs)
        context['photo_form'] = PhotoFormSet(self.request.POST or None,
                                                self.request.FILES or None)
        context['hidden_form'] = PhotoHiddenFormSet(self.request.POST
                                        or None, self.request.FILES or None)
        return context

    def get_success_url(self):
        return reverse('my_ads')

    def form_valid(self, form):
        messages.success(self.request, u'Anúncio criado com sucesso.')
        photo_form = PhotoHiddenFormSet(self.request.POST or None, self.
                                                        request.FILES or None)
        if photo_form.is_valid():
            obj = form.save()
            for photo in photo_form.save(commit=False):
                photo.ad = obj
                photo.save()
            return super(NewAdFormView, self).form_valid(form)
        return super(NewAdFormView, self).form_invalid(form)


@require_POST
def edit_photo_view(request, slug):
    obj = get_object_or_404(Ad, slug=slug)
    photo_form = PhotoFormSet(request.POST, request.FILES, instance=obj)
    if photo_form.is_valid():
        photo_form.save()
    return redirect(reverse('edit_ad', kwargs={'slug': slug}))


def view_ad(request, slug, extra_content={}):
    '''Página do anúncio'''
    ad = get_object_or_404(Ad, slug=slug)

    city = request.session.get('city')

    if 'submit-indicate' in request.POST:
        form_indicate = AdIndicateForm(request.POST)
        if  form_indicate.is_valid():
            form_indicate.save(slug)
            messages.success(request,
                                'Sua indicação foi enviada com sucesso.')
            form_indicate = AdIndicateForm()
            form_contact = AdContactForm()
        else:
            form_contact = AdContactForm()
    elif 'submit-contact' in request.POST:
        form_contact = AdContactForm(request.POST)
        if form_contact.is_valid():
            form_contact.save(slug)
            messages.success(request, 'Mensagem foi enviada com sucesso.'
                                                u' Entraremos em contato.')
            form_indicate = AdIndicateForm()
            form_contact = AdContactForm()
        else:
            form_indicate = AdIndicateForm()

    if not request.POST:
        form_indicate = AdIndicateForm()
        form_contact = AdContactForm()

    qs_list_area = Area.objects.all()

    list_ads = Ad.active.filter(category=ad.category)
    qs_list_area = None

    qs_promotions = Promotion.active.filter(ad=ad)
    qs_coupons = qs_promotions.filter(type_promotion='coupon')
    qs_valley_toast = qs_promotions.filter(type_promotion='valley_toast')

    if city:
        list_ads = list_ads.filter(Q(city=city, is_national=False) |
            Q(is_national=True))
        area = list_ads.values('area')
        qs_list_area = Area.objects.filter(pk__in=area)

    activities = list_ads.values('activities__id').distinct()
    qs_list_activity = Activity.objects.filter(pk__in=activities)\
                                                    .order_by('ordering')
    extra_content.update({
        'ad': ad,
        'form_contact': form_contact,
        'form_indicate': form_indicate,
        'qs_list_area': qs_list_area,
        'list_activity': qs_list_activity,
        'qs_coupons': qs_coupons,
        'qs_valley_toast': qs_valley_toast,
    })
    ad.add_views()
    return render_to_response('ads/ads_detail.html', extra_content,
                                context_instance=RequestContext(request))


@csrf_exempt
@to_json_response
def disable_ad(request, slug):
    try:
        ad = Ad.objects.filter(user=request.user.get_profile().\
                                            get_final_profile()).get(slug=slug)
    except Ad.DoesNotExist:
        return {'status': False}
    if ad.is_active:
        ad.is_active = False
    else:
        ad.is_active = True
    ad.save()
    return {'status': True}


@csrf_exempt
@to_json_response
def get_city(request):
    state = request.POST.get('state', None)
    if state:
        city = ZipCode.objects.filter(zip_code=state).values('id', 'city')
        if city.exists():
            return {'city': list(city)}
        return {'empty': True}
    else:
        return {'empty': True}


@csrf_exempt
@to_json_response
def get_area(request):
    city = request.POST.get('city', None)
    if city:
        area = Area.objects.filter(city__pk=city).values('id', 'name', 'city')
        if area.exists():
            return {'area': list(area)}
        return {'empty': True}
    else:
        return {'empty': True}


# def activities_filter(request, category_id):
#     activities = [activity.id for activity in Activity.objects.\
#                               filter(categories__id=category_id)] or None
#     return to_json_response({
#         'activities': activities
#     })

def activities_filter(request, category_id, ad_id):
    activities = []
    if ad_id == '0':
        for activity in Activity.objects.filter(categories__id=category_id):
            ac_id = activity.id
            ac_name = activity.name
            activities.append({'id': ac_id,
                            'name': ac_name,
                            })
        return to_json_response({
            'activities': activities or None,
            })
    else:
        ad_activities = []
        ad = Ad.objects.get(id=ad_id)
        for ac in ad.activities.all():
            ad_activities.append({
                    'id': ac.id,
                })
        for activity in Activity.objects.filter(categories__id=category_id):
            ac_id = activity.id
            ac_name = activity.name
            activities.append({'id': ac_id,
                                'name': ac_name,
                                })
        return to_json_response({
            'activities': activities or None,
            'ad_activities': ad_activities or None,
            })

# def values_filter(request):
#     activities = request.GET.getlist('activities')
#     activities = Activity.objects.filter(pk__in=activities)
#     option_groups = activities.values('option_groups').distinct()
#     values = []
#     for option_group in option_groups:
#         if option_group['option_groups']:
#             option = OptionGroup.objects.\
#                                    get(pk=option_group['option_groups'])
#             values.extend([v.id for v in option.optionvalue_set.all()])
#     return to_json_response({
#         'values': values or None
#     })


def values_filter(request, ad_id):
    activities = request.GET.getlist('activities')
    activities = Activity.objects.filter(pk__in=activities)
    option_groups = activities.values('option_groups').distinct()
    values = []
    if ad_id == '0':
        for option_group in option_groups:
            if option_group['option_groups']:
                option = OptionGroup.objects.\
                                        get(pk=option_group['option_groups'])
                for v in option.optionvalue_set.all():
                    v_id = v.id
                    v_name = v.name
                    values.append({'id': v_id,
                                    'name': v_name,
                                    })
        return to_json_response({
            'values': values or None
        })
    else:
        ad_values = []
        ad = Ad.objects.get(id=ad_id)
        for v in ad.option_values.all():
            ad_values.append({
                'id': v.id,
                })
        for option_group in option_groups:
            if option_group['option_groups']:
                option = OptionGroup.objects.\
                                        get(pk=option_group['option_groups'])
                for v in option.optionvalue_set.all():
                    v_id = v.id
                    v_name = v.name
                    values.append({'id': v_id,
                                    'name': v_name,
                                    })
        return to_json_response({
            'values': values or None,
            'ad_values': ad_values or None,
        })


def image_upload(request):
    if request.POST:
        form = EditImageAdForm(request.POST, request.FILES)
        if form.is_valid():
            upload_full_path = '%s/ads/logo/%s/' % \
                            (settings.MEDIA_ROOT, datetime.now().year)
            media_path = '%sads/logo/%s' % (settings.MEDIA_URL,
                                            datetime.now().year)
            upload = request.FILES['image']
            filename = '%s.%s' % (uuid4(), upload.name.split('.')[-1])
            dest = open(os.path.join(upload_full_path, filename), 'wb+')

            for chunk in upload.chunks():
                dest.write(chunk)
            dest.close()
            size = 194, 194
            thumb_root = '%s/thumb-logo.%s' % (upload_full_path, filename)
            base_image = Image.open(os.path.\
                                        join(upload_full_path, filename), 'r')
            base_image.thumbnail(size)
            base_image.save(thumb_root)
            return HttpResponse('{"image_url": "%s/thumb-logo.%s", \
                                "image": "ads/logo/%s/%s", \
                                "image_save": "ads/logo/%s/thumb-logo.%s"}'
                % (media_path, filename,
                    datetime.now().year, filename,
                    datetime.now().year, filename,
                    ))
            # return to_json_response({
            #           'image_url':"%s/thumb.%s" % (media_path, filename),
            #           'image': 'ads/%s/%s' % (datetime.now().year, filename)
            #           })

    return to_json_response({
        'error': 'error'
    })


def photos_upload(request):
    if request.POST:
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            list_photos = []
            for image in request.FILES:
                upload = request.FILES[image]
                upload_full_path = '%s/ads/%s/' % \
                                (settings.MEDIA_ROOT, datetime.now().year)
                media_path = '%sads/%s' % \
                                (settings.MEDIA_URL, datetime.now().year)

                filename = '%s.%s' % (uuid4(), upload.name.split('.')[-1])
                dest = open(os.path.join(upload_full_path, filename), 'wb+')

                for chunk in upload.chunks():
                    dest.write(chunk)
                dest.close()
                size = 104, 86
                thumb_root = '%s/thumb-photo.%s' % (upload_full_path, filename)
                base_image = Image.open(os.path.\
                                        join(upload_full_path, filename), 'r')
                base_image.thumbnail(size)
                base_image.save(thumb_root)
                list_photos.append({
                    'image_url': '%s/thumb-photo.%s' % (media_path, filename),
                    'image': 'ads/%s/%s' % (datetime.now().year, filename)
                })

            return HttpResponse('{"list_photos": "%s" }' % list_photos)
        else:
            return HttpResponse("{'formset': %s}" % formset)
    return HttpResponse("{ 'error': 'error'}")


def images_delete(request):
    for images in request.GET.getlist('images_path'):
        try:
            image_full_path = '%s/%s' % (
                                settings.MEDIA_ROOT, images)
            os.remove(image_full_path)
            return to_json_response({'ok': 'ok'})
        except Exception, e:
            return to_json_response({'error': e})
    return to_json_response({
        'message': 'Nenhuma imagem selecionada'
    })


def authorize_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    ad = Ad.objects.get(pk=comment.object_pk)
    if request.user.is_authenticated():
        user = request.user.get_profile().get_final_profile()
        if user == ad.user:
            comment.is_public = True
            comment.save()
            return render_to_response('ads/comment_authorized.html', {},
                                    context_instance=RequestContext(request))
        return Http404
    url = reverse('customer_signin')
    next = reverse('authorize_comment', kwargs={'pk': pk, })
    messages.warning(request, 'É necessario estar logado para autorizar o' +
                                                             u' comentário.')
    return redirect('%s?next=%s' % (url, next))


def block_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    ad = Ad.objects.get(pk=comment.object_pk)
    if request.user.is_authenticated():
        user = request.user.get_profile().get_final_profile()
        if user == ad.user:
            comment.is_public = False
            comment.save()
            return render_to_response('ads/comment_block.html', {},
                                    context_instance=RequestContext(request))
        return Http404
    url = reverse('customer_signin')
    next = reverse('authorize_comment', kwargs={'pk': pk, })
    messages.warning(request, 'É necessario estar logado para bloquear' +
                                                            u'o comentário.')
    return redirect('%s?next=%s' % (url, next))
