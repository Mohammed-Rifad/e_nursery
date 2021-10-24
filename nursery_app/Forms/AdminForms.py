from django import forms
from django.db import models
from django.db.models import fields
from django.forms.widgets import Textarea
from ..models import CategoryDetails, NurseryProduct,ModeratorDetails
import re


class CategoryForm(forms.ModelForm):
   
    
    c_name=forms.CharField(label="Category Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    c_desc=forms.CharField(label="Description",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    c_img=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model=CategoryDetails
        exclude=('c_id','m_id')


class ProductForms(forms.ModelForm):

    # def __init__(self,*args,**kwargs):
    #     super(ProductForms,self).__init__(*args,**kwargs)
        
    #     for key,field in self.field.iteritems():
    #         self.fields[key].required=False
    container_types=(
        ('plastic','Plastic'),
        ('ceramic','Ceramic')
    )
    material_type=(
        ('plastic','Plastic'),
        ('ceramic','Ceramic')
    )
    shapes=(
        ('circular','Circular'),
        ('rectangular','Rectangular')
    )
    f_types=(
        ('solid','Solid'),
        ('liquid','Liquid'),
        ('granular','Granular')
    )
    seed_type=(
        ('Vegetable','vegetable'),
        ('fruits','Fruits'),
        
    )
    p_name=forms.CharField(label="Product Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_desc=forms.CharField(label="Product Desciption",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    p_dimension=forms.CharField(label="Dimension",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_location=forms.CharField(label="Locaton Suitable",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_color=forms.CharField(label="Color",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_sales_package=forms.CharField(label="Sales Package",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_container=forms.CharField(label="Container Type",widget=forms.Select(choices=container_types,attrs={'class':'form-control'}))
    p_features=forms.CharField(label="Features",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    p_suitable_for=forms.CharField(label="Price",widget=forms.TextInput(attrs={'class':'form-control'}))
    p_shape=forms.CharField(label="Shape",widget=forms.Select(choices=shapes, attrs={'class':'form-control'}))
    p_material=forms.CharField(label="Material Type",widget=forms.Select(choices=material_type,attrs={'class':'form-control'}))
    p_type=forms.CharField(label="Type",widget=forms.Select(choices=f_types, attrs={'class':'form-control'}))
    p_caring_tips=forms.CharField(label="Caring Tips",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    p_price=forms.CharField(label="Price",widget=forms.NumberInput(attrs={'class':'form-control'}))
    p_seeds=forms.CharField(label="Seed Type",widget=forms.Select(choices=seed_type,attrs={'class':'form-control'}))
    p_exp_days=forms.CharField(label="Expected Days For Delivery",widget=forms.NumberInput(attrs={'class':'form-control','min':1}))
    p_img=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'class':'form-control'}))
    p_stock=forms.IntegerField(label="Current Stock",widget=forms.NumberInput(attrs={'class':'form-control','min':1}))

    class Meta:
        model=NurseryProduct
       # fields=('p_name','p_desc','p_dimension','p_location','p_color','p_sales_package','p_container','p_features',
       # 'p_suitable_for','p_shape','p_shape','p_material','p_type','p_caring_tips','p_price','p_seeds','p_exp_days','p_img','p_stock')
        fields="__all__"
class NurseryPlantsForm(ProductForms):

    def __init__(self,*args,**kwargs):
        super(NurseryPlantsForm,self).__init__(*args,**kwargs)
        self.fields.pop('p_color');
        self.fields.pop('p_type');
        self.fields.pop('p_features');
        self.fields.pop('p_shape');
        self.fields.pop('p_seeds');
        self.fields.pop('p_material');
        self.fields.pop('p_location');
        self.fields.pop('p_suitable_for');

    
    class Meta(ProductForms.Meta):
        
        fields=('p_name','p_desc','p_dimension','p_sales_package','p_container','p_caring_tips','p_price','p_exp_days','p_img','p_stock')
         
class PotsForm(ProductForms):
    def __init__(self,*args,**kwargs):
        super(PotsForm,self).__init__(*args,**kwargs)
        self.fields.pop('p_caring_tips');
        self.fields.pop('p_type');
        self.fields.pop('p_features');
        self.fields.pop('p_seeds');
        self.fields.pop('p_suitable_for');
        self.fields.pop('p_shape');
        self.fields.pop('p_container');
        
        
   
    class Meta(ProductForms.Meta):
        fields=('p_name','p_desc','p_location','p_dimension','p_material','p_sales_package','p_color','p_price','p_exp_days','p_img','p_stock')
        
class StandForm(ProductForms):
    def __init__(self,*args,**kwargs):
        super(StandForm,self).__init__(*args,**kwargs)
        self.fields.pop('p_caring_tips');
        self.fields.pop('p_type');
        self.fields.pop('p_features');
        self.fields.pop('p_seeds');
        self.fields.pop('p_suitable_for');
        self.fields.pop('p_container');
        self.fields.pop('p_material');
    class Meta(ProductForms.Meta):
        fields=('p_name','p_desc','p_dimension','p_sales_package','p_color','p_location','p_price','p_exp_days','p_img','p_stock','p_shape')

class FertilizersForm(ProductForms):
    def __init__(self,*args,**kwargs):
        super(FertilizersForm,self).__init__(*args,**kwargs)
        self.fields.pop('p_caring_tips');
        self.fields.pop('p_features');
        self.fields.pop('p_seeds');
        self.fields.pop('p_shape');
        self.fields.pop('p_container');
        self.fields.pop('p_material');
        self.fields.pop('p_dimension');
        self.fields.pop('p_color');
        self.fields.pop('p_location');
        self.fields.pop('p_suitable_for');


        
    class Meta(ProductForms.Meta):
        
        fields=('p_name','p_desc','p_sales_package','p_type','p_price','p_exp_days','p_img','p_stock')

class SeedForm(ProductForms):
    
    def __init__(self,*args,**kwargs):
        super(SeedForm,self).__init__(*args,**kwargs)
        self.fields.pop('p_caring_tips');
        self.fields.pop('p_features');
        self.fields.pop('p_shape');
        self.fields.pop('p_material');
        self.fields.pop('p_dimension');
        self.fields.pop('p_color');
        self.fields.pop('p_location');
        self.fields.pop('p_container');
        self.fields.pop('p_suitable_for');
        self.fields.pop('p_seeds');
        self.fields.pop('p_type');

    class Meta(ProductForms.Meta):
      fields=('p_name','p_desc','p_sales_package','p_price','p_exp_days','p_img','p_stock')

class OtherProducts(ProductForms):
    def __init__(self,*args,**kwargs):
        super(OtherProducts,self).__init__(*args,**kwargs)
        self.fields.pop('p_caring_tips');
        self.fields.pop('p_shape');
        self.fields.pop('p_material');
        self.fields.pop('p_dimension');
        self.fields.pop('p_color');
        self.fields.pop('p_location');
        self.fields.pop('p_container');
        self.fields.pop('p_suitable_for');
        self.fields.pop('p_seeds');
        self.fields.pop('p_type');

    
    class Meta(ProductForms.Meta):
        fields=('p_name','p_desc','p_sales_package','p_features','p_price','p_exp_days','p_img','p_stock')


class ModeratorForm(forms.ModelForm):
    mod_name=forms.CharField(label="Moderator Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    mod_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'class':'form-control'}))
    mod_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'class':'form-control'}))
    mod_pic=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model=ModeratorDetails
        fields=('mod_name','mod_phno','mod_email','mod_pic')
    