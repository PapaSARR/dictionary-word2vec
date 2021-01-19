from django.shortcuts import render
from .embeddings import Embedding
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
			model = Embedding('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\GoogleNews-vectors-negative300.bin.gz')
			responses = model.find_words(positive_words, negative_words, 'C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\words.txt')
			context = {'form':form, 'responses': responses}
		else:
			context = {'form': form}  
	return render(request, 'index.html', context)     
    
       
