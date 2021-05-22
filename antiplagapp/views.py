from .models import Document
from django.shortcuts import render, redirect
import difflib

from antiplagapp.forms import DocumentForm


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            last_file = form.save()
            open_last_file = last_file.document.readlines()
            files = Document.objects.exclude(pk=last_file.pk)

            open_list = []
            for file in files:
                matcher = difflib.SequenceMatcher(None, open_last_file, file.document.readlines()).ratio()*100
                open_list.append(matcher)
            
            if len(open_list) < 1:
                return render(request, 'antiplagapp/index.html', {'form': form})
            else:
                result = float(100) - round((sum(open_list) / len(open_list)), 2)
                context = {'result': result}
                return render(request, 'antiplagapp/result.html', context)
    else:
        form = DocumentForm()
    return render(request, 'antiplagapp/index.html', {'form': form})



def result(request):
    return render(request, 'antiplagapp/result.html')
