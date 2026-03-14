from django.db import models


class House(models.Model):
    house_number = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.house_number


class Payment(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Not Paid', 'Not Paid')])
    date_paid = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.house.house_number} - {self.month}"


class Message(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.house.house_number} - {self.created_at:%Y-%m-%d %H:%M}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title