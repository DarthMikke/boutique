from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, blank=True, null=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        if (self.brand):
            return "%s, %s" % (self.name, self.brand)

        return self.name


class ProductSize(models.Model):
    UNIT_CHOICES = (
        ['kg', 'kg'], ['g', 'g'],
        ['l', 'l'], ['cl', 'cl'], ['dl', 'dl'], ['ml', 'ml'],
        ['m', 'm'], ['cm', 'cm'], ['sqm', 'sqm'],
        ['pcs', 'pcs'],
    )
    size = models.DecimalField(max_digits=7, decimal_places=3, default=1)
    unit = models.CharField(max_length=250,
                            choices=UNIT_CHOICES,
                            blank=False,
                            default='pcs')

    def __str__(self):
        return str(self.size) + " " + str(self.unit)


class Receipt(models.Model):
    date = models.DateTimeField()
    store = models.ForeignKey(Store,
                              on_delete=models.CASCADE)

    def total_amount(self):
        return sum([x.total_price - x.discount
                    for x in self.purchases.all()])/100.0

    def __str__(self):
        return "%.2f kr, %s" % (
            self.total_amount(),
            self.date
        )


class Purchase(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize,
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=3)
    total_price = models.IntegerField()
    discount = models.IntegerField()
    receipt = models.ForeignKey(Receipt, related_name="purchases",
                                on_delete=models.CASCADE)
