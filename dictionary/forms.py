from django import forms
from django.forms.utils import ErrorList

class DictForm(forms.Form):
    definition = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Definition'}), required=True)

class ParagraphErrorList(ErrorList):
	def __str__(self):
	    return self.as_divs()
	def as_divs(self):
	    if not self: return ''
	    return ''.join(['%s' % e for e in self])