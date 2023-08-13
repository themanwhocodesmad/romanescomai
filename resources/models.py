from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    stockcode = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.stockcode}"


class ErrorCodes(models.Model):
    code = models.CharField(max_length=50)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='error_codes')

    def __str__(self):
        return self.code


class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
