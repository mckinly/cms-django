import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cms.models import Region, Language


def feedback_handler(func):
    @csrf_exempt
    def handle_feedback(request, region_slug, language_code):
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request."}, status=405)
        try:
            region = Region.objects.get(slug=region_slug)
            language = Language.objects.get(code=language_code)
        except Region.DoesNotExist:
            return JsonResponse(
                {"error": f'No region found with slug "{region_slug}"'}, status=404
            )
        except Language.DoesNotExist:
            return JsonResponse(
                {"error": f'No language found with code "{language_code}"'}, status=404
            )
        if request.content_type == "application/json":
            data = json.loads(request.body.decode())
        else:
            data = {}
            for key in request.POST:
                data[key] = request.POST.get(key)
        comment = data.pop("comment", "")
        rating = data.pop("rating", None)
        category = data.pop("category", None)

        if rating not in [None, "up", "down"]:
            return JsonResponse({"error": "Invalid rating."}, status=400)
        if comment == "" and not rating:
            return JsonResponse(
                {"error": "Either comment or rating is required."}, status=400
            )
        if rating == "up":
            emotion = "POS"
        elif rating == "down":
            emotion = "NEG"
        else:
            emotion = "NA"
        is_technical = category == "Technisches Feedback"
        return func(data, region, language, comment, emotion, is_technical)

    return handle_feedback
