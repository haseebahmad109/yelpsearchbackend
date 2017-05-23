# Create your views here.

from django.views import View
from django.db import transaction
from .serializers import BusinessSerializer
from django.conf import settings
from .models import Business

from .yelp_api import search

from django.http import JsonResponse

class SearchResults(View):

    @transaction.atomic
    def process_business_items(self, yelp_business_list):
        db_objects = []
        for business_obj in yelp_business_list:
            defaults = {
                'name': business_obj.get('name', ""),
                'logo': business_obj.get('image_url', ""),
                'phone_number': business_obj.get('phone', ""),
                'url': business_obj.get('url', ""),
                'address': " ".join(business_obj.get('location', {}).get('display_address', []))
            }
            obj, created = Business.objects.update_or_create(business_id=business_obj['id'], defaults=defaults)
            db_objects.append(obj)
        return db_objects

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('term', "")
        location = request.GET.get('location', "")
        page = int(request.GET.get('page', 1))
        
        businesses = []
        search_results = {}
        if search_term and location:
            search_results = search(search_term, location, page)
            if search_results.get('error', False):
                return JsonResponse({
                    'error': search_results.get('error', {}).get('description', "Something Went Wrong")
                }, status=400)
            businesses = self.process_business_items(search_results.get('businesses', []) or [])

        serializer = BusinessSerializer(businesses, many=True)
        return JsonResponse({
            'page_size': settings.YELP_SEARCH_LIMIT,
            'total': search_results.get('total', 0),
            'results': serializer.data
        }, safe=False)

