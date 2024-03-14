from django.db import models

class Transaction(models.Model):
    app_id = models.IntegerField()
    xref = models.IntegerField()
    settlement_date = models.DateField()
    broker = models.CharField(max_length=255)
    sub_broker = models.CharField(max_length=255, null=True)
    borrower_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    total_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    upfront = models.DecimalField(max_digits=10, decimal_places=2)
    upfront_incl_gst = models.DecimalField(max_digits=10, decimal_places=2)

    TIER_CHOICES = [
        ('Tier 1', 'Tier 1'),
        ('Tier 2', 'Tier 2'),
        ('Tier 3', 'Tier 3'),
        ('Tier 4', 'Tier 4')
    ]

    tier_level = models.CharField(max_length=20, choices=TIER_CHOICES, default='Tier 4')
    

    def __str__(self):
        return f"Transaction - ID: {self.id}, XREF: {self.xref}, Amount: {self.total_loan_amount}"
