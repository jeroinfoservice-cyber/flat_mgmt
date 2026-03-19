from django.db import models


class House(models.Model):
    house_number = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.house_number} - {self.owner_name}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Not Paid", "Not Paid"),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE)
    month = models.DateField(help_text="Use first day of month, example: 2026-03-01")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Paid")
    date_paid = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.house.house_number} - {self.month.strftime('%B %Y')} - {self.status}"


class Message(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.house.house_number}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Maintenance", "Maintenance"),
        ("Cleaning", "Cleaning"),
        ("Repair", "Repair"),
        ("Security", "Security"),
        ("Utility", "Utility"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="Maintenance")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_month = models.DateField(help_text="Use first day of month, example: 2026-03-01")
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.expense_month.strftime('%b %Y')}"