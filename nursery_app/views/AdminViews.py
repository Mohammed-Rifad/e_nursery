import datetime
from django.core.paginator import Paginator
from django.http import request
from nursery_app.models import GardenIdeas, GardenProducts, MainCategory,OrderDetails, RatingDetails, SellerReg, StandPotIdeas,ReturnProducts
from django.forms.widgets import SelectDateWidget
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from nursery_app.Forms.AdminForms import *
from ..services import AddRating, email_moderator, getModID, getPagination, getProductNo
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from nursery_app.auth_guard import auth_admin


@auth_admin
def AdminHome(request):
    return render(request,'Admin/AdminHome.html')

@auth_admin
def AddCategory(request):
    form=CategoryForm()
    main_cat=MainCategory.objects.all()
    if request.method=='POST':
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            m_id=MainCategory.objects.get(m_id=request.POST['main_cat'])
            c_name=form.cleaned_data['c_name'].lower()
            c_desc=form.cleaned_data['c_desc'].lower()
            c_img=form.cleaned_data['c_img']

            cat_exist=CategoryDetails.objects.filter(m_id=m_id,c_name=c_name).exists()
            if not cat_exist:
                qry=CategoryDetails(m_id=m_id,c_name=c_name,c_desc=c_desc,c_img=c_img)
                qry.save()
                success_msg="Category Added Succesfully"
                return render(request,'Admin/AddCategory.html',{'form':form,'success_msg':success_msg,'main_cat':main_cat})
            else:
                error_msg="Category Already Added"
                return render(request,'Admin/AddCategory.html',{'form':form,'error_msg':error_msg,'main_cat':main_cat})
        else:
            print(form.errors)
    return render(request,'Admin/AddCategory.html',{'form':form,'main_cat':main_cat})

@auth_admin
def AddNurseryPlants(request):
    form=NurseryPlantsForm()
    categories=CategoryDetails.objects.filter(m_id=1)
    if request.method=='POST':
        form=NurseryPlantsForm(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=1)
            p_name=form.cleaned_data['p_name'].lower()
            p_desc=form.cleaned_data['p_desc'].lower()
            p_dimension=form.cleaned_data['p_dimension']
            p_sales_package=form.cleaned_data['p_sales_package'].lower()
            p_container=form.cleaned_data['p_container'].lower()
            p_caring_tips=form.cleaned_data['p_caring_tips'].lower()
            p_price=form.cleaned_data['p_price']
            p_stock=form.cleaned_data['p_stock']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']

            product_exist=NurseryProduct.objects.filter(cat_id=request.POST['cat'],p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')
                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,m_id=m_id,p_rating=3.72,p_name=p_name,p_desc=p_desc,p_dimension=p_dimension,p_sales_package=p_sales_package,p_container=p_container,p_caring_tips=p_caring_tips,p_price=p_price,p_exp_days=p_exp_days,p_stock=p_stock,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,"e_nursery")
                success_msg="Product Added Succesfully"
                form=NurseryPlantsForm()
                return render(request,'Admin/AddPlants.html',{'form':form,'categories':categories,'success_msg':success_msg})
            else:
                form=NurseryPlantsForm()
                error_msg="Product Already Added"
                return render(request,'Admin/AddPlants.html',{'form':form,'categories':categories,'error_msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddPlants.html',{'form':form,'categories':categories})


@auth_admin
def AddPots(request):
    form=PotsForm()
    categories=CategoryDetails.objects.filter(m_id=2)
    if request.method=='POST':
        form=PotsForm(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=2)
            p_name=form.cleaned_data['p_name'].lower()
            p_desc=form.cleaned_data['p_desc'].lower()
            p_dimension=form.cleaned_data['p_dimension']
            p_sales_package=form.cleaned_data['p_sales_package'].lower()
            p_color=form.cleaned_data['p_color'].lower()
            p_location=form.cleaned_data['p_location'].lower()
            p_price=form.cleaned_data['p_price']
            p_material=form.cleaned_data['p_material']
            p_stock=form.cleaned_data['p_stock']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']

            product_exist=NurseryProduct.objects.filter(cat_id=request.POST['cat'],p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')
                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,m_id=m_id,p_name=p_name,p_rating=3.72,p_desc=p_desc,p_material=p_material,p_dimension=p_dimension,p_sales_package=p_sales_package,p_color=p_color,p_location=p_location,p_price=p_price,p_exp_days=p_exp_days,p_stock=p_stock,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,'e_nursery')
                success_msg="Pots Added Succesfully"
                form=PotsForm()
                return render(request,'Admin/AddPots.html',{'form':form,'categories':categories,'success_msg':success_msg})
            else:
                error_msg="Pots Already Added"
                form=PotsForm()
                return render(request,'Admin/AddPots.html',{'form':form,'categories':categories,'error_msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddPots.html',{'form':form,'categories':categories,})


@auth_admin
def AddStands(request):
    form=StandForm()
    categories=CategoryDetails.objects.filter(m_id=3)
    if request.method=='POST':
        form=StandForm(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=3)
            p_name=form.cleaned_data['p_name'].lower()
            p_desc=form.cleaned_data['p_desc'].lower()
            p_dimension=form.cleaned_data['p_dimension']
            p_sales_package=form.cleaned_data['p_sales_package'].lower()
            p_color=form.cleaned_data['p_color'].lower()
            p_shape=form.cleaned_data['p_shape'].lower()
            p_location=form.cleaned_data['p_location'].lower()
            p_price=form.cleaned_data['p_price']
            p_stock=form.cleaned_data['p_stock']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']


            product_exist=NurseryProduct.objects.filter(cat_id=request.POST['cat'],p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')
                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,p_rating=3.72,m_id=m_id,p_name=p_name,p_shape=p_shape,p_desc=p_desc,p_dimension=p_dimension,p_sales_package=p_sales_package,p_color=p_color,p_location=p_location,p_price=p_price,p_exp_days=p_exp_days,p_stock=p_stock,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,"e_nursery")
                success_msg="Product Added Succesfully"
                form=StandForm()
                return render(request,'Admin/AddStands.html',{'form':form,'categories':categories,'success_msg':success_msg})
            else:
                error_msg="Product Already Added"
                form=StandForm()
                return render(request,'Admin/AddStands.html',{'form':form,'categories':categories,'error_msg':msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddStands.html',{'form':form,'categories':categories,})

@auth_admin
def AddFertilizers(request):
    categories=CategoryDetails.objects.filter(m_id=5)
    form=FertilizersForm()
    if request.method=='POST':
        form=FertilizersForm(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=5)
            p_name=form.cleaned_data['p_name']
            p_desc=form.cleaned_data['p_desc']
            p_sales_package=form.cleaned_data['p_sales_package']
            
            p_type=form.cleaned_data['p_type']
            p_price=form.cleaned_data['p_price']
            p_stock=form.cleaned_data['p_stock']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']
            product_exist=NurseryProduct.objects.filter(cat_id=cat_id,p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')
                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,p_rating=3.72,m_id=m_id,p_name=p_name,p_desc=p_desc,p_type=p_type,p_sales_package=p_sales_package,p_price=p_price,p_stock=p_stock,p_exp_days=p_exp_days,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,"e_nursery")
                success_msg="Fertilizer Added Succesfully"
                form=FertilizersForm()
                return render(request,'Admin/AddFertilizer.html',{'form':form,'success_msg':success_msg,'categories':categories})
            else:
                error_msg="Fertilizer Already Added"
                form=FertilizersForm()
                return render(request,'Admin/AddFertilizer.html',{'form':form,'error_msg':error_msg,'categories':categories})
        else:
            print(form.errors)
    return render(request,'Admin/AddFertilizer.html',{'form':form,'categories':categories})


@auth_admin
def AddSeeds(request):
    form=SeedForm()
    categories=CategoryDetails.objects.filter(m_id=4)
    
    if request.method=='POST':
        form=SeedForm(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=4)
            p_name=form.cleaned_data['p_name']
            p_desc=form.cleaned_data['p_desc']
            
            p_sales_package=form.cleaned_data['p_sales_package']
            p_price=form.cleaned_data['p_price']
            p_stock=form.cleaned_data['p_stock']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']
            
            product_exist=NurseryProduct.objects.filter(cat_id=cat_id,p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')

                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,p_rating=3.72,m_id=m_id,p_name=p_name,p_desc=p_desc,p_sales_package=p_sales_package,p_price=p_price,p_stock=p_stock,p_exp_days=p_exp_days,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,"e_nursery")
                form=SeedForm()
                success_msg="Seeds Added Succesfully"
                return render(request,'Admin/AddSeeds.html',{'form':form,'success_msg':success_msg,'categories':categories})
            else:
                error_msg="Seeds Already Added"
                form=SeedForm()
                return render(request,'Admin/AddSeeds.html',{'form':form,'error_msg':error_msg,'categories':categories})
        else:
            print(form.errors)
    return render(request,'Admin/AddSeeds.html',{'form':form,'categories':categories})




@auth_admin
def AddTools(request):
    categories=CategoryDetails.objects.filter(m_id=6)
    form=OtherProducts()
    
    if request.method=='POST':
        form=OtherProducts(request.POST,request.FILES)
        if form.is_valid():
            cat_id=CategoryDetails.objects.get(c_id=request.POST['cat'])
            m_id=MainCategory.objects.get(m_id=6)
            p_name=form.cleaned_data['p_name']
            p_desc=form.cleaned_data['p_desc']
            p_sales_package=form.cleaned_data['p_sales_package']
            p_price=form.cleaned_data['p_price']
            p_stock=form.cleaned_data['p_stock']
            p_features=form.cleaned_data['p_features']
            p_exp_days=form.cleaned_data['p_exp_days']
            p_img=form.cleaned_data['p_img']
            product_exist=NurseryProduct.objects.filter(cat_id=cat_id,p_name=p_name).exists()
            if not product_exist:
                product_no=getProductNo('e_nursery')
                qry=NurseryProduct(prod_no=product_no,cat_id=cat_id,p_rating=3.72,m_id=m_id,p_name=p_name,p_desc=p_desc,p_features=p_features,p_sales_package=p_sales_package,p_price=p_price,p_stock=p_stock,p_exp_days=p_exp_days,p_img=p_img)
                qry.save()
                p_id=NurseryProduct.objects.latest('p_id')
                AddRating(p_id,"e_nursery")
                form=OtherProducts()
                success_msg="Tool Added Succesfully"
                return render(request,'Admin/AddTools.html',{'form':form,'categories':categories,'success_msg':success_msg})
            else:
                error_msg="Tools Already Added"
                form=OtherProducts()
                return render(request,'Admin/AddTools.html',{'form':form,'categories':categories,'error_msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddTools.html',{'form':form,'categories':categories})


@auth_admin
def ViewPendingOrders(request):
    orde_list=OrderDetails.objects.filter(Q(order_status='ordered')|Q( order_status='packed'),sell_type='e_nursery')
    page_obj=getPagination(orde_list,request.GET.get('page'))    
    return render(request,'Admin/PendingOrders.html',{'orde_list':page_obj})

@auth_admin
def OrderDetail(request,ord_id):
    order_data=OrderDetails.objects.get(order_no=ord_id)
    if request.method=='POST':
        upd_date=datetime.date.today()
        upd_converted=upd_date.strftime("%d/%m/%Y")
        if 'packed' in request.POST:
            order_data.order_status='packed'
            
        if 'delivered' in request.POST:
            order_data.order_status='delivered'
            
        order_data.exp_delivery=upd_converted
        order_data.save()
        return redirect("e_nursery:pending_orders")
    return render(request,'Admin/OrderDetails.html',{'order_data':order_data,})



@auth_admin
def AddModerator(request):
    form=ModeratorForm()
    
    
    if request.method=='POST':
        form=ModeratorForm(request.POST,request.FILES)
        if form.is_valid():
            mod_id=getModID()
            mod_name=form.cleaned_data['mod_name'].lower()
            mod_phno=form.cleaned_data['mod_phno']
            mod_email=form.cleaned_data['mod_email']
            mod_pic=form.cleaned_data['mod_pic']
            passwd=get_random_string(length=8)
            enc_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)

            data_exist=ModeratorDetails.objects.filter(mod_email=mod_email).exists()

            if not data_exist:
                qry=ModeratorDetails(mod_id=mod_id,mod_name=mod_name,mod_phno=mod_phno,mod_email=mod_email,mod_pic=mod_pic,mod_passwd=enc_passwd)
                qry.save()
                msg="Moderator Added Succesfully"
                # email_moderator(mod_email,mod_id,passwd)
                print('passwd is',passwd)
                return render(request,'Admin/AddModerator.html',{'form':form,'msg':msg})
            else:
                msg="Moderator Already Succesfully"
                print('passwd is',passwd)
                return render(request,'Admin/AddModerator.html',{'form':form,'msg':msg})
            

    return render(request,'Admin/AddModerator.html',{'form':form,})



@auth_admin
def RecentGardenRequest(request):
    request_list=GardenIdeas.objects.filter(status="pending")

    if request.method=='POST':
        if 'details' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            return render(request,'Admin/GardenDetails.html',{'req_data':req_data})
        
        
       

    return render(request,'Admin/RecentGardenRequest.html',{'request_list':request_list})


@auth_admin
def PendingGardenRequest(request):
    request_list=GardenIdeas.objects.filter(Q(status="payment completed")|Q(status="approved"))
    if request.method=='POST':
        req_id=request.POST['req_id']
        if 'details' in request.POST:
           
            
            req_data=GardenIdeas.objects.get(req_id=req_id)
            return render(request,'Admin/GardenDetails.html',{'req_data':req_data})
        if 'estimation' in request.POST:
            total=0
            est_data=GardenIdeas.objects.get(req_id=req_id)
            est_prod=GardenProducts.objects.filter(req_id=req_id)

            for item in est_prod:
                total=total+item.total_amt

            return render(request,'Admin/ViewEstimation.html',{'est_prod':est_prod,'total':total,'est_data':est_data})
        if 'completed' in request.POST:
            est_data=GardenIdeas.objects.get(req_id=req_id)
            est_data.status="work completed"
            est_data.save()
        return redirect("e_nursery:admin_home")
    
    return render(request,'Admin/ApprovedGardenRequest.html',{'request_list':request_list})


@auth_admin
def gardenRequestHistory(request):
    garre_list=GardenIdeas.objects.filter(Q(status="rejected")|Q(status="customer rejected")|Q(status="work completed"))
    page_obj=getPagination(garre_list,request.GET.get('page'))
    return render(request,'Admin/GardenHistory.html',{'garre_list':page_obj})


@auth_admin
def ViewEstimation(request,req_id):

    if request.method=='POST':
        est_data=GardenIdeas.objects.get(req_id=req_id)
        est_data.status="work completed"
        est_data.save()
        return redirect("e_nursery:admin_home")

    total=0
    est_data=GardenIdeas.objects.get(req_id=req_id)
    est_prod=GardenProducts.objects.filter(req_id=req_id)

    for item in est_prod:
        total=total+item.total_amt

    return render(request,'Admin/ViewEstimation.html',{'est_prod':est_prod,'total':total,'est_data':est_data})

@auth_admin
def RecentSPRequest(request):
    request_list=StandPotIdeas.objects.filter(status="pending")
    if request.method=='POST':
        req_data=StandPotIdeas.objects.get(id=request.POST['id'])
        return render(request,'Admin/StandPotDetails.html',{'req_data':req_data,})
    return render(request,'Admin/ViewRecentSP.html',{'request_list':request_list})


@auth_admin
def ApprovedSPRequest(request):
    request_list=StandPotIdeas.objects.filter(Q(status="approved")|Q(status="payment completed")|Q(status="work completed"))
    if request.method=='POST':
        req_data=StandPotIdeas.objects.get(id=request.POST['id'])
        if 'details' in request.POST:
            
            return render(request,'Admin/StandPotDetails.html',{'req_data':req_data})
        if 'delivered' in request.POST:
            dt=datetime.date.today()
           
            date=dt.strftime("%d/%m/%Y")
            req_data.delivered_date=date
            req_data.status="delivered"
            req_data.save()

    return render(request,'Admin/ApprovedSPRequest.html',{'request_list':request_list})



@auth_admin
def StandPotHistory(request):
    request_list=StandPotIdeas.objects.filter(Q(status="rejected")|Q(status="customer rejected")|Q(status="delivered"))
    page_obj=getPagination(request_list,request.GET.get('page'))
    return render(request,'Admin/StandPotHistory.html',{'request_list':page_obj})




@auth_admin
def ViewSellRequest(request):
    sell_data=SellerReg.objects.filter(status='pending')
    if request.method=='POST':
        id=request.POST['id']
        print(id)
        data=SellerReg.objects.get(sell_id=id)
        if 'approve' in request.POST:
            data.status="approved"
            print('approve')
        if 'reject' in request.POST:
            data.status="rejected"
        data.save()
    return render(request,'Admin/PendingSellRequest.html',{'sell_data':sell_data,})

@auth_admin
def ViewAllProducts(request):
    products=NurseryProduct.objects.all()
    page_obj=getPagination(products,request.GET.get('page'))
    if request.method=='POST':
        prod_no=request.POST['prod_no']
        products=NurseryProduct.objects.filter(prod_no=prod_no)
        page_obj=getPagination(products,1)
    return render(request,'Admin/ViewAllProducts.html',{'products':page_obj})




@auth_admin
def UpdateStock(request):
    
    
    if request.method=='POST':
        p_no=request.POST['p_no']
        product=NurseryProduct.objects.get(prod_no=p_no)
        stock=product.p_stock
        product.p_stock=request.POST['new_stock']
        product.save()
        return redirect("e_nursery:all_prod")
    p_no=request.GET['no']
    product=NurseryProduct.objects.get(prod_no=p_no)
    stock=product.p_stock
    return render(request,'Admin/Stock.html',{'p_no':p_no,'stock':stock})


@auth_admin
def SellerOrders(request):
    orders_list=OrderDetails.objects.filter(sell_type="seller")
    page_obj=getPagination(orders_list,request.GET.get('page'))
    return render(request,'Admin/SellerOrders.html',{'order_list':page_obj})

@auth_admin
def OrderHistory(request):
    orders=OrderDetails.objects.filter(Q(order_status='cancelled')|Q( order_status='delivered'),sell_type='e_nursery')
    # paginator=Paginator(orders,2)
    # page_no=request.GET.get('page')
    page_obj=getPagination(orders,request.GET.get('page'))
    return render(request,'Admin/OrderHistory.html',{'orders':page_obj})

@auth_admin
def HistoryDetail(request,ord_id):
     order_data=OrderDetails.objects.get(order_no=ord_id)
   
     return render(request,'Admin/HistoryDetails.html',{'order_data':order_data})


@auth_admin
def ViewSellers(request):
    data=True
    sellers=SellerReg.objects.filter(status="approved")
    page_obj=getPagination(sellers,request.GET.get('page'))
    if request.method=='POST':
        sellers=SellerReg.objects.filter(sell_name__startswith=request.POST['sell_name'])
        if sellers:
            page_obj=getPagination(sellers,request.GET.get('page'))
        else:
            data=False
    return render(request,'Admin/Sellers.html',{'sellers':page_obj,'data':data})


@auth_admin
def ViewReturnproducts(request):
     return_pro=ReturnProducts.objects.filter(Q(status='pending')|Q( status='packed'))
    

     return render(request,'Admin/ViewReturnProduct.html',{'return_pro':return_pro})


def ReturnDetail(request,ord_no):
    order_data=ReturnProducts.objects.get(order_no=ord_no)
    if request.method=='POST':
         if 'packed' in request.POST:
            order_data.status="packed"
         else:
            order_data.status="delivered"
         order_data.save()
         return redirect("e_nursery:view_return")
    return render(request,'Admin/ReturnCustomerDetails.html',{'order_data':order_data})


