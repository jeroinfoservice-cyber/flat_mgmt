from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html

from .models import House, Payment, Message, Announcement, Expense


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("house", "month", "amount", "colored_status", "date_paid")
    list_filter = ("month", "status")
    search_fields = ("house__house_number", "house__owner_name")

    def colored_status(self, obj):
        if obj.status == "Paid":
            return format_html('<span style="color:green; font-weight:bold;">Paid</span>')
        return format_html('<span style="color:red; font-weight:bold;">Not Paid</span>')

    colored_status.short_description = "Status"


class MessageAdmin(admin.ModelAdmin):
    list_display = ("house", "message_text", "created_at")
    search_fields = ("house__house_number", "message_text")


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "amount", "expense_month", "created_at")
    list_filter = ("expense_month", "category")
    search_fields = ("title", "details")


admin.site.register(House)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Expense, ExpenseAdmin)


original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}

    selected_month = request.GET.get("month")

    all_payment_months = list(
        Payment.objects.order_by("-month").values_list("month", flat=True).distinct()
    )

    all_expense_months = list(
        Expense.objects.order_by("-expense_month").values_list("expense_month", flat=True).distinct()
    )

    all_months = sorted(set(all_payment_months + all_expense_months), reverse=True)

    if selected_month:
        selected_month_obj = None
        for m in all_months:
            if m.strftime("%Y-%m") == selected_month:
                selected_month_obj = m
                break
    else:
        selected_month_obj = all_months[0] if all_months else None

    houses = House.objects.all().order_by("house_number")
    house_status_data = []

    paid_count = 0
    not_paid_count = 0
    month_collected = Decimal("0.00")
    total_pending = Decimal("0.00")
    all_time_collected = Payment.objects.filter(status="Paid").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    month_expenses = Expense.objects.none()
    month_expense_total = Decimal("0.00")

    if selected_month_obj:
        month_payments = Payment.objects.filter(month=selected_month_obj)
        month_expenses = Expense.objects.filter(expense_month=selected_month_obj).order_by("-created_at")

        month_collected = month_payments.filter(status="Paid").aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

        month_expense_total = month_expenses.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

        for house in houses:
            payment = month_payments.filter(house=house).order_by("-id").first()

            if payment and payment.status == "Paid":
                status = "Paid"
                paid_count += 1
                paid_amount = payment.amount
                amount_due = payment.amount
            else:
                status = "Not Paid"
                not_paid_count += 1
                paid_amount = Decimal("0.00")
                amount_due = house.monthly_fee
                total_pending += house.monthly_fee

            house_status_data.append({
                "house": house.house_number,
                "owner_name": house.owner_name,
                "paid_amount": paid_amount,
                "amount_due": amount_due,
                "status": status,
            })

        selected_month_label = selected_month_obj.strftime("%B %Y")
    else:
        selected_month_label = "No Month Found"

        for house in houses:
            house_status_data.append({
                "house": house.house_number,
                "owner_name": house.owner_name,
                "paid_amount": Decimal("0.00"),
                "amount_due": house.monthly_fee,
                "status": "Not Paid",
            })

        not_paid_count = houses.count()

    extra_context.update({
        "available_months": all_months,
        "selected_month": selected_month_obj.strftime("%Y-%m") if selected_month_obj else "",
        "selected_month_label": selected_month_label,
        "total_houses": houses.count(),
        "paid_count": paid_count,
        "not_paid_count": not_paid_count,
        "month_collected": month_collected,
        "all_time_collected": all_time_collected,
        "total_pending": total_pending,
        "month_expense_total": month_expense_total,
        "house_status_data": house_status_data,
        "month_expenses": month_expenses,
    })

    return original_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index