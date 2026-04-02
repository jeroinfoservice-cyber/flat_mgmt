from django.db import models


class House(models.Model):
    house_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.house_number


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FlatInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Message(models.Model):
    sender_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    ]

    MONTH_CHOICES = [
        ('JAN-2026', 'JAN-2026'),
        ('FEB-2026', 'FEB-2026'),
        ('MAR-2026', 'MAR-2026'),
        ('APR-2026', 'APR-2026'),
        ('MAY-2026', 'MAY-2026'),
        ('JUN-2026', 'JUN-2026'),
        ('JUL-2026', 'JUL-2026'),
        ('AUG-2026', 'AUG-2026'),
        ('SEP-2026', 'SEP-2026'),
        ('OCT-2026', 'OCT-2026'),
        ('NOV-2026', 'NOV-2026'),
        ('DEC-2026', 'DEC-2026'),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Paid')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('house', 'month')
        ordering = ['month', 'house__house_number']

    def __str__(self):
        return f"{self.house.house_number} - {self.month} - {self.status}"