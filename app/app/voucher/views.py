#coding: utf-8
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from ads.models import Ad
from customer.models import UserProfile
from forms import PromotionForm, NewVoucherForm
from models import Promotion, Voucher
from report import write_to_pdf
from wqti_util.json import to_json_response


class PromotionFormView(CreateView):
    form_class = PromotionForm
    template_name = 'voucher/form_promotion.html'

    def get_form_kwargs(self):
        kwargs = super(PromotionFormView, self).get_form_kwargs()
        ad = Ad.objects.get(slug=self.kwargs['slug'])
        kwargs['ad'] = ad
        return kwargs

    def get_success_url(self):
        messages.success(self.request,
            u'Seu cupom foi criado com sucesso.')
        return reverse('my_ads')


class MyPromotionListView(ListView):
    template_name = 'voucher/my_promotion.html'
    model = Promotion

    def get_context_data(self, *args, **kwargs):
        context = super(MyPromotionListView, self).\
                                get_context_data(*args, **kwargs)
        user = self.request.user.get_profile().get_final_profile()
        context['my_promotions'] = Promotion.objects.filter(ad__user=user)
        return context


class TesteDetailView(DetailView):
    template_name = 'voucher/voucher_pdf.html'
    context_object_name = 'voucher'
    model = Voucher


class PromotionDetailView(DetailView):
    template_name = 'voucher/promotion_detail.html'
    context_object_name = 'voucher'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Promotion.objects, pk=self.kwargs['pk'])


class VoucherCreateView(CreateView):
    template_name = 'voucher/form_create_voucher.html'
    form_class = NewVoucherForm

    def get_context_data(self, *args, **kwargs):
        context = super(VoucherCreateView, self).\
                                            get_context_data(*args, **kwargs)
        promotion = Promotion.objects.get(pk=self.kwargs['pk'])
        context['promotion'] = promotion
        return context

    def get_form_kwargs(self):
        kwargs = super(VoucherCreateView, self).get_form_kwargs()
        promotion = Promotion.objects.get(pk=self.kwargs['pk'])
        kwargs['promotion'] = promotion
        user = UserProfile.objects.get(email=self.request.user)
        kwargs['user'] = user
        return kwargs

    def get_success_url(self):
        return reverse('create_voucher_pdf', kwargs={'pk': self.object.id})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VoucherCreateView, self).dispatch(*args, **kwargs)


@csrf_exempt
@to_json_response
def disable_promotion(request, pk):
    try:
        promotion = Promotion.active.get(pk=pk)
    except Promotion.DoesNotExist:
        return {'status': False}
    if promotion.is_active:
        promotion.is_active = False
    else:
        promotion.is_active = True
    promotion.save()
    return {'status': True}


def voucher_pdf(request, pk):
    voucher = Voucher.objects.get(pk=pk)
    coupons = voucher.promotion.coupons
    limit = voucher.promotion.limit_vouchers
    if coupons < limit:
        voucher.promotion.new_coupon()
        c = Context({'voucher': voucher, 'MEDIA_URL': settings.MEDIA_URL,
                                            'STATIC_URL': settings.STATIC_URL})
        return write_to_pdf('voucher/voucher_pdf.html', c, 'virtuallia')
    return HttpResponseRedirect(reverse('my_promotion_detail',
                                        kwargs={'pk': voucher.promotion.id}))


class AllPromotionListView(ListView):
    template_name = 'voucher/all_promotions.html'
    queryset = Promotion.active.all()
    context_object_name = 'list_promotions'
