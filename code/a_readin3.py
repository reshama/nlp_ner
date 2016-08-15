#------------------------------------------------------------------------------
# Description:   
# Project:       NLP - NER
# Date Updated:  08/13/2016
# Author:        Reshama
# Updated By:    Reshama
# Python:        version 2.7
# Input:         data/all.iob
# Output:        
# -----------------------------------------------------------------------------
# ner_list:  tweet_num, tweet_item, token, class
# want to add:  tweet_char
# -----------------------------------------------------------------------------
# include libraries
from nltk.util import ngrams
from collections import defaultdict
from pprint import pprint

# this is sample of raw data structure:
'''
RT    O
@PeterRabbitt    O
:    O
HAPPY    O
BIRTHDAY    O
TO    O
@DaDaDaphne    O
WISHIN    O
'''



def read_data(datafile, logp):
    """
    read in text file and return list with tweet number word number, token and class
    """
    with open(datafile, "r") as infile:
        ner_list = []
        tweet_num = 1
        tweet_word = 0
        for line in infile:
            # add a blank line at begining of file, so first tweet follows format
            # tweets are separated by a blank line
            #if tweet_num ==1 and tweet_word ==0:
            #    linetemp = "\n" + line
            #    line = linetemp
            
            # remove carriage return at end of line
            line=line.rstrip()

            # split line items that are separated by tab
            lineitems = line.split("\t")

            # if line is a space, indicates start of new tweet
            # increment tweet number count; reset tweet word count
            if line == '':
                tweet_num += 1
                tweet_word = 0
            else:
                tweet_word += 1
                token = lineitems[0]
                tclass1 = lineitems[1]

                # create array with tweet key (num, word) and token, class
                item = [tweet_num, tweet_word, token, tclass1]
                ner_list.append(item)
        if logp == 1:
            print 'ner_list: '
            print 'len(ner_list): ', len(ner_list)
            pprint(ner_list)
        return ner_list
    
# this is the full data
ner_list = read_data("../data/all.iob", 0)

# use data (some small subsets to test code)
#ner_list = read_data("../data/lines50.iob", 1)
#ner_list = read_data("../data/lines60.iob", 0)
#ner_list = read_data("../data/line350.iob", 0)



def add_class(datalist, logp):
    """
    add newly defined class.  Example:  mention, url, emoji
    """
    newlist = []
    # identify records with a change in class
    for item in datalist:
        change = 0
        token=item[2]
        # add class for twitter mention
        if token[0] == "@":
            tclass2 = "B-mention"
            change = 1
        elif token.startswith("http"):
            # Add a class for url links
            tclass2 = "B-url"
            change = 1
        else:
            tclass2 = item[3]
            change = 0

        # print any items where classes were changed, as a check
        if logp == 1:
            if change == 1:
                print "changed:   ", item
                
        item.append(tclass2)
        newlist.append(item)

    return newlist

ner_list_run2 = add_class(ner_list, 0)

#pprint(ner_list_run2)

def output_file(datalist, out_filename):
    """
    write out list to workable tsv file name so it can be tested
    """
    with open(out_filename, "w") as fh:
            for row in datalist:
                        fh.write(row[2] + "\t" + row[4] + "\n")


output_file(ner_list_run2, "../data_recoded/run2_recode_class.tsv")

# check that list length matches output file length

print "--------------------------------------"
print "length of list:  ", len(ner_list_run2)
print "--------------------------------------"

# wc -l *.tsv

def create_dict(datalist, logp):
    """
    put list in dictionary format in order to create ngrams
    """
    
    # initialize dictionaries
    d = defaultdict(list)
    dtweetword = defaultdict(list)
    dtweetword_class = defaultdict(list)
    dclass = defaultdict(list)
    

create_dict(ner_list_run2, 1)

def create_ngrams():
    return



'''       
# initialize dictionaries
d = defaultdict(list)
dtweetword = defaultdict(list)
dtweetword_class = defaultdict(list)
dclass = defaultdict(list)

# Fill in the entries one by one

for line in ner_list:
    #setkey = tuple((line[0], line[1], line[2], line[4], line[5]))
    #setkey = tuple(str(line[0]))
    setkey = tuple((line[0], line[1]))
    token = line[3]
    tclass1 = tuple((line[4], line[5]))
    #token_class = tuple((token, line[4], line[5]))
    token_class = list((token, line[4], line[5]))
    #print setkey, token_class
    d[setkey].append(line[3])
    dclass[setkey].append(tclass1)

    dtweet[str(line[0])].append(line[3])
    dtweetcl[str(line[0])].append(line[4])
    
    
#print "\nlen(d=dictionary): ", len(d)
#print "\nlen(dclass dict):  ", len(dclass)

print "\nlen(dtweet dict):  ", len(dtweet)
print "\nlen(dclass dict):  ", len(dtweetcl)


def printDict(dictname):
    for k, v in dictname.items():
        print k, v


print "------------------------------"
printDict(dtweet)
print "------------------------------"
printDict(dtweetcl)

print "------------------------------"
# tkey = tweet number 
# tvalue = each character of tweet
# ckey = tweet number
# cvalue = class

from itertools import izip
for (tkey, tvalue), (ckey, cvalue) in izip(dtweet.iteritems(), dtweetcl.iteritems()):
       tweet_length = sum(1 for v in tvalue if v)
       print "\ntweet_length: ", tweet_length
       print tkey
       print tvalue
       print ckey
       print cvalue
       for gramlength in range(3, tweet_length):
           gramitems = ngrams(tvalue, gramlength)

           for index, grams in enumerate(gramitems, start=0):
               #print "\ngrams: ", grams
               #print "\tclass: ", cvalue[index]

               gramsjoined = "".join(grams)
               #print "grams: ", gramsjoined
               
       print "\nmaximum-length gram: "
       print gramsjoined
       print cvalue[index]
'''