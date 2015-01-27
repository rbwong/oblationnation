from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Slide, Banner, Category, Item


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


class ProductView(DetailView):
    template_name = 'product.html'

    def get_object(self):
        return get_object_or_404(Item, slug=self.kwargs['product'])

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
