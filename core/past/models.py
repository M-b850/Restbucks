from django.db import models
import choices


class Production(models.Model):
    """ Product model """

    CUSTOMIZATION_CHOICES = (
        ('MILK', 'MILK'),
        ('SIZE', 'SIZE'),
        ('KIND', 'KIND'),
    )
    name = models.CharField(max_length=100)
    # CN is customizations name
    cn = models.CharField(max_length=6, choices=CUSTOMIZATION_CHOICES)
    CN = f'{cn}_CHOICES'
    customization = models.CharField(max_length=12, choices=choices.CN)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    """ Order model """
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    production_customization = models.CharField(max_length=12, blank=True)
    location = models.CharField(max_length=12, choices=choices.CONSUME_LOCATION_CHOICES)
    status = models.CharField(max_length=12, choices=choices.STATUS_CHOICES, default='waiting')
    quantity = models.IntegerField()
    total = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00,
        editable=False,
        help_text='Total price of the order'
    )

    @property
    def total_price(self):
        return self.production.price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError('Quantity must be greater than 0')
        
        self.total = self.total_price

        self.production_customization = self.production.cn
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.production}'