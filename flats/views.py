from django.shortcuts import render, redirect, get_object_or_404
from .models import House, Payment, Message, Announcement


def owner_login(request):
    if request.method == "POST":
        house_number = request.POST.get("house", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            house = House.objects.get(house_number=house_number, password=password)
            request.session["house_id"] = house.id
            return redirect("owner_home")
        except House.DoesNotExist:
            return render(request, "owner/login.html", {
                "error": "Invalid house number or password"
            })

    return render(request, "owner/login.html")


def owner_home(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    current_payment = Payment.objects.filter(house=house).order_by("-id").first()

    if current_payment and current_payment.status == "Paid":
        current_status = "Paid"
    else:
        current_status = "Not Paid"

    return render(request, "owner/home.html", {
        "house": house,
        "current_status": current_status,
    })


def owner_payments(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    payments = Payment.objects.filter(house=house).order_by("-id")

    return render(request, "owner/payments.html", {
        "house": house,
        "payments": payments,
    })


def owner_receipt(request, payment_id):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    payment = get_object_or_404(Payment, id=payment_id, house=house)

    return render(request, "owner/receipt.html", {
        "house": house,
        "payment": payment,
    })


def owner_announcements(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)
    announcements = Announcement.objects.all().order_by("-created_at")

    return render(request, "owner/announcements.html", {
        "house": house,
        "announcements": announcements,
    })


def owner_message(request):
    house_id = request.session.get("house_id")
    if not house_id:
        return redirect("owner_login")

    house = House.objects.get(id=house_id)

    if request.method == "POST":
        message_text = request.POST.get("message_text", "").strip()
        if message_text:
            Message.objects.create(house=house, message_text=message_text)
            return render(request, "owner/message.html", {
                "house": house,
                "success": "Message sent successfully"
            })

    return render(request, "owner/message.html", {"house": house})


def owner_logout(request):
    request.session.flush()
    return redirect("owner_login")
