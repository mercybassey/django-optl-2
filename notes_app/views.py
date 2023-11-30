from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from .metrics import request_count
from opentelemetry import trace
import logging

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

def increment_request_count(request):
    request_count.add(1, {"path": request.path, "http.method": request.method})

def note_list(request):
    increment_request_count(request)
    notes = Note.objects.all()
    return render(request, 'note_list.html', {'notes': notes})

def note_create(request):
    increment_request_count(request)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_create.html', {'form': form})

def note_update(request, pk):
    increment_request_count(request)
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_update.html', {'form': form})

def note_delete(request, pk):
    increment_request_count(request)
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'note_delete.html', {'note': note})

def note_detail(request, pk):
    increment_request_count(request)
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'note_detail.html', {'note': note})


