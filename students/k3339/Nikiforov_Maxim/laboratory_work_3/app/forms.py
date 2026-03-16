from django import forms
from .models import ReadingRoom, Reader, Book, BookCopy, BookAssignment


class ReadingRoomForm(forms.ModelForm):
    class Meta:
        model = ReadingRoom
        fields = ['number', 'name', 'capacity']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = [
            'ticket_number', 'full_name', 'passport_number', 'birth_date',
            'address', 'phone_number', 'education', 'has_degree', 'reading_room'
        ]
        widgets = {
            'ticket_number': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'has_degree': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reading_room': forms.Select(attrs={'class': 'form-control'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'publisher', 'publication_year', 'section', 'code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'reading_room', 'quantity']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'reading_room': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class BookAssignmentForm(forms.ModelForm):
    class Meta:
        model = BookAssignment
        fields = ['book', 'reader']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'reader': forms.Select(attrs={'class': 'form-control'}),
        }
