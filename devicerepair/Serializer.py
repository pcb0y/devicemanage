from rest_framework import serializers
from devicerepair.models import *


class DeviceRepairSerializers(serializers.ModelSerializer):
    """设备维修"""
    device_name = serializers.CharField(read_only=True, label='设备名')
    report_repair_category = serializers.CharField(read_only=True, label='设备类别')
    report_repair_category_id=serializers.CharField(label='设备类别id')
    device_name_id = serializers.CharField(label='设备id')

    class Meta:
        model = DeviceRepair
        fields = "__all__"


class DeviceDetailSerializers(serializers.ModelSerializer):
    """设备清单"""
    class Meta:
        model = DeviceDetail
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    text = serializers.CharField(source="Category_name")
    value = serializers.IntegerField(source="id")
    """维修类别"""
    class Meta:
        model = Category
        fields = ['text', 'value']
