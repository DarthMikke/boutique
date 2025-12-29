from django.db import models


class Upload(models.Model):
    date = models.DateTimeField(
        name='date', db_column='date',
        null=True, blank=True,
    )
    provider = models.CharField(max_length=250)
    attachment = models.FileField(null=True, blank=True)
    raw = models.FileField(null=True, blank=True)


class ReceiptScanner:
    name: str = None
    """
    Name of the interpreter, will be used to fill in the result's
    provider.
    """

    def scan(self, upload: Upload) -> dict:
        """
        actual implementation goes here.
        """
        pass
