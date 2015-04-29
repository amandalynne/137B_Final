#!/usr/bin/python
#compute the accuracy of an NE tagger

#usage: evaluate-head.py [gold_file][output_file]

import sys, re

if len(sys.argv) != 2:
    sys.exit("usage: evaluate-head.py [output_file]")

output = open(sys.argv[1], 'r')

gold_tag_list = []
test_tag_list = []

emptyline_pattern = re.compile(r'^\s*$')

gold_tags_for_line = []
test_tags_for_line = []

for line in output.readlines():
    if emptyline_pattern.match(line):
        pass
        #if len(gold_tags_for_line) > 0:
        #    gold_tag_list.append(gold_tags_for_line)
        #gold_words_for_line = []
    else:
        parts = line.split()
        gold_tags_for_line.append(parts[-1])
        test_tags_for_line.append(parts[-2])

#dealing with the last line
if len(gold_tags_for_line) > 0:
    gold_tag_list.append(gold_tags_for_line)

if len(test_tags_for_line) > 0:
    test_tag_list.append(test_tags_for_line)


test_total = 0
gold_total = 0
correct = 0

for i in range(len(gold_tag_list)):
    #print gold_tag_list[i]
    #print test_tag_list[i]
    for j in range(len(gold_tag_list[i])):
        if gold_tag_list[i][j] != 'O':
            gold_total += 1
        if test_tag_list[i][j] != 'O':
            test_total += 1
        if gold_tag_list[i][j] != 'O' and gold_tag_list[i][j] == test_tag_list[i][j]:
            correct += 1


precision = float(correct) / test_total
recall = float(correct) / gold_total
f = precision * recall * 2 / (precision + recall)

#print correct, gold_total, test_total
print 'p =', precision, 'r =', recall, 'f =', f
