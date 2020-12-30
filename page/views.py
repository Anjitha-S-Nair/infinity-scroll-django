from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,Http404
import json
from infinite_scroll_pagination import paginator
from infinite_scroll_pagination import serializers
from.models import Notification


def infinity(request, count):
    for i in range(count):
        title = get_random_string(100)
        description = get_random_string(200)
        Notification.objects.create(title=title, description=description)

    return HttpResponse('success')
    
def view_page(request):
    # obj = Notification.objects.all()
    # print (obj)
    template_name = 'view_page.html'
    # context = {"objects":obj}
    return render(request,template_name)


 
def notification_ajax(request):
    # if not request.is_ajax():
    #     return Http404()

    try:
        value, pk = serializers.page_key(request.GET.get('p', ''))
    except serializers.InvalidPage:
        return Http404()

    try:
        page = paginator.paginate(
            query_set=Notification.objects.all(),
            lookup_field='-created_at',
            value=value,
            pk=pk,
            per_page=20,
            move_to=paginator.NEXT_PAGE)
    except paginator.EmptyPage:
        data = {'error': "this page is empty"}
    else:

        data = {
            'notification': [{
                'title': notification.title, 
                'description': notification.description
                } for notification in page],
            'has_next': page.has_next(),
            'has_prev': page.has_previous(),
            'next_objects_left': page.next_objects_left(limit=100),
            'prev_objects_left': page.prev_objects_left(limit=100),
            'next_pages_left': page.next_pages_left(limit=100),
            'prev_pages_left': page.prev_pages_left(limit=100),
            'next_page': serializers.to_page_key(**page.next_page()),
            'prev_page': serializers.to_page_key(**page.prev_page())}

    return HttpResponse(json.dumps(data), content_type="application/json")


    