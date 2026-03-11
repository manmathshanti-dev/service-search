from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
import uuid
from django.db import models


class OTAService(models.Model):
    """
    One row per detected service per operator.
    Populated by: python manage.py fetch_service_timetable --save_db
    Search by: from_alias_en + to_alias_en
    """
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    updated_at      = models.DateTimeField(auto_now=True, null=True)

    operator_id     = models.UUIDField(db_index=True)
    operator_name   = models.CharField(max_length=255, blank=True, default='')
    bus_route_ids   = models.JSONField(default=list)        # POS bus_route_id UUIDs (for trip lookup)
    departure_time  = models.TimeField(db_index=True)
    from_town_alias = models.CharField(max_length=255)      # display name (first stop)
    to_town_alias   = models.CharField(max_length=255)      # display name (last stop)
    from_alias_en   = models.CharField(max_length=255, db_index=True)  # normalised for search
    to_alias_en     = models.CharField(max_length=255, db_index=True)  # normalised for search
    coverage_pct    = models.FloatField(default=0)
    confidence      = models.CharField(max_length=20, default='low')   # high / medium / low
    operated_by     = models.JSONField(default=list)        # list of bus number strings

    # Seat layout — max capacity across operated_by buses, stored at ingest time
    normal_seats          = models.IntegerField(null=True, blank=True)
    single_sleeper        = models.IntegerField(null=True, blank=True)
    sharing_sleeper       = models.IntegerField(null=True, blank=True)
    upper_single_sleeper  = models.IntegerField(null=True, blank=True)
    upper_sharing_sleeper = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'ota'
        managed = False
        db_table  = 'ota_service'
        constraints = [
            models.UniqueConstraint(
                fields=['operator_id', 'departure_time', 'from_alias_en', 'to_alias_en'],
                name='unique_ota_service',
            )
        ]
        indexes = [
            models.Index(fields=['from_alias_en', 'to_alias_en']),
        ]

    def __str__(self):
        return f"{self.operator_name} | {self.departure_time} | {self.from_town_alias}→{self.to_town_alias}"


class OTAServiceStop(models.Model):
    """
    One row per timetable stop in a service, in order.
    Used for the itinerary view. alias_en used to highlight searched from/to towns.
    """
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service      = models.ForeignKey(OTAService, on_delete=models.CASCADE, related_name='stops')
    order_index  = models.PositiveIntegerField()
    town_alias   = models.CharField(max_length=255)                    # display name
    alias_en     = models.CharField(max_length=255, db_index=True)     # normalised (for highlight matching)
    arrival_time = models.CharField(max_length=20)                     # "06:20 AM" string

    class Meta:
        app_label = 'ota'
        managed = False
        db_table  = 'ota_service_stop'
        ordering  = ['order_index']
        indexes   = [
            models.Index(fields=['service', 'order_index']),
        ]

    def __str__(self):
        return f"{self.service_id} | {self.order_index} | {self.town_alias} @ {self.arrival_time}"

    
