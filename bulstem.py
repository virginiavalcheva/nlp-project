'''
Algorithm author: Preslav Nakov <nakov@cs.berkeley.edu>, UC Berkeley
Paper: BulStem: Inflectional Stemmer For Bulgarian http://people.ischool.berkeley.edu/~nakov/bulstem/
'''

import codecs
import pickle
import re

# CONSTANTS
RULES_FILE = "rules/stem_rules_context_2_UTF-8.txt"
MIN_RULE_FREQ = 2
MIN_WORD_LEN = 3

re_bg_vowels = re.compile(u"[аъоуеияю]")

def fetchTheRules(RULES_FILE, MIN_RULE_FREQ):
	'Read the rules and load them into dictionary'
	re_empty_line = re.compile('^\s*$') 
	re_rule_line = re.compile(u"([а-я-]+) ==> ([a-я-]+) (\d+)", re.U)
	StemmingRules = {}

	for rule in codecs.open(RULES_FILE, 'r', 'utf-8').readlines():
		if re_empty_line.match(rule):
			continue
			
		'Break the rule line in three parts match(1) - reduce(2) - probability(3)'
		rule_parts = re_rule_line.match(rule)
		
		if rule_parts is not None:
			if rule_parts.group(3) > MIN_RULE_FREQ:
				
				'Build a dictionary indexed by the lenght of the match'
				match_len = len(rule_parts.group(1))
				try:
					StemmingRules[match_len][rule_parts.group(1)] = rule_parts.group(2)					
				except KeyError:
					StemmingRules[match_len] = {}
					StemmingRules[match_len][rule_parts.group(1)] = rule_parts.group(2)

		else:
			continue

	pickle.dump(StemmingRules, open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'wb'))
	return StemmingRules

def stem(word):
	'Stemm the word'

	'Do not stem short words'
	wordLen = len(word)
	if wordLen <= MIN_WORD_LEN:
		return word

	'If no bulgarian vowel - no valid word'
	if not re_bg_vowels.match(word):
		return word

	'Convert to lower case in order to compare it easy'
	word = word.lower()

	'Start from the minimal meaningful word'
	c = MIN_WORD_LEN
	for _ in word:
		'Reduce the word from the begining towards the end'
		stem = word[c:wordLen]
	
		'Calculate the reminding symbols for better search'
		word_reminder = wordLen - c
		
		'Check if there is a stem matching the reminder of the word'
		# print(stem)
		# print(StemmingRules[word_reminder])
		if stem in StemmingRules[word_reminder]:
			'Return stemmed word'
			return word[:c]+StemmingRules[word_reminder][stem]
			break
		else:
			c += 1

	'Always return something'		
	return word

'Try to reload the rules or build them from the text files'
try:
	StemmingRules = pickle.load(open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'rb'))
except:
	StemmingRules = fetchTheRules(RULES_FILE, MIN_RULE_FREQ)
