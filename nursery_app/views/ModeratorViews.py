from datetime import datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from ..services import getPagination,getModName
from django.db.models import Q
from ..models import GardenProducts, ModeratorDetails,GardenIdeas, NurseryProduct, StandPotIdeas
from nursery_app.Forms.ModeratorForms import ChangePasswordForm
from passlib.hash import pbkdf2_sha256
from nursery_app.auth_guard import auth_moderator




@auth_moderator
def ModeratorHome(request):
   
    mod_name,mod_pic=getModName(request.session['mod_id'])
    return render(request,'Moderator/ModeratorHome.html',{'mod_name':mod_name,'mod_pic':mod_pic})

@auth_moderator
def PendingGardenRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    request_list=GardenIdeas.objects.filter(status="pending")

    if request.method=='POST':
        if 'details' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            return render(request,'Moderator/GardenDetails.html',{'req_data':req_data,'mod_name':mod_name,'mod_pic':mod_pic})
        if 'approve' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            req_data.status="approved"
            req_data.mod_id=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
            req_data.save()
        if 'reject' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            req_data.status="rejected"
            req_data.mod_id=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
            req_data.save()
            return render(request,'Moderator/RejectReason.html',{'req_id':req_id,'mod_name':mod_name,'mod_pic':mod_pic})
        
                

    return render(request,'Moderator/PendingGardenRequest.html',{'request_list':request_list,'mod_name':mod_name,'mod_pic':mod_pic})


@auth_moderator    
def RejectReason(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])

    req_id=request.POST['req_id']
    req_data=GardenIdeas.objects.get(req_id=req_id)
    req_data.reject_reason=request.POST['reason']
    req_data.save()
    return redirect("e_nursery:p_grequest",{'mod_name':mod_name,'mod_pic':mod_pic})

@auth_moderator
def GardenRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
   
    #request_list=GardenIdeas.objects.filter((~Q(status='pending')|~Q(status='completed')|~Q(status='customer rejected')),mod_id=request.session['mod_id'])
    request_list=GardenIdeas.objects.filter(status='approved',mod_id=request.session['mod_id'])
    page_obj=getPagination(request_list,request.GET.get('page'))
    
    for i in request_list:
        print(i.status)
    return render(request,'Moderator/GardenRequest.html',{'request_list':page_obj,'mod_name':mod_name,'mod_pic':mod_pic})



@auth_moderator
def ConfirmedGardenRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    request_list=GardenIdeas.objects.filter(status="payment completed",mod_id=request.session['mod_id'])
    return render(request,'Moderator/ConfirmedGRequest.html',{'request_list':request_list,'mod_name':mod_name,'mod_pic':mod_pic})


@auth_moderator
def AddEstimation(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])

  
    product={}
    try:
        request.session['req_id']=request.GET['req']
        
    except:
        None

    try:
        
        pr_no=request.GET['pr_no']
        product=NurseryProduct.objects.get(prod_no=pr_no)
      
        return product.prod_no
    except Exception as e:
        print(e)
    
    if  request.method=='POST':
        if 'est_date' in request.POST:
            
            
            g_idea=GardenIdeas.objects.get(req_id=request.session['req_id'])
            est_dt=datetime.strptime(request.POST['date'],"%Y-%m-%d")

            est_convert=est_dt.strftime("%d/%m/%Y")
            g_idea.est_date=est_convert
            g_idea.plot_design=request.FILES['design']
            g_idea.save()
            date_msg="Date Updated Succesfully"
            return render(request,'Moderator/EstimationProduct.html',{'date_msg':date_msg,'mod_name':mod_name,'mod_pic':mod_pic})

            
        if 'Add' in request.POST:
            p_no=request.POST['p_no']
           
            product=NurseryProduct.objects.get(prod_no=p_no)

            p_id=NurseryProduct.objects.get(p_id=product.p_id)
            req=GardenIdeas.objects.get(req_id=request.session['req_id'])

            is_product_added=GardenProducts.objects.filter(req_id=request.session['req_id'],product_id=product.p_id).exists()

            if not is_product_added:

         
                est_product=GardenProducts(req_id=req,product_id=p_id,total_amt=product.p_price)
                est_product.save()
                product_msg="Product Updated Succesfully"
                return render(request,'Moderator/EstimationProduct.html',{'product_msg':product_msg})
            else:
                product_msg="Product already added"
                return render(request,'Moderator/EstimationProduct.html',{'product_msg':product_msg})

    return render(request,'Moderator/EstimationProduct.html',{'product':product})



#ajax
@auth_moderator
def getProductDetails(request):
    

    
    

    try:
        
        pr_no=request.GET['pr_no']
        #product=NurseryProduct.objects.get(prod_no=pr_no)
        product=NurseryProduct.objects.get(prod_no=pr_no)
        list=[product.p_name,product.p_price]
        return JsonResponse(list,safe=False)
    except :
        return HttpResponse()

@auth_moderator
def ViewEstimation(request,req_id):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    total=0

    if request.method=='POST':
        p_id=request.POST['p_id']
        data=GardenProducts.objects.get(product_id=p_id)
        data.delete()
    est_data=GardenIdeas.objects.get(req_id=req_id)
    est_prod=GardenProducts.objects.filter(req_id=req_id)

    for item in est_prod:
        total=total+item.total_amt

    return render(request,'Moderator/ViewEstimation.html',{'est_prod':est_prod,'total':total,'est_data':est_data,'mod_name':mod_name,'mod_pic':mod_pic})


@auth_moderator
def ViewStandPotRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    request_list=StandPotIdeas.objects.filter(status="pending")

    if request.method=='POST':
        id=request.POST['id']
        req_data=StandPotIdeas.objects.get(id=id)
        if 'approve' in request.POST:
            
           
            
            req_data.status="approved"
            req_data.mod_id=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
            req_data.save()
            return render(request,'Moderator/ViewStandPotRequest.html',{'request_list':request_list,})
        if 'details' in request.POST:
            return render(request,'Moderator/StandPotDetails.html',{'req_data':req_data,})
        
        if 'reject' in request.POST:
            req_data.status="rejected"
            req_data.mod_id=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
            req_data.save()
            return render(request,'Moderator/StandPotReject.html',{'id':id,})
        if 'add_reason' in request.POST:
            
            reason=request.POST['reason']
            req_data.mod_id=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
            req_data.reject_reason=reason
            req_data.save()
            
    return render(request,'Moderator/ViewStandPotRequest.html',{'request_list':request_list,'mod_name':mod_name,'mod_pic':mod_pic})



@auth_moderator
def ViewAllProducts(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    products=NurseryProduct.objects.all()
    page_obj=getPagination(products,request.GET.get('page'))
    if request.method=='POST':
        prod_no=request.POST['prod_no']
        products=NurseryProduct.objects.filter(prod_no=prod_no)
        page_obj=getPagination(products,1)
    return render(request,'Moderator/ViewAllProducts.html',{'products':page_obj,'mod_name':mod_name,'mod_pic':mod_pic})


@auth_moderator
def ApprovedSPRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    request_list=StandPotIdeas.objects.filter(status="approved",mod_id=request.session['mod_id'])
    if request.method=='POST':
        id=request.POST['id']
        req_data=StandPotIdeas.objects.get(id=request.POST['id'])
        if 'details' in request.POST:
            return render(request,'Moderator/StandPotDetails.html',{'req_data':req_data,})
        if 'add_est' in request.POST:
            
            return render(request,'Moderator/SPEstimation.html',{'id':id,})
        if 'add' in request.POST:
           
            est_data=StandPotIdeas.objects.get(id=id)
            dt=datetime.strptime(request.POST['est_date'],"%Y-%m-%d")
            est_data.budget=request.POST['est_budget']
            date=dt.strftime("%d/%m/%Y")
            est_data.est_date=date
            est_data.save()
    return render(request,'Moderator/ApprovedSPRequest.html',{'request_list':request_list,'mod_name':mod_name,'mod_pic':mod_pic})




@auth_moderator
def ConfirmedSPRequest(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    request_list=StandPotIdeas.objects.filter(status="payment completed",mod_id=request.session['mod_id'])
    if request.method=='POST':
        req_data=StandPotIdeas.objects.get(id=request.POST['id'])
        if 'details' in request.POST:
            return render(request,'Moderator/StandPotDetails.html',{'req_data':req_data,})
        if 'completed' in request.POST:
            
            req_data.status='work completed'
            dt=datetime.today()
            # est_data.budget=request.POST['est_budget']
            date=dt.strftime("%d/%m/%Y")
            req_data.completed_date=date
            req_data.save()
    
    return render(request,'Moderator/ConfirmedSPRequest.html',{'request_list':request_list,'mod_name':mod_name,'mod_pic':mod_pic})

@auth_moderator
def ChangeModeratorPasswd(request):
    mod_name,mod_pic=getModName(request.session['mod_id'])
    form=ChangePasswordForm()
    mod_data=ModeratorDetails.objects.get(mod_id=request.session['mod_id'])
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            print('form is valid')
            user_old_passwd=form.cleaned_data['old_passwd']
            user_new_passwd=form.cleaned_data['new_passwd']
            user_confirm_passwd=form.cleaned_data['confirm_passwd']
            is_true=pbkdf2_sha256.verify(user_old_passwd,mod_data.mod_passwd)
            if is_true:
                if len(user_new_passwd)>=8:
                    if user_new_passwd==user_confirm_passwd:
                        new_encrypted_passwd=pbkdf2_sha256.hash(user_new_passwd,rounds=1000,salt_size=32)
                        mod_data.mod_passwd=new_encrypted_passwd
                        mod_data.save()
                        success_msg="Password Changed Succesfully"
                        return render(request,'Moderator/ChangeModeratorPassword.html',{'form':form,'success_msg':success_msg})
                    else:
                        error_msg="Password Mismatch"
                        return render(request,'Moderator/ChangeModeratorPassword.html',{'form':form,'error_msg':error_msg})
                else:
                    error_msg="Password Should be atleast 8 characters"
                    return render(request,'Moderator/ChangeModeratorPassword.html',{'form':form,'error_msg':error_msg})
            else:
                error_msg="Invalid Password! enter Your correct password"
                return render(request,'Moderator/ChangeModeratorPassword.html',{'form':form,'error_msg':error_msg})
    return render(request,'Moderator/ChangeModeratorPassword.html',{'form':form,'mod_name':mod_name,'mod_pic':mod_pic})