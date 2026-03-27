from django.shortcuts import render, redirect, get_object_or_404
from .models import FlatInfo, House, Payment, Message, Announcement


def owner_login(request):
    flat = FlatInfo.objects.first()

    if request.method == "POST":
        house_number = request.POST.get("house", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            house = House.objects.get(house_number=house_number, password=password)
            request.session["house_id"] = house.id
            return redirect("owner_home")
        except House.DoesNotExist:
            return render(request, "owner/login.html", {
                "flat": flat,
                "error": "Invalid house number or password"
            })

    return render(request, "owner/login.html", {
        "flat": flat
    })


def owner_home(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    flat = FlatInfo.objects.first()

    payment_count = Payment.objects.filter(house=house, status="Paid").count()

    return render(request, "owner/home.html", {
        "house": house,
        "flat": flat,
        "payment_count": payment_count
    })


def owner_payments(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    payments = Payment.objects.filter(house=house).order_by("-id")
    flat = FlatInfo.objects.first()

    return render(request, "owner/payments.html", {
        "house": house,
        "payments": payments,
        "flat": flat
    })


def owner_receipt(request, payment_id):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    payment = get_object_or_404(Payment, id=payment_id, house=house)
    flat = FlatInfo.objects.first()

    return render(request, "owner/receipt.html", {
        "house": house,
        "payment": payment,
        "flat": flat
    })


def owner_announcements(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    announcements = Announcement.objects.all().order_by("-created_at")
    flat = FlatInfo.objects.first()

    return render(request, "owner/announcements.html", {
        "house": house,
        "announcements": announcements,
        "flat": flat
    })


def owner_message(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    flat = FlatInfo.objects.first()

    if request.method == "POST":
        message_text = request.POST.get("message_text", "").strip()

        if message_text:
            Message.objects.create(
                house=house,
                message_text=message_text
            )

            return render(request, "owner/message.html", {
                "house": house,
                "flat": flat,
                "success": "Message sent successfully"
            })

    return render(request, "owner/message.html", {
        "house": house,
        "flat": flat
    })


def owner_logout(request):
    request.session.flush()
    return redirect("owner_login")