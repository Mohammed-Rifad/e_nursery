from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator

from nursery_app.models import CartDetails, CraftDetails, NurseryProduct,OrderDetails, RatingDetails,ModeratorDetails


def getProductFeatures(product_data):
    FeaturesKey={}
    FeaturesValue={}
    if product_data.m_id.m_id==1:
        feat1="Type"
        feat1Val=product_data.cat_id.c_name.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Conatiner Type"
        feat3Val=product_data.p_container
        feat4="Caring Tips"
        feat4Val=product_data.p_caring_tips

        
        
    if product_data.m_id.m_id==2:
        feat1="Location Suitable"
        feat1Val=product_data.p_location.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Material"
        feat3Val=product_data.p_material
        feat4="Color"
        feat4Val=product_data.p_color.title()

    if product_data.m_id.m_id==3:
        feat1="Location Suitable"
        feat1Val=product_data.p_location.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Shape"
        feat3Val=product_data.p_shape
        feat4="Color"
        feat4Val=product_data.p_color.title()
    
    if product_data.m_id.m_id==4:
        feat1="Location Suitable"
        feat1Val=product_data.p_location.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Shape"
        feat3Val=product_data.p_shape
        feat4="Color"
        feat4Val=product_data.p_color.title()
    
    if product_data.m_id.m_id==5:
        feat1="Type"
        feat1Val=product_data.p_type.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Shape"
        feat3Val=product_data.p_shape
        feat4="Color"
        feat4Val=product_data.p_color.title()

    if product_data.m_id.m_id==6:
        feat1="Location Suitable"
        feat1Val=product_data.p_location.title()
        feat2="Sales package"
        feat2Val=product_data.p_sales_package
        feat3="Shape"
        feat3Val=product_data.p_shape
        feat4="Color"
        feat4Val=product_data.p_color.title()

    FeaturesKey['feat1']=feat1
    FeaturesKey['feat2']=feat2
    FeaturesKey['feat3']=feat3
    FeaturesKey['feat4']=feat4

    FeaturesValue['value1']=feat1Val.title()
    FeaturesValue['value2']=feat2Val.title()
    FeaturesValue['value3']=feat3Val.title()
    FeaturesValue['value4']=feat4Val
    
       
    return FeaturesKey,FeaturesValue


def AddToCart(p_id,sell_type,u_id,qty,seller=0):
    if sell_type=='e_nursery':

        product_data=NurseryProduct.objects.get(p_id=p_id)
 
        price=product_data.p_price * int(qty)
        product_exist=CartDetails.objects.filter(nursery_product=p_id,cust_id=u_id).exists()
        if not product_exist:  
            cart=CartDetails(sell_type=sell_type,nursery_product=product_data,cust_id=u_id,qty=qty,total=price)
            cart.save()
        else:
            return 'exist'
    else:
        product_data=CraftDetails.objects.get(cr_id=p_id)
        price=product_data.cr_price * int(qty)
        product_exist=CartDetails.objects.filter(craft_product=p_id,cust_id=u_id).exists()
        if not product_exist:  
            cart=CartDetails(sell_type=sell_type,seller_id=seller,craft_product=product_data,cust_id=u_id,qty=qty,total=price)
            cart.save()
        else:
            return 'exist'
def getOrderNo(type):
      order_id=randint(1000000000,9999999999)
      if type=="e_nursery":
        order_no="OD"+str(order_id)
      else:
          order_no="ODSL"+str(order_id)
      exist=OrderDetails.objects.filter(order_no=order_no).exists()
      if exist:
          getOrderNo()
      return order_no


def getProductNo(pr_type):
    prod_id=randint(1000000000,9999999999)
    if pr_type=="e_nursery":
    
        product_no="PR"+str(prod_id)
        exist=NurseryProduct.objects.filter(prod_no=product_no).exists()
        
    else:
        product_no="PRSL"+str(prod_id)
        exist=CraftDetails.objects.filter(prod_no=product_no).exists()
    if exist:
            getProductNo()
    return product_no




def AddRating(p_id,pr_type):
    if pr_type=="e_nursery":
        rating=RatingDetails(product_id=p_id,five_star=300,four_star=250,three_star=200,two_star=100,one_star=50)
    else:
        rating=RatingDetails(craft_id=p_id,five_star=300,four_star=250,three_star=200,two_star=100,one_star=50)

    rating.save()

def RatingCalculation(p_id,pr_type):
    
    if pr_type=="e_nursery":
        product_rating=RatingDetails.objects.get(product_id=p_id)
    else:
        product_rating=RatingDetails.objects.get(craft_id=p_id)

    rating=((product_rating.five_star * 5)+(product_rating.four_star * 4) + (product_rating.three_star * 3) + (product_rating.two_star * 2) + (product_rating.one_star * 1)) / ( product_rating.five_star + product_rating.four_star +product_rating.three_star +product_rating.two_star + product_rating.one_star)
    product=NurseryProduct.objects.get(p_id=p_id)
    product.p_rating=rating
    product.save()
    

def getModID():
      mod_id=randint(10000,99999)
      
      
      exist=ModeratorDetails.objects.filter(mod_id=mod_id).exists()
      if exist:
          getModID()
      return mod_id


def email_moderator(mail_recipient,user_id,passwd):
    subject="username and password"
    message="Hi your username is "+str(user_id)+" and temporary password is "+passwd
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)


def loadCart(products):
    is_nursery=False
    is_seller=False
    

    for product in products:
        if product.sell_type=='e_nursery':
            is_nursery=True
        if product.sell_type=='seller':
            is_seller=True
            
    if is_nursery==True and is_seller==True:
        return 'is_both'
    elif is_nursery==True:
        return 'is_nursery'
    else:
        return 'is_seller'


def getSellerID(cart_list):
    if cart_list.exists():
        for data in cart_list:
            id=data.seller_id
        try:
            return id.sell_id
        except:
            None


def getPagination(model,p_no):
    paginator=Paginator(model,2)
    
    page_obj=paginator.get_page(p_no)
    return page_obj


def UpdateCartItems(user,p_type,p_id,qty):
    if p_type=="e_nursery":
        product_data=NurseryProduct.objects.get(p_id=p_id)
        cart_data=CartDetails.objects.get(nursery_product=p_id,cust_id=user)
        price=product_data.p_price
    elif p_type=="seller":
        product_data=CraftDetails.objects.get(cr_id=p_id)
        cart_data=CartDetails.objects.get(craft_product=p_id,cust_id=user)
        price=product_data.cr_price
    cart_data.qty=qty
    cart_data.total=price * int(qty)
    cart_data.save()

def UpdateStarCount(previous_star,current_star,model):
    if previous_star==current_star:
                pass
            
    else:
        if previous_star==1:
            model.one_star-=1
        if previous_star==2:
                model.two_star-=1
        if previous_star==3:
                model.three_star-=1
        if previous_star==4:
                model.four_star-=1
        if previous_star==5:
                model.five_star-=1
        
        if current_star=='1':
            model.one_star+=1
        if current_star=='2':
            model.two_star+=1

        if current_star=='3':
            model.three_star+=1
        if current_star=='4':
            model.four_star+=1
        if current_star=='5':
            model.five_star+=1

def getModName(id):
    moderator=ModeratorDetails.objects.get(mod_id=id)
    return moderator.mod_name,moderator.mod_pic
   
