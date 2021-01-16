from django.shortcuts import render
from . import dictionary
from .forms import DictForm, ParagraphErrorList
from .dictionary import find_words
# Create your views here.

def home(request):
	if request.method == 'GET':
		form = DictForm()
		context = {'form': form}
	else:
		form = DictForm(request.POST,  error_class=ParagraphErrorList)
		if form.is_valid():
			words = form.cleaned_data['definition'].split()
			#words = definition.split()
			negative_words = ''
			positive_words = ''
			for i in range(len(words)):
				if(words[i][0] == '-'):                
				    negative_words += words[i][1:] + ' '                
				else:                
				    positive_words += words[i] + ' '    
	        
			responses = find_words(positive_words, negative_words)
			context = {'form':form, 'responses': responses}
		else:
			context = {'form': form}  
	return render(request, 'index.html', context)     
    
       
