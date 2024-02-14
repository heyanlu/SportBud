from django.core import paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .models import Activity, Review
from .forms import ActivityForm, ReviewForm
from .search import searchActivities, paginateActivities

def activities(request):  
    activities, search_query = searchActivities(request)
    #custom_range is set to 6
    custom_range, activities = paginateActivities(request, activities, 6)
    
    context = {
        'activities': activities,
        'search_query': search_query,
        'custom_range':custom_range,
    }
    return render(request, 'base/activities.html', context)



def activity(request, pk):
    activityObj = Activity.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.activity = activityObj
            review.owner = request.user.profile
            review.save()
            
            activityObj.getVoteCount
            
            messages.success(request, 'Your review was successfully submitted!')
            return redirect('activity', pk=pk)
        else:
            messages.error(request, 'Invalid form data')
    
    context = {'activity':activityObj, 'form':form}
    return render(request, 'base/activity.html', context)


@login_required(login_url='login')
def createActivity(request):
    profile = request.user.profile
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.owner = profile
            activity.save()
            activity.signed_up_users.add(request.user)  # Add the creator to the signed-up users
            return redirect('account')
            
    context = {'form':form}
    return render(request, 'base/activity_form.html', context)


@login_required(login_url='login')
def updateActivity(request, pk):
    profile = request.user.profile
    activity = profile.activity_set.get(id=pk)
    form = ActivityForm(instance=activity)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('account')
            
    context = {'form':form}
    return render(request, 'base/activity_form.html', context)


@login_required(login_url='login')
def deleteActivity(request, pk):
    profile = request.user.profile
    activity = profile.activity_set.get(id=pk)
    
    if request.method == 'POST':
        activity.delete()
        return redirect('activities')
            
    context = {'object':activity}
    return render(request, 'delete_template.html', context)




