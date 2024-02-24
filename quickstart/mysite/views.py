from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Band


def band_listing(request):
    """A view of all bands"""
    bands = Band.objects.all()
    return render(request, "bands/band_Listing.html", {'bands': bands})


def register_band(request):
    """Processes band registration"""
    if request.method == "POST":
        form = forms.BandContactForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/url")

    else:
        form = forms.BandContactForm()

    return render(request, "bands/register.html", {"form": form})

@login_required
def my_protected_view(request):
    """A view that can only be accessed by logged-in users"""
    return render(request, "protected.html", {"current_user": request.user})
