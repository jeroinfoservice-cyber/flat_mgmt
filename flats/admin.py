from django.contrib import admin
from datetime import datetime
from .models import FlatInfo, House, Payment, Message, Announcement


admin.site.register(FlatInfo)
admin.site.register(House)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(Announcement)


original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    houses = House.objects.all()
    flat_info = FlatInfo.objects.first()

    current_year = datetime.now().year

    month_choices = [
        {"value": f"JAN-{current_year}", "label": "January"},
        {"value": f"FEB-{current_year}", "label": "February"},
        {"value": f"MAR-{current_year}", "label": "March"},
        {"value": f"APR-{current_year}", "label": "April"},
        {"value": f"MAY-{current_year}", "label": "May"},
        {"value": f"JUN-{current_year}", "label": "June"},
        {"value": f"JUL-{current_year}", "label": "July"},
        {"value": f"AUG-{current_year}", "label": "August"},
        {"value": f"SEP-{current_year}", "label": "September"},
        {"value": f"OCT-{current_year}", "label": "October"},
        {"value": f"NOV-{current_year}", "label": "November"},
        {"value": f"DEC-{current_year}", "label": "December"},
    ]

    current_abbr = datetime.now().strftime("%b").upper()
    default_selected = f"{current_abbr}-{current_year}"

    selected_month = request.GET.get("month")
    if not selected_month:
        selected_month = default_selected

    selected_month = selected_month.strip().upper()

    display_month = selected_month
    for item in month_choices:
        if item["value"] == selected_month:
            display_month = item["label"]
            break

    paid_count = 0
    not_paid_count = 0
    total_collected = 0
    total_pending = 0
    house_status_data = []

    for house in houses:
        month_payments = Payment.objects.filter(
            house=house,
            month__iexact=selected_month
        )

        paid_payment = month_payments.filter(status="Paid").first()

        if paid_payment:
            paid_count += 1
            total_collected += float(paid_payment.amount or 0)
            house_status_data.append({
                "house": house.house_number,
                "status": "Paid"
            })
        else:
            not_paid_count += 1
            pending_payment = month_payments.filter(status="Not Paid").first()
            if pending_payment:
                total_pending += float(pending_payment.amount or 0)

            house_status_data.append({
                "house": house.house_number,
                "status": "Not Paid"
            })

    extra_context = extra_context or {}
    extra_context.update({
        "flat_name": flat_info.name if flat_info else "PERBADANAN PENGURUSAN BLOK B1",
        "selected_month": selected_month,
        "display_month": display_month,
        "month_choices": month_choices,
        "total_houses": houses.count(),
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "total_collected": total_collected,
        "total_pending": total_pending,
        "house_status_data": house_status_data,
    })

    return original_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index