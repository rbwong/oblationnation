from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Slide, Banner, Category, Item, Variation
from order.models import Order, OrderProduct
from customer.models import UserProfile

from post_office import mail


class IndexView(ListView):
    queryset = Slide.objects.all().order_by('date_added')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        context['request'] = self.request

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

        context['user'] = self.request.user
        context['request'] = self.request

        return context

    def get_queryset(self):
        return Item.objects.filter(category__slug=self.kwargs['category']).order_by('-date_added')


class ProductView(CreateView):
    template_name = 'product.html'
    model = Order
    fields = ['name', 'email', 'contact', 'address']
    success_url = reverse_lazy('thankyou')

    def get_initial(self):
        try:
            user = self.request.user
            userprofile = UserProfile.objects.get(user=self.request.user)

            return {'name': user.get_full_name, 'email': userprofile.email, 'contact': userprofile.contact, 'address': userprofile.address}
        except:
            return {}

    def form_valid(self, form):
        form.instance.claiming = self.request.POST['claiming']
        form.instance.payment = self.request.POST['payment']

        #hook user
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user

        # get items
        for var in Item.objects.get(slug=self.kwargs['product']).variations.all():
            product = get_object_or_404(Item, slug=self.kwargs['product'])
            variation = Variation.objects.get(slug=var.slug)
            quantity = self.request.POST['variation_' + var.slug]
            if int(quantity) != 0:
                OrderProduct.objects.create_product(
                    quantity=quantity, variation=variation, product=product)

        # send mail
        mail.send(
            form.instance.email,
            'upoblationnation@gmail.com',
            subject='My email',
            message='Hi there!',
            html_message='Hi <strong>there</strong>!',
            priority='now',
        )

        return super(ProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        try:
            context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        except:
            context['userprofile'] = False
        context['request'] = self.request

        context['product'] = get_object_or_404(
            Item, slug=self.kwargs['product'])
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs['category']
        return context
