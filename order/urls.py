from django.conf.urls import patterns, url
from shop.util.decorators import cart_required
from .views import CheckoutSelectionView, ThankYouView, CartDetails, CartItemDetail

cart_url = patterns('',
    url(r'^cart/delete/$', CartDetails.as_view(action='delete'),  # DELETE
        name='cart_delete'),
    url(r'^cart/item/$', CartDetails.as_view(action='post'),  # POST
        name='cart_item_add'),
    url(r'^cart/$', CartDetails.as_view(), name='cart'),  # GET
    url(r'^cart/update/$', CartDetails.as_view(action='put'),
        name='cart_update'),

    # CartItems
    url(r'^cart/item/(?P<id>[0-9]+)$', CartItemDetail.as_view(),
        name='cart_item'),
    url(r'^cart/item/(?P<id>[0-9]+)/delete$',
        CartItemDetail.as_view(action='delete'),
        name='cart_item_delete'),
)

urlpatterns = patterns('',
                       url(r'^checkout/$', cart_required(CheckoutSelectionView.as_view()),
                           name='checkout_selection'
                           ),
                       url(r'^thankyou/$', cart_required(ThankYouView.as_view()),
                           name='thankyou'
                           ),
                       )

urlpatterns += cart_url
