from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from .models import Organizer, Events
from accounts.models import CustomUser
from utilities import (
    send_email_with_sendgrid,
    generate_random_password,
    upload_S3_image,
)


# Create your views here.
def organizer(request):
    if request.method == "POST":
        organizer_name = request.POST["organizer_name"]
        industry_type = request.POST["industry_type"]
        organizer_email = request.POST["organizer_email"]
        organizer_mobile_no = request.POST["organizer_mobile_no"]
        contact_person_name = request.POST["contact_person_name"]
        contact_person_email = request.POST["contact_person_email"]
        contact_person_mobile_no = request.POST["contact_person_mobile_no"]
        contact_person_designation = request.POST["contact_person_designation"]
        address_line1 = request.POST["address_line1"]
        address_line2 = request.POST["address_line2"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        pincode = request.POST["pincode"]
        org = Organizer.objects.create(
            organizer_name=organizer_name,
            industry_type=industry_type,
            organizer_email=organizer_email,
            organizer_mobile_no=organizer_mobile_no,
            contact_person_name=contact_person_name,
            contact_person_email=contact_person_email,
            contact_person_mobile_no=contact_person_mobile_no,
            contact_person_designation=contact_person_designation,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
        )
        org.save()
        return render(request, "temp_organization.html")
    return render(request, "temp_organization.html")


def event(request):
    organizers = Organizer.objects.all()

    if request.method == "POST":
        events_name = request.POST.get("events_name")
        events_description = request.POST.get("events_description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        venue = request.POST.get("venue")
        total_seats = request.POST.get("total_seats")
        organizer_id = request.POST.get("organizer_id")
        organizer_instance = Organizer.objects.get(organizer_id=organizer_id)
        # Create and save a new event
        event = Events(
            events_name=events_name,
            events_description=events_description,
            start_date=start_date,
            end_date=end_date,
            venue_link=venue,
            date_created=timezone.now(),
            date_updated=timezone.now(),
            total_seats=total_seats,
            organizer=organizer_instance,
        )
        event.save()
        return render(
            request, "temp_events.html", {"organizers": organizers}
        )  # Change 'success_page' to your desired URL

    return render(request, "temp_events.html", {"organizers": organizers})


def Speaker(request):
    events = Events.objects.all()
    if request.method == "POST":
        speaker_fname = request.POST["first_name"]
        speaker_lname = request.POST["last_name"]
        speaker_email = request.POST["email"]
        speaker_mobile_no = request.POST["mobile_no"]
        speaker_dob = request.POST["date_of_birth"]
        speaker_gender = request.POST["gender"]
        speaker_job_title = request.POST["job_title"]
        role = request.POST["role"]
        speaker_address_line1 = request.POST["address_line1"]
        speaker_address_line2 = request.POST["address_line2"]
        speaker_city = request.POST["city"]
        speaker_state = request.POST["state"]
        speaker_country = request.POST["country"]
        speaker_pincode = request.POST["pincode"]
        events_id = request.POST.get("event_id")
        password = generate_random_password()
        speaker_image = request.FILES.get("image").name
        events_instance = Events.objects.get(events_id=events_id)
        if speaker_image:
            folder_name = "speaker_images/"
            result, s3_url = upload_S3_image(folder_name, request, speaker_image)
            print("Image uploaded successfully")
            if result:
                print("Image uploaded successfully")
                print("S3 URL:", s3_url)
        else:
            print("Image not uploaded")

        speaker = CustomUser.objects.create(
            email=speaker_email,
            mobile_no=speaker_mobile_no,
            first_name=speaker_fname,
            last_name=speaker_lname,
            date_of_birth=speaker_dob,
            gender=speaker_gender,
            job_title=speaker_job_title,
            is_user=False,
            status="profile_created",
            role=role,
            address_line1=speaker_address_line1,
            address_line2=speaker_address_line2,
            city=speaker_city,
            state=speaker_state,
            country=speaker_country,
            pincode=speaker_pincode,
            user_image=s3_url,
            date_created=datetime.now(),
        )
        send_email_with_sendgrid(
            speaker_email,
            f"Your Login email is {speaker_email} & password is {password}. Please click on the LOGIN Link on the app.",
        )
        speaker.set_password(password)
        events_instance.user.add(speaker)
        events_instance.save()
        speaker.save()
        return render(request, "new_speaker.html", {"events": events})

    return render(request, "new_speaker.html", {"events": events})


def count_speaker(request):
    speakers = CustomUser.objects.filter(is_user=False, role="speaker").values(
        "first_name", "last_name"
    )
    # Convert QuerySet to a list of dictionaries
    speaker_list = list(speakers)
    return JsonResponse({"count": len(speaker_list), "list": speaker_list})


# def aprroveURL(request):
#     return render(request, "temp_payment.html")


#     # Convert QuerySet to a list of dictionaries
#     speaker_list = list(speakers)
#     return JsonResponse({"count": count_speaker, "list": speaker_list})
