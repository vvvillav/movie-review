from django.http import HttpResponse
from .schema import schema
def index(request):
    return HttpResponse("Hola, mundo. Estás en el índice de movies.")
