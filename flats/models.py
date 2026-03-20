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
    month = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Paid")
    date_paid = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.house.house_number} - {self.month} - {self.status}"


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
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_month = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.expense_month}"