from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import urllib.request
import json


class CurrencyConverter:
    rates = {}

    def __init__(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': 'Currency Bot'})
        data = urllib.request.urlopen(req).read()
        data = json.loads(data.decode('utf-8'))
        self.rates = data["rates"]

    def convert(self, to_currency):
            return self.rates[to_currency]


def index(request):
    userdata = {
        'username': request.session['username'],
        'id': request.session['id'],
        'location': request.session['location'],
    }

    items = Items.objects.all()
    amount_mod = 1.00
    amount_sign = "BDT"

    if request.session['location'] == "USA":
        amount_sign = "USD"
        bdt_converter = CurrencyConverter("http://data.fixer.io/api/latest?access_key=613212d138e913ef0d74e299cb89c9cc&symbols=BDT")
        # bdt_res = bdt_converter.convert("BDT")
        # bdt_response = bdt_res[3]
        bdt_response = bdt_converter[4]
        bdt_response = "%.2f" % bdt_response
        usd_converter = CurrencyConverter("http://data.fixer.io/api/latest?access_key=613212d138e913ef0d74e299cb89c9cc&symbols=USD")
        # usd_res = usd_converter.convert("USD")
        # usd_response = usd_res[3]
        usd_response = usd_converter[4]
        usd_response = "%.2f" % usd_response
        amount_mod = usd_response/bdt_response

    context = {
        'data': userdata,
        'items': items,
        'amount_mod': amount_mod,
        'amount_sign': amount_sign,
    }
    return render(request, 'account/home.html', context)


def login(request):
    if 'logged_in' in request.session:
        return redirect('account:index')
    return render(request, 'account/login.html')


def login_validate(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = Users.objects.get(username=username)
            request.session['logged_in'] = True
            request.session['username'] = user.username
            request.session['id'] = user.pk
            request.session['location'] = user.location
        except Exception as ex:
            messages.error(request, 'Username Mismatched')
            return redirect('account:login')
    return render(request, 'account/login.html')


def logout(request):
    try:
        del request.session['logged_in']
        return redirect('account:login')
    except:
        return redirect('account:login')
