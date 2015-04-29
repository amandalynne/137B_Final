"""Extract features from files for CRF training format"""

import nltk, os, string, sys
from bs4 import BeautifulSoup
from itertools import izip
from xml.etree.ElementTree import ElementTree


def pairwise(iterable):
    """Helps iterate over pairs of items"""
    a = iter(iterable)
    return izip(a, a)

def extract_features_from_files(directory):
    """Extract features from corpus of files"""
    side_effect_list = []
    for annotated, raw in pairwise(os.listdir(directory)):
        if annotated.endswith('extents.xml'):
            annotated_tree = ElementTree().parse(directory+annotated)
            tags = annotated_tree.find('TAGS')
            for effect in tags.findall('SIDE_EFFECT'):
                print effect.attrib['text']
    



if __name__ == "__main__":
    directory = sys.argv[1]
    extract_features_from_files(directory)
