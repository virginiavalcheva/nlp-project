import re

RESOURCE_FILENAME = "../resources/IR_lecture_notes.txt"
QESTIONS_PATH_TO_FILE = "../resources/questions.json"

RULES_FILE = "../resources/rules/stem_rules_context_2_UTF-8.txt"
MIN_RULE_FREQUENCY = 2
MIN_WORD_LENGTH = 3
BG_VOWELS = re.compile(u"[аъоуеияю]")
STEMMING_RULES_MIN_FREQ = "../resources/rules/StemmingRules-MinFreq-"