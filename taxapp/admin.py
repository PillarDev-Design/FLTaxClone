# Enable Admin
from django.contrib import admin

# Import Models
from taxapp.models import County
from taxapp.models import Zip_Code
from taxapp.models import City

# Register Models
admin.site.register(County)
admin.site.register(Zip_Code)
admin.site.register(City)
