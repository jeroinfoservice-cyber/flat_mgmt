from decimal import Decimal
from datetime import datetime
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


def normalize_text(value):
    return str(value).strip().upper() if value else ""


def generate_year_months(year):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                   "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return [f"{m}-{year}" for m in month_names]


def custom_admin_index(request, extra_context=None):
    if extra_context is None:
        extra_context = {}

    houses = House.objects.all().order_by("house_number")
    payments = Payment.objects.select_related("house").all()
    flat_info = FlatInfo.objects.first()

    current_year = datetime.now().year
    months = generate_year_months(current_year)

    selected_month = (request.GET.get("month") or "").strip().upper()
    if not selected_month:
        selected_month = datetime.now().strftime("%b-%Y").upper()

    paid_house_ids = set()
    total_collected = Decimal("0.00")

    for payment in payments:
        payment_month = normalize_text(payment.month)
        payment_status = normalize_text(payment.status)

        if payment_month == selected_month and payment_status == "PAID":
            paid_house_ids.add(payment.house_id)
            total_collected += payment.amount or Decimal("0.00")

    total_houses = houses.count()
    paid_count = len(paid_house_ids)
    not_paid_count = total_houses - paid_count

    house_status_data = []
    for house in houses:
        house_status_data.append({
            "house_number": house.house_number,
            "status": "Paid" if house.id in paid_house_ids else "Not Paid",
        })

    context = {
        **admin.site.each_context(request),
        "title": "Site administration",
        "flat_info": flat_info,
        "months": months,
        "selected_month": selected_month,
        "total_houses": total_houses,
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "total_collected": total_collected,
        "total_pending": Decimal("0.00"),
        "house_status_data": house_status_data,
        "available_apps": admin.site.get_app_list(request),
    }
    context.update(extra_context)

    return TemplateResponse(request, "admin/custom_index.html", context)


admin.site.index = custom_admin_index