from django.contrib import admin
from django.utils.html import format_html
from .models import House, Payment, Message, Announcement, Expense


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("house", "month", "amount", "colored_status", "date_paid")
    list_filter = ("month", "status")
    search_fields = ("house__house_number",)

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