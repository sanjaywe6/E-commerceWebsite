"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path for admin page
    path('admin/', admin.site.urls),

    # path for home page
    path('', views.home, name='homePage'),

    # path for signup page
    path('signup/', views.signup, name='signUpPage'),

    # path for login page
    path('login/', views.loginUser, name='loginPage'),

    # path for logging out user
    path('logout/', views.logoutUser, name='logout'),

    # path for specific product using that's id
    path('allProduct/<str:id>', views.product_with_id, name='product_with_id'),

    # path for updating cart
    path('update_cart/', views.update_cart, name='updateCart'),

    # path for showing all cart product
    path('cart/', views.cart, name='cart'),

    # path for showing all roducts with_same category
    path('products/<str:category>', views.product_with_category, name='cart'),

    # path for adding comment
    path('comment/', views.comment, name='cart'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
