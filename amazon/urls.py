from django.urls import path
from . import views
app_name="amazon"
urlpatterns=[
    path("",views.index,name="index"),
    path("detail/<str:slug>",views.detail,name="detail"),
    path("old_url",views.old_url_redirect,name="old_url"),
    path("new_something_url",views.new_page_url,name="new_url"),
    path("contact",views.contact,name="contact"),
    path("about",views.about,name="about"),
    path("register",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("fashionhub",views.fashionhub,name="fashionhub"),
    path("logout",views.logout,name="logout"),
    path("forgotpassword",views.forgotpassword,name="forgotpassword"),
    path("resetpassword/<uidb64>/<token>",views.resetpassword,name="resetpassword"),
    path("new_post",views.new_post,name="new_post"),
    path("edit_post/<int:post_id>",views.edit_post,name="edit_post"),
    path("delete_post/<int:post_id>",views.delete_post,name="delete_post"),
    path("publish_post/<int:post_id>",views.publish_post,name="publish_post")
]