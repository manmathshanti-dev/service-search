from django.db import models
import uuid

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(is_deleted=False)

class PredictionBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    meta = models.JSONField(null=True, blank=True)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True,db_index=True
    )
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True 


        
class SearchableAlias(PredictionBaseModel):


    alias_en = models.CharField(max_length=255, null=True, blank=True)
    alias_iast = models.CharField(max_length=255, null=True, blank=True)

    alias_iast_pair = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "predicted_searchable_alias"