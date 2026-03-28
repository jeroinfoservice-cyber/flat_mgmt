from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import FlatInfo, House, Payment, Message, Announcement


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('house', 'month', 'amount', 'colored_status', 'date_paid')
    list_filter = ('month', 'status')
    search_fields = ('house__house_number',)

    def colored_status(self, obj):
        if obj.status == "Paid":
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', "Paid")
        return format_html('<span style="color:red; font-weight:bold;">{}</span>', "Not Paid")

    colored_status.short_description = "Status"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('house', 'short_message', 'created_at')
    search_fields = ('house__house_number', 'message_text')

    def short_message(self, obj):
        return obj.message_text[:60]
    short_message.short_description = "Message"


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')


admin.site.register(FlatInfo)
admin.site.register(House)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Announcement, AnnouncementAdmin)

original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    houses = House.objects.all()
    flat = FlatInfo.objects.first()

    month_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    selected_month = request.GET.get("month")
    if not selected_month or selected_month not in month_list:
        selected_month = datetime.now().strftime("%B")

    data = []
    paid_count = 0
    not_paid_count = 0
    total_collected = 0
    total_pending = 0

    for house in houses:
        payment = Payment.objects.filter(
            house=house,
            month=selected_month
        ).order_by('-id').first()

        if payment and payment.status == "Paid":
            status = "Paid"
            paid_count += 1
            total_collected += float(payment.amount)
        else:
            status = "Not Paid"
            not_paid_count += 1
            if payment:
                total_pending += float(payment.amount)

        data.append({
            "house": house.house_number,
            "status": status
        })

    # chart data for all months
    chart_labels = month_list
    chart_values = []

    for month in month_list:
        month_total = 0
        month_payments = Payment.objects.filter(month=month, status="Paid")
        for p in month_payments:
            month_total += float(p.amount)
        chart_values.append(month_total)

    extra_context = extra_context or {}
    extra_context.update({
        "flat_name": flat.name if flat else "PERBADANAN PENGURUSAN BLOK B1",
        "total_houses": houses.count(),
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "house_status_data": data,
        "selected_month": selected_month,
        "month_list": month_list,
        "total_collected": total_collected,
        "total_pending": total_pending,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "popup_title": "Management Notification",
        "popup_message": f"Showing payment summary for {selected_month}.",
    })

    return original_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index