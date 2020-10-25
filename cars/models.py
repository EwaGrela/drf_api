from django.db import models
from django.core.exceptions import ValidationError


class Car(models.Model):
    """
    Car Model
    Defines the attributes of a car
    """
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    sum_rates = models.IntegerField(default=0)
    average_rate = models.FloatField(default=0)
    number_of_rates = models.IntegerField(default=0)

    class Meta:
        unique_together = ['make', 'model']

    def __str__(self):
        return "{} {}".format(self.make, self.model)

    def provide_self_data(self):
        return {"make": self.make, "model": self.model,
                "sum_rates": self.sum_rates,
                "average_rate": self.average_rate,
                "number_of_rates": self.number_of_rates}

    def update_self(self, data):
        if self.number_of_rates == 0:
            self.sum_rates = data["score"]
        else:
            self.sum_rates += data["score"]
        self.number_of_rates += 1
        self.average_rate = self.sum_rates / self.number_of_rates


class Rate(models.Model):
    """
    Rate model, rating a car
    """
    model = models.ForeignKey(Car, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)

    def clean(self):
        if self.score < 1 or self.score > 6:
            raise ValidationError('Measurement is outside the run')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Rate, self).save(*args, **kwargs)
