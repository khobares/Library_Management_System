
# Import necessary classes
from django.shortcuts import render
from django.http import HttpResponse
from libapp.models import Book, DVD, Libuser, Libitem, Suggestion
from libapp.forms import SuggestionForm, SearchlibForm, RegisterForm
from django.conf.urls import patterns, url
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import random


# Create your views here.
def index(request):

    # booklist = Book.objects.all() [:10]
    # dvdlist = DVD.objects.all().order_by('-pubyr')[:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of books: ' + '</p>'
    # response.write(heading1)
    # for book in booklist:
    #     para = '<p>' + str(book) + '</p>'
    #     response.write(para)
    #
    # heading2 = '<p>' + 'List of dvds: ' + '</p>'
    # response.write(heading2)
    # for dvd in dvdlist:
    #     para = '<p>' + str(dvd) + str(DVD.objects.values('pubyr').filter(pubyr__contains=dvd.pubyr)) + '</p>'
    #     response.write(para)
    # return response

    itemlist = Libitem.objects.all().order_by('title')[:10]
    return render(request, "libapp/index.html", {'itemlist': itemlist})


def about(request):
    # response  HttpResponse()
    # response.write('This is a Library app')
    # return response
    if 'about_visits' in request.COOKIES:
        aboutVisits = int(request.COOKIES['about_visits']) + 1
    else:
        aboutVisits = 1
    response = render(request, 'libapp/about.html', {'aboutVisits': aboutVisits})
    response.set_cookie('about_visits', aboutVisits, 300)
    return response


def detail(request, item_id):
    try:
        item = Libitem.objects.get(pk=item_id)
        if item.itemtype == 'Book':
            item = Book.objects.get(pk=item_id)
        else:
            item = DVD.objects.get(pk=item_id)
        return render(request, 'libapp/detail.html', {'item': item})
    except:
        raise Http404


def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist})


def newitem(request):
    suggestionss = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form': form, 'suggestions': suggestionss})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form': form, 'suggestions': suggestionss})


def searchlib(request):
    if request.method == 'GET':
        form = SearchlibForm()
        return render(request, 'libapp/searchlib.html')
    else:
        return HttpResponseRedirect(reverse('libapp:searchlib'))


def result(request):
    if 'title'or 'author' or 'maker' in request.GET:
        title = request.GET['title']
        author = request.GET['author']
        maker = request.GET['maker']
        try:
            if author and maker:
                message = 'Wow! Please fill in either author or maker '
                return render(request,'libapp/result.html', {'message':message})
            elif title:
                items = DVD.objects.filter(title__icontains=title) or Book.objects.filter(title__icontains=title)
            elif title and maker:
                items = DVD.objects.filter(title__icontains=title).filter(maker__icontains=maker)
            elif title and author:
                items = Book.objects.filter(title__icontains=title).filter(author__icontains=author)
            elif maker:
                items = DVD.objects.filter(maker__icontains=maker)
            elif author:
                items = Book.objects.filter(author__icontains=author)
            return render(request, 'libapp/result.html', {'items':items, 'title':title, 'author':author, 'maker':maker})
        except:
            message = 'You submitted an empty form'
        return render(request, 'libapp/result.html', {'message':message})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        request.session.set_expiry(3600)

        if user:
            if user.is_active:
                # get or set luckynum
                if 'luckynum' in request.session:
                    luckynum = request.session.get('luckynum')
                else:
                    request.session['luckynum'] = str(random.randint(1,9))
                login(request, user)
                return HttpResponseRedirect(reverse('libapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'libapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))


def myitems(request):
    if request.user.is_authenticated():
        try:
            Libuser.objects.get(username=request.user)
        except:
            message = 'You are not a Libuser'
            return render(request, 'libapp/myitems.html', {'message':message})
        myitem=Libitem.objects.filter(checked_out=True).filter(user=request.user)
        return render(request, 'libapp/myitems.html',{'myitem':myitem})
    else:
        message = 'login please'
        return render(request, 'libapp/myitems.html', {'message':message})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            firstname=request.POST['first_name']
            lastname=request.POST['last_name']
            user = Libuser.objects.create_user(username, email, password)
            user.last_name=lastname
            user.first_name=firstname
            user.save()
            return HttpResponseRedirect(reverse( 'libapp:index'))
        else:
            return render(request, 'libapp/register.html',{'form':form})
    else:
        form = RegisterForm()
        return render(request,'libapp/register.html',{'form':form})


def book(request):
    booklist=Book.objects.all()
    return render(request, 'libapp/book.html', {'booklist':booklist})


def dvd(request):
    dvdlist=DVD.objects.all()
    return render(request, 'libapp/dvd.html', {'dvdlist':dvdlist})


def other(request):
    otherlist=Libitem.objects.filter(itemtype='Other')
    return render(request, 'libapp/other.html', {'otherlist':otherlist})



def suggestdetail(request, suggest_id):
    try:
        suggestlist = Suggestion.objects.get(pk=suggest_id)
        return render(request, 'libapp/suggestdetail.html', {'suggestlist': suggestlist})
    except:
        raise Http404