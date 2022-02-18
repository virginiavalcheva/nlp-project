import codecs
import pickle
import re

from constants import RULES_FILE, MIN_RULE_FREQUENCY, \
    MIN_WORD_LENGTH, BG_VOWELS, STEMMING_RULES_MIN_FREQ


def fetch_rules(RULES_FILE, MIN_RULE_FREQ):
    regex_for_empty_line = re.compile('^\s*$')
    regex_for_rule_line = re.compile(u"([а-я-]+) ==> ([a-я-]+) (\d+)", re.U)
    stemming_rules = {}
    for rule in codecs.open(RULES_FILE, 'r', 'utf-8').readlines():
        if regex_for_empty_line.match(rule):
            continue
        rule_parts = regex_for_rule_line.match(rule)
        if rule_parts:
            if rule_parts.group(3) > MIN_RULE_FREQ:
                len_for_match = len(rule_parts.group(1))
                try:
                    stemming_rules[len_for_match][rule_parts.group(1)] = rule_parts.group(2)
                except KeyError:
                    stemming_rules[len_for_match] = {}
                    stemming_rules[len_for_match][rule_parts.group(1)] = rule_parts.group(2)
        else:
            continue
    pickle.dump(stemming_rules, open(STEMMING_RULES_MIN_FREQ + str(MIN_RULE_FREQ) + '.pickle', 'wb'))
    return stemming_rules


def get_stemming_rules():
    try:
        stemming_rules = pickle.load(
            open(STEMMING_RULES_MIN_FREQ + str(MIN_RULE_FREQUENCY) + '.pickle', 'rb'))
    except:
        stemming_rules = fetch_rules(RULES_FILE, MIN_RULE_FREQUENCY)
    return stemming_rules


def word_to_lower(word):
    return word.lower()


def process_word_for_stemming(word, counter, word_length, stemming_rules):
    for s in word:
        stem = word[counter:word_length]
        word_reminder = word_length - counter
        if stem in stemming_rules[word_reminder]:
            return word[:counter] + stemming_rules[word_reminder][stem]
        counter += 1
    return word


def stem_word(word_to_stem):
    stemming_rules = get_stemming_rules()
    word_length = len(word_to_stem)
    if word_length <= MIN_WORD_LENGTH or not BG_VOWELS.match(word_to_stem):
        return word_to_stem
    # lower the word
    word_to_stem = word_to_lower(word_to_stem)
    counter = MIN_WORD_LENGTH
    return process_word_for_stemming(word_to_stem, counter, word_length, stemming_rules)
