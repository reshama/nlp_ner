#------------------------------------------------------------------------------
# Description:   
# Project:       NLP - NER
# Date Updated:  09/03/2016
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
from itertools import izip
import re

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
    read in text file and returns 2 lists (one by char, one by word)
       with tweet number word number, token and class
    """
    with open(datafile, "r") as infile:
        ner_list = []
        ner_word_list = []
        tweet_num = 1
        tweet_word = 0
        tweet_item = 0
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

                # break each word by each character
                for char in token:
                    # create array with tweet key (num, word) and token, class
                    item = [tweet_num, tweet_word, token, char, tclass1]
                    ner_list.append(item)
            #print tweet_num, tweet_word, token, tclass1
            item_word_list = [tweet_num, tweet_word, token, tclass1]
            ner_word_list.append(item_word_list)
        if logp == 1:
            print 'ner_list: '
            print 'len(ner_list): ', len(ner_list)
            pprint(ner_list[0:10])
            print '\nner_word_list: '
            print 'len(ner_word_list): ', len(ner_word_list)
            pprint(ner_word_list[0:10])
        return ner_list, ner_word_list
    
# this is the full data
#ner_list = read_data("../data/all.iob", 0)

# this is what ner_list looks like
'''
ner_list: 
len(ner_list):  221
[[1, 0, 'RT', 'R', 'O'],
 [1, 0, 'RT', 'T', 'O'],
 [1, 0, '@PeterRabbitt', '@', 'O'],
 [1, 0, '@PeterRabbitt', 'P', 'O'],
 [1, 0, '@PeterRabbitt', 'e', 'O'],
 [1, 0, '@PeterRabbitt', 't', 'O'],
 [1, 0, '@PeterRabbitt', 'e', 'O'],
'''

# this is what ner_word_list looks like
'''
ner_word_list: 
len(ner_word_list):  50
[[1, 1, 'RT', 'O'],
 [1, 2, '@PeterRabbitt', 'O'],
 [1, 3, ':', 'O'],
 [1, 4, 'HAPPY', 'O'],
 [1, 5, 'BIRTHDAY', 'O'],
 [1, 6, 'TO', 'O'],
 [1, 7, '@DaDaDaphne', 'O'],
 [1, 8, 'WISHIN', 'O'],
 [1, 9, 'YOU', 'O'],
 [1, 10, 'THE', 'O']]
'''


def add_class(datalist, tclass1_loc, logp):
    """
    add newly defined class.  Example:  mention, url
    tclass1_loc = token location in array of original class, depends on structure of list
    """
    newlist = []
    changect = 0
    extra_url = 0  # urls that have .com, .en, org (don't begin with http)
    # identify records with a change in class
    for item in datalist:
        change = 0
        token=item[2]

        # check for urls in token
        url_http_start = token.startswith("http")

        pattern = re.compile(r'([^\/]*\.(?:com|en|org|edu|net|gov|biz|info|me|co))')
        url_domain_end = pattern.search(token)

        if not url_http_start and url_domain_end:
            print item
        # add class for twitter mention
        if token[0] == "@":
            tclass2 = "B-mention"
            changect += 1
            change = 1
        elif url_http_start or url_domain_end:
            # Add a class for url links
            tclass2 = "B-url"
            changect += 1
            change = 1
            if not url_http_start and url_domain_end:
                extra_url += 1
                #print extra_url, token
        else:
            tclass2 = item[tclass1_loc]
            change = 0

        # print any items where classes were changed, as a check
        if logp == 1:
            if change == 1:
                print "changed:   ", item

        item.append(tclass2)
        newlist.append(item)
        
    print "--------------------------------------"
    print "number of changes:  ", changect
    print "newlist (with updated classes) "
    pprint(newlist[0:10])
    print "--------------------------------------"
    print "extra_url (don't begin with 'http'): ", extra_url
    return newlist


def output_file(datalist, out_filename):
    """
    write out list to workable tsv file name so it can be tested
    """
    with open(out_filename, "w") as fh:
            for row in datalist:
                # add a blank line before each tweet
                if row[1]==1:
                    fh.write("\n" + row[2] + "\t" + row[4] + "\n")
                else:
                    fh.write(row[2] + "\t" + row[4] + "\n")
                    
def output_file2(datalist, out_filename):
    """
    write out list to workable tsv file name so it can be tested
    """
    current = 1
    with open(out_filename, "w") as fh:
            for row in datalist:
                if row[0] != current:
                    fh.write("\n")
                    current = row[0]
                # add a blank line before each tweet
                if row[0]==1:
                    fh.write("\n" + row[2] + "\t" + row[3] + "\n")
                else:
                    fh.write(row[2] + "\t" + row[3] + "\n")



# Note:  in original data file, the first line is not blank, but the last line is.
# check that list length matches output file length

# check number of lines in file
# wc -l *.tsv

# check that blank space has been added between tweets
# head -20 run2_recode_class.tsv

# remove first line in file
# tail -n +2 run2_recode_class.tsv > run2_recode_class_clean.tsv 


def create_dict(datalist, whichclass, logp):
    """
    put list in dictionary format in order to create ngrams
    logp = log print = print data for trouble-shooting
    """    
    # initialize dictionary
    dicttweet = defaultdict(list)

    linect = 0
    # Fill in the entries one by one
    for line in datalist:
        linect += 1
        setkey = tuple((line[0], line[1]))
        token = line[3]
        
        #if logp == 1:
        #    print setkey, token_class

        dicttweet[str(line[0])].append(line[whichclass])

        #print setkey

        if logp == 1:
            #print line
            if linect == 250:
                #pprint(dicttweet)
                print "len(dictionary): ", len(dicttweet)
                for k, v in dicttweet.items():
                    print "-"*10
                    print k, v

    return dicttweet

#----------------------------------------------
#  print dictionary
#----------------------------------------------

def printDict(dictname):
    print"\n------------------------------"
    print "len(dictionary): ", len(dictname)
    for k, v in dictname.items():
        print k, v

#printDict(d_bychar_char)
#printDict(d_bychar_tclass1)
#printDict(d_bychar_tclass2)



#----------------------------------------------
#  create ngrams
#----------------------------------------------
def create_ngrams(dict1, dict2, num_ngrams, logp):
    """
    tkey = tweet number 
    tvalue = each character of tweet
    ckey = tweet number
    cvalue = class
    logp = log print = print for troubleshooting
    """
    ngrams_list = []
    for (tkey, tvalue), (ckey, cvalue) in izip(dict1.iteritems(), \
                                               dict2.iteritems()):
        tweet_length = sum(1 for v in tvalue if v)
        for gram_length in range(num_ngrams, num_ngrams + 1):
            gramitems = ngrams(tvalue, gram_length)

            for index, grams in enumerate(gramitems, start=-1):
                #print "\ngrams: ", grams
                #print "\tclass: ", cvalue[index]
                gramsjoined = "".join(grams)
                item = [tkey, gram_length, gramsjoined, cvalue[index+1]]
                ngrams_list.append(item)

                if logp == 1:
                    print "item: ", item
                    print "gram_length: ", gram_length
                    print "grams: ", gramsjoined
        if logp == 1:
            print tkey
            print tvalue
            print ckey
            print cvalue

            print "\nmaximum-length gram: ", tweet_length
            print gramsjoined
            print cvalue[index]
            #pprint(ngrams_list)

    return ngrams_list

# Note: I am including the class that corresponds to letter at start of ngram
#       This will be adjusted later
# this is what ngrams list looks like: tweet number, ngram length, ngram, class at start of ngram
'''
[['1', 2, 'RT', 'O'],
 ['1', 2, 'T@', 'O'],
 ['1', 2, '@P', 'B-mention'],
 ['1', 2, 'Pe', 'B-mention'],
 ['1', 2, 'et', 'B-mention'],
 ['1', 2, 'te', 'B-mention'],
 ['1', 2, 'er', 'B-mention'],
 ['1', 2, 'rR', 'B-mention'],
 ['1', 2, 'Ra', 'B-mention'],
 ['1', 2, 'ab', 'B-mention'],
 ['1', 2, 'bb', 'B-mention'],
 ['1', 2, 'bi', 'B-mention'],
 ['1', 2, 'it', 'B-mention'],
'''

def main(eval_run, eval_desc, add_newclass, num_ngrams, train_file, dev_file):
    """
    function input:  train or dev datafiles
    function returns:  by char list, by word list
    train    : 36,695 lines
    test(dev): 12,170 lines
    """

    # Pablo's run - Evaluation 1
    # Step 1:  make lists from raw input file
    #ner_list_train, ner_word_list = read_data("../../wnut_ner_evaluation/data/train", 0)
    #ner_list_dev, ner_word_list = read_data("../../wnut_ner_evaluation/data/dev", 0)

    # Step 2:  add new class
    # NA

    # Step x:  output file
    # NA
    
    # Step 3: create dictionaries needed for adding new class and ngrams  
    #d_bychar_char_train = create_dict(ner_list_train, 3, 0)
    #d_bychar_tclass1_train = create_dict(ner_list_train, 4, 0)

    #d_bychar_char_dev = create_dict(ner_list_dev, 3, 0)
    #d_bychar_tclass1_dev = create_dict(ner_list_dev, 4, 0)
    
    # Step 4:  create ngrams
    #ngrams_list_class1_train = create_ngrams(d_bychar_char_train, d_bychar_tclass1_train, num_ngrams, 0)
    #ngrams_list_class1_dev = create_ngrams(d_bychar_char_dev, d_bychar_tclass1_dev, num_ngrams, 0)

    # Step 5:  output ngrams to a file
    #output_file2(ngrams_list_class1_train, "../eval_files/eval_1_train_4gram")
    #output_file2(ngrams_list_class1_dev, "../eval_files/eval_1_dev_4gram")

    #-------------------------------------
    # Reshama's run - Evaluation 3
    # Step 1:  make lists from raw input file
    ner_char_list_train, ner_word_list_train = read_data("../../wnut_ner_evaluation/data/" + train_file, 0)
    ner_char_list_dev, ner_word_list_dev = read_data("../../wnut_ner_evaluation/data/" + dev_file, 0)

    # Step 2:  add new class
    if add_newclass == 1:
        ner_char_list_train_newclass = add_class(ner_char_list_train, 4, 0)
        ner_word_list_train_newclass = add_class(ner_word_list_train, 3, 0)

        ner_char_list_dev_newclass = add_class(ner_char_list_dev, 4, 0)
        ner_word_list_dev_newclass = add_class(ner_word_list_dev, 3, 0)

        train_output_file = "eval_" + str(eval_run) + "_train_newclass" 
        dev_output_file = "eval_" + str(eval_run) + "_dev_newclass" 
        
        #print "train_output_file: " , train_output_file
        #print "dev_output_file:   ", dev_output_file
        
        output_file(ner_word_list_train_newclass, "../eval_files/" + train_output_file)
        output_file(ner_word_list_dev_newclass,   "../eval_files/" + dev_output_file)

    if num_ngrams > 0:
        # create dictionaries, then ngrams
        # Step 3: create dictionaries needed for adding new class and ngrams  
        d_bychar_train_newclass= create_dict(ner_char_list_train_newclass, 3, 0)
        d_bychar_dev_newclass= create_dict(ner_char_list_dev_newclass, 3, 0)

        d_bychar_train_tclass2 = create_dict(ner_char_list_train_newclass, 5, 0)
        d_bychar_dev_tclass2   = create_dict(ner_char_list_dev_newclass, 5, 0)

        # Step 4: create ngrams
        ngrams_train_class2 = create_ngrams(d_bychar_train_newclass, d_bychar_train_tclass2, num_ngrams, 0)
        ngrams_dev_class2   = create_ngrams(d_bychar_dev_newclass, d_bychar_dev_tclass2, num_ngrams, 0)

        print "-"*25
        pprint(ngrams_train_class2[:25])
        pprint(ngrams_dev_class2[:25])

        # Step 5:  output ngrams to a file
        train_output_file = "eval_" + str(eval_run) + "_train_" + eval_desc
        dev_output_file = "eval_" + str(eval_run) + "_dev_" + eval_desc
        print "train_output_file: " , train_output_file
        print "dev_output_file:   ", dev_output_file

        output_file2(ngrams_train_class2, "../eval_files/" + train_output_file)
        output_file2(ngrams_dev_class2, "../eval_files/" + dev_output_file)




      
if __name__ == '__main__':
    # these are the fields to send up to main program
    # main(eval_run, eval_desc, add_newclass, num_ngrams, train_file, dev_file)

    #main(1, "4gram", 0, 4, "train", "dev")
    #main(2, "bigram", 0, 2, "train", "dev")
    
    #main(3, "newclass", 1, 0, "train", "dev")

    #main(4, "newclass_4gram", 1, 4, "train", "dev")

    main(5, "newclass_bigram", 1, 2, "train", "dev")
    



