from pathlib import Path
import gensim
from gensim.models import KeyedVectors

def determine_words(definition): 
    load_model()        
    possible_words = definition.split()
    for i in range(len(possible_words) - 1, -1, -1):
        if possible_words[i] not in model.vocab:                    
            del possible_words[i]          

    possible_expressions = []
    for w in [possible_words[i:i+3] for i in range(len(possible_words)-3+1)]:        
       possible_expressions.append('_'.join(w))            

    ex_to_remove = []

    for i in range(len(possible_expressions)):        
        if possible_expressions[i] in model.vocab:                    
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
    
def find_words(definition, negative_definition):          
    positive_words = determine_words(definition)
    negative_words = determine_words(negative_definition)
     # read dictionary words
    dict_words = []
    f = open('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\words.txt', "r")
    for line in f:
        dict_words.append(line.strip())    
    f.close()    
    # remove copyright notice    
    dict_words = dict_words[44:] 

    similar_words = [i[0] for i in model.most_similar(positive=positive_words, negative=negative_words, topn=30)]  

    words = []    

    for word in similar_words:
        if (word in dict_words):
            words.append(word)

    if (len(words) > 20):
        words = words[0:20]
    
    return words



def generate_optimized_version():
    model = KeyedVectors.load_word2vec_format('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\GoogleNews-vectors-negative300.bin.gz', binary=True)
    model.init_sims(replace=True)
    model.save('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\GoogleNews-vectors-gensim-normed.bin')

def load_model():
    global model
    # Load Google's pre-trained Word2Vec model. 
    optimized_file = Path('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\GoogleNews-vectors-gensim-normed.bin')
    if optimized_file.is_file():        
        model = KeyedVectors.load('C:\home\Desktop\djangoProjects\dictionary_word2vec\dictionary\models\GoogleNews-vectors-gensim-normed.bin',mmap='r')
    else:
        generate_optimized_version()
    # keep everything ready    
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
