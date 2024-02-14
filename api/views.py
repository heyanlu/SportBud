from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ActivitySerializer
from base.models import Activity, Review, Tag
from django.http import JsonResponse


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/activities'},
        {'GET': '/api/activities/id'},
        {'POST': '/api/activities/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def getActivities(request):
    activities = Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getActivity(request, pk):
    activity = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(activity, many=False)
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def activityVote(request, pk):
#     activity = Activity.objects.get(id=pk)
#     user = request.user.profile
#     data = request.data

#     review, created = Review.objects.get_or_create(
#         owner=user,
#         activity=activity,
#     )

#     review.value = data['value']
#     review.save()
#     activity.getVoteCount

#     serializer = ActivitySerializer(activity, many=False)
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def removeTag(request):
#     tagId = request.data['tag']
#     activityId = request.data['activity']

#     activity = Activity.objects.get(id=activityId)
#     tag = Tag.objects.get(id=tagId)

#     activity.tags.remove(tag)

#     return Response('Tag was deleted!')