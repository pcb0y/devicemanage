from django.db import models

# Create your models here.


class Category(models.Model):
    Category_name = models.CharField(max_length=50, verbose_name='维修类别')

    def __str__(self):
        return self.Category_name


class DeviceDetail(models.Model):
    """设备清单"""
    device_name = models.CharField(max_length=50, verbose_name="设备名")

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name = "设备清单"
        verbose_name_plural = verbose_name


class DeviceRepair(models.Model):
    """设备报修"""
    device_name = models.ForeignKey(to=DeviceDetail, on_delete=models.CASCADE, verbose_name="设备名")
    report_repair_person = models.CharField(max_length=6,verbose_name="报修人")
    repair_person = models.CharField(max_length=6, verbose_name="维修人")
    repair_time = models.DateTimeField(auto_now_add=True, verbose_name="维修时间")
    description_problem = models.CharField(max_length=200, verbose_name="故障描述")
    repair_status = models.BooleanField(default=False, verbose_name="修复状态")
    # category = ((1, '电气问题'), (2, '设备问题'), (3, '网络问题'))
    report_repair_category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='报修类别')

    def __str__(self):
        return self.device_name

    class Mate:
        verbose_name = "设备报修"
        verbose_name_plural = verbose_name
