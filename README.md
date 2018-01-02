Search Engine Project
Sudhansh Aggarwal
CS 600 Fall 17
Stevens Institute of Technology, Hoboken NJ USA

Data Structures
I have used a Trie in Python3.
There is a class node that contains
	label: name(alphabet) of the node
	data: if a complete word is present, that will be stored in data, otherwise None
	links: if the word is complete, we will sotre the links that it has appeared in
	Children: To keep track of the other nodes in the trie for the words
There is a class Trie that uses objects of the class Node to make a trie. It has methods
	add: to add a eord to the trie
	has_word: to check if the word is present in the trie or not
	getData: used to get links of the words that exist


Approach
There is a file 'links.txt' that contains the links we use to populate the trie for the search engine
I have used the BeautifulSoup library to parse the webpages.
The webpages are read, all non-words are removed using regex.
The remaining words, if not pronouns and prepositions are added to the trie.
This happens in the method 'scrap2Trie'

Then the user is aksed to enter a search query.
The search query is split, converted to lower case and its words are searched for in the trie.
For each word, the search result links are tallied. The link with the most occurances of the search terms will be displayed first.


Running Instructions
1. From the terminal, go to the location of the folder containing searchEngine.py and links.txt
2. Run the program as
	python3 searchEngine.py
3. When prompted to search, pless any key except 'n'
4. Enter search query
5. See results
6. Copy result and paste in your browser
7. If you have another search, press any key except 'n'