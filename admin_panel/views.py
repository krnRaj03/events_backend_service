from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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


@login_required
def admin_home(request):
    return render(request, "panel/admin_home.html")


@login_required
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
            venue_url = request.POST["venue_link"]
            venue_name = request.POST["venue_name"]
            total_seats = request.POST["total_seats"]
            organizer_id = request.POST.getlist("organizer_id")

            # organizer_instance = Organizer.objects.get(organizer_id=organizer_id)
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
                venue_link=venue_url,
                venue_name=venue_name,
                date_created=timezone.now(),
                date_updated=timezone.now(),
                total_seats=total_seats,
                # organizer=organizer,
            )
            event.save()
            for org in organizer_id:
                organizer = Organizer.objects.get(pk=org)
                event.organizer.add(organizer)

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
            ticket_start_date = request.POST["start_date"]
            ticket_end_date = request.POST["end_date"]
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
                ticket_start_date=ticket_start_date,
                ticket_end_date=ticket_end_date,
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


@login_required
def all_events(request):
    events = Events.objects.all()
    events_speaker = Events.objects.filter(user__role="speaker")
    context = {
        "events": events,
        "events_speaker": events_speaker,
    }
    return render(request, "panel/all_events.html", context)


@login_required
def view_event(request, event_id):
    event = Events.objects.get(event_id=event_id)
    panels = Panels.objects.filter(events=event)
    tickets = TicketInfo.objects.filter(events=event)

    """Organizers related to the event"""
    organizers = event.organizer.all()

    """Speakers related to the event"""
    speakers = event.user.filter(role="speaker")

    """Moderators related to the event"""
    moderators = event.user.filter(role="moderator")

    """Duration of the event"""
    # string format "%d %b %Y"
    start_date_str = event.start_date.strftime("%d %b %Y")
    end_date_str = event.end_date.strftime("%d %b %Y")
    # Convert the date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%d %b %Y")
    end_date = datetime.strptime(end_date_str, "%d %b %Y")
    # Calculate the difference between the dates
    date_difference = start_date - end_date
    # Access the difference in days
    days_difference = date_difference.days

    context = {
        "event": event,
        "panels": panels,
        "tickets": tickets,
        "days_difference": days_difference,
        "organizers": organizers,
        "speakers": speakers,
        "moderators": moderators,
    }
    return render(request, "panel/view_event.html", context)


@login_required
def delete_event(request, event_id):
    event = Events.objects.get(event_id=event_id)
    event.delete()
    return redirect("admin_stastics")


@login_required
def edit_event(request, event_id):
    event = Events.objects.get(event_id=event_id)
    if event.start_date and event.end_date:
        event_start_date = event.start_date.strftime("%Y-%m-%d")
        event_start_time = event.start_date.strftime("%H:%M")
        event_end_date = event.end_date.strftime("%Y-%m-%d")
        event_end_time = event.end_date.strftime("%H:%M")
        print(event_start_date, event_start_time, event_end_date, event_end_time)
    else:
        event_end_date, event_end_time, event_start_date, event_end_time = (
            None,
            None,
            None,
            None,
        )

    if request.method == "POST":
        event.event_name = request.POST["event_name"]
        event.event_type = request.POST["event_type"]
        event.event_agenda = request.POST["event_agenda"]
        event.event_description = request.POST["event_description"]
        event.start_date = request.POST["start_date"]
        event.end_date = request.POST["end_date"]
        event.number_of_panels = request.POST["number_of_panels"]
        event.venue_link = request.POST["venue_link"]
        event.venue_name = request.POST["venue_name"]
        event.total_seats = request.POST["total_seats"]
        if "image" in request.FILES:
            event_image = request.FILES["image"].name
            folder_name = "event_images/"
            result, s3_url = upload_S3_image(folder_name, request, event_image)
            if result:
                print("Image uploaded successfully")
                print("S3 URL:", s3_url)
                event.event_image = s3_url
            else:
                print("Image not uploaded")
        else:
            print("Image not uploaded")
        event.save()
    context = {
        "event": event,
        "event_start_date": event_start_date,
        "event_end_date": event_end_date,
        "event_start_time": event_start_time,
        "event_end_time": event_end_time,
    }
    return render(request, "panel/edit_event.html", context)


@login_required
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


@login_required
def delete_speaker(request, speaker_id):
    speaker = CustomUser.objects.get(id=speaker_id)
    speaker.delete()
    return redirect("all_speakers")


@login_required
def edit_ticket(request, ticket_id):
    ticket = TicketInfo.objects.get(ticket_id=ticket_id)

    if ticket.ticket_start_date and ticket.ticket_end_date:
        ticket_start_date = ticket.ticket_start_date.strftime("%Y-%m-%d")
        ticket_start_time = ticket.ticket_start_date.strftime("%H:%M")
        ticket_end_date = ticket.ticket_end_date.strftime("%Y-%m-%d")
        ticket_end_time = ticket.ticket_end_date.strftime("%H:%M")
    else:
        ticket_start_date, ticket_end_date, ticket_start_time, ticket_end_time = (
            None,
            None,
            None,
            None,
        )

    if request.method == "POST":
        ticket.ticket_type = request.POST["ticket_type"]
        ticket.ticket_price = request.POST["ticket_price"]
        ticket.ticket_description = request.POST["ticket_description"]
        ticket.tickets_available = request.POST["tickets_available"]
        ticket.ticket_start_date = request.POST["ticket_start_date"]
        ticket.ticket_end_date = request.POST["ticket_end_date"]
        if "image" in request.FILES:
            ticket_image = request.FILES["image"].name
            folder_name = "ticket_images/"
            result, s3_url = upload_S3_image(folder_name, request, ticket_image)
            if result:
                print("Image uploaded successfully")
                print("S3 URL:", s3_url)
                ticket.ticket_image = s3_url
        else:
            print("Image not uploaded")
        ticket.save()

    context = {
        "ticket": ticket,
        "ticket_start_date": ticket_start_date,
        "ticket_end_date": ticket_end_date,
        "ticket_start_time": ticket_start_time,
        "ticket_end_time": ticket_end_time,
    }
    return render(request, "panel/edit_ticket.html", context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = TicketInfo.objects.get(ticket_id=ticket_id)
    ticket.delete()
    return redirect("all_events")


@login_required
def all_speakers(request):
    users = CustomUser.objects.filter(Q(role="speaker") | Q(role="moderator"))
    # Retrieve the panels associated with these users
    panels = Panels.objects.filter(user__in=users)
    context = {"speakers": users, "users": users}
    return render(request, "panel/all_speakers.html", context=context)


@login_required
def all_users(request):
    users = CustomUser.objects.filter(role="user")
    context = {"users": users}
    return render(request, "panel/all_users.html", context)


@login_required
def all_tickets(request):
    tickets = TicketInfo.objects.all()
    context = {"tickets": tickets}
    return render(request, "panel/all_tickets.html", context)
