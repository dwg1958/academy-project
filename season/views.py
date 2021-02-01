from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Competitor

# Create your views here.
def tables(request):
#	textreceived = request.GET['fname']
    competitors = Competitor.objects
    return render(request, 'season/tables.html', {'competitors': competitors})

def tableformula(request, formula):

    # Go find drivers in this formula only
    if formula == "4":
        formula = "W"
        formulaname = "W Series"
    else:
        formulaname = "Formula " + formula

    competitors = Competitor.objects.filter(formula=formula, role="D")
    managers    = Competitor.objects.filter(formula=formula, role="M")

    ## Find personality dataset
    try:
        per = request.GET['per']
        pers_data = Competitor.objects.filter(surname=per)
        showPersonal = "show"
    except:
        pers_data = list(competitors[:1])
        showPersonal = " "

    #pers_data = get_object_or_404(Competitor,pk=11)
    #pers_data = get_list_or_404(Competitor,pk=per)

    #"pers_data": pers_data,

    return render(request, 'season/tables.html', {'personality':pers_data, 'competitors': competitors,'managers':managers,'formulaname':formulaname, 'formula':formula, 'showPersonal':showPersonal})
