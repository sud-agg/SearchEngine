from bs4 import BeautifulSoup
from urllib.request import urlopen

import re
import sys

ignoreWords = ['mr','mrs','was','his', 'her','he','she', 'a','an','the','how','what','who','when','why','can','could','will','would','shall','should','might','must','in','at','on','of','it','be']
searchString = "[A-Za-z]+"
tags = ['p', 'h1','h2','h3','h4','h5','h6'] # tags we're interested in

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.links = []
        self.children = dict()
        '''
        The class node is for the nodes of the trie.
        Label - the aplhabet of this node.
        Data - If a word is completed at this node, the word will be saved here so that we don't have to re-consruct it on the way back up.
        Links - If there is a word getting completed at this node, then the links on which it is mentioned.
        Children - The other nodes for other words.
        '''
    
    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
        '''
        This method is for adding a new node to the trie.
        '''
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word, link):
        current_node = self.head
        word_finished = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
                '''
                We will iterate the word till it's longest prefix.
                '''
            else:
                word_finished = False
                break
        
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
                '''
                For every new letter we will create a new child node
                '''
        
        current_node.data = word
        current_node.links.append(link)
    
    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        
        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        
        '''
        Confirming that the word is a full word, not a partial match
        '''
        if exists:
            if current_node.data == None:
                exists = False
        
        return exists
    
    def getData(self, word):
        ''' This returns the 'data' of the node identified by the given word '''
        if not self.has_word(word):
            return False
        
        # Race to the bottom, get links
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]
        
        return current_node.links

# GLOBAL TRIE
trie = Trie()

def scrap2Trie(URL):
    htmlFile = urlopen(URL)
    htmlText = htmlFile.read().decode('utf8')
    soup = BeautifulSoup(htmlText, "html.parser")

    for mainData in soup.findAll('div', {'class': 'mw-parser-output'}):
        paragraphs = mainData.findAll(tags)
        for item in paragraphs:
            if item != None:
                words = (item.text.strip()).split()
                # print(words)
                for word in words:
                    # use regex to keep only alphabets
                    if re.search(searchString, word):
                        onlyAlpha = re.search(searchString, word)
                        # if null, or if in ignoreWords, continue
                        if onlyAlpha.group():
                            # to lower
                            lowerCase = onlyAlpha.group().lower()
                            if lowerCase in ignoreWords:
                                continue
                            # add word to trie
                            trie.add(lowerCase,URL)


def searching():
    response = input("Do you want to search (Press n for no): ")
    while response not in ['N','n']:
        results = {"No more results to display" : -1} # Dictionary storing results of that search
        searchInput = input("Enter Search Query: ")
        inputSplit = searchInput.split()
        for word in inputSplit:
            if re.search(searchString, word):
                onlyAlpha = re.search(searchString, word)
                # if null, or if in ignoreWords, continue
                if onlyAlpha.group():
                    # to lower
                    lowerCase = onlyAlpha.group().lower()
                    if lowerCase in ignoreWords:
                        continue
                    # search for the word now
                    links = trie.getData(lowerCase)
                    if not links:
                        continue
                    for link in links: # counting frequency of occurences in the results
                        if link in results:
                            results[link] = results[link] + 1
                        else:
                            results[link] = 1

        sortedResults = sorted(results, key=results.get, reverse = True)
        for result in sortedResults:
            print(result)

        results.clear()
        response = input("Do you want to search again? (Press n for no): ")
    return


try:
    with open("links.txt") as file:
        for line in file:
            scrap2Trie(line)
        searching()
        print("Thank you for using Sudhansh Search")

except FileNotFoundError:
    print("\nlinks.txt not found. Can't populate trie for search engine")
