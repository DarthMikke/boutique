from django.db import models
import json
from datetime import datetime

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
    date = models.DateTimeField(name='date', db_column='date',
                                null=True, blank=True)
    store = models.ForeignKey(Store, name='store', db_column='store',
                              on_delete=models.CASCADE,
                              null=True, blank=True)
    picture = models.FileField(null=True, blank=True)
    analyzed = models.FileField(null=True, blank=True)

    def get_date_extended(self):
        """
        Return a tuple of `datetime` associated with this receipt and a boolean
        of whether the datetime was imported through Azure.
        """
        return (self.date, False) if self.date is not None \
            else (self.analyzed_receipt.date, True)

    def get_date(self):
        return self.get_date_extended()[0]

    @property
    def date_admin(self):
        (dtg, imported) = self.get_date_extended()
        templates = ['%s', '%s*']

        if dtg is not None:
            ret = (templates[imported] % dtg.strftime('%d %h %Y %H:%M')) if dtg is not None \
                else None
            return ret

    def get_store_name(self):
        if self.store is not None:
            return self.store
        if hasattr(self, 'analyzed_receipt'):
            return (self.analyzed_receipt.store.store
                    if self.analyzed_receipt.store.store is not None
                    else self.analyzed_receipt.store.name)

    def total_amount(self):
        return self.analyzed_receipt.total_amount \
            if hasattr(self, 'analyzed_receipt') \
            and self.analyzed_receipt.total_amount is not None \
            else sum([x.total_price - x.discount
                     for x in self.purchases.all()])/100.0

    def __str__(self):
        return "%.2f kr, %s" % (
            self.total_amount(),
            self.date
        )

    def analyze(self):
        # TODO: Check if self.analyzed is null. If it is the case, check
        # if there's a picture, and upload it to Azure.

        analyzed, created = AnalyzedReceipt.objects.get_or_create(receipt=self)

        with open(self.analyzed.path) as f:
            result = json.load(f)

        if 'documents' in result.keys() and len(result['documents']) > 0:
            fields = result['documents'][0]['fields']
            if 'MerchantName' in fields.keys():
                alias, created = AnalyzedStoreAlias.objects.get_or_create(
                    name=fields['MerchantName']['valueString'])
                analyzed.store = alias
            if 'TransactionDate' in fields.keys():
                transaction_tstamp = (
                    fields['TransactionDate']['valueDate'],
                    fields['TransactionTime']['valueTime']
                    if 'TransactionTime' in fields.keys()
                    else '12:00:00'
                )
                transaction_dt = datetime.fromisoformat(
                    "%s %s" % transaction_tstamp
                )
                analyzed.date = transaction_dt
            if 'Total' in fields.keys():
                analyzed.total_amount = float(fields['Total']['valueCurrency']['amount'])
                analyzed.currency = fields['Total']['valueCurrency']['currencyCode']

        analyzed.save()


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


class AnalyzedStoreAlias(models.Model):
    """
    Associates an analyzed MerchantName with appropriate Store.
    """
    name = models.CharField(max_length=250)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,
                              null=True, blank=True)


class AnalyzedReceipt(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name="analyzed_receipt")
    date = models.DateTimeField(null=True, blank=True)
    store = models.ForeignKey(AnalyzedStoreAlias, on_delete=models.SET_NULL,
                              null=True, blank=True)
    total_amount = models.DecimalField(max_digits=7, decimal_places=3,
                                       null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    def as_dict(self):
        serialized = {k: repr(self.__dict__[k])
                      for k in self.__dict__.keys()}
        return json.dumps(serialized, indent=4)
