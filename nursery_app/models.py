
from os import stat
from django import db
from django.db import models
from django.db.models.base import Model
from django.http import request
from passlib.hash import pbkdf2_sha256
# Create your models here.



class AdminDetails(models.Model):
    login_id=models.CharField(max_length=20,db_column="log_id")
    login_passwd=models.CharField(max_length=120,db_column='passwd')

    class Meta:
        db_table="tb_super"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.login_passwd)

class MainCategory(models.Model):
    m_id=models.AutoField(primary_key=True,db_column="m_id")
    m_name=models.CharField(max_length=20,db_column="m_name")
  
    class Meta:
        db_table="tb_main"

class CategoryDetails(models.Model):
    
    c_id=models.AutoField(primary_key=True,db_column="c_id")
    m_id=models.ForeignKey(MainCategory,on_delete=models.CASCADE,db_column="m_id")
    c_name=models.CharField(max_length=30,db_column="c_name")
    c_desc=models.CharField(max_length=200,db_column="c_desc")
    c_img=models.ImageField(upload_to="Category/",db_column="c_img")

    class Meta:
        db_table="tb_category"


class NurseryProduct(models.Model):
    p_id=models.AutoField(primary_key=True,db_column="p_id")
    prod_no=models.CharField(max_length=20,db_column="prod_no")
    cat_id=models.ForeignKey(CategoryDetails,on_delete=models.CASCADE,db_column="cat_id",null=True)
    m_id=models.ForeignKey(MainCategory,on_delete=models.CASCADE,db_column="m_id")
    p_name=models.CharField(max_length=20,db_column="p_name")
    p_desc=models.CharField(max_length=200,db_column="p_desc")
    p_dimension=models.CharField(max_length=30,db_column="p_dimension")
    p_location=models.CharField(max_length=20,db_column="p_location")
    p_color=models.CharField(max_length=10,db_column="p_color")
    p_sales_package=models.CharField(max_length=20,db_column="p_package")
    p_material=models.CharField(max_length=20,db_column="p_material",default="")
    p_shape=models.CharField(max_length=20,db_column="p_shape",default="")
    p_qty=models.IntegerField(db_column="p_qty",null=True)
    p_type=models.CharField(max_length=20,db_column="p_type",default="")
    p_suitable_for=models.CharField(max_length=20,db_column="p_suitable")
    p_seed=models.CharField(max_length=20,db_column="p_seed")
    p_container=models.CharField(max_length=20,db_column="p_container",null=True)
    p_caring_tips=models.CharField(max_length=200,db_column="p_tips",null=True)
    p_features=models.CharField(max_length=100,db_column="p_features")
    p_price=models.FloatField(db_column="p_price")
    p_offer=models.FloatField(db_column="p_offer",default=0)
    p_rating=models.FloatField(db_column="p_rating",default=0)
    p_exp_days=models.IntegerField(db_column="p_expected_days")
    p_img=models.ImageField(upload_to="Products/",db_column="p_img")
    p_stock=models.IntegerField(db_column="p_stock",default=0)
    p_status=models.CharField(max_length=20,default="available")
    
    class Meta:
        db_table="tb_nursery_product"

class CustomerDetails(models.Model):
    cust_id=models.AutoField(primary_key=True)
    cust_name=models.CharField(max_length=30,db_column="c_name")
    cust_address=models.CharField(max_length=255,db_column="c_address")
    cust_phno=models.CharField(max_length=10,db_column="c_phno")
    cust_email=models.CharField(max_length=40,db_column="c_email")
    cust_passwd=models.CharField(max_length=40,db_column="c_passwd")
    cust_img=models.ImageField(upload_to="Customer/",db_column="c_img")
    class Meta:
        db_table="tb_customer"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.cust_passwd)

        
class SellerReg(models.Model):
    sell_id=models.AutoField(primary_key=True,db_column="sel_id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="c_id")
    sell_name=models.CharField(max_length=30,db_column="s_name")
    sell_exp=models.IntegerField(db_column="s_exp")
    doc_type=models.CharField(max_length=20,db_column="doc_type")
    doc=models.FileField(upload_to="Seller/Documents",db_column="seller_doc")
    about_me=models.CharField(max_length=200,db_column='abt_me')
    status=models.CharField(max_length=10,db_column="status")
    
    class Meta:
        db_table="tb_seller"

class CraftDetails(models.Model):
    cr_id=models.AutoField(primary_key=True,db_column="cr_id")
    seller_id=models.ForeignKey(SellerReg,on_delete=models.CASCADE,db_column="sel_id")
    # cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="c_id")
    cr_name=models.CharField(max_length=30,db_column="cr_name")
    cr_type=models.CharField(max_length=20,db_column="c_type")
    prod_no=models.CharField(max_length=20,db_column="p_no")
    cr_color=models.CharField(max_length=10,db_column="cr_clr")
    cr_material=models.CharField(max_length=20,db_column="cr_material")
    cr_desc=models.CharField(max_length=200,db_column="cr_desc")
    cr_exp_days=models.IntegerField(db_column='p_exp')
    cr_rating=models.FloatField(db_column="cr_rating",default=3.72)
    cr_price=models.FloatField(db_column="price",default=0.0)
    cr_sales_pack=models.CharField(max_length=30,db_column="package")
    cr_img=models.ImageField(upload_to="Seller/Products",db_column="cr_img")
    cr_stock=models.IntegerField(db_column="p_stock",default=0)
    cr_status=models.CharField(max_length=20)

    class Meta:
        db_table="tb_craft"

class CartDetails(models.Model):
    cart_id=models.AutoField(primary_key=True,db_column="c_id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="cust_id")
    sell_type=models.CharField(max_length=10,db_column="s_type")
    seller_id=models.ForeignKey(SellerReg,on_delete=models.CASCADE,db_column="seller_id",null=True)
    craft_product=models.ForeignKey(CraftDetails,on_delete=models.CASCADE,db_column="cr_id",null=True,blank=True)
    nursery_product=models.ForeignKey(NurseryProduct,on_delete=models.CASCADE,null=True,blank=True,db_column="n_id")
    qty=models.IntegerField(db_column="qty")
    total=models.FloatField(db_column="total")
   
    class Meta:
        db_table="tb_cart"

class OrderDetails(models.Model):
    order_no=models.CharField(max_length=20,primary_key=True,db_column='ord_no')
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="cust_id")
    sell_type=models.CharField(max_length=10,db_column="s_type")
    seller_id=models.ForeignKey(SellerReg,on_delete=models.CASCADE,db_column="seller_id",null=True)
    craft_product=models.ForeignKey(CraftDetails,on_delete=models.CASCADE,db_column="cr_id",null=True,blank=True)
    nursery_product=models.ForeignKey(NurseryProduct,on_delete=models.CASCADE,null=True,blank=True,db_column="n_id")
    order_date=models.CharField(max_length=10,db_column='ord_date')
    exp_delivery=models.CharField(max_length=10,db_column='exp_date')
    shipping_address=models.CharField(max_length=200,db_column="shipping_address")
    qty=models.IntegerField(db_column='qty')
    total=models.FloatField(db_column='total')
    order_status=models.CharField(max_length=10,db_column='ord_status')

    class Meta:
        db_table="tb_order"


class ProductFeedBack(models.Model):
    nursey_id=models.ForeignKey(NurseryProduct,null=True,on_delete=models.CASCADE,db_column="n_id")
    craft_id=models.ForeignKey(CraftDetails,null=True,on_delete=models.CASCADE,db_column="cr_id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="c_id")
    feedback_date=models.CharField(max_length=20,db_column="f_date")
    feedback=models.CharField(max_length=100,db_column="feed_back")
    prod_img=models.ImageField(upload_to="Feedback/",db_column="feed_img")
    class Meta:
        db_table="tb_feedback"

class RatingDetails(models.Model):
    product_id=models.ForeignKey(NurseryProduct,null=True,on_delete=models.CASCADE,db_column="p_id")
    craft_id=models.ForeignKey(CraftDetails,null=True,on_delete=models.CASCADE,db_column="c_id")
    five_star=models.IntegerField(db_column="five_star")
    four_star=models.IntegerField(db_column="four_star")
    three_star=models.IntegerField(db_column="three_star")
    two_star=models.IntegerField(db_column="two_star")
    one_star=models.IntegerField(db_column="one_star")
    class Meta:
        db_table="tb_star"

class Rating(models.Model):
    product_id=models.ForeignKey(NurseryProduct,null=True,on_delete=models.CASCADE,db_column="p_id")
    craft_id=models.ForeignKey(CraftDetails,null=True,on_delete=models.CASCADE,db_column="c_id")
    customer=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="cust_id")
    cust_star=models.IntegerField(db_column="cust_star")

    class Meta:
        db_table="tb_rating"

class ModeratorDetails(models.Model):
    mod_id=models.IntegerField(primary_key=True,db_column="mod_id")
    mod_name=models.CharField(max_length=30,db_column="m_name")
    mod_phno=models.CharField(max_length=10,db_column="m_phno")
    mod_email=models.CharField(max_length=30,db_column="m_email")
    mod_passwd=models.CharField(max_length=30,db_column="m_passwd")
    mod_pic=models.ImageField(upload_to="Moderator/",db_column="m_pic")
    
    class Meta:
        db_table="tb_moderator"
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.mod_passwd)



class GardenIdeas(models.Model):
    req_id=models.AutoField(primary_key=True,db_column="req_id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="c_id")
    plot_pic=models.ImageField(upload_to="Ideas/Garden",db_column="plot_pic")
    requirements=models.CharField(max_length=255,db_column="req")
    exp_date=models.CharField(max_length=10,db_column="exp_date")
    budget=models.FloatField(db_column="budget")
    date_posted=models.CharField(max_length=10,db_column="date_posted")
    est_date=models.CharField(max_length=10,db_column="est_date")
    mod_id=models.ForeignKey(ModeratorDetails,models.SET_NULL ,null=True,db_column="mod_id")
    status=models.CharField(max_length=20,db_column="status")
    reject_reason=models.CharField(max_length=100,db_column="r_reason")
    plot_design=models.ImageField(upload_to="Ideas/Garden/Design")

    class Meta:
        db_table="tb_garden"

class GardenProducts(models.Model):
    req_id=models.ForeignKey(GardenIdeas,on_delete=models.CASCADE,db_column="req_id")
    product_id=models.ForeignKey(NurseryProduct,on_delete=models.SET_NULL,null=True,db_column="p_id")
    total_amt=models.FloatField(db_column="total")

    class Meta:
        db_table="tb_gProducts"


class StandPotIdeas(models.Model):
    
    id=models.AutoField(primary_key=True,db_column="id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="cust_id")
    posted_date=models.CharField(max_length=10,db_column="post_date")
    item=models.CharField(max_length=10,db_column="item")
    requirements=models.CharField(max_length=255,db_column="req")
    design=models.ImageField(upload_to="Ideas/StandPot",db_column="design")
    mod_id=models.ForeignKey(ModeratorDetails,models.SET_NULL ,null=True,db_column="mod_id")
    est_date=models.CharField(max_length=10,db_column="est_date")
    budget=models.FloatField(db_column="budget",null=True)
    reject_reason=models.CharField(max_length=100,db_column="r_reason")
    completed_date=models.CharField(max_length=10,db_column="com_date")
    delivered_date=models.CharField(max_length=10,db_column="del_date")
    status=models.CharField(max_length=20,db_column="status")
    class Meta:
        db_table="tb_standPot"

class ReturnProducts(models.Model):
    id=models.AutoField(primary_key=True,db_column="id")
    order_no=models.ForeignKey(OrderDetails,on_delete=models.CASCADE,db_column="order_id")
    cust_id=models.ForeignKey(CustomerDetails,on_delete=models.CASCADE,db_column="cust_id")
    prod_img=models.ImageField(upload_to="return Product/",db_column="img")
    reason=models.CharField(max_length=100,db_column="return_reason")
    status=models.CharField(max_length=20,db_column="status")
    class Meta:
        db_table="tb_returnproduct"



