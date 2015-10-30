from django.db import models


class LiquorLocation(models.Model):
    store_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.store_name


class PrivateStore(LiquorLocation):
    pass


class BCLiquorStore(LiquorLocation):
    post_code = models.CharField(max_length=7)


class RuralAgencyStore(LiquorLocation):
    post_code = models.CharField(max_length=7)
