from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from devicerepair.Serializer import *
from devicerepair import models
from rest_framework.pagination import PageNumberPagination


# 定义分页类

class MyPageNumberPagination(PageNumberPagination):
    # 分页数量
    page_size = 10


class DeviceRepairView(ModelViewSet):
    """设备维修视图"""

    queryset = models.DeviceRepair.objects.all()
    serializer_class = DeviceRepairSerializers
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        """倒序排列"""
        queryset = super().get_queryset()

        return queryset.order_by('-id')


class DeviceDetailView(ModelViewSet):
    """设备清单视图"""

    queryset = models.DeviceDetail.objects.all()
    serializer_class = DeviceDetailSerializers


class CategoryView(ModelViewSet):
    """维修类别视图"""
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializers


