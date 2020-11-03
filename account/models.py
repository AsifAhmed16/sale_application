from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=10, blank=False)
    username = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=10)

    class Meta:
        db_table = 'USERS'

    def __str__(self):
        return self.username


class Items(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ITEMS'


class Gift_Card(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'GIFT_CARD'


class Order(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    seller = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    net_total = models.FloatField(default=0.0)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered_date = models.DateField()
    gift_card = models.ForeignKey(Gift_Card, on_delete=models.SET_NULL, blank=True, null=True)
    tax_rate = models.FloatField()

    def __str__(self):
        return self.item.name

    def get_total(self):
        total = self.item.price * self.quantity
        if self.gift_card:
            total -= self.gift_card.amount
        total += (total * ((self.tax_rate)/100))
        return total

    class Meta:
        db_table = 'ORDER'
