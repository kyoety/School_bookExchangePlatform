from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from utsbookex.models import Bookforsale, BeUser
from django.db.models import Q
from .forms import BookEditForm, PrfEditForm
from allauth.socialaccount.models import SocialAccount
from .models import BeUser, Bookforsale
import os
import csv

# Create your views here.

def index(request):

    book_list = Bookforsale.objects.order_by('-bdate')[:4]
    my_dict = {'book_recent': book_list}

    print (str(request.user.is_authenticated))

    if  request.user.is_authenticated:
        try:
            info_user = BeUser.objects.get(umail = request.user.email)
            my_dict.update({"info_user" : info_user.uname})
        except BeUser.DoesNotExist:
            print('not exist!!!')
    return render(request, 'uts,b-e,lnding.html', context=my_dict)


def utsbe(request):
    book_list = Bookforsale.objects.filter(id__exact= request.GET['bid'])[:1]
    my_dict = {'book_recent': book_list}
    if  request.user.is_authenticated:
        try:
            info_user = BeUser.objects.get(umail = request.user.email)
            my_dict.update({"info_user" : info_user.uname})
        except BeUser.DoesNotExist:
            print('not exist!!!')
    return render(request, 'uts-be-detail-shop.html', context=my_dict)

def utsbe_shop(request):
    grade = request.GET.get('grade')
    searchtxt = request.GET.get('searchtxt')
    if searchtxt:
        filter = (Q(bname__icontains=searchtxt))
    if request.method == 'POST':
        subject = request.POST.getlist('subject')
        quality = request.POST.getlist('quality')
        order = request.POST.getlist('order')
        print (str(quality))
        print (str(subject))
        print (str(order))
        if searchtxt:
            print('there is filter')
            filter = filter & (Q(bsubject__in = subject) & Q(bqual__in = quality))
        else:
            filter = (Q(bsubject__in = subject) & Q(bqual__in = quality))
        if grade:
            filter = filter & Q(bgrade__exact = grade)
        book_list = Bookforsale.objects.filter(filter).order_by(order[0])
    else:
        if grade:
            if searchtxt:
                filter = filter & Q(bgrade__exact = grade)
            else:
                filter = Q(bgrade__exact = grade)
            book_list = Bookforsale.objects.filter(filter).order_by('-bdate')
        else:
            if searchtxt:
                book_list =  Bookforsale.objects.filter(filter).order_by('-bdate')
            else:
                book_list =  Bookforsale.objects.order_by('-bdate')
    my_dict = {'book_recent': book_list}
    if  request.user.is_authenticated:
        try:
            info_user = BeUser.objects.get(umail = request.user.email)
            my_dict.update({"info_user" : info_user.uname})
        except BeUser.DoesNotExist:
            print('not exist!!!')
    return render(request, 'uts-be-shop.html', context=my_dict)


def utsbe_prf_books(request):
    print (str(request.user.is_authenticated))
    if  request.user.is_authenticated:
        if (request.user.email.endswith('utschools.ca') or request.user.email == "utsbeweb@gmail.com"):
            info_user = BeUser.objects.filter(umail__exact = request.user.email)
            if info_user:
                book_list = Bookforsale.objects.filter(buser__exact = info_user[0]).order_by('-bdate')[:12]
                my_dict = {'book_user': book_list, 'info_user': info_user}
                return render(request, 'uts-be-userprofile-display.html', context=my_dict)
            else:
                print ("new user")
                return HttpResponseRedirect('/uts-be-userprofile')
        else:
            return HttpResponseRedirect('/?error=utsonly')
    return HttpResponseRedirect('/')

def utsbe_bookedit(request):

    bid = request.GET.get('bid')
    if bid :
        book = Bookforsale.objects.get(id = bid)

    if request.method == 'POST':
        if bid :
            if book:
                form = BookEditForm(request.POST,request.FILES, instance = book)
            else:
                form = BookEditForm(request.POST,request.FILES)
        else:
            form = BookEditForm(request.POST,request.FILES)
        if form.is_valid():
           new_book = form.save(commit=False)
           current_login_user_data = BeUser.objects.filter(umail__exact = 'yeka@utschools.ca')
           new_book.buser = current_login_user_data[0]
           new_book.save()
           return HttpResponseRedirect('/uts-be-userprofile-display')
        else:
            print("le form error")
    else :
        if bid :
            if book :

                form = BookEditForm(instance = book )
            else:
                form = BookEditForm()
        else:
            form = BookEditForm()
        my_dictionary = {"form" : form}

        if bid:
            if book:
                my_dictionary.update({"bookimage" : book.bimage})

        if  request.user.is_authenticated:
            try:
                info_user = BeUser.objects.get(umail = request.user.email)
                my_dictionary.update({"info_user" : info_user.uname})
            except BeUser.DoesNotExist:
                print('not exist!!!')
        return render(request, 'uts-be-book-edit.html', my_dictionary)

def utsbe_profileedit(request):
    uid = request.GET.get('uid')

    if uid :
        prf = BeUser.objects.get(id = uid)

    if request.method == 'POST':
        if uid :
            if prf:
                form = PrfEditForm(request.POST,request.FILES, instance = prf)
            else:
                form = PrfEditForm(request.POST,request.FILES)
        else:
            form = PrfEditForm(request.POST,request.FILES)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.umail =  request.user.email
            new_user.save()
            return HttpResponseRedirect('/uts-be-userprofile-display')
        else:
            print("le form error")
    else:
        print ("it is not post")
        if uid :
            if prf:
                form = PrfEditForm(instance = prf)
            else:
                form = PrfEditForm()
        else :
            form = PrfEditForm()
        my_dictionary = {"form" : form}
        if  request.user.is_authenticated:
            try:
                info_user = BeUser.objects.get(umail = request.user.email)
                my_dictionary.update({"info_user" : info_user.uname})
            except BeUser.DoesNotExist:
                print('not exist!!!')
    return render(request, 'uts-be-userprofile.html', my_dictionary)

def deletee(request):
    buid = request.GET.get('buid')
    
    buid = request.GET.get('buid')
    book = Bookforsale.objects.get(pk=buid)
    if os.path.isfile(book.bimage):
       os.remove(book.bimage)
    book.delete()
    return HttpResponseRedirect('/uts-be-userprofile-display')
"""
def importfile(request):

    Bookforsale.objects.all().delete()

    f = open('booklist.csv', encoding = "utf-8")
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        print(row[2]+row[4])
        #Create User
        try:
            user = BeUser.objects.get(umail = row[1])
        except BeUser.DoesNotExist:
            user = BeUser(uname = row[2], umail = row[1], udate = row[0])
            user.save()
        #Create Book
        book = Bookforsale(
            bname = row[4],
            bdate = row[0],
            bgrade = row[5],
            bqual = row[7],
            bprice = row[8],
            bdescript = row[9]+' Contact: '+row[3],
            bsubject = row[6],
            buser = user
            )
        book.save()

    return HttpResponseRedirect('/')
"""