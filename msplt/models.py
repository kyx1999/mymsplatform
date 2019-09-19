from django.db import models

# Create your models here.


# 普通用户表
class UserProfile(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(verbose_name='昵称', max_length=128, unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='电子邮箱', unique=True)
    sex = models.CharField(verbose_name='性别', max_length=32, choices=gender, default='男')
    create_time = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    class Meta:
        ordering = ['create_time']
        verbose_name = '普通用户'
        verbose_name_plural = '普通用户'

    def __str__(self):
        return self.name
