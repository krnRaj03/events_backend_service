from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .models import Organizer, Events, TicketInfo, Panels
from accounts.models import CustomUser
from utilities import (
    send_email_sendgrid,
    generate_random_password,
    upload_S3_image,
)


# Create your views here.
def admin_login(request):
    if request.method == "POST":
        if "test1" in request.POST:
            email = request.POST["email"]
            password = request.POST["pass1"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("Login successful", user)
                return redirect("admin_home")
    return render(request, "auth/admin_login.html")


def admin_home(request):
    return render(request, "panel/admin_home.html")


def add_events(request):
    organizers = Organizer.objects.all()
    events = Events.objects.all()
    panels = Panels.objects.all()

    if request.method == "POST":
        if "org_form" in request.POST:
            organizer_name = request.POST["organizer_name"]
            industry_type = request.POST["industry_type"]
            organizer_email = request.POST["organizer_email"]
            organizer_mobile_no = request.POST["organizer_mobile_no"]
            contact_person_name = request.POST["contact_person_name"]
            contact_person_email = request.POST["contact_person_email"]
            contact_person_mobile_no = request.POST["contact_person_mobile_no"]
            contact_person_designation = request.POST["contact_person_designation"]
            org_image = request.FILES["image"].name
            address_line1 = request.POST["address_line1"]
            address_line2 = request.POST["address_line2"]
            city = request.POST["city"]
            state = request.POST["state"]
            country = request.POST["country"]
            pincode = request.POST["pincode"]
            if org_image:
                folder_name = "organization_images/"
                result, s3_url = upload_S3_image(folder_name, request, org_image)
                if result:
                    print("Image uploaded successfully")
                    print("S3 URL:", s3_url)
                else:
                    print("Image not uploaded")
            org = Organizer.objects.create(
                organizer_name=organizer_name,
                industry_type=industry_type,
                organizer_email=organizer_email,
                organizer_mobile_no=organizer_mobile_no,
                contact_person_name=contact_person_name,
                organizer_image=s3_url,
                contact_person_email=contact_person_email,
                contact_person_mobile_no=contact_person_mobile_no,
                contact_person_designation=contact_person_designation,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                country=country,
                pincode=pincode,
                date_created=datetime.now(),
                date_updated=datetime.now(),
            )
            org.save()
            print("Organizer form submitted")

        elif "event_form" in request.POST:
            events_name = request.POST["event_name"]
            events_type = request.POST["event_type"]
            events_agenda = request.POST["event_agenda"]
            events_image = request.FILES["image"].name
            events_description = request.POST["event_description"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            events_panels = request.POST["number_of_panels"]
            venue = request.POST["venue_link"]
            total_seats = request.POST["total_seats"]
            organizer_id = request.POST["organizer_id"]
            organizer_instance = Organizer.objects.get(organizer_id=organizer_id)
            if events_image:
                folder_name = "event_images/"
                result, s3_url = upload_S3_image(folder_name, request, events_image)
                if result:
                    print("Image uploaded successfully")
                    print("S3 URL:", s3_url)
                else:
                    print("Image not uploaded")

            event = Events(
                event_name=events_name,
                event_type=events_type,
                event_agenda=events_agenda,
                event_image=s3_url,
                number_of_panels=events_panels,
                event_description=events_description,
                start_date=start_date,
                end_date=end_date,
                venue_link=venue,
                date_created=timezone.now(),
                date_updated=timezone.now(),
                total_seats=total_seats,
                organizer=organizer_instance,
            )
            event.save()

        elif "panel_form" in request.POST:
            panel_name = request.POST["panel_name"]
            panel_no = request.POST["panel_no"]
            panel_description = request.POST["panel_description"]
            panel_topic = request.POST["panel_topic"]
            panel_image = request.FILES["image"].name
            start_time = request.POST["panel_start_time"]
            end_time = request.POST["panel_end_time"]
            events_id = request.POST["event_id"]
            events_instance = Events.objects.get(event_id=events_id)
            panel = Panels.objects.create(
                panel_name=panel_name,
                panel_no=panel_no,
                events=events_instance,
                panel_description=panel_description,
                panel_topic=panel_topic,
                # panel_image=panel_image,
                panel_start_time=start_time,
                panel_end_time=end_time,
                date_created=datetime.now(),
                date_updated=datetime.now(),
            )
            panel.save()

        elif "speaker_form" in request.POST:
            speaker_fname = request.POST["first_name"]
            speaker_lname = request.POST["last_name"]
            speaker_email = request.POST["email"]
            speaker_mobile_no = request.POST["mobile_no"]
            speaker_dob = request.POST["date_of_birth"]
            speaker_gender = request.POST["gender"]
            speaker_job_title = request.POST["job_title"]
            speaker_work_place = request.POST["work_place"]
            role = request.POST["role"]
            speaker_address_line1 = request.POST["address_line1"]
            speaker_address_line2 = request.POST["address_line2"]
            speaker_city = request.POST["city"]
            speaker_state = request.POST["state"]
            speaker_country = request.POST["country"]
            speaker_pincode = request.POST["pincode"]
            speaker_bio = request.POST.get("speaker_bio", "")
            linkedin_url = request.POST["linkedin"]
            twitter_url = request.POST["twitter"]
            facebook_url = request.POST["facebook"]
            instagram_url = request.POST["instagram"]
            events_id = request.POST.get("event_id")
            panel_id = request.POST.get("panel_id")
            password = (
                generate_random_password()
            )  # generate_random_password() for speaker/moderator
            speaker_image = request.FILES.get("image").name
            events_instance = Events.objects.get(event_id=events_id)
            panels_instance = Panels.objects.get(panel_id=panel_id)
            if speaker_image:
                folder_name = "speaker_images/"
                result, s3_url = upload_S3_image(folder_name, request, speaker_image)
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
                work_place=speaker_work_place,
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
                linkedin_url=linkedin_url,
                twitter_url=twitter_url,
                facebook_url=facebook_url,
                instagram_url=instagram_url,
                date_created=datetime.now(),
            )
            speaker.save()
            send_email_sendgrid(
                speaker_email,
                f"Your Login email is <strong>{speaker_email}</strong> & password is <strong>{password}</strong>. Please click on the LOGIN Link on the app.",
            )
            speaker.set_password(password)
            events_instance.user.add(speaker)
            events_instance.save()
            panels_instance.user.add(speaker)
            speaker.save()
            return render(
                request,
                "panel/add_events.html",
                {"organizers": organizers, "events": events},
            )

        elif "ticket_form" in request.POST:
            ticket_type = request.POST["ticket_type"]
            ticket_price = request.POST["ticket_price"]
            ticket_description = request.POST["ticket_description"]
            tickets_available = request.POST["tickets_available"]
            ticket_image = request.FILES["image"].name
            events_id = request.POST["event_id"]
            events_instance = Events.objects.get(event_id=events_id)
            if ticket_image:
                folder_name = "ticket_images/"
                result, s3_url = upload_S3_image(folder_name, request, ticket_image)
                if result:
                    print("Image uploaded successfully")
                    print("S3 URL:", s3_url)
                else:
                    print("Image not uploaded")
            ticket = TicketInfo.objects.create(
                ticket_type=ticket_type,
                ticket_price=ticket_price,
                ticket_description=ticket_description,
                ticket_image=s3_url,
                tickets_available=tickets_available,
                events=events_instance,
            )
            ticket.save()

    return render(
        request,
        "panel/add_events.html",
        {"organizers": organizers, "events": events, "panels": panels},
    )


def admin_stastics(request):
    events = Events.objects.all()
    events_speaker = Events.objects.filter(user__role="speaker")
    context = {
        "events": events,
        "events_speaker": events_speaker,
    }
    return render(request, "panel/all_events.html", context)


def delete_event(request, event_id):
    event = Events.objects.get(event_id=event_id)
    event.delete()
    return redirect("admin_stastics")


def edit_event(request, event_id):
    event = Events.objects.get(event_id=event_id)
    print(event)
    if request.method == "POST":
        pass
    return render(request, "panel/edit_event.html", {"event": event})


def edit_speaker(request, speaker_id):
    speaker = CustomUser.objects.get(id=speaker_id)
    if request.method == "POST":
        # Update user attributes based on the form fields
        speaker.first_name = request.POST["first_name"]
        speaker.last_name = request.POST["last_name"]
        speaker.job_title = request.POST["job_title"]
        speaker.work_place = request.POST["work_place"]
        speaker.mobile_no = request.POST["mobile_no"]
        speaker.date_updated = datetime.now()
        speaker.save()

        #     # Handle image upload
        # if "image" in request.FILES:
        #     speaker.user_image = request.FILES["image"].name
        #     folder_name = "speaker_images/"
        #     result, s3_url = upload_S3_image(folder_name, request, speaker.user_image)
        #     if result:
        #         print("Image uploaded successfully")
        #         print("S3 URL:", s3_url)
        #         speaker.user_image = s3_url
        #     else:
        #         print("Image not uploaded")
    return render(request, "panel/edit_speaker.html", {"speaker": speaker})


def count_speaker(request):
    speakers = CustomUser.objects.filter(is_user=False, role="speaker").values(
        "first_name", "last_name"
    )
    # Convert QuerySet to a list of dictionaries
    speaker_list = list(speakers)
    return JsonResponse({"count": len(speaker_list), "list": speaker_list})


def all_speakers(request):
    users = CustomUser.objects.filter(Q(role="speaker") | Q(role="moderator"))

    # Retrieve the events associated with these users
    events = Events.objects.filter(user__in=users)

    ############

    # Retrieve the panels associated with these users
    panels = Panels.objects.filter(user__in=users)
    print("Panels:", panels)
    context = {"speakers": users, "users": users}
    return render(request, "panel/all_speakers.html", context=context)


# def Speaker(request):
#     events = Events.objects.all()
#     if request.method == "POST":
#         speaker_fname = request.POST["first_name"]
#         speaker_lname = request.POST["last_name"]
#         speaker_email = request.POST["email"]
#         speaker_mobile_no = request.POST["mobile_no"]
#         speaker_dob = request.POST["date_of_birth"]
#         speaker_gender = request.POST["gender"]
#         speaker_job_title = request.POST["job_title"]
#         role = request.POST["role"]
#         speaker_address_line1 = request.POST["address_line1"]
#         speaker_address_line2 = request.POST["address_line2"]
#         speaker_city = request.POST["city"]
#         speaker_state = request.POST["state"]
#         speaker_country = request.POST["country"]
#         speaker_pincode = request.POST["pincode"]
#         events_id = request.POST.get("event_id")
#         password = generate_random_password()
#         speaker_image = request.FILES.get("image").name
#         events_instance = Events.objects.get(events_id=events_id)
#         if speaker_image:
#             folder_name = "speaker_images/"
#             result, s3_url = upload_S3_image(folder_name, request, speaker_image)
#             print("Image uploaded successfully")
#             if result:
#                 print("Image uploaded successfully")
#                 print("S3 URL:", s3_url)
#         else:
#             print("Image not uploaded")

#         speaker = CustomUser.objects.create(
#             email=speaker_email,
#             mobile_no=speaker_mobile_no,
#             first_name=speaker_fname,
#             last_name=speaker_lname,
#             date_of_birth=speaker_dob,
#             gender=speaker_gender,
#             job_title=speaker_job_title,
#             is_user=False,
#             status="profile_created",
#             role=role,
#             address_line1=speaker_address_line1,
#             address_line2=speaker_address_line2,
#             city=speaker_city,
#             state=speaker_state,
#             country=speaker_country,
#             pincode=speaker_pincode,
#             user_image=s3_url,
#             date_created=datetime.now(),
#         )
#         send_email_with_sendgrid(
#             speaker_email,
#             f"Your Login email is {speaker_email} & password is {password}. Please click on the LOGIN Link on the app.",
#         )
#         speaker.set_password(password)
#         events_instance.user.add(speaker)
#         events_instance.save()
#         speaker.save()
#         return render(request, "new_speaker.html", {"events": events})

#     return render(request, "new_speaker.html", {"events": events})
