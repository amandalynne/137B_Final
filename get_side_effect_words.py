"""This is a script to pull out all the words in extents tagged as "SIDE EFFECT"
   from adjudicated, gold standard documents in our drug reviews corpus."""

import os, sys
from nltk.stem.snowball import SnowballStemmer
from xml.etree.ElementTree import Element Tree


def compile_side_effect_set(xml_file):
    """Given an annotated file, look for the SIDE EFFECT extents,
    stem the words, and add them to the set of side effect words."""
    tree = ElementTree().parse(xml_file)
    tags = tree.find('TAGS')
    for se in tags.findall('SIDE_EFFECT'):
        line = se.attrib['text'].split()

def 
    for xml_file in os.listdir(directory):
    



if __name__ == "__main__":
    directory = sys.argv[1]
       
