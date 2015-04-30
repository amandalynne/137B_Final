"""Extract features from files for CRF training format"""

import nltk, os, string, sys
from bs4 import BeautifulSoup
from itertools import izip
from nltk.stem.snowball import SnowballStemmer
from xml.etree.ElementTree import ElementTree

# Heh not sure what the right style is here
_stemmer = SnowballStemmer("english")

with open("side_effects.txt", 'r') as inf:
    _side_effects = set(inf.read().split())

def pairwise(iterable):
    """Helps iterate over pairs of items"""
    a = iter(iterable)
    return izip(a, a)

def parse_spans(spans):
    """Parses spans from MAE output"""
    start_end = spans.split("~")
    return int(start_end[0]), int(start_end[1])

def side_effect_stem(word):
    """Is the word in the list of side effects?"""
    #return '1' if _stemmer.stem(word.lower()) in _side_effects else '0'
    return '1' if word.lower() in _side_effects else '0'

def extract_features_from_files(directory, mode, filename):
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
                    start+=len(word)+1
            else:
                IOB_side_effects[(split[0], start, end)] = "B-"+tag
        
        with open(directory+raw) as inf:
            review = inf.read()
        soup = BeautifulSoup(directory+review)
        comment = soup.comment.text
        
        # Maneuvering to get correct offsets
        review_split = review.split("\n")
        number_of_newlines = 6
        
        offset = len(review_split[0]) + len(review_split[1]) +\
                 len(review_split[2]) + len(review_split[3]) +\
                 len(review_split[4]) + len(review_split[5]) +\
                 number_of_newlines + len("<comment>") + 1

 
        char_index = offset 
        untagged_offsets = []
        tokenized = []
        word = ''

        # Scan characters in comment
        for i in range(len(comment)):
            if i < (len(comment)-1): 
                if not comment[i].isspace():
                    if comment[i] in ('-:.') and not comment[i+1].isspace():
                        word+=comment[i]
                    elif comment[i] == "'" and comment[i+1] == 's':
                        tokenized.append(word)
                        untagged_offsets.append((word, char_index-len(word), char_index))
                        word = comment[i]
                    elif comment[i] in string.punctuation:
                        if comment[i+1].isspace() or comment[i+1] in string.punctuation:
                            tokenized.append(word)
                            untagged_offsets.append((word, char_index-len(word), char_index))
                            word = comment[i]
                        else:
                            word+=comment[i]
                    else:
                        word+=comment[i]
                else:
                    if word:
                        tokenized.append(word)
                        untagged_offsets.append((word, char_index-len(word), char_index))
                    word=''
                char_index+=1 
            else:
                if word:
                    tokenized.append(word)
                    untagged_offsets.append((word, char_index-len(word), char_index))
                    tokenized.append(comment[i])
                    untagged_offsets.append((comment[i], char_index+1, char_index+2))
                else:
                    word+=comment[i]
                    tokenized.append(word)
                    untagged_offsets.append((word, char_index-len(word), char_index))        

        pos_tagged = nltk.pos_tag(tokenized)


        with open(filename, 'ab') as outf:
            for triple, pair in zip(untagged_offsets, pos_tagged):
                elements = [triple[0], pair[1], side_effect_stem(triple[0])] 
                
                if triple in IOB_side_effects:
                    elements.append(IOB_side_effects[triple])
                    #outf.write(triple[0] +'\t'+pair[1]+'\t'+ IOB_side_effects[triple]+ '\n')
                else:
                    elements.append("O")
                    #outf.write(triple[0]+'\t'+pair[1]+'\t'+ "O"+'\n')
                outf.write('\t'.join(elements) + '\n')

if __name__ == "__main__":
    directory = sys.argv[1]
    mode = sys.argv[2]
    filename = sys.argv[3]
    extract_features_from_files(directory, mode, filename)
