from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from devicerepair.Serializer import *
from devicerepair import models
from rest_framework.pagination import PageNumberPagination
from devicerepair import dingding
from rest_framework.response import Response
from rest_framework.views import APIView


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

    def create(self, request, *args, **kwargs):
        """创建钉钉审批流"""
        description_problem = request.data.get('description_problem')
        report_repair_category_id = request.data.get('report_repair_category_id')
        device_name_id = request.data.get('device_name_id')
        phone = request.data.get('report_repair_phone')
        repair_person = request.data.get('repair_person')
        report_repair_person = request.data.get('report_repair_person')

        # 获取token
        token = dingding.token().get('accessToken')
        category = models.Category.objects.filter(id=report_repair_category_id).values("Category_name")
        category = category[0].get('Category_name')
        device_name = models.DeviceDetail.objects.filter(id=device_name_id).values("device_name")
        device_name = device_name[0].get('device_name')
        # print(description_problem, report_repair_category_id, device_name_id, phone, type(category), device_name)
        # 通过手机号获取userid
        user_id = dingding.get_user_id(token, phone)
        user = user_id.get("result").get("userid")
        # print("用户", user)
        # 通过userid获取用户的dept_id_list部门id
        user_detail = dingding.get_user_detail(token, user)
        dept_id_list = user_detail.get('result').get('dept_id_list')[0]
        response = dingding.create_oa(token, dept_id_list, user, category, description_problem, device_name)
        # print(response)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeviceDetailView(ModelViewSet):
    """设备清单视图"""

    queryset = models.DeviceDetail.objects.all()
    serializer_class = DeviceDetailSerializers


class CategoryView(ModelViewSet):
    """维修类别视图"""
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializers


class PhoneView(APIView):
    """通过手机号查人"""
    def get(self,request,phone,*args,**kwargs):
        token = dingding.token().get('accessToken')
        # 通过手机号获取userid
        user_id = dingding.get_user_id(token, phone)
        user = user_id.get("result").get("userid")

        # 通过userid获取用户的dept_id_list部门id
        user_detail = dingding.get_user_detail(token, user)
        # dept_id_list = user_detail.get('result').get('dept_id_list')[0]
        user_name = user_detail.get('result').get('name')
        # print(user_name)
        return Response(user_name)


