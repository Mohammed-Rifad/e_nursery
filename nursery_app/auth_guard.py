from django.shortcuts import render,redirect
from.models import AdminDetails,ModeratorDetails,CustomerDetails

def auth_admin(func):
    def wrap(request,*args,**kwargs):
        if 'admin_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('e_nursery:login')


    return wrap


def auth_moderator(func):
    def wrap(request,*args,**kwargs):
        if 'mod_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('e_nursery:login')


    return wrap

def auth_customer(func):
    def wrap(request,*args,**kwargs):
        if 'user_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('e_nursery:login')


    return wrap


