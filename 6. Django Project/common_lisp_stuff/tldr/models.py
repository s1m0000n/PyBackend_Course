from django.db import models
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry


# Create your models here.
class Function(models.Model):
    name = models.CharField('Имя функции', max_length=128)
    call_spec = models.CharField('Вызов с именами аругментов', max_length=512)
    args = models.TextField('Описание агрументов', null=True)
    description = models.TextField('Описание функции', null=True)
    examples = models.TextField('Примеры вызовов', null=True)


@registry.register_document
class FunctionDocument(Document):
    class Index:
        name = 'functions'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    class Django:
        model = Function
        fields = [
            'name',
            'call_spec',
            'description',
            'args',
            'examples'
        ]
