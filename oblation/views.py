from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Slide, Banner, Category, Item, Variation, ONProfile
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

        context['profile'] = ONProfile.objects.all()[:1].get()
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

        context['profile'] = ONProfile.objects.all()[:1].get()
        context['categories'] = Category.objects.all()

        context['user'] = self.request.user
        context['request'] = self.request

        return context

    def get_queryset(self):
        return Item.objects.filter(category__slug=self.kwargs['category']).order_by('-date_added')


class ProductView(CreateView):
    template_name = 'product.html'
    model = Order
    fields = ['name', 'email', 'contact', 'address', 'remarks']
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
        product = get_object_or_404(Item, slug=self.kwargs['product'])
        oblation_profile = ONProfile.objects.all()[:1].get()

        # hook user
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user

        # get items
        total_price = 0
        items_message = '<h3>'+ product.name +'</h3>'
        items_message += '<table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">'
        for var in Item.objects.get(slug=self.kwargs['product']).variations.all():
            product = get_object_or_404(Item, slug=self.kwargs['product'])
            variation = Variation.objects.get(slug=var.slug)
            quantity = self.request.POST['variation_' + var.slug]
            total_price += product.unit_price*int(quantity)
            items_message += '<tr align="left" valign="top"><th><label>' + product.name + ' - ' + variation.name  + ':</label></th><td>' + quantity + '</td><td>' + str(product.unit_price*int(quantity)) + '</td></tr>'

            if int(quantity) != 0:
                OrderProduct.objects.create_product(
                    quantity=quantity, variation=variation, product=product)

        #addd shipping cost
        if self.request.POST['claiming'] == 'Shipping':
            total_price += oblation_profile.shipping
            items_message += '<tr align="left" valign="top"><th></th><td><b>Shipping</b></td><td>' + str(oblation_profile.shipping) + '</td></tr>'
        items_message += '<tr align="left" valign="top"><th></th><td><b>Total</b></td><td>' + str(total_price) + '</td></tr>'
        items_message += '</table>'

        # send mail
        details_message = '<h3>Basic Info</h3>'
        details_message += '<table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">'
        details_message += '<tr align="left" valign="top"><th><label>Name:</label></th><td>' + self.request.POST['name'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Contact:</label></th><td>' + self.request.POST['contact'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Email:</label></th><td>' + self.request.POST['email'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Address:</label></th><td>' + self.request.POST['address'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Remarks:</label></th><td>' + self.request.POST['remarks'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Payment Method:</label></th><td>' + self.request.POST['payment'] + '</td></tr>'
        details_message += '<tr align="left" valign="top"><th><label>Claiming Method:</label></th><td>' + self.request.POST['claiming'] + '</td></tr>'
        details_message += '</table>'

        top_message = '<h3>Good day!</h3><p>This is to confirm that we have received your order.</p><p>Please make sure to pay the downpayment/full payment so that we can process your order/s. Please also check if the details of your order are correct. If there are any changes in your order, just send another response and note in the remarks section that it is a change of order.</p><p>Thank you!</p>'
        footer_message = '<a href="http://oblationnation.upce.net/"><img src="http://oblationnation.upce.net/static/images/logo.png" title="Grocery Shoppe" alt="Grocery Shoppe" class="img-responsive"></a>'
        complete_message = top_message + '<br>' + details_message + items_message + '<br>' + footer_message
        mail.send(
            form.instance.email,
            'upoblationnation@gmail.com',
            subject= 'Order Confirmation for Oblation Nation - ' + product.name,
            message='Hi there!',
            html_message=complete_message,
            priority='now',
        )

        return super(ProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        try:
            context['userprofile'] = UserProfile.objects.get(
                user=self.request.user)
        except:
            context['userprofile'] = False
        context['request'] = self.request

        context['profile'] = ONProfile.objects.all()[:1].get()
        context['product'] = get_object_or_404(
            Item, slug=self.kwargs['product'])
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs['category']
        return context
