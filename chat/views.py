from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from electricity.models import Location
from django.contrib.auth.models import User


def index(request):
    username = request.user.username
    obj = Location.objects.filter(user=username).first()
    print(obj.area)

    values = {
        'area': obj.area,
        'city': obj.city
    }

    return render(request, 'chat/index.html', values)


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
