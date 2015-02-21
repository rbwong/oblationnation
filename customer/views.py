from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

import datetime

from .models import UserProfile


class ProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'userprofile.html'
    model = UserProfile
    fields = ['email', 'contact', 'address']
    success_url = reverse_lazy('auth:userprofile')
    success_message = "Profile was updated successfully"

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        return super(ProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = ONProfile.objects.all()[:1].get()
        context['user'] = self.request.user
        context['request'] = self.request
        return context


@login_required
def logoutnow(request):
    logout(request)

    return HttpResponseRedirect(    reverse('index'))

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            profile = UserProfile.objects.get(user=user)
        except:
            profile = UserProfile(user=user)
        profile.gender = response.get('gender')
        profile.save()
