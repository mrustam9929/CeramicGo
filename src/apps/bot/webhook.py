import json
import logging

import telebot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.bot.handlers import bot


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            bot.process_new_updates([telebot.types.Update.de_json(json_data)])
        except Exception as e:
            logging.error(e)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)
