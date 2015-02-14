from django.core.urlresolvers import reverse
from django.forms import models as model_forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import redirect

from shop.forms import BillingShippingForm, get_cart_item_formset
from shop.models import AddressModel, OrderExtraInfo, Product
from shop.models import Order
from shop.util.address import (
    assign_address_to_request,
    get_billing_address_from_request,
    get_shipping_address_from_request,
)
from shop.util.cart import get_or_create_cart
from shop.util.order import add_order_to_request, get_order_from_request
from shop.views import ShopTemplateView, ShopView, ShopTemplateResponseMixin
from shop.util.login_mixin import LoginMixin


class CheckoutSelectionView(LoginMixin, ShopTemplateView):
    template_name = 'shop/checkout/selection.html'

    def _get_dynamic_form_class_from_factory(self):
        """
        Returns a dynamic ModelForm from the loaded AddressModel
        """
        form_class = model_forms.modelform_factory(
            AddressModel, exclude=['user_shipping', 'user_billing'])
        return form_class

    def get_shipping_form_class(self):
        """
        Provided for extensibility.
        """
        return self._get_dynamic_form_class_from_factory()

    def get_billing_form_class(self):
        """
        Provided for extensibility.
        """
        return self._get_dynamic_form_class_from_factory()

    def create_order_object_from_cart(self):
        """
        This will create an Order object form the current cart, and will pass
        a reference to the Order on either the User object or the session.
        """
        print 'created'
        cart = get_or_create_cart(self.request)
        cart.update(self.request)
        order = Order.objects.create_from_cart(cart, self.request)
        request = self.request
        add_order_to_request(request, order)
        return order

    def get_shipping_address_form(self):
        """
        Initializes and handles the form for the shipping address.
        AddressModel is a model of the type defined in
        ``settings.SHOP_ADDRESS_MODEL``.
        The trick here is that we generate a ModelForm for whatever model was
        passed to us by the SHOP_ADDRESS_MODEL setting, and us this, prefixed,
        as the shipping address form. So this can be as complex or as simple as
        one wants.
        Subclasses of this view can obviously override this method and return
        any other form instead.
        """
        # Try to get the cached version first.
        form = getattr(self, '_shipping_form', None)
        if not form:
            # Create a dynamic Form class for the model specified as the
            # address model
            form_class = self.get_shipping_form_class()

            # Try to get a shipping address instance from the request (user or
            # session))
            shipping_address = get_shipping_address_from_request(self.request)
            if self.request.method == "POST":
                form = form_class(self.request.POST, prefix="ship",
                    instance=shipping_address)
            else:
                # We should either have an instance, or None
                if not shipping_address:
                    # The user or guest doesn't already have a favorite
                    # address. Instanciate a blank one, and use this as the
                    # default value for the form.
                    shipping_address = AddressModel()

                # Instanciate the form
                form = form_class(instance=shipping_address, prefix="ship")
            setattr(self, '_shipping_form', form)
        return form

    def get_billing_address_form(self):
        """
        Initializes and handles the form for the shipping address.
        AddressModel is a model of the type defined in
        ``settings.SHOP_ADDRESS_MODEL``.
        """
        # Try to get the cached version first.
        form = getattr(self, '_billing_form', None)
        if not form:
            # Create a dynamic Form class for the model specified as the
            # address model
            form_class = self.get_billing_form_class()

            # Try to get a shipping address instance from the request (user or
            # session))
            billing_address = get_billing_address_from_request(self.request)
            if self.request.method == "POST":
                form = form_class(self.request.POST, prefix="bill",
                    instance=billing_address)
            else:
                # We should either have an instance, or None
                if not billing_address:
                    # The user or guest doesn't already have a favorite
                    # address. Instansiate a blank one, and use this as the
                    # default value for the form.
                    billing_address = AddressModel()

                #Instanciate the form
                form = form_class(instance=billing_address, prefix="bill")
            setattr(self, '_billing_form', form)
        return form

    def get_billing_and_shipping_selection_form(self):
        """
        Get (and cache) the BillingShippingForm instance
        """
        form = getattr(self, '_billingshipping_form', None)
        if not form:
            if self.request.method == 'POST':
                form = BillingShippingForm(self.request.POST)
            else:
                form = BillingShippingForm()
            self._billingshipping_form = form
        return form

    def save_addresses_to_order(self, order, shipping_address):
        """
        Provided for extensibility.
        Adds both addresses (shipping and billing addresses) to the Order
        object.
        """
        order.set_shipping_address(shipping_address)
        order.save()

    def get_extra_info_form(self):
        """
        Initializes and handles the form for order extra info.
        """
        # Try to get the cached version first.
        form = getattr(self, '_extra_info_form', None)
        if not form:
            # Create a dynamic Form class for the model
            form_class = model_forms.modelform_factory(OrderExtraInfo, exclude=['order'])
            if self.request.method == 'POST':
                form = form_class(self.request.POST)
            else:
                form = form_class()
            setattr(self, '_extra_info_form', form)
        return form

    def save_extra_info_to_order(self, order, form):
        if form.cleaned_data.get('text'):
            extra_info = form.save(commit=False)
            extra_info.order = order
            extra_info.save()

    def post(self, *args, **kwargs):
        """ Called when view is POSTed """
        shipping_form = self.get_shipping_address_form()
        extra_info_form = self.get_extra_info_form()
        if shipping_form.is_valid() and extra_info_form.is_valid():

            # Add the address to the order
            shipping_address = shipping_form.save()
            order = self.create_order_object_from_cart()
            print 'ok1'
            self.save_addresses_to_order(order, shipping_address)

            # The following marks addresses as being default addresses for
            # shipping and billing. For more options (amazon style), we should
            # remove this
            assign_address_to_request(self.request, shipping_address,
                shipping=True)

            # add extra info to order
            self.save_extra_info_to_order(order, extra_info_form)

            return HttpResponseRedirect(reverse('thankyou'))

        return self.get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        This overrides the context from the normal template view
        """
        ctx = super(CheckoutSelectionView, self).get_context_data(**kwargs)

        shipping_address_form = self.get_shipping_address_form()
        extra_info_form = self.get_extra_info_form()
        ctx.update({
            'shipping_address': shipping_address_form,
            'billing_shipping_form': billingshipping_form,
            'extra_info_form': extra_info_form,
        })
        return ctx


class ThankYouView(LoginMixin, ShopTemplateView):
    template_name = 'shop/thankyou.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShopTemplateView, self).get_context_data(**kwargs)

        # put the latest order in the context only if it is completed
        order = get_order_from_request(self.request)
        if order and order.status == Order.COMPLETED:
            ctx.update({'order': order, })

        cart_object = get_or_create_cart(self.request)
        cart_object.empty()

        return ctx


class CartItemDetail(ShopView):
    """
    A view to handle CartItem-related operations. This is not a real view in
    the sense that it is not designed to answer to GET or POST request nor to
    display anything, but only to be used from AJAX.
    """
    action = None

    def dispatch(self, request, *args, **kwargs):
        """
        Submitting form works only for "GET" and "POST".
        If `action` is defined use it dispatch request to the right method.
        """
        if not self.action:
            return super(CartItemDetail, self).dispatch(request, *args,
                **kwargs)
        if self.action in self.http_method_names:
            handler = getattr(self, self.action, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Update one of the cartItem's quantities. This requires a single
        ``item_quantity`` POST parameter, but should be posted to a properly
        RESTful URL (that should contain the item's ID):
        http://example.com/shop/cart/item/12345
        """
        cart_object = get_or_create_cart(self.request)
        item_id = self.kwargs.get('id')
        # NOTE: it seems logic to be in POST but as tests client shows
        # with PUT request, data is in GET variable
        # TODO: test in real client
        # quantity = self.request.POST['item_quantity']
        try:
            quantity = int(self.request.POST['item_quantity'])
        except (KeyError, ValueError):
            return HttpResponseBadRequest("The quantity has to be a number")
        cart_object.update_quantity(item_id, quantity)
        return self.put_success()

    def delete(self, request, *args, **kwargs):
        """
        Deletes one of the cartItems. This should be posted to a properly
        RESTful URL (that should contain the item's ID):
        http://example.com/shop/cart/item/12345
        """
        cart_object = get_or_create_cart(self.request)
        item_id = self.kwargs.get('id')
        try:
            cart_object.delete_item(item_id)
            return self.delete_success()
        except ObjectDoesNotExist:
            raise Http404

    # success hooks
    def success(self):
        """
        Generic hook by default redirects to cart
        """
        if self.request.is_ajax():
            return HttpResponse('Ok<br />')
        else:
            return HttpResponseRedirect(reverse('cart'))

    def post_success(self, product, cart_item):
        """
        Post success hook
        """
        return self.success()

    def delete_success(self):
        """
        Post delete hook
        """
        return self.success()

    def put_success(self):
        """
        Post put hook
        """
        return self.success()

    # TODO: add failure hooks


class CartDetails(ShopTemplateResponseMixin, CartItemDetail):
    """
    This is the actual "cart" view, that answers to GET and POST requests like
    a normal view (and returns HTML that people can actually see)
    """

    template_name = 'shop/cart.html'
    action = None

    def get_context_data(self, **kwargs):
        # There is no get_context_data on super(), we inherit from the mixin!
        ctx = {}
        cart = get_or_create_cart(self.request)
        cart.update(self.request)
        ctx.update({'cart': cart})
        ctx.update({'cart_items': cart.get_updated_cart_items()})
        return ctx

    def get(self, request, *args, **kwargs):
        """
        This is lifted from the TemplateView - we don't get this behavior since
        this only extends the mixin and not templateview.
        """
        context = self.get_context_data(**kwargs)
        formset = get_cart_item_formset(cart_items=context['cart_items'])
        context.update({'formset': formset, })
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        """
        This is to *add* a new item to the cart. Optionally, you can pass it a
        quantity parameter to specify how many you wish to add at once
        (defaults to 1)
        """
        try:
            product_id = int(self.request.POST['add_item_id'])
            product_quantity = int(self.request.POST.get('add_item_quantity', 1))
        except (KeyError, ValueError):
            return HttpResponseBadRequest("The quantity and ID have to be numbers")
        product = Product.objects.get(pk=product_id)
        cart_object = get_or_create_cart(self.request, save=True)
        cart_item = cart_object.add_product(product, product_quantity)
        cart_object.save()
        return self.post_success(product, cart_item)

    def delete(self, *args, **kwargs):
        """
        Empty shopping cart.
        """
        cart_object = get_or_create_cart(self.request)
        cart_object.empty()
        return self.delete_success()

    def put(self, *args, **kwargs):
        """
        Update shopping cart items quantities.
        Data should be in update_item_ID=QTY form, where ID is id of cart item
        and QTY is quantity to set.
        """
        context = self.get_context_data(**kwargs)
        try:
            formset = get_cart_item_formset(cart_items=context['cart_items'],
                    data=self.request.POST)
        except ValidationError:
            return redirect('cart')
        if formset.is_valid():
            formset.save()
            return self.put_success()
        context.update({'formset': formset, })
        return self.render_to_response(context)
