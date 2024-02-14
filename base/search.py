from .models import Activity, Tag 
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginateActivities(request, activities, results):
    page = request.GET.get('page')
    paginator = Paginator(activities, results)
    
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        activities = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        activities = paginator.page(page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, activities



def searchActivities(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)
     
    activities = Activity.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags) |
        Q(location__icontains=search_query) |
        Q(scheduled_date__icontains=search_query)

        )
    
    return activities, search_query