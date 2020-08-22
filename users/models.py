from django.db import models
class UserSelf(models.Model):
    '''用户表'''
    userName = models.CharField(max_length=128,unique=True)
    realName = models.CharField(max_length=128,unique=True)
    anoahName = models.CharField(max_length=128,unique=True)
    aeduName = models.CharField(max_length=128,unique=True)
    aeduPassword = models.CharField(max_length=128,unique=True)
    passWord = models.CharField(max_length=256)
    signinTime = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.userName
 
    class Meta:
        ordering = ['signinTime']
        verbose_name = '用户_外部'
        verbose_name_plural = '用户_外部'