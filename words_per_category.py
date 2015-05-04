"""This is a script to pull out all the words in extents tagged as "SIDE EFFECT"
   from adjudicated, gold standard documents in our drug reviews corpus."""

import json, os, re, sys
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from xml.etree.ElementTree import ElementTree


def process_word(word):
    """Stem and lowercase the word"""
    stemmer = SnowballStemmer("english")
    return stemmer.stem(word.lower()) 

def list_of_categories(directory):
    """Returns a set of all the side effect categories in corpus"""
    cat_dict = defaultdict(set)
    for xml_file in os.listdir(directory):  
        if xml_file.endswith('extents.xml'):
            tree = ElementTree().parse(directory+xml_file)
            tags = tree.find('TAGS')
            for se in tags.findall('SIDE_EFFECT'):
                cat_dict[se.attrib['category']].update(process_word(word) for word in se.attrib['text'].split())
    for key in cat_dict.keys():
        cat_dict[key] = list(cat_dict[key])
    return cat_dict

if __name__ == "__main__":
    directory = sys.argv[1]
    with open('cat_dict.json', 'w') as outf: 
        json.dump(list_of_categories(directory), outf) 
