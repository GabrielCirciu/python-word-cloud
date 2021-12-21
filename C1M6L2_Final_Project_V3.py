get_ipython().system('pip install wordcloud')
get_ipython().system('pip install fileupload')
get_ipython().system('pip install ipywidgets')
get_ipython().system('jupyter nbextension install --py --user fileupload')
get_ipython().system('jupyter nbextension enable --py fileupload')

import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import sys

def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 **10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)

_upload()

def calculate_frequencies(file_contents):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my",
                           "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers",
                           "its", "they", "them", "their", "what", "which", "who", "whom", "this", "that", "am",
                           "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
                           "but", "at", "by", "with", "from", "here", "when", "where", "how", "all", "any", "both",
                           "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]

    lowercase_document = file_contents.lower()
    document_words = lowercase_document.split()
    final_document = []
    
    for word in document_words:
        valid = True
        word = word.strip(punctuations)
        if word.isalpha():
            for un_word in uninteresting_words:
                if word == un_word:
                    valid = False
        else:
            valid = False
        if valid:
            final_document.append(word)
    
    document_dictionary = {}
    for word in final_document:
        if document_dictionary.get(word) == None:
            document_dictionary[word] = 0
        document_dictionary[word] += 1
    
    wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(document_dictionary)
    return cloud.to_array()

myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation = 'nearest')
plt.axis('off')
plt.show()
