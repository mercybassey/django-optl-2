from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

# Tracing
from opentelemetry import trace
# from opentelemetry.instrumentation.django import DjangoInstrumentor

tracer = trace.get_tracer(__name__)


def note_list(request):
    with tracer.start_as_current_span("note_list"):
        notes = Note.objects.all()
        return render(request, 'note_list.html', {'notes': notes})

def note_create(request):
    with tracer.start_as_current_span("note_create"):
        if request.method == "POST":
            form = NoteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('note_list')
        else:
            form = NoteForm()
        return render(request, 'note_create.html', {'form': form})

def note_update(request, pk):
    with tracer.start_as_current_span("note_update"):
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
    with tracer.start_as_current_span("note_delete"):
        note = get_object_or_404(Note, pk=pk)
        if request.method == "POST":
            note.delete()
            return redirect('note_list')
        return render(request, 'note_delete.html', {'note': note})

def note_detail(request, pk):
    with tracer.start_as_current_span("note_detail"):
        notes = get_object_or_404(Note, pk=pk)
        return render(request, 'note_detail.html', {'notes': notes})



