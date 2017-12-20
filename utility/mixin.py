from django.conf import settings

from django.utils import timezone
from django.db import models
from django.db.models.query import QuerySet


from polymorphic.models import PolymorphicModel
from polymorphic.manager import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class MetaInformationMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   blank=True)
    updated = models.DateTimeField(auto_now=True,
                                   blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='%(app_label)s_%(class)s_created_by',
                                      blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='%(app_label)s_%(class)s_updated_by',
                                      blank=True)

    
    class Meta:
        abstract = True
        
        
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
            
class SoftDeletionQuerySet(QuerySet):
    def delete(self,user):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now(),deleted_by=user)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)
    
        
class SoftDeletionModelMixin(models.Model):
    deleted_at = models.DateTimeField(blank=True,
                                        null=True
                                        )
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='%(app_label)s_%(class)s_deleted_by',
                                      blank=True,
                                      null=True
                                      )
    objects = models.Manager()
    soft_objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self,user):
        self.deleted_at = timezone.now()
        self.deleted_by= user
        self.save()

    def hard_delete(self):
        super(SoftDeletionModelMixin, self).delete()