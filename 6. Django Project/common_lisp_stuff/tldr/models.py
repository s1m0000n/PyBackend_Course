from django.db import models


# Create your models here.
class Function(models.Model):
    name = models.CharField('Имя функции', max_length=128)
    call_spec = models.CharField('Вызов с именами аругментов', max_length=512)
    args = models.TextField('Описание агрументов', null=True)
    description = models.TextField('Описание функции', null=True)
    examples = models.TextField('Примеры вызовов', null=True)
