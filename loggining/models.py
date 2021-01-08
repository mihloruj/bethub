from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    price = models.IntegerField()
    description = models.CharField(max_length=150, blank=True)
    period = models.IntegerField()

    
    def __str__(self):
        if self.period % 10 == 1 and self.period not in range(5, 20):
            return "Подписка на %s месяц" % (self.period)
        elif self.period % 10 in [2, 3, 4] and self.period not in range(5, 20):
            return "Подписка на %s месяца" % (self.period)
        else:
            return "Подписка на %s месяцев" % (self.period)


class UserSub(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

