from django.db import models


# Область
class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Район
class District(models.Model):
    name = models.CharField(max_length=200)
    parent_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} ({self.parent_region})"


# Місто
class City(models.Model):
    name = models.CharField(max_length=200)
    parent_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name} ({self.parent_region})"


# Тривога
class Alert(models.Model):
    ALERTS = [
        ("air_raid_alert", "Повітряна тривога"),
        ("artillery_strike_threat", "Загроза артобстрілу"),
        ("street_battle_threat", "Загроза вуличних боїв"),
        ("radiation_hazard", "Радіаційна небезпека"),
        ("chemical_threat", "Хімічна загроза"),
    ]

    alert_type = models.CharField(
        max_length=64,
        choices=ALERTS,
        verbose_name="Тип тривоги"
    )

    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Початок тривоги")
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name="Кінець тривоги")

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, related_name="alerts")
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, related_name="alerts")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name="alerts")

    def __str__(self):
        target = self.region or self.district or self.city
        return f"{self.get_alert_type_display()} @ {target} ({self.started_at})"