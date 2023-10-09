from django.db import models


class Visitor(models.Model):
    objects = None
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')
    os_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='OS Info')
    browser_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='Browser Info')
    device_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='Device Info')
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'All Visitor'

    def __str__(self):
        return str(f'{self.ip_address}')