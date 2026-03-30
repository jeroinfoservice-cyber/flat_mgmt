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


def custom_admin_index(request, extra_context=None):
    if extra_context is None:
        extra_context = {}

    houses = House.objects.all().order_by("house_number")
    flat_info = FlatInfo.objects.first()

    months = list(
        Payment.objects.exclude(month__isnull=True)
        .exclude(month__exact="")
        .values_list("month", flat=True)
        .distinct()
    )
    months = sorted(months)

    selected_month = request.GET.get("month", "").strip()
    if not selected_month and months:
        selected_month = months[-1]

    paid_payments = Payment.objects.none()
    if selected_month:
        paid_payments = Payment.objects.filter(
            month__iexact=selected_month,
            status__iexact="Paid"
        )

    paid_house_ids = set(paid_payments.values_list("house_id", flat=True))
    total_collected = sum(payment.amount for payment in paid_payments)

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
        "subtitle": None,
        "flat_info": flat_info,
        "months": months,
        "selected_month": selected_month,
        "total_houses": total_houses,
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "total_collected": total_collected,
        "total_pending": 0,
        "house_status_data": house_status_data,
    }
    context.update(extra_context)

    return TemplateResponse(request, "admin/index.html", context)


admin.site.index = custom_admin_index