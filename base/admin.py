from django.contrib import admin
from .models import Activity, Review, Tag, Submission 

admin.site.register(Activity)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Submission)