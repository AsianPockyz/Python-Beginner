import os
import re
import string
import random

from Graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, 'r') as f:
        text = f.read()

        # remove [text]
        text = re.sub(r'\[(.+)\]', ' ', text)

        text = ' '.join(text.split()) # turn all whitespace/tabs etc. into a single space
        text = text.lower() # make everything lowercase to be able to compare easily

        # now dealing with the complexity of punctuation
        # but let's remove it to not deal with it
        text = text.translate(str.maketrans('','', string.punctuation))
    words = text.split() # split spaces again

    return words

def make_graph(words):
    g = Graph()
    previous_word = None

    # for each word in words, check that the word is in the graph and if not add it
    # if there was a previous word, then add an edge if it does not already exist
    # in the graph, otherwise increment the weight by 1
    # set our word to the previous word, and iterate
    # remember that we want to generate the probability mappings before composing
    # and this would be the ideal place to do it before the graph object get's returned
    for word in words:
        word_vertex = g.get_vertex(word)
        if previous_word:
            previous_word.increment_edge(word_vertex)
        previous_word = word_vertex
    g.generate_probability_mappings()

    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words)) # pick a random word to start from
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)
    
    return composition

def main(artist):
    # What is being accomplished here
    # setp 1: get words from text
    
    #words = get_words_from_text("/texts/hp_sorcerer_stone.txt") # change directory to suit your device
    words = []
    for song_file in os.listdir(f'/songs/{artist}'): # change directory to suit your device
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'/songs/{artist}/{song_file}') # change directory to suit your device
        words.extend(song_words)

    # step 2: make a graph using those words
    g = make_graph(words)
    # step 3: get the next word for x number of words (defined by user)
    composition = compose(g, words, 100)
    return ' '.join(composition) # returns a string, where all the words are separated by a space
    # step 4: show the user


if __name__ == '__main__':
    print(main('drake'))
    
