# Copyright (c) 2010, Chris Jones
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Python implementation of megahal markov bot"""

from time import time
import shelve
import random
import math
import os

__version__ = '0.2'
__author__ = 'Chris Jones <cjones@gruntle.org>'
__license__ = 'BSD'
__all__ = ['MegaHAL', 'Dictionary', 'Tree', '__version__', 'DEFAULT_ORDER', 'DEFAULT_BRAINFILE', 'DEFAULT_TIMEOUT']

DEFAULT_ORDER = 5
DEFAULT_BRAINFILE = os.path.join(os.environ.get('HOME', ''), '.pymegahal-brain')
DEFAULT_TIMEOUT = 1.0

API_VERSION = '1.0'
END_WORD = '<FIN>'
ERROR_WORD = '<ERROR>'

DEFAULT_BANWORDS = ['A', 'ABILITY', 'ABLE', 'ABOUT', 'ABSOLUTE', 'ABSOLUTELY', 'ACROSS', 'ACTUAL', 'ACTUALLY', 'AFTER',
                    'AGAIN', 'AGAINST', 'AGO', 'AGREE', 'ALL', 'ALMOST', 'ALONG', 'ALREADY', 'ALTHOUGH', 'ALWAYS',
                    'AN', 'AND', 'ANOTHER', 'ANY', 'ANYHOW', 'ANYTHING', 'ANYWAY', 'ARE', "AREN'T", 'AROUND', 'AS',
                    'AWAY', 'BACK', 'BAD', 'BE', 'BEEN', 'BEFORE', 'BEHIND', 'BEING', 'BELIEVE', 'BELONG', 'BEST',
                    'BETWEEN', 'BIG', 'BIGGER', 'BIGGEST', 'BIT', 'BOTH', 'BUDDY', 'BUT', 'BY', 'CALL', 'CALLED',
                    'CAME', 'CAN', "CAN'T", 'CANNOT', 'CARE', 'CARING', 'CASE', 'CATCH', 'CAUGHT', 'CERTAIN',
                    'CHANGE', 'CLOSE', 'CLOSER', 'COME', 'COMING', 'COMMON', 'CONSTANT', 'CONSTANTLY', 'COULD',
                    'DAY', 'DAYS', 'DERIVED', 'DESCRIBE', 'DESCRIBES', 'DETERMINE', 'DETERMINES', 'DID', "DIDN'T",
                    'DOES', "DOESN'T", 'DOING', "DON'T", 'DONE', 'DOUBT', 'DOWN', 'EACH', 'EARLIER', 'EARLY', 'ELSE',
                    'ESPECIALLY', 'EVEN', 'EVER', 'EVERY', 'EVERYBODY', 'EVERYONE', 'EVERYTHING', 'FACT', 'FAIR',
                    'FAR', 'FELLOW', 'FEW', 'FIND', 'FINE', 'FOR', 'FORM', 'FOUND', 'FROM', 'FULL', 'FURTHER', 'GAVE',
                    'GETTING', 'GIVE', 'GIVEN', 'GIVING', 'GO', 'GOING', 'GONE', 'GOOD', 'GOT', 'GOTTEN', 'GREAT',
                    'HAS', "HASN'T", 'HAVE', "HAVEN'T", 'HAVING', 'HELD', 'HERE', 'HIGH', 'HOLD', 'HOLDING', 'HOW',
                    'IN', 'INDEED', 'INSIDE', 'INSTEAD', 'INTO', 'IS', "ISN'T", 'IT', "IT'S", 'ITS', 'JUST', 'KEEP',
                    'KNEW', 'KNOW', 'KNOWN', 'LARGE', 'LARGER', 'LARGETS', 'LAST', 'LATE', 'LATER', 'LEAST', 'LESS',
                    "LET'S", 'LEVEL', 'LIKES', 'LITTLE', 'LONG', 'LONGER', 'LOOK', 'LOOKED', 'LOOKING', 'LOOKS', 'LOW',
                    'MAKE', 'MAKING', 'MANY', 'MATE', 'MAY', 'MAYBE', 'MEAN', 'MEET', 'MENTION', 'MERE', 'MIGHT',
                    'MORE', 'MORNING', 'MOST', 'MOVE', 'MUCH', 'MUST', 'NEAR', 'NEARER', 'NEVER', 'NEXT', 'NICE',
                    'NONE', 'NOON', 'NOONE', 'NOT', 'NOTE', 'NOTHING', 'NOW', 'OBVIOUS', 'OF', 'OFF', 'ON', 'ONCE',
                    'ONTO', 'OPINION', 'OR', 'OTHER', 'OUR', 'OUT', 'OVER', 'OWN', 'PART', 'PARTICULAR',
                    'PERHAPS', 'PERSON', 'PIECE', 'PLACE', 'PLEASANT', 'PLEASE', 'POPULAR', 'PREFER', 'PRETTY', 'PUT',
                    'REAL', 'REALLY', 'RECEIVE', 'RECEIVED', 'RECENT', 'RECENTLY', 'RELATED', 'RESULT', 'RESULTING',
                    'SAID', 'SAME', 'SAW', 'SAY', 'SAYING', 'SEE', 'SEEM', 'SEEMED', 'SEEMS', 'SEEN', 'SELDOM',
                    'SET', 'SEVERAL', 'SHALL', 'SHORT', 'SHORTER', 'SHOULD', 'SHOW', 'SHOWS', 'SIMPLE', 'SIMPLY',
                    'SO', 'SOME', 'SOMEONE', 'SOMETHING', 'SOMETIME', 'SOMETIMES', 'SOMEWHERE', 'SORT', 'SORTS',
                    'SPENT', 'STILL', 'STUFF', 'SUCH', 'SUGGEST', 'SUGGESTION', 'SUPPOSE', 'SURE', 'SURELY',
                    'SURROUNDS', 'TAKE', 'TAKEN', 'TAKING', 'TELL', 'THAN', 'THANK', 'THANKS', 'THAT', "THAT'S",
                    'THE', 'THEIR', 'THEM', 'THEN', 'THERE', 'THEREFORE', 'THESE', 'THEY', 'THING', 'THINGS', 'THIS',
                    'THOUGH', 'THOUGHTS', 'THOUROUGHLY', 'THROUGH', 'TINY', 'TO', 'TODAY', 'TOGETHER', 'TOLD',
                    'TOO', 'TOTAL', 'TOTALLY', 'TOUCH', 'TRY', 'TWICE', 'UNDER', 'UNDERSTAND', 'UNDERSTOOD', 'UNTIL',
                    'US', 'USED', 'USING', 'USUALLY', 'VARIOUS', 'VERY', 'WANT', 'WANTED', 'WANTS', 'WAS', 'WATCH',
                    'WAYS', 'WE', "WE'RE", 'WELL', 'WENT', 'WERE', 'WHAT', "WHAT'S", 'WHATEVER', 'WHATS', 'WHEN',
                    "WHERE'S", 'WHICH', 'WHILE', 'WHILST', 'WHO', "WHO'S", 'WHOM', 'WILL', 'WISH', 'WITH', 'WITHIN',
                    'WONDERFUL', 'WORSE', 'WORST', 'WOULD', 'WRONG', 'YESTERDAY', 'YET']

DEFAULT_AUXWORDS = ['DISLIKE', 'HE', 'HER', 'HERS', 'HIM', 'HIS', 'I', "I'D", "I'LL", "I'M", "I'VE", 'LIKE', 'ME',
                    'MY', 'MYSELF', 'ONE', 'SHE', 'THREE', 'TWO', 'YOU', "YOU'D", "YOU'LL", "YOU'RE", "YOU'VE", 'YOUR',
                    'YOURSELF']

DEFAULT_SWAPWORDS = {"YOU'RE": "I'M", "YOU'D": "I'D", 'HATE': 'LOVE', 'YOUR': 'MY', "I'LL": "YOU'LL", 'NO': 'YES',
                     'WHY': 'BECAUSE', 'YOU': 'ME', 'LOVE': 'HATE', 'I': 'YOU', 'MINE': 'YOURS', 'YOURSELF': 'MYSELF',
                     'DISLIKE': 'LIKE', "I'M": "YOU'RE", 'ME': 'YOU', 'MYSELF': 'YOURSELF', 'LIKE': 'DISLIKE',
                     "I'D": "YOU'D", "YOU'VE": "I'VE", 'YES': 'NO', 'MY': 'YOUR'}

class Tree(object):

    def __init__(self, symbol=0):
        self.symbol = symbol
        self.usage = 0
        self.count = 0
        self.children = []

    def add_symbol(self, symbol):
        node = self.get_child(symbol)
        node.count += 1
        self.usage += 1
        return node

    def get_child(self, symbol, add=True):
        for child in self.children:
            if child.symbol == symbol:
                break
        else:
            if add:
                child = Tree(symbol)
                self.children.append(child)
            else:
                child = None
        return child


class Dictionary(list):

    def add_word(self, word):
        try:
            return self.index(word)
        except ValueError:
            self.append(word)
            return len(self) - 1

    def find_word(self, word):
        try:
            return self.index(word)
        except ValueError:
            return 0


class Brain(object):

    def __init__(self, order, file, timeout):
        self.timeout = timeout
        self.db = shelve.open(file, writeback=True)
        if self.db.setdefault('api', API_VERSION) != API_VERSION:
            raise ValueError('This brain has an incompatible api version: %d != %d' % (self.db['api'], API_VERSION))
        if self.db.setdefault('order', order) != order:
            raise ValueError('This brain already has an order of %d' % self.db['order'])
        self.forward = self.db.setdefault('forward', Tree())
        self.backward = self.db.setdefault('backward', Tree())
        self.dictionary = self.db.setdefault('dictionary', Dictionary())
        self.error_symbol = self.dictionary.add_word(ERROR_WORD)
        self.end_symbol = self.dictionary.add_word(END_WORD)
        self.banwords = self.db.setdefault('banwords', Dictionary(DEFAULT_BANWORDS))
        self.auxwords = self.db.setdefault('auxwords', Dictionary(DEFAULT_AUXWORDS))
        self.swapwords = self.db.setdefault('swapwords', DEFAULT_SWAPWORDS)
        self.closed = False

    @property
    def order(self):
        return self.db['order']

    @staticmethod
    def get_words_from_phrase(phrase):
        phrase = phrase.upper()
        words = []
        if phrase:
            offset = 0

            def boundary(string, position):
                if position == 0:
                    boundary = False
                elif position == len(string):
                    boundary = True
                elif (string[position] == "'" and
                    string[position - 1].isalpha() and
                    string[position + 1].isalpha()):
                    boundary = False
                elif (position > 1 and
                    string[position - 1] == "'" and
                    string[position - 2].isalpha() and
                    string[position].isalpha()):
                    boundary = False
                elif (string[position].isalpha() and
                    not string[position - 1].isalpha()):
                    boundary = True
                elif (not string[position].isalpha() and
                    string[position - 1].isalpha()):
                    boundary = True
                elif string[position].isdigit() != string[position -1].isdigit():
                    boundary = True
                else:
                    boundary = False
                return boundary

            while True:
                if boundary(phrase, offset):
                    word, phrase = phrase[:offset], phrase[offset:]
                    words.append(word)
                    if not phrase:
                        break
                    offset = 0
                else:
                    offset += 1
            if words[-1][0].isalnum():
                words.append('.')
            elif words[-1][-1] not in '!.?':
                words[-1] = '.'
        return words

    def communicate(self, phrase, learn=True, reply=True):
        words = self.get_words_from_phrase(phrase)
        if learn:
            self.learn(words)
        if reply:
            return self.get_reply(words)

    def get_context(self, tree):

        class Context(dict):

            def __enter__(context):
                context.used_key = False
                context[0] = tree
                return context

            def __exit__(context, *exc_info):
                context.update(self.end_symbol)

            @property
            def root(context):
                return context[0]

            def update(context, symbol):
                for i in xrange(self.order + 1, 0, -1):
                    node = context.get(i - 1)
                    if node is not None:
                        context[i] = node.add_symbol(symbol)

            def seed(context, keys):
                if keys:
                    i = random.randrange(len(keys))
                    for key in keys[i:] +  keys[:i]:
                        if key not in self.auxwords:
                            try:
                                return self.dictionary.index(key)
                            except ValueError:
                                pass
                if context.root.children:
                    return random.choice(context.root.children).symbol
                return 0

            def babble(context, keys, replies):
                for i in xrange(self.order + 1):
                    if context.get(i) is not None:
                        node = context[i]
                if not node.children:
                    return 0
                i = random.randrange(len(node.children))
                count = random.randrange(node.usage)
                symbol = 0
                while count >= 0:
                    symbol = node.children[i].symbol
                    word = self.dictionary[symbol]
                    if word in keys and (context.used_key or word not in self.auxwords):
                        context.used_key = True
                        break
                    count -= node.children[i].count
                    if i >= len(node.children) - 1:
                        i = 0
                    else:
                        i = i + 1
                return symbol

        return Context()

    def learn(self, words):
        if len(words) > self.order:
            with self.get_context(self.forward) as context:
                for word in words:
                    context.update(self.dictionary.add_word(word))
            with self.get_context(self.backward) as context:
                for word in reversed(words):
                    context.update(self.dictionary.index(word))

    def get_reply(self, words):
        keywords = self.make_keywords(words)
        dummy_reply = self.generate_replywords()
        if not dummy_reply or words == dummy_reply:
            output = self.get_words_from_phrase("I don't know enough to answer yet!")
        else:
            output = dummy_reply

        max_surprise = -1.0
        basetime = time()
        while time() - basetime < self.timeout:
            reply = self.generate_replywords(keywords)
            surprise = self.evaluate_reply(keywords, reply)
            if reply and surprise > max_surprise and reply != keywords:
                max_surprise = surprise
                output = reply

        return ''.join(output).capitalize()

    def evaluate_reply(self, keys, words):
        state = {'num': 0, 'entropy': 0.0}
        if words:

            def evaluate(node, words):
                with self.get_context(node) as context:
                    for word in words:
                        symbol = self.dictionary.index(word)
                        context.update(symbol)
                        if word in keys:
                            prob = 0.0
                            count = 0
                            state['num'] += 1
                            for j in xrange(self.order):
                                node = context.get(j)
                                if node is not None:
                                    child = node.get_child(symbol, add=False)
                                    if child:
                                        prob += float(child.count) / node.usage
                                    count += 1
                            if count:
                                state['entropy'] -= math.log(prob / count)

            evaluate(self.forward, words)
            evaluate(self.backward, reversed(words))

            if state['num'] >= 8:
                state['entropy'] /= math.sqrt(state['num'] - 1)
            if state['num'] >= 16:
                state['entropy'] /= state['num']
        return state['entropy']

    def generate_replywords(self, keys=None):
        if keys is None:
            keys = []
        replies = []
        with self.get_context(self.forward) as context:
            start = True
            while True:
                if start:
                    symbol = context.seed(keys)
                    start = False
                else:
                    symbol = context.babble(keys, replies)
                if symbol in (self.error_symbol, self.end_symbol):
                    break
                replies.append(self.dictionary[symbol])
                context.update(symbol)
        with self.get_context(self.backward) as context:
            if replies:
                for i in xrange(min([(len(replies) - 1), self.order]), -1, -1):
                    context.update(self.dictionary.index(replies[i]))
            while True:
                symbol = context.babble(keys, replies)
                if symbol in (self.error_symbol, self.end_symbol):
                    break
                replies.insert(0, self.dictionary[symbol])
                context.update(symbol)

        return replies

    def make_keywords(self, words):
        keys = Dictionary()
        for word in words:
            try:
                word = self.swapwords[word]
            except KeyError:
                pass
            if (self.dictionary.find_word(word) != self.error_symbol and word[0].isalnum() and
                word not in self.banwords and word not in self.auxwords and word not in keys):
                keys.append(word)

        if keys:
            for word in words:
                try:
                    word = self.swapwords[word]
                except KeyError:
                    pass
                if (self.dictionary.find_word(word) != self.error_symbol and word[0].isalnum() and
                    word in self.auxwords and word not in keys):
                    keys.append(word)

        return keys

    def add_key(self, keys, word):
        if (self.dictionary.find_word(word) != self.error_symbol and
            self.banwords.find_word(word) == self.error_symbol and
            self.auxwords.find_word(word) == self.error_symbol):
            keys.add_word(word)

    def sync(self):
        self.db.sync()

    def close(self):
        if not self.closed:
            print 'Closing database'
            self.db.close()
            self.closed = True

    def __del__(self):
        try:
            self.close()
        except:
            pass


class MegaHAL(object):

    def __init__(self, order=None, brainfile=None, timeout=None):
        if order is None:
            order = DEFAULT_ORDER
        if brainfile is None:
            brainfile = DEFAULT_BRAINFILE
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        self.__brain = Brain(order, brainfile, timeout)

    @property
    def banwords(self):
        """This is a list of words which cannot be used as keywords"""
        return self.__brain.banwords

    @property
    def auxwords(self):
        """This is a list of words which can be used as keywords only in order to supplement other keywords"""
        return self.__brain.auxwords

    @property
    def swapwords(self):
        """The word on the left is changed to the word on the right when used as a keyword"""
        return self.__brain.swapwords

    def train(self, file):
        """Train the brain with textfile, each line is a phrase"""
        with open(file, 'rb') as fp:
            for line in fp:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.learn(line)

    def learn(self, phrase):
        """Learn from phrase"""
        self.__brain.communicate(phrase, reply=False)

    def get_reply(self, phrase):
        """Get a reply based on the phrase"""
        return self.__brain.communicate(phrase)

    def get_reply_nolearn(self, phrase):
        """Get a reply without updating the database"""
        return self.__brain.communicate(phrase, learn=False)

    def interact(self):
        """Have a friendly chat session.. ^D to exit"""
        while True:
            try:
                phrase = raw_input('>>> ')
            except EOFError:
                break
            if phrase:
                print self.get_reply(phrase)

    def sync(self):
        """Flush any changes to disk"""
        self.__brain.sync()

    def close(self):
        """Close database"""
        self.__brain.close()
