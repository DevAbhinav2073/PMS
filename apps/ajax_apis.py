from django.http import JsonResponse

from apps.course.models import Stream


def get_faculty_according_to_level(request):
    academic_level_id = request.GET.get('academic_level_id', '')
    queryset = Stream.objects.all()
    if not academic_level_id == '':
        queryset = queryset.filter(level=academic_level_id)
        response = []

        for stream in queryset:
            response_dict = dict(
                display_text=stream.__str__()
                , value=stream.id
            )
            response.append(response_dict)
    print(response)
    return JsonResponse(response, safe=False)
