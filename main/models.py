from django.db import models

# Create your models here.
class Match(models.Model):
    date = models.CharField(max_length=25)
    league_name = models.CharField(max_length=150)
    match_name = models.CharField(max_length=150)
    total_score = models.CharField(max_length=10)
    first_half_score = models.CharField(max_length=10)
    coef_p1 = models.DecimalField( max_digits=5, decimal_places=2)
    coef_x = models.DecimalField( max_digits=5, decimal_places=2)
    coef_p2 = models.DecimalField( max_digits=5, decimal_places=2)


    def __str__(self):
        return self.match_name


class NextMatch(models.Model):
    url = models.CharField(max_length=256)
    league_name = models.CharField(max_length=150, blank=True, null=True)
    match_name = models.CharField(max_length=150)
    time = models.CharField(max_length=25)
    coef_p1 = models.DecimalField( max_digits=5, decimal_places=2, blank=True, null=True)
    coef_x = models.DecimalField( max_digits=5, decimal_places=2, blank=True, null=True)
    coef_p2 = models.DecimalField( max_digits=5, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.match_name    