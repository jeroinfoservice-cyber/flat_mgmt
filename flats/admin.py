from decimal import Decimal
from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Sum
from .models import FlatInfo, House, Payment, Message, Announcement


@admin.register(FlatInfo)
class FlatInfoAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ("house_number",)
    search_fields = ("house_number",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("house", "month", "amount", "status", "created_at")
    list_filter = ("status", "month")
    search_fields = ("house__house_number", "month")
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "subject", "created_at")
    search_fields = ("sender_name", "subject", "content")
    readonly_fields = ("created_at",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at",)


def normalize_text(value):
    return str(value).strip().upper() if value else ""


def custom_admin_index(request, extra_context=None):
    if extra_context is None:
        extra_context = {}

    houses = House.objects.all().order_by("house_number")
    flat_info = FlatInfo.objects.first()

    # Get months directly from payment records
    raw_months = Payment.objects.values_list("month", flat=True).distinct()

    months = sorted(
        [normalize_text(month) for month in raw_months if month],
        reverse=False
    )

    selected_month = normalize_text(request.GET.get("month"))

    # Default to latest available month from DB
    if not selected_month:
        selected_month = months[-1] if months else ""

    paid_payments = Payment.objects.filter(
        month=selected_month,
        status="Paid"
    ) if selected_month else Payment.objects.none()

    paid_house_ids = set(
        paid_payments.values_list("house_id", flat=True).distinct()
    )

    total_houses = houses.count()
    paid_count = len(paid_house_ids)
    not_paid_count = total_houses - paid_count

    total_collected = paid_payments.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    MONTHLY_FEE = Decimal("100.00")
    total_pending = Decimal(not_paid_count) * MONTHLY_FEE

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
        "total_pending": total_pending,
        "house_status_data": house_status_data,
        "available_apps": admin.site.get_app_list(request),
    }
    context.update(extra_context)

    return TemplateResponse(request, "admin/custom_index.html", context)


admin.site.index = custom_admin_index