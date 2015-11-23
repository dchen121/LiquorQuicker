from django.contrib import admin
from .models import LiquorLocation, Review
from .parser import LocationParser

# Register your models here.
class LiquorLocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'city']}),
        ("Longitude/Latitude", {'fields': ['latitude', 'longitude', 'avg_rating'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'address', 'city', 'latitude', 'longitude', 'avg_rating')
    search_fields = ['name', 'address']
    actions = ['save_lat_long', 'load_data']

    def save_lat_long(self, request, queryset):
        count_success = 0
        count_failure = 0
        failure_string = ""
        for location in queryset:
            lat_lng = location.get_lat_long()
            if lat_lng:
                location.latitude = lat_lng['lat']
                location.longitude = lat_lng['lng']
                location.save()
                count_success = count_success + 1
            else:
                count_failure = count_failure + 1
                failure_string = failure_string + location.name + " (" + \
                                location.address + ", " + location.city + "), "
        if count_failure == 0:
            self.message_user(request, "%d locations were successfully updated." % count_success)
        else:
            message = "%d locations were successfully updated. " % count_success + \
                    "Geocoding could not be completed for %d locations: " % count_failure + \
                    failure_string
            self.message_user(request, message)
    save_lat_long.short_description = "Update location with latitude and longitude"

    def load_data(self, request, queryset):
        LocationParser()
    load_data.short_description = "Parse location data from csv and save it to the database"

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('store', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']
    
admin.site.register(LiquorLocation, LiquorLocationAdmin)
admin.site.register(Review, ReviewAdmin)
