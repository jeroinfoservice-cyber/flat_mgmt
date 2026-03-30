from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FlatInfo, House, Payment, Message, Announcement, MaintenanceRequest


def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        house_id = request.session.get("house_id")

        if not house_id:
            return redirect("owner_login")

        return view_func(request, *args, **kwargs)

    return wrapper


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


@owner_required
def owner_home(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    flat = FlatInfo.objects.first()

    total_payments = Payment.objects.filter(house=house, status="Paid").count()
    announcements_count = Announcement.objects.count()
    messages_count = Message.objects.filter(house=house).count()
    maintenance_count = MaintenanceRequest.objects.filter(house=house).count()

    return render(request, "owner/home.html", {
        "house": house,
        "flat": flat,
        "total_payments": total_payments,
        "announcements_count": announcements_count,
        "messages_count": messages_count,
        "maintenance_count": maintenance_count,
    })


@owner_required
def owner_payments(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    payments = Payment.objects.filter(house=house).order_by("-id")
    flat = FlatInfo.objects.first()

    return render(request, "owner/payments.html", {
        "house": house,
        "payments": payments,
        "flat": flat
    })


@owner_required
def owner_receipt(request, payment_id):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    payment = get_object_or_404(Payment, id=payment_id, house=house)
    flat = FlatInfo.objects.first()

    return render(request, "owner/receipt.html", {
        "house": house,
        "payment": payment,
        "flat": flat
    })


@owner_required
def owner_announcements(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    announcements = Announcement.objects.all().order_by("-created_at")
    flat = FlatInfo.objects.first()

    return render(request, "owner/announcements.html", {
        "house": house,
        "announcements": announcements,
        "flat": flat
    })


@owner_required
def owner_message(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
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


@owner_required
def owner_maintenance_list(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    flat = FlatInfo.objects.first()

    maintenance_requests = MaintenanceRequest.objects.filter(
        house=house
    ).order_by("-created_at")

    return render(request, "owner/maintenance_list.html", {
        "house": house,
        "flat": flat,
        "maintenance_requests": maintenance_requests
    })


@owner_required
def owner_maintenance_create(request):

    house_id = request.session.get("house_id")
    house = get_object_or_404(House, id=house_id)
    flat = FlatInfo.objects.first()

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title and description:

            MaintenanceRequest.objects.create(
                house=house,
                title=title,
                description=description
            )

            messages.success(
                request,
                "Maintenance request submitted successfully."
            )

            return redirect("owner_maintenance_list")

        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, "owner/maintenance_create.html", {
        "house": house,
        "flat": flat
    })


def owner_logout(request):

    request.session.flush()

    return redirect("owner_login")