from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import Slide, Banner, Category, Item, Variation
from order.models import Order, OrderProduct
from order.forms import OrderForm

from django.conf import settings
from django.core.mail import send_mail


class IndexView(ListView):
    queryset = Slide.objects.all().order_by('date_added')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['banners'] = Banner.objects.filter(active=True)
        context['featured'] = Item.objects.filter(
            featured=True).order_by('last_modified')

        return context


class ShopView(ListView):
    context_object_name = "products"
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Item.objects.filter(category__slug=self.kwargs['category']).order_by('-date_added')


class ProductView(CreateView):
    template_name = 'product.html'
    model = Order
    fields = ['name', 'email', 'contact', 'address']
    success_url = reverse_lazy('thankyou')

    def form_valid(self, form):
        form.instance.claiming = self.request.POST['claiming']
        form.instance.payment = self.request.POST['payment']

        #get items
        for var in Item.objects.get(slug=self.kwargs['product']).variations.all():
            product = get_object_or_404(Item, slug=self.kwargs['product'])
            variation = Variation.objects.get(slug=var.slug)
            quantity = self.request.POST['variation_' + var.slug]
            if int(quantity) != 0:
                OrderProduct.objects.create_product(quantity=quantity, variation=variation, product=product)

        #send mail
        send_mail('Subject here', 'Here is the message.', settings.EMAIL_HOST_USER, [form.instance.email], fail_silently=False)
        return super(ProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Item, slug=self.kwargs['product'])
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs['category']
        return context
