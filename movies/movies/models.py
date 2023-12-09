from django.db import models


class Review(models.Model):
    productid = models.CharField(max_length=255, null=True)
    userid = models.CharField(max_length=255, null=True)
    profilename = models.TextField(null=True)
    helpfulness = models.CharField(max_length=50, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    reviewtime = models.BigIntegerField(null=True)
    summary = models.TextField(null=True)
    reviewtext = models.TextField(null=True)


    def __str__(self):
        return self.summary
