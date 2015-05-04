import os, string
from bs4 import BeautifulSoup

def get_review_text(review_file):
    with open(review_file, 'r') as inf:
        soup = BeautifulSoup(inf)
    comment = soup.comment.text.encode('ascii', 'ignore')
    trans = comment.translate(string.maketrans("",""), string.punctuation)
    return trans + "\n"

directory = 'junel-reviews/'

with open("input.txt", "w") as outf:
    for review in os.listdir(directory):
        if not review.endswith("extents.xml"):
            outf.write(get_review_text(directory+review))
