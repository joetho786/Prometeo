from pickle import FALSE
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtendedUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from django.contrib import messages

User = get_user_model()


@login_required
def user_profile(request):
    if(request.method == "POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        college_name = request.POST['college_name']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        city = request.POST['city']
        current_year = request.POST['current_year']
        isCampusAmbassador = request.POST.get('isCampusAmbassador', False)
        referralCode = request.POST.get('referral_code', 'default')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        extendeduser = ExtendedUser.objects.filter(user=request.user).first()
        # If the current user is using referral code.
        if referralCode and referralCode != "default":
            referredBy = ExtendedUser.objects.filter(invite_referral=referralCode).first()
            if referredBy:
                extendeduser.referred_by = referredBy.user
            else:
                messages.error(request, 'No referral code found, either check your code again or leave the field empty.')
                return redirect("/users/profile")
        extendeduser.gender = gender
        extendeduser.contact = phone_no
        extendeduser.current_year = gender
        extendeduser.college = college_name
        extendeduser.city = city
        extendeduser.current_year = current_year
        if isCampusAmbassador == "on":
            extendeduser.ambassador = True
        # If the user wants to be the campus ambassador.
        invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
        if extendeduser.isProfileCompleted is False and extendeduser.ambassador is True:
            invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
            extendeduser.invite_referral = invite_referral
            send_mail(
                'Campus Ambassador',
                f"Dear {user.first_name},\nYou are now a campus ambassador. Your referral code is {invite_referral}.\nRegards,\nPrometeo 2022 Team",
                'iitj.iotwebportal@gmail.com',
                [user.email],
                fail_silently=False,
            )
        extendeduser.isProfileCompleted = True
        extendeduser.save()
        messages.success(request, 'Your profile has been updated.')

    return render(request, 'profile.html')


@login_required
def make_ca(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.success(request, 'Complete your profile first.')
        return redirect("/users/profile")

    extendeduser = ExtendedUser.objects.filter(user=user).first()
    if(extendeduser.ambassador==False):
        extendeduser.ambassador = True
        invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
        extendeduser.invite_referral = invite_referral
        extendeduser.save()
        send_mail(
            'Campus Ambassador',
            f"Dear {user.first_name},\nYou are now a campus ambassador. Your referral code is {invite_referral}.\nRegards,\nPrometeo 2022 Team",
            'iitj.iotwebportal@gmail.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(request, 'You are now a campus ambassador. Please check you email for referral code.')
        return redirect('/')

    else:
        messages.success(request, 'Your are already campus ambassador')
        return redirect('/')
