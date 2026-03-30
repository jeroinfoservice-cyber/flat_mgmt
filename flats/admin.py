from django.contrib import admin
from django.template.response import TemplateResponse
from .models import FlatInfo, House, Payment, Message, Announcement

@admin.register(FlatInfo)
class FlatInfoAdmin(admin.ModelAdmin):
list_display = ("name",)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
list_display = ("house_number", "owner_name", "phone")
search_fields = ("house_number", "owner_name", "phone")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
list_display = ("house", "month", "amount", "status", "date_paid")
list_filter = ("status", "month")
search_fields = ("house__house_number", "month")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
list_display = ("house", "message_text", "created_at")
search_fields = ("house__house_number", "message_text")
readonly_fields = ("created_at",)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
list_display = ("title", "created_at")
search_fields = ("title", "content")
readonly_fields = ("created_at",)

original_index = admin.site.index

def custom_admin_index(request, extra_context=None):
houses = House.objects.all()
flat_info = FlatInfo.objects.first()


month_choices = sorted(
    list(Payment.objects.values_list("month", flat=True).distinct())
)

if not month_choices:
    month_choices = ["JAN-2026"]

selected_month = request.GET.get("month")
if not selected_month:
    selected_month = month_choices[0]

paid_count = 0
not_paid_count = 0
total_collected = 0
total_pending = 0
house_status_data = []

for house in houses:
    payment = Payment.objects.filter(
        house=house,
        month=selected_month
    ).order_by("-id").first()

    if payment and payment.status == "Paid":
        paid_count += 1
        total_collected += float(payment.amount)
        house_status_data.append({
            "house": house.house_number,
            "status": "Paid"
        })
    else:
        not_paid_count += 1
        if payment:
            total_pending += float(payment.amount)
        house_status_data.append({
            "house": house.house_number,
            "status": "Not Paid"
        })

extra_context = extra_context or {}
extra_context.update({
    "flat_name": flat_info.name if flat_info else "PERBADANAN PENGURUSAN BLOK B1",
    "selected_month": selected_month,
    "month_choices": month_choices,
    "total_houses": houses.count(),
    "paid_count": paid_count,
    "not_paid_count": not_paid_count,
    "total_collected": total_collected,
    "total_pending": total_pending,
    "house_status_data": house_status_data,
})

return TemplateResponse(request, "admin/index.html", extra_context)


admin.site.index = custom_admin_index
