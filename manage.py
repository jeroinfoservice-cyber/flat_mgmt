from django.contrib import admin
from datetime import datetime
from .models import FlatInfo, House, Payment, Message, Announcement


# ---- SIMPLE ADMIN REGISTRATION ----
admin.site.register(FlatInfo)
admin.site.register(House)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(Announcement)


# ---- CUSTOM DASHBOARD ----
original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    houses = House.objects.all()
    flat = FlatInfo.objects.first()

    month_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    selected_month = request.GET.get("month")
    if not selected_month:
        selected_month = datetime.now().strftime("%B")

    selected_month = selected_month.strip()

    paid_count = 0
    not_paid_count = 0
    total_collected = 0
    total_pending = 0
    house_status_data = []

    for house in houses:

        # get all payments for this house and month
        month_payments = Payment.objects.filter(
            house=house,
            month__icontains=selected_month[:3]  # safer matching
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
        "flat_name": flat.name if flat else "PERBADANAN PENGURUSAN BLOK B1",
        "selected_month": selected_month,
        "month_list": month_list,
        "total_houses": houses.count(),
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "total_collected": total_collected,
        "total_pending": total_pending,
        "house_status_data": house_status_data,
    })

    return original_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index