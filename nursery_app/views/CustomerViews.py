from django import http
from razorpay.resources import payment
from nursery_app.Forms.CustomerForms import CraftAddForm, FeedBackForm,GardenRequestForm, SellerRegForm, StandPotForm
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from ..models import CraftDetails, GardenProducts, CustomerDetails, GardenIdeas, NurseryProduct,CartDetails, OrderDetails, ProductFeedBack, Rating, RatingDetails, SellerReg, StandPotIdeas,ReturnProducts
from datetime import date, datetime,timedelta
from ..services import getPagination
from ..services import AddRating, AddToCart, UpdateCartItems, UpdateStarCount, getProductFeatures,getOrderNo,RatingCalculation, getProductNo, getSellerID, loadCart
from nursery_app.auth_guard import auth_customer
import razorpay



@auth_customer
def CustomerHome(request):
    try:
        seller_data=SellerReg.objects.get(cust_id=request.session['user_id'])
        request.session['sell_id']=seller_data.sell_id
       
    except:

        request.session['sell_id']=0
    return render(request,'Customer/CustomerHome.html')



@auth_customer
def ViewProducts(request):
    product_type=request.GET['p']

    if product_type=='plt' :id=1
    elif product_type=='pt':id=2
    elif product_type=='std':id=3
    elif product_type=='sd':id=4
    elif product_type=='frt':id=5
    elif product_type=='oth':id=6
    elif product_type=='crft':
         craft_products=CraftDetails.objects.all()
         
         return render(request,'Customer/ViewCraftProducts.html',{'craft_products':craft_products,})
    product_list=NurseryProduct.objects.filter(m_id=id)
   
    return render(request,'Customer/ViewProducts.html',{'product_list':product_list})


@auth_customer
def ProductDetails(request,pid):
    success=False
    exist=False
    success_msg=""
    exist_msg=""
    disable=""
    product_detail=NurseryProduct.objects.get(p_id=pid)
    cur_date=date.today()
    exp_date1=cur_date+timedelta(days=1)
    exp_date2=cur_date+timedelta(days=product_detail.p_exp_days)
    featuresKey,featuresValue=getProductFeatures(product_detail)
    stock=product_detail.p_stock
    product_rating=NurseryProduct.objects.get(p_id=pid)
    reviews_count=ProductFeedBack.objects.filter(nursey_id=pid).count()

    review_list=ProductFeedBack.objects.filter(nursey_id=pid)
   
    if stock<10:
        display=True
    else:
        
        display=False

    if stock==0:
        disable='disabled'
        
    if request.method=="POST":
        user=CustomerDetails.objects.get(cust_id=request.session['user_id'])
        qty=request.POST['txtQty']
        
        status=AddToCart(pid,'e_nursery',user,qty)
        if status=="exist":
            exist=True
          
            exist_msg=" Product Already In Cart"
        else:
            success=True
            success_msg="Product Added To Cart"
            
        
        context=   {'product_detail':product_detail,
            'exp_date1':exp_date1,
            'exp_date2':exp_date2,
            'featuresKey':featuresKey,
            'featuresValue':featuresValue,
            'display':display,
            'disable':disable,
            'count':reviews_count,
            'review_list':review_list,
            'rating':product_rating.p_rating,
            'success_msg':success_msg,
            'exist_msg':exist_msg,
            'success':success,
            'exist':exist
             }
        return render(request,'Customer/ProductDetails.html',context)
    
    
    return render(request,'Customer/ProductDetails.html',{'product_detail':product_detail,'exp_date1':exp_date1,'exp_date2':exp_date2,'featuresKey':featuresKey,'featuresValue':featuresValue,'display':display,'disable':disable,'count':reviews_count,'review_list':review_list,'rating':product_rating.p_rating})
    
    
  
@auth_customer  
def OrderHistory(request):
    cur_date=date.today()
    order_converted=cur_date.strftime("%d/%m/%Y")
    orders=OrderDetails.objects.filter(Q(order_status="delivered")|Q(order_status="cancelled"), cust_id=request.session['user_id'])
    page_obj=getPagination(orders,request.GET.get('page'))
    return render(request,'Customer/OrderHistory.html',{'orders':orders,'page_obj':order_converted})




@auth_customer
def CraftProductDetails(request,cr_id):
    disable=""
    success=False
    exist=False
    success_msg=""
    exist_msg=""
    product_detail=CraftDetails.objects.get(cr_id=cr_id)
    cur_date=date.today()
    exp_date1=cur_date+timedelta(days=1)
    exp_date2=cur_date+timedelta(days=product_detail.cr_exp_days)
    stock=product_detail.cr_stock
    reviews_count=ProductFeedBack.objects.filter(craft_id=cr_id).count()

    review_list=ProductFeedBack.objects.filter(craft_id=cr_id)
   
    if stock<10:
        display=True
    else:
        
        display=False

    if stock==0:
        disable='disabled'
        
    if request.method=="POST":
        user=CustomerDetails.objects.get(cust_id=request.session['user_id'])
        seller=SellerReg.objects.get(sell_id=request.POST['seller'])
        qty=request.POST['txtQty']
        status=AddToCart(cr_id,'seller',user,qty,seller)
        if status=="exist":
            exist=True
          
            exist_msg=" Product Already In Cart"
        else:
            success=True
            success_msg="Product Added To Cart"
    
    
    return render(request,'Customer/CraftDetail.html',{'product_detail':product_detail,'exp_date1':exp_date1,'exp_date2':exp_date2,'exist_msg':exist_msg,'exist':exist,'success_msg':success_msg,'success':success,'display':display,'disable':disable,'count':reviews_count,'review_list':review_list,})
    





@auth_customer
def Cart(request):
    checkOutDisble=""
    total=0
    cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
    for product in cart_list:
        total=total+product.total
    cart_count=CartDetails.objects.filter(cust_id=request.session['user_id']).count()
    if cart_count==0:
        checkOutDisble='disabled'   

        
    cart_data=CartDetails.objects.filter(cust_id=request.session['user_id'])

    cart=loadCart(cart_data)
    

    if request.method=='POST':
            if 'remove' in request.POST:
                pr_id=request.POST['pr_id']
                seller_type=request.POST['seller_type']
                if seller_type=='e_nursery':
            
                    cart_product=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
                else:
                    cart_product=CartDetails.objects.get(craft_product=pr_id,cust_id=request.session['user_id'])

                cart_product.delete()
                cart_data=CartDetails.objects.filter(cust_id=request.session['user_id'])
                cart=loadCart(cart_data)
                return redirect("e_nursery:cart")
            if 'update' in request.POST:
                pr_id=request.POST['pr_id']
                qty=request.POST['qty']
                cart_type=request.POST['cart_type']
                if cart_type=='e_nursery':

                    product_data=NurseryProduct.objects.get(p_id=pr_id)
                    cart_data=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
            
                    cart_data.qty=qty
                    cart_data.total=product_data.p_price * int(qty)
                elif cart_type=='craft':
                    
                    product_data=CraftDetails.objects.get(cr_id=pr_id)
                    cart_data=CartDetails.objects.get(craft_product=pr_id,cust_id=request.session['user_id'])
            
                    cart_data.qty=qty
                    cart_data.total=product_data.cr_price * int(qty)

                cart_data.save()
                return redirect("e_nursery:cart")
        
            if 'checkout' in request.POST:
                pr_id=request.POST['pr_id']
                seller_type=request.POST['seller_type']
                qty=request.POST['qty']
                if seller_type=='e_nursery':
                    UpdateCartItems(request.session['user_id'],"e_nursery",pr_id,qty)
                    product_data=NurseryProduct.objects.get(p_id=pr_id)
                    cart_data=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
                
                    total=cart_data.total
                    if int(cart_data.qty)<=int(product_data.p_stock):
                    
                        return render(request,'Customer/CheckOut.html',{'pr_id':pr_id,'seller_type':seller_type,'total':total})
                    else:
        
                        msg_nursery=True
                        cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                        return render(request,'Customer/Cart.html',{'cart_list':cart_list,'total':total,'checkOutDisble':checkOutDisble,'msg_nursery':msg_nursery,'cart_type':'e_nursery'})
                if seller_type=='seller':
                    UpdateCartItems(request.session['user_id'],"seller",pr_id,qty)
                    product_data=CraftDetails.objects.get(cr_id=pr_id)
                    cart_data=CartDetails.objects.get(craft_product=pr_id,cust_id=request.session['user_id'])
                    
                    
                
                    total=cart_data.total
                    seller_id=request.POST['seller_id']
                    if int(cart_data.qty)<=int(product_data.cr_stock):
                        return render(request,'Customer/CheckOut.html',{'pr_id':pr_id,'seller_type':seller_type,'total':total,'seller_id':seller_id,'cart_type':'craft'})
                    else:
                    
                        msg_craft=True
                        cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                    return render(request,'Customer/Cart.html',{'cart_list':cart_list,'total':total,'checkOutDisble':checkOutDisble,'msg_craft':msg_craft,'cart_type':'craft'})
                        

            
        
        
    
    
    if cart=='is_both':   
          
        return render(request,'Customer/Cart.html',{'cart_list':cart_list,'total':total,'checkOutDisble':checkOutDisble})
    elif cart=='is_nursery':
    
        return render(request,'Customer/NurseryCart.html',{'cart_list':cart_list,'total':total,'checkOutDisble':checkOutDisble})
    elif cart=='is_seller':
        
        seller_id=getSellerID(cart_list)
        return render(request,'Customer/CraftCart.html',{'cart_list':cart_list,'seller_id':seller_id,'total':total,'checkOutDisble':checkOutDisble})
            









@auth_customer
def OrderProduct(request):
    msg_arr=False
    i=0
    if request.method=='POST':
      
        if 'type' in request.POST:
            pr_id=request.POST['pr_id']
            seller_type=request.POST['seller_type']
            if seller_type=='e_nursery':
                    
                cart_data=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
                customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
                prd=NurseryProduct.objects.get(p_id=cart_data.nursery_product.p_id)
                shipping_address=request.POST['shipping_addr']
                order_date=date.today()
                order_no=getOrderNo('e_nursery')
                e=prd.p_exp_days
                exp_delivery=order_date+timedelta(days=e)
                qty=cart_data.qty
                total=cart_data.total
                prd.p_stock=prd.p_stock-qty
                order_converted=order_date.strftime("%d/%m/%Y")
                exp_converted=exp_delivery.strftime("%d/%m/%Y")
                    
                order=OrderDetails(order_no=order_no,sell_type="e_nursery",nursery_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
                shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
                order.save()
                prd.save()
                
                if prd.p_stock==0:
                    prd.p_status="out of order"
                prd.save()
                cart_data.delete()

                    
                

            if seller_type=='seller':
                    
                cart_data=CartDetails.objects.get(craft_product=pr_id,cust_id=request.session['user_id'])
                prd=CraftDetails.objects.get(cr_id=cart_data.craft_product.cr_id)
                

                customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
                seller_id=SellerReg.objects.get(sell_id=request.POST['seller_id'])
                shipping_address=request.POST['shipping_addr']
                order_date=date.today()
                order_no=getOrderNo('seller')
                e=prd.cr_exp_days
                exp_delivery=order_date+timedelta(days=e)
                qty=cart_data.qty
                total=cart_data.total
                prd.cr_stock=prd.cr_stock-qty
                order_converted=order_date.strftime("%d/%m/%Y")
                exp_converted=exp_delivery.strftime("%d/%m/%Y")
                    
                order=OrderDetails(order_no=order_no,sell_type="seller",seller_id=seller_id,craft_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
                shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
                order.save()
                prd.save()
                
                if prd.cr_stock==0:
                    prd.cr_status="out of order"
                prd.save()
                cart_data.delete()

        else:
            cart_type=request.POST['cart_type']
            cart_data=CartDetails.objects.filter(cust_id=request.session['user_id'])
            order_date=date.today()
            customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            shipping_address=request.POST['shipping_addr']
            
            if cart_type=='e_nursery':
                # print('pppppppppppp')
                # print(request.POST['amt'],'kkk')
                amt=request.POST['amt']
                order_currency="INR"
                
                client=razorpay.Client(auth=('rzp_test_uDR5CKMGQFhq9N','uTuv4wenuQqoclmfiZHAWZFp'))
                payment=client.order.create({
                    'amount':5000,
                    'currency':order_currency,
                    'payment_capture':'1'
                })
                cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                #return JsonResponse(payment)
                return render(request,'Customer/NurseryCart.html',{'cart_list':cart_list,'total':amt,'payment':payment})

               
                # for product in cart_data:
                    
                #     prd=NurseryProduct.objects.get(p_id=product.nursery_product.p_id)
                #     if product.qty<= prd.p_stock:
                #         e=prd.p_exp_days
                #         order_no=getOrderNo('e_nursery')
                #         exp_delivery=order_date+timedelta(days=e)
                #         qty=product.qty
                #         total=product.total
                        
                #         prd.p_stock=prd.p_stock-qty

                #         order_converted=order_date.strftime("%d/%m/%Y")
                #         exp_converted=exp_delivery.strftime("%d/%m/%Y")

                        
                #         order=OrderDetails(order_no=order_no,nursery_product=prd,sell_type="e_nursery",cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
                #         shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
                #         order.save()
                #         prd.save()
                #         cart_product=CartDetails.objects.get(nursery_product=product.nursery_product,cust_id=request.session['user_id'])
                #         cart_product.delete()
            
                #         if prd.p_stock==0:
                #             prd.p_status="out of order"
                #             prd.save()
                    
                checkOutDisble=""
                total=0
                cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                for product in cart_list:
                    total=total+product.total
                cart_count=CartDetails.objects.filter(cust_id=request.session['user_id']).count()
                if cart_count==0:
                    checkOutDisble='disabled'   
                
                cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                msg_arr=True
                return render(request,'Customer/NurseryCart.html',{'cart_list':cart_list,'total':total,'checkOutDisble':checkOutDisble,'msg_array':msg_arr})
           
            if cart_type=='craft':
                print('pppppppppppppppppppppppppppppppppppp')
                for product in cart_data:
                    prd=CraftDetails.objects.get(cr_id=product.craft_product.cr_id)
                    if product.qty<=prd.cr_stock:
                        order_no=getOrderNo('seller')
                        
                        e=prd.cr_exp_days
                        exp_delivery=order_date+timedelta(days=e)
                        qty=product.qty
                        total=product.total
                        seller_id=SellerReg.objects.get(sell_id=request.POST['seller_id']) #######
                        prd.cr_stock=prd.cr_stock-qty
                        order_converted=order_date.strftime("%d/%m/%Y")
                        exp_converted=exp_delivery.strftime("%d/%m/%Y")

                        order=OrderDetails(order_no=order_no,sell_type="seller",seller_id=seller_id,craft_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
                        shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
                        order.save()
                        prd.save()
                        cart_product=CartDetails.objects.get(craft_product=product.craft_product,cust_id=request.session['user_id'])
                        cart_product.delete()
                        msg_arr=True


                    
                    
                
                        if prd.cr_stock==0:
                            prd.cr_status="out of order"
                            prd.save()
                checkOutDisble=""
                total=0
                cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                for product in cart_list:
                    total=total+product.total
                cart_count=CartDetails.objects.filter(cust_id=request.session['user_id']).count()
                if cart_count==0:
                    checkOutDisble='disabled'   
                seller_id=request.POST['seller_id']
                cart_list=CartDetails.objects.filter(cust_id=request.session['user_id'])
                
                    
                
                return render(request,'Customer/CraftCart.html',{'cart_list':cart_list,'seller_id':seller_id,'total':total,'checkOutDisble':checkOutDisble,'msg_array':msg_arr})    
               
                    

        return redirect("e_nursery:cart")




@auth_customer
def updateCart(request):
    pr_id=request.GET['prod_id']
    qty=request.GET['qty']
    product_data=NurseryProduct.objects.get(p_id=pr_id)
    cart_data=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
    # qty=request.GET['qty']
    cart_data.qty=qty
    cart_data.total=product_data.p_price * int(qty)
    cart_data.save()
    return redirect("e_nursery:cart")




@auth_customer
def MyOrders(request):
    current_date=date.today()
    date_convrt=current_date.strftime("%d/%m/%Y")
    print(date_convrt)
    order_list=OrderDetails.objects.filter(cust_id=request.session['user_id'])
    if 'p_id' in request.GET:
        p_id=request.GET['p_id']
        product=OrderDetails.objects.get(cust_id=request.session['user_id'],nursery_product=p_id)
        product.order_status="cancelled"
        cancel_date=date.today()
        cancel_converted=cancel_date.strftime("%d/%m/%Y")
        product.exp_delivery=cancel_converted
        product.save()
        
        return redirect("e_nursery:cust_orders")
    return render(request,'Customer/MyOrders.html',{'order_list':order_list,'current_date':date_convrt})
        





@auth_customer
def FeedbackNursery(request):
    
    
    if request.method=='POST':
        star_count=request.POST['starCount']
        status=request.POST['status']   
        product_id=request.POST['prod']
        product=NurseryProduct.objects.get(p_id=product_id)
        customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
          
        if status=="update":
            customer_star=Rating.objects.get(product_id=product,customer=customer)   
            
            if star_count=="":
                star_count=customer_star.cust_star
            
            previous_star=customer_star.cust_star
            customerRating= RatingDetails.objects.get(product_id=product_id)
            UpdateStarCount(previous_star,star_count,customerRating)
           
            
            feedback=ProductFeedBack.objects.get(nursey_id=product_id,cust_id=request.session['user_id'])
            customerRating.save()
            customer_star.cust_star=int(star_count)
            customer_star.save()
            feedback.feedback=request.POST['feed_back']
            if 'pic' in request.FILES:
                feedback.prod_img=request.FILES['pic']
            else:
                feedback.prod_img="FeedBack/sales.png"  # should be changed to nopic.png
            feedback.save()
            RatingCalculation(product_id,'e_nursery')

            return redirect("e_nursery:cust_orders") 
            
        
        else:
            # product_id=request.POST['prod']
            # product=NurseryProduct.objects.get(p_id=product_id)
            # customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            
            # star_count=request.POST['starCount']
            rating_model=RatingDetails.objects.get(product_id=product_id)

            if star_count=="":
                star_count=5
                rating_model.five_star+=1
            Rating(product_id=product,customer=customer,cust_star=star_count).save()
            if  star_count=='1':
                
               
                rating_model.one_star+=1
            if  star_count=='2':
                
               
                rating_model.two_star+=1
                
            elif star_count=='3':
               
                rating_model.three_star+=1
                    
            elif star_count=='4':
                rating_model.four_star+=1
                
            elif star_count=='5':
                rating_model.five_star+=1
                    
           
            rating_model.save()
            RatingCalculation(product_id,'e_nursery')
            customer_feedback=request.POST['feed_back']                
            if 'pic' in request.FILES:
                product_pic=request.FILES['pic']
            else:
                product_pic="FeedBack/sales.png"  # should be changed to nopic.png
            feed_date=date.today()
            feed_converted=feed_date.strftime("%d/%m/%Y")
            feedback=ProductFeedBack(nursey_id=product,cust_id=customer,feedback_date=feed_converted,feedback=customer_feedback,prod_img=product_pic)
            feedback.save()
            return redirect("e_nursery:cust_orders")
            
    
    product_id=request.GET['p_id']
     
    
        
    rating_exist=Rating.objects.filter(customer_id=request.session['user_id'],product_id=product_id).exists()

    rating_model=RatingDetails.objects.get(product_id=product_id)

    if rating_exist:
        
        data=Rating.objects.get(product_id=product_id,customer=request.session['user_id'])
        
        status="update"
        product_feedback=ProductFeedBack.objects.get(nursey_id=product_id,cust_id=request.session['user_id'])
        return render(request,'Customer/NurseryFeedback.html',{'id':product_id,'data':data,'feedback':product_feedback,'status':status,})
    
 
    return render(request,'Customer/NurseryFeedback.html',{'id':product_id,})















@auth_customer
def FeedbackCraft(request):
    
   
    if request.method=='POST':
        star_count=request.POST['starCount']
        status=request.POST['status']
        
        
        if status=="update":
            product_id=request.POST['prod']
            product=CraftDetails.objects.get(cr_id=product_id)
            customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            customer_star=Rating.objects.get(craft_id=product,customer=customer)
            if star_count=="":
                star_count=customer_star.cust_star
            
            previous_star=customer_star.cust_star
            customerRating= RatingDetails.objects.get(craft_id=product_id)
            if previous_star==star_count:
                pass
            
            else:
                if previous_star==1:
                    customerRating.one_star-=1
                if previous_star==2:
                        customerRating.two_star-=1
                if previous_star==3:
                        customerRating.three_star-=1
                if previous_star==4:
                        customerRating.four_star-=1
                if previous_star==5:
                        customerRating.five_star-=1
                
                if star_count=='1':
                    customerRating.one_star+=1
                if star_count=='2':
                    customerRating.two_star+=1

                if star_count=='3':
                    customerRating.three_star+=1
                if star_count=='4':
                    customerRating.four_star+=1
                if star_count=='5':
                    customerRating.five_star+=1
            
            feedback=ProductFeedBack.objects.get(craft_id=product_id,cust_id=request.session['user_id'])
            customerRating.save()
            customer_star.cust_star=int(star_count)
            customer_star.save()
            feedback.feedback=request.POST['feed_back']
            if 'pic' in request.FILES:
                feedback.prod_img=request.FILES['pic']
            else:
                feedback.prod_img="FeedBack/sales.png"  # should be changed to nopic.png
            feedback.save()
            RatingCalculation(product_id,'seller')

            return redirect("e_nursery:cust_orders") 
            
        
        else:
            product_id=request.POST['prod']
            product=CraftDetails.objects.get(cr_id=product_id)
            customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            
            star_count=request.POST['starCount']
            rating_model=RatingDetails.objects.get(craft_id=product_id)

            if star_count=="":
                star_count=5
                rating_model.five_star+=1
            Rating(craft_id=product,customer=customer,cust_star=star_count).save()
            if  star_count=='1':
                
                
                rating_model.one_star+=1
            if  star_count=='2':
                
               
                rating_model.two_star+=1
                
            elif star_count=='3':
               
                rating_model.three_star+=1
                    
            elif star_count=='4':
                rating_model.four_star+=1
                
            elif star_count=='5':
                rating_model.five_star+=1
                    
           
            rating_model.save()
            RatingCalculation(product_id,'e_nursery')
            customer_feedback=request.POST['feed_back']                
            if 'pic' in request.FILES:
                product_pic=request.FILES['pic']
            else:
                product_pic="FeedBack/sales.png"  # should be changed to nopic.png
            feed_date=date.today()
            feed_converted=feed_date.strftime("%d/%m/%Y")
            feedback=ProductFeedBack(craft_id=product,cust_id=customer,feedback_date=feed_converted,feedback=customer_feedback,prod_img=product_pic)
            feedback.save()
            return redirect("e_nursery:cust_orders")
            
    
    product_id=request.GET['p_id']
     
    
        
    rating_exist=Rating.objects.filter(customer_id=request.session['user_id'],craft_id=product_id).exists()

    rating_model=RatingDetails.objects.get(craft_id=product_id)

    if rating_exist:
        
        data=Rating.objects.get(craft_id=product_id,customer=request.session['user_id'])
        
        status="update"
        product_feedback=ProductFeedBack.objects.get(craft_id=product_id,cust_id=request.session['user_id'])
        return render(request,'Customer/CraftFeedback.html',{'id':product_id,'data':data,'feedback':product_feedback,'status':status,})
    
   
    return render(request,'Customer/CraftFeedback.html',{'id':product_id,})













# def StarRating(request,p_id):
#     if 'star1' in request.POST:
#         rating="one_star"
#     if 'star2' in request.POST:
#         rating="two_star"
#     if 'star3' in request.POST:
#        rating="three_star"
#     if 'star4' in request.POST:
#         rating="four_star"
#     if 'star5' in request.POST:
#         rating="five_star"
    
#     rating_exist=RatingDetails.objects.filter(customer_id=request.session['user_id'],product_id=p_id).exists()
#     if not rating_exist:

#         customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
#         product=NurseryProduct.objects.get(p_id=p_id)
        
#         #rating_qry=RatingDetails(customer_id=customer,product_id=product,rating=)

#     return HttpResponse('')


# def doRating(request):
#     product=request.GET['product']
#     star=request.GET['star']
#     return redirect("e_nursery:prod_feedback")


@auth_customer
def RequestGardenIdeas(request):
    form=GardenRequestForm()
    if request.method=='POST':
        form=GardenRequestForm(request.POST,request.FILES)
        if form.is_valid():
            requirements=form.cleaned_data['requirements']
            exp_date=form.cleaned_data['exp_date']
            budget=form.cleaned_data['budget']
            plot_pic=form.cleaned_data['plot_pic']
            cust_id=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            status="pending"
            posted_date=date.today()
            date_converted=posted_date.strftime("%d/%m/%Y")
            req_query=GardenIdeas(plot_pic=plot_pic,requirements=requirements,date_posted=date_converted,exp_date=exp_date,budget=budget,cust_id=cust_id,status=status)
            req_query.save()
            success_msg="Requirements Submitted Succesfully"
            return render(request,'Customer/GardenIdeas.html',{'form':form,'success_msg':success_msg})
    return render(request,'Customer/GardenIdeas.html',{'form':form})


@auth_customer
def GardenRequest(request):
    request_list=GardenIdeas.objects.filter((~Q(status='pending')|~Q(status='completed')),cust_id=request.session['user_id'])
    
    page_obj=getPagination(request_list,request.GET.get('page'))
    if request.method=='POST':
        if 'confirm' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            req_data.status="payment completed"
            req_data.save()
        if 'reject' in request.POST:
            req_id=request.POST['req_id']
            req_data=GardenIdeas.objects.get(req_id=req_id)
            req_data.status="customer rejected"
            g_products=GardenProducts.objects.get(req_id=req_id)
            g_products.delete()
            req_data.save()

    return render(request,'Customer/GardenRequest.html',{'request_list':page_obj})



@auth_customer
def ViewEstimation(request,req_id):
    total=0

    if request.method=='POST':
        p_id=request.POST['p_id']
        data=GardenProducts.objects.get(product_id=p_id)
        data.delete()
    est_data=GardenIdeas.objects.get(req_id=req_id)
    est_prod=GardenProducts.objects.filter(req_id=req_id)
    
    for item in est_prod:
        total=total+item.total_amt
    
      
    return render(request,'Customer/ViewEstProducts.html',{'est_prod':est_prod,'total':total,'est_data':est_data})
    

@auth_customer    
def StandPotRequest(request):
    form=StandPotForm()
    if request.method=='POST':
        form=StandPotForm(request.POST,request.FILES)
        if form.is_valid():
            item=form.cleaned_data['item']
            design=form.cleaned_data['design']
            requirements=form.cleaned_data['requirements']
            cust_id=CustomerDetails.objects.get(cust_id=request.session['user_id'])
            status="pending"
            posted_date=date.today()
            date_converted=posted_date.strftime("%d/%m/%Y")
            qry=StandPotIdeas(cust_id=cust_id,item=item,requirements=requirements,posted_date=date_converted,design=design,status=status)
            qry.save()
            success_msg="Requirements Posted Succesfully"
            return render(request,'Customer/StandPotRequest.html',{'form':form,'success_msg':success_msg})
    return render(request,'Customer/StandPotRequest.html',{'form':form,})


@auth_customer
def ViewStandPotRequest(request):
    standpot_list=StandPotIdeas.objects.filter(cust_id=request.session['user_id'])
    page_obj=getPagination(standpot_list,request.GET.get('page'))
    if request.method=='POST':
        id=request.POST['req_id']
        data=StandPotIdeas.objects.get(id=id)
        if 'confirm' in request.POST:
            data.status="payment completed"
            
        if 'reject' in request.POST:
            data.status="customer rejected"
        data.save()
    return render(request,'Customer/ViewStandPotRequest.html',{'standpot_list':page_obj})



@auth_customer
def SellerRequest(request):
    form=SellerRegForm()
    show_form=True
    already_registered=SellerReg.objects.filter(cust_id=request.session['user_id']).exists()
    
    if not already_registered:
        
        msg=""
        if request.method=='POST':
            form=SellerRegForm(request.POST,request.FILES)
            if form.is_valid():
                cust_id=CustomerDetails.objects.get(cust_id=request.session['user_id'])
                sell_name=form.cleaned_data['sell_name'].lower()
                sell_exp=form.cleaned_data['sell_exp']
                doc_type=form.cleaned_data['doc_type']
                doc=form.cleaned_data['doc']
                about_me=form.cleaned_data['about_me'].lower()
                qry=SellerReg(cust_id=cust_id,sell_name=sell_name,sell_exp=sell_exp,doc_type=doc_type,doc=doc,about_me=about_me,status="pending")
                qry.save()
                msg="Request Submitted Succesfully"
                return render(request,'Customer/SellerRequest.html',{'form':form,'msg':msg,'show':show_form})
        return render(request,'Customer/SellerRequest.html',{'form':form,'msg':msg,'show':show_form})
    else:
        reg_data=SellerReg.objects.get(cust_id=request.session['user_id'])
        if reg_data.status=='approved':
            form=CraftAddForm()
            if not 'sell_id' in request.POST:
                request.session['sell_id']=reg_data.sell_id
              
            return render(request,'Customer/AddProducts.html',{'form':form})
        elif reg_data.status=='pending':
            show_form=False
            status_msg="Your Request Is Not Approved Yet"
            return render(request,'Customer/SellerRequest.html',{'form':form,'show':show_form,'status_msg':status_msg})
        elif reg_data.status=='rejected':
            show_form=False
            status_msg="Your Request Has Been Rejected By Admin"
            return render(request,'Customer/SellerRequest.html',{'form':form,'show':show_form,'status_msg':status_msg})



@auth_customer
def AddProducts(request):

    msg=""
    form=CraftAddForm(request.POST,request.FILES)
    print('formmmmm',form)
    if form.is_valid():
        cr_name=form.cleaned_data['cr_name'].lower()
        cr_type=form.cleaned_data['cr_type']
        cr_color=form.cleaned_data['cr_color'].lower()
        cr_material=form.cleaned_data['cr_material'].lower()
        cr_desc=form.cleaned_data['cr_desc'].lower()
        cr_exp_days=form.cleaned_data['cr_exp_days']
        cr_stock=form.cleaned_data['cr_stock']
        cr_sales_pack=form.cleaned_data['cr_sales_pack'].lower()
        cr_img=form.cleaned_data['cr_img']
        cr_price=form.cleaned_data['cr_price']
        prod_no=getProductNo("seller")
        cr_status='available'
        seller_id=SellerReg.objects.get(sell_id=request.session['sell_id'])

        product_exist=CraftDetails.objects.filter(cr_name=cr_name).exists()

        if not product_exist:
            product=CraftDetails(seller_id=seller_id,cr_name=cr_name,cr_type=cr_type,cr_color=cr_color,cr_material=cr_material,cr_desc=cr_desc,cr_exp_days=cr_exp_days,cr_stock=cr_stock,cr_sales_pack=cr_sales_pack,cr_img=cr_img,prod_no=prod_no,cr_price=cr_price,cr_status=cr_status)

            product.save()
            p_id=CraftDetails.objects.filter(seller_id=request.session['sell_id']).latest('cr_id')
            AddRating(p_id,'seller')
            success_msg="Product Added Succesfully"
            return render(request,'Customer/AddProducts.html',{'form':form,'success_msg':success_msg})
        else:
            error_msg="Product Already Added"
            form=CraftAddForm()
            return render(request,'Admin/AddProducts.html',{'form':form,'error_msg':error_msg})

    else:
        print(form.errors)
    return render(request,'Customer/AddProducts.html',{'form':form})



 
@auth_customer       
def ViewCraftProducts(request):
    craft_products=CraftDetails.objects.all()
    return render(request,'Customer/ViewCraftProducts.html',{'craft_products':craft_products,})



@auth_customer
def ViewOrders(request):
   
    order_list=OrderDetails.objects.filter(Q(order_status='ordered')|Q( order_status='packed'),seller_id=request.session['sell_id'],)
    page_obj=getPagination(order_list,request.GET.get('page'))
    return render(request,'Customer/ViewOrders.html',{'order_list':page_obj})





@auth_customer
def OrderDetail(request,ord_no):
    order_detail=OrderDetails.objects.get(order_no=ord_no)
    if request.method=='POST':
        if 'packed' in request.POST:
            order_detail.order_status='packed'
        if 'delivered' in request.POST:
            order_detail.order_status='delivered'
            deliver_date=date.today()
            deliver_converted=deliver_date.strftime("%d/%m/%Y")
            order_detail.exp_delivery=deliver_converted
        order_detail.save()
        return redirect("e_nursery:view_orders")
    
    return render(request,'Customer/OrderDetails.html',{'order_data':order_detail})


@auth_customer
def MyProducts(request):
    exist=True
    products=CraftDetails.objects.filter(seller_id=request.session['sell_id'])
    page_obj=getPagination(products,request.GET.get('page'))
    if request.method=='POST':
        prod_no=request.POST['prod_no']
        products=CraftDetails.objects.filter(prod_no=prod_no)
        page_obj=getPagination(products,1)
        if  products.exists():
            
            products=CraftDetails.objects.filter(seller_id=request.session['sell_id'])
        else:
            products=CraftDetails.objects.filter(seller_id=request.session['sell_id'])
            exist=False
    return render(request,'Customer/MyProducts.html',{'products':page_obj,'exist':exist})



@auth_customer
def UpdateStock(request):
    
    
    if request.method=='POST':
        p_no=request.POST['p_no']
        product=CraftDetails.objects.get(prod_no=p_no)
        stock=product.cr_stock
        product.cr_stock=request.POST['new_stock']
        product.save()
        return redirect("e_nursery:my_prod")
    p_no=request.GET['no']
    product=CraftDetails.objects.get(prod_no=p_no)
    stock=product.cr_stock
    return render(request,'Customer/Stock.html',{'p_no':p_no,'stock':stock})


def ReturnProduct(request,ord_no):
    order_details=OrderDetails.objects.get(order_no=ord_no)
    customer_details=CustomerDetails.objects.get(cust_id=request.session['user_id'])
    if request.method=='POST':
        img=request.FILES['img']
        reason=request.POST['reason']
        already_exist=ReturnProducts.objects.filter(order_no=ord_no).exists()
        if not already_exist:
            return_data=ReturnProducts(order_no=order_details,prod_img=img,reason=reason,status="pending",cust_id=customer_details)
            return_data.save()
            order_details.order_status="returned"
            order_details.save()
            success_msg="Request submitted Succesfully"
            return render(request,'Customer/ReturnProduct.html',{'success_msg':success_msg,'order_no':ord_no})
         
        else:
            error_msg="Request Already Submitted"
            return render(request,'Customer/ReturnProduct.html',{'error_msg':error_msg,'order_no':ord_no})
        
    
    
    return render(request,'Customer/ReturnProduct.html',{'order_no':ord_no,})



def ViewReturnProduct(request):
    product_list=ReturnProducts.objects.filter(cust_id=request.session['user_id'])
   

    return render(request,'Customer/ViewReturnPDetails.html',{'product_list':product_list})



def NurseryPaySuccess(request):

    
    cart_data=CartDetails.objects.filter(cust_id=request.session['user_id'])
    order_date=date.today()
    customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
    shipping_address=request.GET['addr']
    
   
    
     

    
    for product in cart_data:
        
        prd=NurseryProduct.objects.get(p_id=product.nursery_product.p_id)
        if product.qty<= prd.p_stock:
            e=prd.p_exp_days
            order_no=getOrderNo('e_nursery')
            exp_delivery=order_date+timedelta(days=e)
            qty=product.qty
            total=product.total
            
            prd.p_stock=prd.p_stock-qty

            order_converted=order_date.strftime("%d/%m/%Y")
            exp_converted=exp_delivery.strftime("%d/%m/%Y")

            
            order=OrderDetails(order_no=order_no,nursery_product=prd,sell_type="e_nursery",cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
            shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
            order.save()
            prd.save()
            cart_product=CartDetails.objects.get(nursery_product=product.nursery_product,cust_id=request.session['user_id'])
            cart_product.delete()

            if prd.p_stock==0:
                prd.p_status="out of order"
                prd.save()
            
        return redirect("e_nursery:cust_home")



def CraftPaySuccess(request):
    cart_data=CartDetails.objects.filter(cust_id=request.session['user_id'])
    order_date=date.today()
    order_no=getOrderNo('e_nursery')
   
    customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
    shipping_address=request.GET['addr']
    for product in cart_data:
        prd=CraftDetails.objects.get(cr_id=product.craft_product.cr_id)
        if product.qty<=prd.cr_stock:
            order_no=getOrderNo('seller')
            
            e=prd.cr_exp_days
            exp_delivery=order_date+timedelta(days=e)
            qty=product.qty
            total=product.total
            seller_id=SellerReg.objects.get(sell_id=request.GET['sell']) #######
            prd.cr_stock=prd.cr_stock-qty
            order_converted=order_date.strftime("%d/%m/%Y")
            exp_converted=exp_delivery.strftime("%d/%m/%Y")

            order=OrderDetails(order_no=order_no,sell_type="seller",seller_id=seller_id,craft_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
            shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
            order.save()
            prd.save()
            cart_product=CartDetails.objects.get(craft_product=product.craft_product,cust_id=request.session['user_id'])
            cart_product.delete()
            


        
                
            
        if prd.cr_stock==0:
            prd.cr_status="out of order"
            prd.save()

        return redirect("e_nursery:cust_home")      \


def CheckOutSuccess(request):
    pr_id=request.GET['pr_id']
    seller_type=request.GET['stype']
    if seller_type=='e_nursery':
            
        cart_data=CartDetails.objects.get(nursery_product=pr_id,cust_id=request.session['user_id'])
        customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
        prd=NurseryProduct.objects.get(p_id=cart_data.nursery_product.p_id)
        shipping_address=request.GET['addr']
        order_date=date.today()
        order_no=getOrderNo('e_nursery')
        e=prd.p_exp_days
        exp_delivery=order_date+timedelta(days=e)
        qty=cart_data.qty
        total=cart_data.total
        prd.p_stock=prd.p_stock-qty
        order_converted=order_date.strftime("%d/%m/%Y")
        exp_converted=exp_delivery.strftime("%d/%m/%Y")
            
        order=OrderDetails(order_no=order_no,sell_type="e_nursery",nursery_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
        shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
        order.save()
        prd.save()
        
        if prd.p_stock==0:
            prd.p_status="out of order"
        prd.save()
        cart_data.delete()

            
        

    if seller_type=='seller':
            
        cart_data=CartDetails.objects.get(craft_product=pr_id,cust_id=request.session['user_id'])
        prd=CraftDetails.objects.get(cr_id=cart_data.craft_product.cr_id)
        

        customer=CustomerDetails.objects.get(cust_id=request.session['user_id'])
        seller_id=SellerReg.objects.get(sell_id=request.GET['sell'])
        shipping_address=request.GET['addr']
        order_date=date.today()
        order_no=getOrderNo('seller')
        e=prd.cr_exp_days
        exp_delivery=order_date+timedelta(days=e)
        qty=cart_data.qty
        total=cart_data.total
        prd.cr_stock=prd.cr_stock-qty
        order_converted=order_date.strftime("%d/%m/%Y")
        exp_converted=exp_delivery.strftime("%d/%m/%Y")
            
        order=OrderDetails(order_no=order_no,sell_type="seller",seller_id=seller_id,craft_product=prd,cust_id=customer,order_date=order_converted,exp_delivery=exp_converted,
        shipping_address=shipping_address,qty=qty,total=total,order_status='ordered')
        order.save()
        prd.save()
        
        if prd.cr_stock==0:
            prd.cr_status="out of order"
        prd.save()
        cart_data.delete()
    return redirect("e_nursery:cust_home")