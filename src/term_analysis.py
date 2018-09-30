import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    ufo = pd.read_pickle('../data/ufo_db.pkl')
    ufo['Occurred'] = ufo['Occurred'].apply(split_occurred)
    ufo['Occurred'] = ufo['Occurred'].apply(split_entered)
    ufo['Reported'] = ufo['Reported'].apply(split_reported)
    ufo['Posted'] = ufo['Posted'].apply(split_posted)
    ufo['Location'] = ufo['Location'].apply(split_location)
    ufo['Shape'] = ufo['Shape'].apply(split_shape)
    ufo['Duration'] = ufo['Duration'].apply(split_duration)

    mpl.rcParams.update({
        'font.size'           : 14.0,
        'axes.titlesize'      : 'large',
        'axes.labelsize'      : 'medium',
        'xtick.labelsize'     : 'xx-small',
        'ytick.labelsize'     : 'small',
        'legend.fontsize'     : 'large',
    })
    #Graph Statecount
    ufo['State']=ufo['Location'].apply(lambda x: x[-2:])
    ufo = ufo[ufo['State'] != '),']
    state_count = ufo.groupby('State').agg('count')
    state_count = state_count[state_count['Occurred']>200]
    state_count.sort_values('Occurred',ascending=False, inplace=True)
    x = state_count.index.values
    fig, ax = plt.subplots(1,1, figsize=(16,8))
    ax.bar(x,state_count['Occurred'])
    ax.set_xlabel('States/Provinces')
    ax.set_ylabel('Number of Sightings')
    # plt.show()
    plt.title('States with UFO Sightings')
    plt.savefig('../images/state_count_ufos.png')
    plt.close()

    mpl.rcParams.update({
        'font.size'           : 16.0,})

    #Graph
    shape_count = ufo.groupby('Shape').agg('count')
    shape_count = shape_count[shape_count['Occurred']>500]
    shape_count.sort_values('Occurred',ascending=False, inplace=True)
    x = shape_count.index.values
    fig2, ax2 = plt.subplots(1,1, figsize=(16,8))
    ax2.bar(x,shape_count['Occurred'])
    ax2.set_xlabel('Shape of UFO')
    ax2.set_ylabel('Number of Sightings')
    # plt.show()
    plt.title('Shapes of UFOs')
    plt.savefig('../images/shape_count_ufos.png')
    plt.close()

    mpl.rcParams.update({
        'font.size'           : 16.0,
        'xtick.labelsize'     : 'small',})

    #Hour of Day
    ufo['Hour']=ufo['Reported'].apply(lambda x: x[-5:-3])
    hour_count = ufo.groupby('Hour').agg('count')
    hour_count = hour_count[hour_count['Occurred']>500]
    # hour_count.sort_values('Occurred',ascending=False, inplace=True)
    x = hour_count.index.values
    fig3, ax3 = plt.subplots(1,1, figsize=(16,8))
    ax3.plot(x,hour_count['Occurred'])
    ax3.set_xlabel('Hour of UFO Sighting')
    ax3.set_ylabel('Number of Sightings')
    # plt.show()
    plt.title('Hours when UFOs Were Sighted')
    plt.savefig('../images/hour_count_ufos.png')
    plt.close()

    #Date
    ufo['Date']=ufo['Reported'].apply(lambda x: x.split(' ')[0])
    ufo['Year']=ufo['Date'].apply(lambda x: x[-4:])
    year_count = ufo.groupby('Year').agg('count')
    year_count = year_count[year_count['Occurred']>500]
    # hour_count.sort_values('Occurred',ascending=False, inplace=True)
    x = year_count.index.values
    fig4, ax4 = plt.subplots(1,1, figsize=(16,8))
    ax4.plot(x,year_count['Occurred'])
    ax4.set_xlabel('Year of UFO Sighting')
    ax4.set_ylabel('Number of Sightings')
    # plt.show()
    plt.title('Years when UFOs Were Sighted')
    plt.savefig('../images/year_count_ufos.png')
    plt.close()
