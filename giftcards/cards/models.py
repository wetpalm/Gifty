from django.db import models

# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.description
    
class Lstate(models.Model):
    statename = models.CharField(max_length=30, null=False, blank=False)
    
    def __str__(self):
        return self.statename

class Partner(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True, blank=True)
    lstate = models.ForeignKey(Lstate, on_delete=models.DO_NOTHING, verbose_name='State', related_name='partners')

class Client(models.Model):
    name = models.CharField(max_length = 100, null=False, blank=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    batchno = models.CharField(max_length=5, null=False, blank=False, unique=True)
    amount = models.IntegerField(default = 5000)
    status = models.BooleanField(default = 0)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, related_name='batches')
    printed = models.BooleanField(default = 0)

    def __str__(self):
        return self.batchno

class Card(models.Model):
    batchno = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='cards')
    cardno = models.CharField(max_length=50, null=False, blank=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cards') # client for which card is made
    status = models.SmallIntegerField(default=0) # 0 = ready, 1 = redeemed, 2 = blocked
    agent = models.SmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)