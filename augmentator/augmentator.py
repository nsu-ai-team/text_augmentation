import os
import random
from argparse import ArgumentParser
import re
import csv
import codecs
import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

def get_wordnet_pos(treebank_tag):

    """ This function changes standard NLTK POS tags to pos tags that are compatible with wordnet

    Parameters
    -----------
    treebank_tag : str
                   standard NLTK POS tag

    Returns
    --------
    string with wordnet pos tag or None if NLTK's tag isn't supported.

    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def tokenize_tag(sentence, state_random = False):

    """ This function returns random word from the given sentence with its pos tag

    Parameters
    -----------
    sentence : str
                Sentence.

    state_random : bool
                Variable for unittests. "False" by default.

    Returns
    --------
    words : tuple
           word (str) and its pos tag (str)

    """
    if not isinstance(sentence, str):
        raise TypeError("write the correct sentence")
    if not isinstance(state_random, bool):
        raise TypeError("'state_random' must be bool")
    full_sent = word_tokenize(sentence)
    tagged = nltk.pos_tag(full_sent)
    words = []
    for word, tag in tagged:
        wntag = get_wordnet_pos(tag)
        if wntag == None:
            pass
        if word in stopwords.words('english'):
            pass
        else:
            word = (word, wntag)
            words.append(word)
    if len(words) == 0:
        return ([(), ()])
    else:
       return words


def augment(sentence, state_random = False, amount=10):
    """This function returns new sentence which differs from the given one to one word (it replaces by a synonym)

    Parameters
    -----------
    sentence : str
                Sentence.

    state_random : bool
                Variable for unittests. "False" by default.

    amount : int
                How many words (in %) should be replaced with the synonyms.

    Returns
    --------
    new_sentence : str
                 Modified sentence with synonyms.

    """
    if not isinstance(sentence, str):
        raise TypeError("write the correct sentence")
    if not isinstance(state_random, bool):
        raise TypeError("'state_random' must be bool")
    if not isinstance(amount, int):
       raise TypeError("'amount' must be int")
    if amount > 100:
       raise ValueError("'amount' must be a percent number")
    word_tag = tokenize_tag(sentence)
    count = round(amount/100*len(sentence.split()))
    # dictionary of synonyms for each word
    synonyms = {}
    # dictionary of words for replacing
    words_dictionary = {}
    words = []
    for c in range(count):
        synonym = []
        word = word_tag[random.randint(0, len(word_tag) - 1)]
        n = 0
        while word[1] == None:
            word = word_tag[random.randint(0, len(word_tag) - 1)]
            n += 1
            if n == 10:
                break
        n = 0
        while word[0] == () and word[1] == ():
            word = word_tag[random.randint(0, len(word_tag) - 1)]
            n += 1
            if n == 10:
                break
        n = 0
        while word[0] in words:
            word = word_tag[random.randint(0, len(word_tag) - 1)]
            n += 1
            if n == 10:
                break
        if word[0] in words:
            continue
        if  word[0] == () and word[1] == ():
            continue
        if word[1] == None:
            continue
        else:
            words.append(word[0])
        for syn in wordnet.synsets(word[0].lower(), pos=word[1]):
            for l in syn.lemmas():
                if l.name() not in synonym:
                    # deleting of '_' in the synonyms from wordnet which are phrases
                    re_l = re.search("(.*)_(.*)", l.name())
                    if re_l:
                        l_syno = str(re_l.group(1) + " " + re_l.group(2))
                        synonym.append(l_syno)
                    else:
                        synonym.append(l.name())
        if synonym != []:
           synonyms[c] = []
           synonyms[c] = synonym
           words_dictionary[c] = word[0]
    new_sentence = sentence
    for r in synonyms:
        if words_dictionary[r].isupper():
            new_sentence = re.sub(words_dictionary[r], synonyms[r][random.randint(0, len(synonyms[r]) - 1)].upper(), new_sentence)
        else:
            new_sentence = re.sub(words_dictionary[r], synonyms[r][random.randint(0, len(synonyms[r]) - 1)], new_sentence)
    return (new_sentence)


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='file', type=str, help='Name of csv file before augmentation')
    parser.add_argument('-n', '--number', dest='number', type=int, help='How many times the  corpus will be augmented')
    parser.add_argument('-d', '--dst', dest='augmented', type=str, help='Name of csv file after augmentation')
    parser.add_argument('-a', '--amount', dest='amount', type=int, help='How many words should be changed (%)')
    args = parser.parse_args()
    assert os.path.isfile(args.file), 'File "{0}" does not exist!'.format(args.file)
    num = args.number
    new_path = args.augmented
    amount = args.amount
    header = None
    true_header = ("id", "comment_text", "toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate")
    line_index = 1
    src_fp = codecs.open(args.file, mode='r', encoding='utf-8', errors='ignore')
    with codecs.open(new_path, mode='w', encoding='utf-8') as dst_fp:
        data_reader = csv.reader(src_fp, delimiter=',', quotechar='"')
        data_writer = csv.writer(dst_fp, delimiter=',', quotechar='"')
        for row in data_reader:
            if len(row) > 0:
                err_msg = 'File "{0}": line {1} is wrong!'.format(args.file, line_index)
                if header is None:
                    header = tuple(row)
                    assert len(header) == len(true_header), err_msg
                    assert header == true_header, err_msg
                    data_writer.writerow(true_header)
                else:
                    data_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    old_text = row[1]
                    for n in range(num):
                        new_text = augment(row[1], amount=amount)
                        if new_text is not None:
                            if len(new_text.strip()) > 0:
                                if old_text.lower().strip() != new_text.lower().strip():
                                    data_writer.writerow(
                                        [
                                            row[0] + 'part{0}'.format(n + 1), new_text, row[2], row[3], row[4], row[5],
                                            row[6], row[7]
                                        ]
                                    )
                                old_text = new_text
            line_index += 1
            if line_index%1000 == 0:
                print(line_index, "sentences are done")


if __name__ == '__main__':
    main()
