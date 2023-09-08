from django.shortcuts import render, redirect
from .models import Notes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def add_notes(request):
    if request.method == 'POST':
        notes_text = request.POST.get('notes_text') 

        if notes_text:
            note = Notes.objects.create(notes_text=notes_text)

            return JsonResponse({'notes_text_rendered': note.notes_text, 'created_date': note.created_date.strftime("%Y-%m-%d %H:%M:%S")})

    notes = Notes.objects.all()

    return render(request, 'add_notes.html', {'notes': notes})



def get_notes(request):
    notes = Notes.objects.all()
    notes_list = [{'id': note.id, 'notes_text': note.notes_text, 'created_date': note.created_date} for note in notes]
    return JsonResponse({'notes': notes_list})


def delete_note(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')

        try:
            note = Notes.objects.get(pk=note_id)
            note.delete()
            return JsonResponse({'success': True})
        except Notes.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Note not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def edit_notes(request, note_id):
    if request.method == 'POST':
        note_text = request.POST.get('notes_text', '')

        try:
            note = Notes.objects.get(id=note_id)
            note.notes_text = note_text
            note.save()

            return JsonResponse({
                'note_id': note.id,
                'notes_text_rendered': note.notes_text,
                'created_date': note.created_date.strftime("%Y-%m-%d %H:%M:%S")
            })
        except Notes.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'})