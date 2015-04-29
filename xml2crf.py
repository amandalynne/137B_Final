"""Extract features from files for CRF training format"""

import nltk, os, string, sys
from bs4 import BeautifulSoup
from itertools import izip
from xml.etree.ElementTree import ElementTree


def pairwise(iterable):
    """Helps iterate over pairs of items"""
    a = iter(iterable)
    return izip(a, a)

def parse_spans(spans):
    """Parses spans from MAE output"""
    start_end = spans.split("~")
    return int(start_end[0]), int(start_end[1])


def extract_features_from_files(directory):
    """Extract features from corpus of files"""
    for annotated, raw in pairwise(os.listdir(directory)):
        side_effect_list = []
        if annotated.endswith('extents.xml'):
            annotated_tree = ElementTree().parse(directory+annotated)
            tags = annotated_tree.find('TAGS')
            for effect in tags.findall('SIDE_EFFECT'):
                text = effect.attrib['text']
                spans = effect.attrib['spans']
                start, end = parse_spans(spans)
                condition = effect.attrib['condition']
                category = effect.attrib['category']
                happened = effect.attrib['happened']
                
                side_effect_list.append(('SE', text, start, end)) 
        IOB_side_effects = {}
        for tag, text, start, end in side_effect_list:
            split = text.split()
            if len(split) > 1:
                IOB_side_effects[(split[0], start, start+len(split[0]))]="B-"+tag
                start+=len(split[0])+1
                for word in split[1:]:
                    IOB_side_effects[(word, start, start+len(word))]="I-"+tag
                    start+=len(word)
            else:
                IOB_side_effects[(split[0], start, end)] = "B-"+tag
        with open(directory+raw) as inf:
            review = inf.read()
        soup = BeautifulSoup(review)
        review_text = soup.comment.text
        
        char_index = 0
        untagged_offsets = []
        tokenized = []
        word = ''
        # THIS IS ALL WRONG ACK GOTTA FIX!

        for i in range(len(text)-1):
            if not text[i].isspace():
                if text[i] in ('-:.') and not text[i+1].isspace():
                    word+=text[i]
                elif text[i] == "'" and text[i+1] == 's':
                    tokenized.append(word)
                    untagged_offsets.append((word, char_index-(len(word)), char_index))
                elif text[i] in string.punctuation:
                    if text[i+1].isspace() or text[i+1] in string.punctuation:
                        tokenized.append(word)
                        untagged_offsets.append((word, char_index-(len(word)), char_index))
                        word = text[i]
                else:
                    word+=text[i]
            else:
                if word:
                    tokenized.append(word)
                    untagged_offsets.append((word, char_index-(len(word)), char_index))
                word=''
                char_index+=1

        print untagged_offsets
          



if __name__ == "__main__":
    directory = sys.argv[1]
    extract_features_from_files(directory)
