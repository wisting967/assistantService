from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Requirement(models.Model):
    reqTitle = models.CharField(_("reqTitle"), max_length=50)
    reqDesc = models.CharField(_("reqDesc"), max_length=300)
    reqStatus = models.CharField(_("reqStatus"), max_length=10)
    reqRemark = models.CharField(_("reqRemark"), max_length=200)  # 自己用来做对需求的备注的
    reqCreateTime = models.DateTimeField(_("reqCreateTime"), auto_now_add=True)

    class Meta:
        db_table = 'hj_requirement'
        ordering = ['-reqCreateTime']