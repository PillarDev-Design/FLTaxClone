# Create your views here.
import models
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext

def home(request):
    county = models.County.objects.all()
    zip_code = models.Zip_Code.objects.all()
    city = models.City.objects.all()

    # Declare zip_query_final and county_query_final to be None
    #   to avoid an error. Without this, our response_dict would
    #   be returning a value that isn't in existence.
    actual_zip_request = None
    zip_query_final = None
    actual_county_request = None
    county_query_final = None
    city_result = None

    # Initial opening of the page
    page_initial_opening = True
    # Successful return of the zip code query
    zip_query_success = False
    # Successful return of the county name query
    county_query_success = False
    # Errors (Errors to return on an invalid query)
    errors = []

    # *** Begin logic on POST request ***
    if request.method == "POST":
        # Check to see if there is a zip_search in the POST request
        #   and assign it to 'actual_zip_request'
        actual_zip_request = request.POST.get('zip_search', None)

        # Check to see if the zip_search is empty
        if not request.POST.get('zip_search', ''):
            errors.append('Enter a zip code.')
        # Check to see if the 'actual_zip_request' is 5 characters long
        elif len(actual_zip_request) != 5:
            errors.append('Enter a valid 5 digit zip.')

        # If the zip code is 5 characters, then continue query
        if len(actual_zip_request) == 5:
            # Find all matches with the 5 digit zip code
            #   and assign the results to 'zip_query_final'
            zip_query_final = models.Zip_Code.objects.filter(zip_code__icontains=actual_zip_request)
            city_result = models.City.objects.filter(zip_code__icontains=actual_zip_request)
            
            # Set initial opening of the page to False
            page_initial_opening = False
            # Set success on return of zip code query
            zip_query_success = True
        
        # Now we are done checking if anything is placed in the zip box,
        #   we will check to see if anything is in the county box.
        
        # Check to see if there is a county_search in the POST request
        #   and assign it to 'actual_county_request'
        actual_county_request = request.POST.get('county_search', None)

        # Ensure 'county_search' is not empty
        if not request.POST.get('county_search', ''):
            errors.append('Enter a county.')

        # If the county box is not empty, then continue query
        else:
            # Find all matches with the actual county request
            #   and assign the results to 'county_query_final'
            county_query_final = models.County.objects.filter(name__icontains=actual_county_request)
            
            # Set initial opening of the page to False
            page_initial_opening = False
            # Set county success query to True
            county_query_success = True
    
    # The response dictionary will return all the values.
    # Without declaring the values in the beginning of the home request
    #   and seeing if the POST request has values in them, the response
    #   dictionary would return values that haven't been declared
    response_dict = {'page_initial_opening':page_initial_opening,
            'zip_query_success':zip_query_success,
            'county_query_success':county_query_success,
            'acutal_zip_request':actual_zip_request,
            'actual_county_request':actual_county_request,
            'zip_query_final':zip_query_final,
            'county_query_final':county_query_final,
            'city_result':city_result,
            'county':county, 'zip_code':zip_code, 'city':city}
    return render_to_response('taxapp/home.html', response_dict,
            context_instance=RequestContext(request))

# This view fuction does a get county call when the user clicks the
#   county feature on the vector layer map. It allows for the return
#   of the tax rate associated with the feature.

def get_county(request, county_name=None):
    if county_name is None:
        return HttpResponse('No County Provided')
    county_object = models.County.objects.filter(name__icontains=county_name)[0]
    tax_rate = county_object.tax_rate
    return HttpResponse(tax_rate)
