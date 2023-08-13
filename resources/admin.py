from django.contrib import admin
from .models import Products, ErrorCodes, Region, Vendor


# Registering Products
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'stockcode')
    search_fields = ('name', 'stockcode')


# Registering ErrorCodes
@admin.register(ErrorCodes)
class ErrorCodesAdmin(admin.ModelAdmin):
    list_display = ('code', 'product')
    search_fields = ('code', 'product__name')


# Registering Region
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Registering Vendor
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')
