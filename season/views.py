from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Competitor

# Create your views here.
def tables(request):
#	textreceived = request.GET['fname']
    competitors = Competitor.objects
    return render(request, 'season/tables.html', {'competitors': competitors})
