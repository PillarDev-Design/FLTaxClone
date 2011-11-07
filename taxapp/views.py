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

    # Initial opening of the page
    inital = True

    # Successful return of the zip code query
    zsuccess = False

    # Successful return of the county name query
    csuccess = False

    # Errors (Errors to return on an invalid query)
    errors = []

    # *** Begin logic on POST request ***
    if request.method == "POST":
        # qz (Query Zip) place holder
        qz = request.POST.get('zip_search')

        # Ensure 'zip_search' is not empty
        if not request.POST.get('zip_search', ''):
            errors.append('Enter a zip code.')
        # Ensure 'zip_search' is a 5 digit string
        elif len(qz) != 5:
            errors.append('Enter a valid 5 digit zip.')
        # If the zip code is 5 characters, then continue query
        if len(qz) == 5:
            # Find all matches with the 5 digit zip code
            zip_query = models.Zip_Code.objects.filter(zip_code__icontains=qz)
            # Set initial opening of the page to False
            initial = False
            # Set zip success query to True
            zsuccess = True
            # Set 'zip_search' variable to grab the actual query so we can
            #   return it with the response dictionary
            zip_search = request.POST.get('zip_search')
            # 
            response_dict = {'zip_query':zip_query, 'zsuccess':zsucces,
                    'initial':initial, 'csuccess':csuccess,
                    'zip_search':zip_search, 'zip_code':zip_code}
            return render_to_response('taxapp/home.html', response_dict,
                    context_instance=RequestContext(request))
        # Now we are done checking if anything is placed in the zip box,
        #   we will check to see if anything is in the county box.

        # Ensure 'county_search' is not empty
        if not request.POST.get('county_search', ''):
            errors.append('Enter a county.')
        # If the county box is not empty, then continue query
        else:
            # qc (Query County) place holder
            qc = request.POST.get('county_search')
            # Find all matches with the county query search
            county_query = models.County.objects.filter(name__icontains=qc)
            # Set initial opening of the page to False
            initial = False
            # Set county success query to True
            csuccess = True
            # Set 'county_search' variable to grab the actual query so we can
            #   return it with the response dictionary
            county_search = request.POST.get('county_search')

