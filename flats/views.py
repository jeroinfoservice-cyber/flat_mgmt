from django.shortcuts import render
from django.db.models import Sum
from .models import House, Payment, Announcement, FlatInfo, Message

MONTHLY_FEE = 100.00


def home(request):
    months = Payment.objects.values_list('month', flat=True).distinct().order_by('month')

    selected_month = request.GET.get('month')

    if not selected_month and months.exists():
        selected_month = months.last()

    houses = House.objects.all().order_by('house_number')
    total_houses = houses.count()

    if selected_month:
        paid_payments = Payment.objects.filter(
            month=selected_month,
            status='Paid'
        )
    else:
        paid_payments = Payment.objects.none()

    paid_house_ids = paid_payments.values_list('house_id', flat=True).distinct()
    paid_houses_count = paid_house_ids.count()

    not_paid_houses_count = total_houses - paid_houses_count
    total_collected = paid_payments.aggregate(total=Sum('amount'))['total'] or 0
    total_pending = not_paid_houses_count * MONTHLY_FEE

    house_status_list = []
    for house in houses:
        is_paid = Payment.objects.filter(
            house=house,
            month=selected_month,
            status='Paid'
        ).exists() if selected_month else False

        house_status_list.append({
            'house_number': house.house_number,
            'status': 'Paid' if is_paid else 'Not Paid'
        })

    context = {
        'months': months,
        'selected_month': selected_month,
        'total_houses': total_houses,
        'paid_houses_count': paid_houses_count,
        'not_paid_houses_count': not_paid_houses_count,
        'total_collected': total_collected,
        'total_pending': total_pending,
        'house_status_list': house_status_list,
    }
    return render(request, 'owner/home.html', context)


def announcements_page(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'owner/announcements.html', {'announcements': announcements})


def flat_infos_page(request):
    flat_infos = FlatInfo.objects.all().order_by('title')
    return render(request, 'owner/flat_infos.html', {'flat_infos': flat_infos})


def houses_page(request):
    houses = House.objects.all().order_by('house_number')
    return render(request, 'owner/houses.html', {'houses': houses})


def messages_page(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'owner/message.html', {'messages': messages})


def payments_page(request):
    payments = Payment.objects.select_related('house').all().order_by('month', 'house__house_number')
    return render(request, 'owner/payments.html', {'payments': payments})


def receipt_page(request):
    return render(request, 'owner/receipt.html')