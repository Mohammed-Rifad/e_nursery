from nursery_app.models import RatingDetails
from django.urls import path
from .views import CommonViews,AdminViews,CustomerViews,ModeratorViews

app_name="e_nursery"

urlpatterns = [
   path('',CommonViews.ProjectHome),
   path('AdminData',CommonViews.AdminData),
   path('Register',CommonViews.CustomerReg,name="cust_reg"),
   path('CustomerHome',CustomerViews.CustomerHome,name="cust_home"),
   path('CustomerHome/MyOrders',CustomerViews.MyOrders,name="cust_orders"),

   path('CustomerHome/ViewProducts',CustomerViews.ViewProducts,name="cust_view_products"),
   path('CustomerHome/ProductDetails/<int:pid>',CustomerViews.ProductDetails,name="cust_product_details"),
   path('CustomerHome/Order/',CustomerViews.OrderProduct,name="cust_order"),
   path('CustomerHome/FeedbackNursery/',CustomerViews.FeedbackNursery,name="feedback_nursery"),
   path('CustomerHome/FeedbackCraft/',CustomerViews.FeedbackCraft,name="feedback_craft"),
   path('AdminHome/Estimation/<int:req_id>',AdminViews.ViewEstimation,name="admin_est"),
   path('CustomerHome/GardenIdea',CustomerViews.RequestGardenIdeas,name='g_ideas'),
   path('update-cart',CustomerViews.updateCart,name="update_cart"),
   path('Logout/<int:user>',CommonViews.logout,name="logout"),
   path('AdminHome/Sellers',AdminViews.ViewSellers,name="sellers"),

  
   path('login',CommonViews.Login,name="login"),
   path('ViewProducts',CommonViews.ViewProducts,name="view_products"),
   path('CustomerHome/Cart',CustomerViews.Cart,name="cart"),
   path('ProductDetails/<int:pid>',CommonViews.ProductDetails,name="product_details"),
   path('AdminHome',AdminViews.AdminHome,name="admin_home"),
   path('AdminHome/SPHistory',AdminViews.StandPotHistory,name="sp_history"),
   path('AdminHome/RecentGRequest',AdminViews.RecentGardenRequest,name="recent_grequest"),
   path('AdminHome/AddModerator',AdminViews.AddModerator,name="add_mod"),
   path('AdminHome/PendingGRequest',AdminViews.PendingGardenRequest,name="admin_grequest"),
   path('AdminHome/GardenReqHistory',AdminViews.gardenRequestHistory,name="g_history"),
   path('AdminHome/ApprovedSP',AdminViews.ApprovedSPRequest,name="ap_sp"),
   path('Admin/AddCat',AdminViews.AddCategory,name="add_cat"),
   path('Admin/OrderDetail/<str:ord_id>',AdminViews.OrderDetail,name="order_details"),
   path('Admin/HistDetail/<str:ord_id>',AdminViews.HistoryDetail,name="hst_detail"),
   path('Admin/PendingOrders',AdminViews.ViewPendingOrders,name="pending_orders"),
   path('Admin/AddPlants',AdminViews.AddNurseryPlants,name="add_plants"),
   path('Admin/AddPots',AdminViews.AddPots,name="add_pots"),
   path('Admin/AddStands',AdminViews.AddStands,name="add_stands"),
   path('Admin/OrderHistory',AdminViews.OrderHistory,name="ord_hist"),
   path('Admin/Fertilizer',AdminViews.AddFertilizers,name="add_fertilizer"),
   path('Admin/RecentSP',AdminViews.RecentSPRequest,name="recent_sp"),
   path('Admin/SellOrders',AdminViews.SellerOrders,name="sell_ord"),
   path('Admin/Seeds',AdminViews.AddSeeds,name="add_seeds"),
   path('Admin/Products',AdminViews.ViewAllProducts,name="all_prod"),
   path('Admin/UpdateStock',AdminViews.UpdateStock,name="stock_update"),
   path('Admin/Tools',AdminViews.AddTools,name="add_tools"),
   path('Admin/SellRequest',AdminViews.ViewSellRequest,name="sell_pending"),
   path('Moderator/ModeratorHome',ModeratorViews.ModeratorHome,name="mod_home"),
   path('Moderator/PendingGRequest',ModeratorViews.PendingGardenRequest,name="p_grequest"),
   path('Moderator/Estimation',ModeratorViews.AddEstimation,name="add_estimation"),
   path('Moderator/Estimation/<int:req_id>',ModeratorViews.ViewEstimation,name="view_est"),
   path('Moderator/GRequest',ModeratorViews.GardenRequest,name="g_request"),
   path('Moderator/ConfirmedRequest',ModeratorViews.ConfirmedGardenRequest,name="g_confirmed"),
   path('CustomerHome/GRequest',CustomerViews.GardenRequest,name="c_grequest"),
   path('CustomerHome/SPRequest',CustomerViews.StandPotRequest,name="sp_request"),
   path('CustomerHome/ViewSPRequest',CustomerViews.ViewStandPotRequest,name="view_sp"),
   path('CustomerHome/Order/<str:ord_no>',CustomerViews.OrderDetail,name="cust_ord"),
   path('CustomerHome/GRequest/<int:req_id>',CustomerViews.ViewEstimation,name="est_product"),
   path('CustomerHome/SellReg',CustomerViews.SellerRequest,name="sell_reg"),
   path('CustomerHome/OrderHistory',CustomerViews.OrderHistory,name="c_ord_hist"),
   path('CustomerHome/Products',CustomerViews.MyProducts,name="my_prod"),
   path('CustomerHome/Stock',CustomerViews.UpdateStock,name="seller_stock"),
   path('CustomerHome/AddCraft',CustomerViews.AddProducts,name="add_craft"),
   path('CustomerHome/ViewOrders',CustomerViews.ViewOrders,name="view_orders"),
   path('CustomerHome/CraftDetails/<int:cr_id>',CustomerViews.CraftProductDetails,name="craft_details"),
   path('Moderator/Reject',ModeratorViews.RejectReason,name="reject_reason"),
   path('Moderator/StandPotRequest',ModeratorViews.ViewStandPotRequest,name="sp_req"),
   path('Moderator/ConfSPRequest',ModeratorViews.ConfirmedSPRequest,name="con_sp"),
   path('Moderator/ApprovedSPRequest',ModeratorViews.ApprovedSPRequest,name="sp_approved"),
   path('Moderator/getData',ModeratorViews.getProductDetails),
   path('Moderator/Products',ModeratorViews.ViewAllProducts,name="mod_allprod"),
   path('Moderator/ChangeModeratorPasswd',ModeratorViews.ChangeModeratorPasswd,name="change_moderator_passwd"),
   path('CustomerHome/ReturnProducts/<str:ord_no>',CustomerViews.ReturnProduct,name="return_product"),
   path('CustomerHome/ReturnProducts',CustomerViews.ViewReturnProduct,name="view_returnpro"),
   path('AdminHome/ReturnProducts',AdminViews.ViewReturnproducts,name="view_return"),
   path('AdminHome/ReturnProducts/<str:ord_no>',AdminViews.ReturnDetail,name="ret_detail"),
   path('Nursery/Success',CustomerViews.NurseryPaySuccess,name="nur_success"),
   path('CustomerHome/Craft/Success',CustomerViews.CraftPaySuccess,name="craft_success"),
   path('CustomerHome/Checkout/Success',CustomerViews.CheckOutSuccess,name="checkout_success")
]
