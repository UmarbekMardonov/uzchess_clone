from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from authuser.models import UserModel, Role
from django.contrib.auth.backends import BaseBackend
from rest_framework.permissions import IsAuthenticated

#
# class BaseShopPermission(IsAuthenticated):
#     role = Role.ADMIN
#
#     def has_permission(self, request, view):
#         if request.method == "POST" or request.method == "PUT" or request.method == "PATCH":
#             shop = request.data.get("shop", None)
#             if shop:
#                 instance = Shop.objects.filter(id=shop).first()
#                 if instance:
#                     return instance in request.user.shops.all()
#                 return False
#         return bool(
#             request.user and request.user.is_authenticated and request.user.role == self.role
#         )


class IsAdmin(BaseShopPermission):
    role = Role.ADMIN


class IsShopOwner(BaseShopPermission):
    role = Role.SHOP_OWNER


class IsWarehouseOwner(BaseShopPermission):
    role = Role.WAREHOUSE_OWNER


class IsSeller(BaseShopPermission):
    role = Role.SELLER
