# -*- coding: utf-8 -*-
"""
Created on Sat May  7 19:11:37 2022

@author: BORDA
"""
# Importaciones
import re, string, unicodedata
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import hstack


# Funcion para remover caracteres no ASCII
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

# Funcion para pasar todas las palabras a minuscula
def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

#Funcion para quitar los signos de puntuacion
def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

#Funcion para reemplazar los numeros a representacion en palabras
def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

#Remover los articulos, preposiciones, etc.
def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

#Hacer preprocesamiento con stemming
def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

#Pasar de lista a texto separado por espacio
def list_to_text(words):
    new_words=''
    for word in words:
        new_words += word + ' '
    new_words=new_words.strip()
    return new_words
            
#Funcion auxiliar para realizar el preprocesamiento 
def preprocessing(words):
    words = to_lowercase(words)
    words = replace_numbers(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    words = remove_stopwords(words)
    return words

#Función que realiza preprocesamiento de columnas
def column_preprocessing(column_df):
    name=column_df.columns[0]
    column_df[name]=column_df[name].apply(contractions.fix)
    column_df[name]=column_df[name].apply(word_tokenize).apply(preprocessing)
    column_df[name]=column_df[name].apply(stem_words)
    column_df[name]=column_df[name].apply(list_to_text)
    column_df[name]=column_df[name].astype(str)
    return column_df
    
#Vectorizar datos
def vectorize_column(column1, column2):
    print(column1, column2, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    vectorizer=TfidfVectorizer()
    x_v1 = vectorizer.fit_transform(column1.tolist())
    x_v2 = vectorizer.fit_transform(column2.tolist())
    X = hstack((x_v1, x_v2))
    return X




