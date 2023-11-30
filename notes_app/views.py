from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
import time
from .metrics import response_times
from opentelemetry import trace
import logging

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

def note_list(request):
    start_time = time.time()
    with tracer.start_as_current_span("note_list") as span:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        notes = Note.objects.all()
        elapsed_time = time.time() - start_time
        response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
        return render(request, 'note_list.html', {'notes': notes})

def note_create(request):
    start_time = time.time()
    with tracer.start_as_current_span("note_create") as span:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        if request.method == "POST":
            form = NoteForm(request.POST)
            if form.is_valid():
                form.save()
                elapsed_time = time.time() - start_time
                response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
                return redirect('note_list')
        else:
            form = NoteForm()
        elapsed_time = time.time() - start_time
        response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
        return render(request, 'note_create.html', {'form': form})

def note_update(request, pk):
    start_time = time.time()
    with tracer.start_as_current_span("note_update") as span:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        note = get_object_or_404(Note, pk=pk)
        if request.method == "POST":
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                elapsed_time = time.time() - start_time
                response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
                return redirect('note_list')
        else:
            form = NoteForm(instance=note)
        elapsed_time = time.time() - start_time
        response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
        return render(request, 'note_update.html', {'form': form})

def note_delete(request, pk):
    start_time = time.time()
    with tracer.start_as_current_span("note_delete") as span:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        note = get_object_or_404(Note, pk=pk)
        if request.method == "POST":
            note.delete()
            elapsed_time = time.time() - start_time
            response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
            return redirect('note_list')
        elapsed_time = time.time() - start_time
        response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
        return render(request, 'note_delete.html', {'note': note})

def note_detail(request, pk):
    start_time = time.time()
    with tracer.start_as_current_span("note_detail") as span:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        note = get_object_or_404(Note, pk=pk)
        elapsed_time = time.time() - start_time
        response_times.record(elapsed_time, {"http.method": request.method, "trace_id": trace_id, "span_id": span_id})
        return render(request, 'note_detail.html', {'note': note})

