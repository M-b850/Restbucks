from django.db import models
from . import choices

class TagManager(models.Manager):
    def related_tags(self, customazation):
        return self.filter(customization=customazation)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    customization = models.ForeignKey('Customization', on_delete=models.CASCADE)
    objects = TagManager()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.slug = self.slug.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Customization(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    production = models.ForeignKey('Production', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = self.slug.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Production(models.Model):
    name = models.CharField(max_length=50)
    CUSTOMIZATION_CHOICES = (
        ('', None),
        ('MILK', 'MILK'),
        ('SIZE', 'SIZE'),
        ('SHOTS', 'SHOTS'),
        ('KIND', 'KIND'),
    )
    # CN for Customization Name
    CN = models.CharField(max_length=6, choices=CUSTOMIZATION_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Order(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Production', on_delete=models.CASCADE)
    customization = models.CharField(max_length=50, null=True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, 
        default=0.00,
        help_text='Price would be calculated automatically.DON\'T ENTER'
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=choices.STATUS_CHOICES, default='waiting')
    consume_location = models.CharField(max_length=10, choices=choices.CONSUME_LOCATION_CHOICES)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValueError('Quantity must be greater than 0')

        self.price = self.get_total_price
        self.customization = self.product.CN
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
