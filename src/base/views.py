#
# Created on Sun Oct 09 2022
#
# The MIT License (MIT)
# Copyright (c) 2022 Rohit Geddam, Arun Kumar, Teja Varma, Kiron Jayesh, Shandler Mason
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import json
import re

from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SignUpForm, SubleasingForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .filters import ProfileFilter
from .matching import matchings

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from base.tokens import account_activation_token
from django.views import View
import requests
import requests_cache
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
requests_cache.install_cache('scrapper_cache',
                             backend='sqlite',
                             expire_after=3600)


class ActivateAccount(View):
    """Account activation"""

    def get(self, request, uidb64, token, *args, **kwargs):
        """GET method for the Account activation."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
                user, token
        ):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(
                request,
                ("Your account have been confirmed. We have logged you in."),
            )
            return redirect("home")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")


class SignUpView(generic.CreateView):
    """Sign up View"""

    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        current_site = get_current_site(self.request)
        subject = "Activate Your FindMyRoomie Account"
        message = render_to_string(
            "emails/account_activation_email.html",
            {
                "user": self.object,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.object.pk)),
                "token": account_activation_token.make_token(self.object),
            },
        )
        self.object.email_user(subject, message)

        messages.success(
            self.request,
            ("Please Confirm your email to complete registration."),
        )

        return HttpResponseRedirect(self.get_success_url())


def home(request):
    """Render Home Page"""
    user_count = get_user_model().objects.all().count()
    return render(request, "index.html", {"user_count": user_count})


@login_required()
def profile(request):
    """Render profile page"""
    if not request.user.profile.is_profile_complete:
        messages.error(request, "Please complete your profile first!")
        return redirect("profile_edit")

    profile = Profile.objects.get(user=request.user)

    return render(request, "pages/profile.html", {"profile": profile})


@login_required()
def profile_edit(request):
    """Render Edit Profile Page"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.is_profile_complete = True
            print(p.profile_photo)
            p.save()

            return redirect("profile")

    person = Profile.objects.all()
    form = ProfileForm(instance=profile)
    return render(
        request, "pages/profile_edit.html", {"form": form, "profiles": person}
    )


@login_required()
def findpeople(request):
    """Render findpeople page"""
    qs = Profile.objects.filter(visibility=True).exclude(user=request.user)
    f = ProfileFilter(request.GET, queryset=qs)
    return render(request, "pages/findpeople.html", {"filter": f})


# this is new
@login_required()
def messageboard(request):
    """Render message board page"""
    return render(request, "pages/messageboard.html")


@login_required()
def myroom(request):
    """Render Myroom page based on Profile Completion"""
    if not request.user.profile.is_profile_complete:
        messages.error(request, "Please complete your profile first!")
        return redirect("profile_edit")

    matches = matchings(request.user)

    return render(request, "pages/myroom.html", {"matches": matches})

@login_required()
def subleasing(request):
    """Render Subleasing Page"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = SubleasingForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.is_profile_complete = True
            print(p.profile_photo)
            p.save()

            return redirect("scrapper_page")

    person = Profile.objects.all()
    form = SubleasingForm(instance=profile)
    return render(
        request, "pages/subleasing.html", {"form": form, "profiles": person}
    )

@login_required()
def scrapper_search_page(request):
    """Render the scrapper search bar"""
    return render(request, "pages/scrapper_search_page.html")


@login_required()
def search(request):
    """Render apartment search on Zillow"""
    results = []
    if request.method == "GET":
        query = request.GET.get('search')
        query = query.lower()
        if query != "" and all(x.isalpha() or x.isspace() for x in query):
            req_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                          '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/107.0.0.0 Safari/537.36 '
            }

            with requests.Session() as s:

                data_list = []

                # Pages 1 - 10
                for i in range(1, 11):
                    if i != 1:
                        url = 'https://www.zillow.com/homes/for_rent/' + query + '/' + str(i) + '_p/'
                    else:
                        url = 'https://www.zillow.com/homes/for_rent/' + query
                    req = s.get(url, headers=req_headers)
                    data = json.loads(re.search(r'!--(\{"queryState".*?)-->', req.text).group(1))
                    data_list.append(data)

                df = pd.DataFrame()

                def make_frame(frame):
                    for i in data_list:
                        for item in i['cat1']['searchResults']['listResults']:
                            frame = frame.append(item, ignore_index=True)
                    return frame

                df = make_frame(df)

                df = df.drop('hdpData', 1)

                df = df.drop_duplicates(subset='zpid', keep="last")

                df['zestimate'] = df['zestimate'].fillna(0)
                df['best_deal'] = df['unformattedPrice'] - df['zestimate']
                df = df.sort_values(by='best_deal', ascending=True)

                results = df[['id', 'address', 'beds', 'baths', 'area', 'price', 'zestimate', 'best_deal']].head(
                    20).values.tolist()
    return render(request, 'pages/scrapper_search.html', {'query': query, 'results': results})


def user_logout(request):
    """Log out and redirect to Home Page"""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")
