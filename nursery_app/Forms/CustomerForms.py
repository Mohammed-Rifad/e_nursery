from django import forms
from django import forms
from django.db import models
from django.db.models import fields
from django.forms.widgets import Textarea
from ..models import CraftDetails, CustomerDetails,ProductFeedBack,GardenIdeas, SellerReg, StandPotIdeas
import re


class CustomerRegForm(forms.ModelForm):
    cust_name=forms.CharField(label="Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    cust_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    cust_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    cust_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    cust_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'style':'width:300px','class':'form-control'}))  
    cust_img=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    class Meta:
        model=CustomerDetails
        exclude=('cust_id',)

    def clean_cust_name(self):
        cust_name=self.cleaned_data['cust_name']
        if not re.match(r'^[A-Za-z]+$', cust_name):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return cust_name
    def clean_cust_email(self):
        cust_email=self.cleaned_data['cust_email']
        if not re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', cust_email):
            raise forms.ValidationError("Invalid Email Format")
        return cust_email
    
    # def clean_cust_phno(self):
    #     cust_phno=self.cleaned_data['cust_phno']
    #     length=len(str(cust_phno))
    #     if length!=10:
    #         raise forms.ValidationError("Phone number must be 10 digits")
    #     if cust_phno.isdigit()==False or cust_phno.startswith('1') or cust_phno.startswith('2') or cust_phno.startswith('3') or cust_phno.startswith('4').cust_phno.startswith('5'):
    #         raise forms.ValidationError("Invalid Number")
    #     return cust_phno
    def clean_cust_passwd(self):
        cust_passwd=self.cleaned_data['cust_passwd']
        length=len(str(cust_passwd))
        if length<8:
            raise forms.ValidationError("Password should be minimun 8 characters long")
        return cust_passwd


class FeedBackForm(forms.ModelForm):
    
    feedback=cust_address=forms.CharField(label="Feedback",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    
    class Meta:
        model=ProductFeedBack
        fields=('feedback',)



class GardenRequestForm(forms.ModelForm):
    plot_pic=forms.ImageField(label="Upload Plot Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    requirements=forms.CharField(label="Requirements",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    exp_date=forms.CharField(label="Expected Date",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    budget=forms.CharField(label="Budget",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))

    class Meta:
        model=GardenIdeas
        fields=('plot_pic','requirements','exp_date','budget')

class StandPotForm(forms.ModelForm):
    items=(
        ('stand','Stand'),
        ('pot','Pot')
    )
    design=forms.ImageField(label="Upload Design",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    requirements=forms.CharField(label="Requirements",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    item=forms.CharField(label="Select Item",widget=forms.Select(choices=items, attrs={'class':'form-control'}))
    

    class Meta:
        model=StandPotIdeas
        fields=('item','requirements','design')

class SellerRegForm(forms.ModelForm):
    docs=(
        ('adhar','Adhar'),
        ('driving license','Driving License'),
        ('pan','Pan')
    )
    sell_name=forms.CharField(label="Name",widget=forms.TextInput( attrs={'class':'form-control'}))
    sell_exp=forms.CharField(label="Experience",widget=forms.NumberInput( attrs={'class':'form-control'}))
    doc_type=forms.CharField(label="Document Type",widget=forms.Select(choices=docs, attrs={'class':'form-control','height':'100px','width':'100px'}))
    doc=forms.FileField(label="Upload Document",widget=forms.FileInput( attrs={'class':'form-control'}))
    about_me=forms.CharField(label="About Me",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    
    class Meta:
        model=SellerReg
        exclude=('cust_id','status',)

class CraftAddForm(forms.ModelForm):
   
    craft_type=(
        ('traditional','Traditional'),
        ('Newer','Newer')
    )
    cr_name=forms.CharField(label="Product Name",widget=forms.TextInput( attrs={'class':'form-control'}))
    cr_price=forms.CharField(label="Price",widget=forms.NumberInput( attrs={'class':'form-control'}))
    cr_type=forms.CharField(label="Craft Type",widget=forms.Select(choices=craft_type, attrs={'class':'form-control','height':'100px','width':'100px'}))
    cr_color=forms.CharField(label="color",widget=forms.TextInput( attrs={'class':'form-control'}))
    cr_material=forms.CharField(label="Material",widget=forms.TextInput( attrs={'class':'form-control'}))
    cr_desc=forms.CharField(label="Description",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    cr_exp_days=forms.CharField(label="Expected days for delivery",widget=forms.NumberInput( attrs={'class':'form-control'}))
    cr_stock=forms.CharField(label="Stock",widget=forms.NumberInput( attrs={'class':'form-control'}))
    cr_sales_pack=forms.CharField(label="Sales package",widget=forms.TextInput( attrs={'class':'form-control'}))
    cr_img=forms.ImageField(label="Upload Image",widget=forms.FileInput( attrs={'class':'form-control'}))

    class Meta:
        model=CraftDetails
        fields=('cr_name','cr_type','cr_color','cr_material','cr_desc','cr_price','cr_exp_days','cr_stock','cr_sales_pack','cr_img')