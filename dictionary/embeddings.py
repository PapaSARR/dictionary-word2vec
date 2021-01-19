from pathlib import Path
import gensim
from gensim.models import KeyedVectors

class Embedding:

	#Constructor: Loading data for attribut model initialisation
	def __init__(self, path):	
		self.model = KeyedVectors.load_word2vec_format(path, binary=True)
		self.model.init_sims(replace=True)   
		self.model.syn0norm = self.model.syn0 

	#Cleaning input string by generating a list of words from the input definition
	def determine_words(self, definition):       
		possible_words = definition.split()
		for i in range(len(possible_words) - 1, -1, -1):
			if possible_words[i] not in self.model.vocab:                    
				del possible_words[i]          

		possible_expressions = []
		for w in [possible_words[i:i+3] for i in range(len(possible_words)-3+1)]:        
		   possible_expressions.append('_'.join(w))            

		ex_to_remove = []

		for i in range(len(possible_expressions)):        
		    if possible_expressions[i] in self.model.vocab:                    
		        ex_to_remove.append(i)        

		words_to_remove = []    
		for i in ex_to_remove:
		    words_to_remove += [i, i+1, i+2]        
		words_to_remove = sorted(set(words_to_remove))    

		words = [possible_expressions[i] for i in ex_to_remove]    
		for i in range(len(possible_words)):
		    if i not in words_to_remove:
		        words.append(possible_words[i])    

		return words

	#Return list of words related to the input definition
	def find_words(self, definition, negative_definition, path_filter):          
	    positive_words = self.determine_words(definition)
	    negative_words = self.determine_words(negative_definition)
	     # read dictionary words
	    dict_words = []
	    f = open(path_filter, "r")
	    for line in f:
	        dict_words.append(line.strip())    
	    f.close()    
	    # remove copyright notice    
	    dict_words = dict_words[44:] 

	    similar_words = [i[0] for i in self.model.most_similar(positive=positive_words, negative=negative_words, topn=30)]  

	    words = []

	    #Filter returned words list by keeping only those which exist in the word.txt file
	    for word in similar_words:
	        if (word in dict_words):
	            words.append(word)

	    if (len(words) > 20):
	        words = words[0:20]
	    
	    return words

