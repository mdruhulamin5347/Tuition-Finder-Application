from django.shortcuts import render,redirect
from .forms import UserProfileForm, TeacherProfileForm
from .models import UserProfile, TeacherProfile
from django.contrib import messages
from notifications.signals import notify
# Create your views here.
def CREATE_PROFILE(request):
    try:
        instance=UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist :
        instance=None
    if request.method=="POST":
        if instance:
            form=UserProfileForm(request.POST, request.FILES, instance=instance)
        else:
            form=UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request,'successfully Updated your profile')
            return redirect('view')
    else:
        form=UserProfileForm(instance=instance)
    return render(request, 'profile/profile.html',{'form':form})

def PROFILE_VIEW(request):
    user=request.user
    return render(request,'profile/profile_view.html',{'user':user})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherProfileForm
from .models import TeacherProfile

def TUITIONBD(request):
    try:
        instance = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        instance = None

    if request.method == "POST":
        if instance:
            form = TeacherProfileForm(request.POST, instance=instance)
        else:
            form = TeacherProfileForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
  
            subjects = form.cleaned_data['subject']
            classins = form.cleaned_data['classin']
            category = form.cleaned_data['category']
            district = form.cleaned_data['district']
     
            if len(subjects) > 3:
                form.add_error('subject', 'You cannot select more than 3 subjects.')
            if len(classins) > 3:
                form.add_error('classin', 'You cannot select more than 3 classin options.')

            if form.errors:
                return render(request, 'profile/teacher.html', {'form': form})

            obj.save()
            obj.subject.set(subjects)
            obj.classin.set(classins)

            other_profiles = TeacherProfile.objects.exclude(user=request.user).filter(district=district)
            for other_profile in other_profiles:
                subject_match = any(subject.name in other_profile.subject.values_list('name', flat=True) for subject in subjects)
                if subject_match and other_profile.category != category:
                    receiver = other_profile.user
                    notify.send(
                        request.user,
                        recipient=receiver,
                        verb=f"is searching for a {other_profile.category} like you.. <a href='/profile/otherprofile/{request.user.id }'>View Profile</a>"
                    )

            messages.success(request, 'Successfully created your profile')
            return redirect('view')
    else:
        form = TeacherProfileForm(instance=instance)

    return render(request, 'profile/teacher.html', {'form': form})



from .models import User
from Post.models import PostModel
def OTHERPROFILE(request,id):
    user=User.objects.get(id=id)
    return render(request,'profile/otherprofile.html',{'user':user})