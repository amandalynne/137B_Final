"""This is a script to pull out all the words in extents tagged as "SIDE EFFECT"
   from adjudicated, gold standard documents in our drug reviews corpus."""

import re, os, sys
from nltk.stem.snowball import SnowballStemmer
from xml.etree.ElementTree import ElementTree


def process_word(word):
    """Stem and lowercase the word"""
    stemmer = SnowballStemmer("english")
    return stemmer.stem(word.lower()) 
    #return word.lower()

def compile_side_effects(xml_file):
    """Given an annotated file, look for the SIDE EFFECT extents,
    remove punctuation, and add processed words to the set of side effect
    words."""
    tree = ElementTree().parse(xml_file)
    tags = tree.find('TAGS')
    for se in tags.findall('SIDE_EFFECT'):
        line = re.split("[-/ .,]", se.attrib['text'])
        for word in line:
            yield process_word(word)


def full_side_effect_set(directory):
    """Returns all the side effects from all files in a directory"""
    side_effect_set = set()
    text = ""
    for xml_file in os.listdir(directory):
        xml_file = directory+xml_file
        print xml_file
        if xml_file.endswith('extents.xml'):
            for word in compile_side_effects(xml_file):
                side_effect_set.add(word)
    for effect in side_effect_set:
        text += effect + " "
    return text
    

if __name__ == "__main__":
    directory = sys.argv[1]
    with open('side_effects.txt', 'w+') as outf:
        outf.write(full_side_effect_set(directory))       
