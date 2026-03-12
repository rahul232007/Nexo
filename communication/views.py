from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Room, Message
from django.contrib.auth.models import User

@login_required
def global_chat(request):
    room, created = Room.objects.get_or_create(name='Global', defaults={'description': 'Global chat for all NEXO users'})
    messages = room.messages.all()[:50]
    return render(request, 'communication/chat.html', {
        'room': room,
        'messages': messages
    })

@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, id=room_id)
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                room=room,
                user=request.user,
                content=content
            )
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.all()
    
    # Simple implementation: return all messages for now
    # In a real app, we would use filtering by timestamp or ID
    data = []
    for msg in messages:
        data.append({
            'user': msg.user.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'is_me': msg.user == request.user
        })
    return JsonResponse({'messages': data})
