import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from .exam_models import Chat

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for API
class ChatView(View):
    def get(self, request):
        # Retrieve all chat messages
        chats = Chat.objects.all()
        chat_data = [
            {
                "username": chat.username,
                "chat_message": chat.chat_message,
                "date": chat.date.isoformat()
            }
            for chat in chats
        ]
        return JsonResponse(chat_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)  # ✅ Parse JSON request body
            username = data.get("username")
            chat_message = data.get("chat_message")

            if not username or not chat_message:
                return JsonResponse({"error": "Username and message are required."}, status=400)

            # Create and save the new chat message
            new_chat = Chat.objects.create(username=username, chat_message=chat_message)
            chat_data = {
                "username": new_chat.username,
                "chat_message": new_chat.chat_message,
                "date": new_chat.date.isoformat()
            }
            return JsonResponse(chat_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)