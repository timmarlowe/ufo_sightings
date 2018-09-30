import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def split_entered(word):
    #word.split('Entered as: ', 1)[1]
    #word.split('Occurred :',1)[1]
    return word.split('(Entered as : ', 1)[0]

def split_occurred(word):
    return word.split('Occurred :')[1]

def split_reported(word):
    return word.split("Reported: ")[1]

def split_location(word):
    return word.split('Location:')[1]

def split_shape(word):
    try:
        return word.split('Shape:')[1]
    except IndexError:
        return word

def split_duration(word):
    try:
        return word.split('Duration:')[1]
    except IndexError:
        return word

def split_posted(word):
    try: 
        return word.split('Posted:')[1]
    except IndexError:
        return word

if __name__=='__main__':
    df = pd.read_pickle('ufo_db.pkl')
    df['Occurred'] = df['Occurred'].apply(split_occurred)
    df['Occurred'] = df['Occurred'].apply(split_entered)
    df['Reported'] = df['Reported'].apply(split_reported)
    df['Posted'] = df['Posted'].apply(split_posted)
    df['Location'] = df['Location'].apply(split_location)
    df['Shape'] = df['Shape'].apply(split_shape)
    df['Duration'] = df['Duration'].apply(split_duration)
