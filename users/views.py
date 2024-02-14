from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf 
from django.db.models import Q 
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .search import searchProfiles, paginateProfiles
from base.models import Activity 




def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
         
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR password is incorrect')
        
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles': profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile':profile,'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)



@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    activities = profile.activity_set.all()
    
    context = {'profile':profile, 'skills':skills, 'activities':activities}
    return render(request, 'users/account.html', context)



@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile 
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect('account')     
    
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


def deleteSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
    
    context = {'object':skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile 
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def viewMessage(request, pk):
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read = True 
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)



def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm
    try:
        sender = request.user.profile 
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient 
            #如果有sender，则还需要提取处name和email的信息，
            #因为在forms里面针对login user，只要求user填写了message.body & subject
            if sender:
                message.name = sender.name 
                message.email = sender.email 
            message.save()
            
            messages.success(request, 'Your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)
    
    
    context = {'recipient':recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


@login_required(login_url='login')
def registrationConfirmation(request, pk):
    activity = Activity.objects.get(id=pk)

    if request.method == 'POST':
        if request.user.profile in activity.participants.all():
            activity.participants.remove(request.user.profile)
            request.user.profile.registered_activities.remove(activity)
        else:
            activity.participants.add(request.user.profile)
            request.user.profile.registered_activities.add(activity)

        return redirect('activity', pk=activity.id)

    context = {'activity': activity}
    return render(request, 'users/activity_confirmation.html', context)


@login_required(login_url='login')
def registeredActivities(request):
    profile = request.user.profile 
    registered_activities = profile.registered_activities.all().order_by('-start_date')
    
    context = {'registered_activities': registered_activities, 'profile':profile}
    return render(request, 'users/registered_activities.html', context)
    




