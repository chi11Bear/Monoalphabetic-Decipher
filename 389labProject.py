'''
Darren Joyner
Csci 389 Spring 19
Lab Project
'''


import re
import random
from math import log10


class cp(object):
    
    def dc(self,string):
        return string
        
    def ab(self,char):
        char = char.upper()
        arr = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,
           'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
           'V':21,'W':22,'X':23,'Y':24,'Z':25}
        return arr[char]

    def iAb(self,i):
        i = i%26
        arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        return arr[i]
        
    def remove_punctuation(self,text,filter='[^A-Z]'):
        return re.sub(filter,'',text.upper())

class replace(cp):
    
    def __init__(self,key='AJPCZWRLFBDKOTYUQGENHXMIVS'):
        assert len(key) == 26
        self.key = [k.upper() for k in key]
        self.revKey = ''

    def dc(self,string,keep_punct=False):
  
        # calculate the inverse key
        if self.revKey == '':
            for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ': 
                self.revKey += self.iAb(self.key.index(i))
        if not keep_punct: string = self.remove_punctuation(string)
        ret = ''      
        for c in string.upper():
            if c.isalpha(): ret += self.revKey[self.ab(c)]
            else: ret += c
        return ret
        
# load a file containing ngrams and counts, calculate log probabilities 
class nScore(object):

    def __init__(self,ngramfile,sep=' '):
        self.ngrams = {}
        for line in open(ngramfile):
            key,count = line.split(sep) 
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    # compute the score of text 
    def score(self,text):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score
    
'''
The list of quadgrams (very large file! too much paper.) used are in a zip file from http: //practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
'''
fitText = nScore('quadgrams.txt')

cipherText='TGZHHADTLHYUZBBZIXBCICJTTGCWXCOLTZWJHJCCVCVTWHTWOCTOLRRZFHTLTZHTZFHZJTGCDBWFYFGLZJVLTLHTWOLNCHZJFCTGCWPCOLBBLIWAJTWRTOLRRZFHTLTZHTZFHFLJDCXWTCJTZLBBQBLONCZJHZMCUCGLPCTWDOCLYAXTGCCJTZOCDWVQWRTOLRRZFHTLTZHTZFHZJTWFGAJYHLJVTWILYCCLFGFWJTOWBBCOTWHTWOCLXWOTZWJWRTGCCJTZOCVLTLHCTFGAJYHLBHWGLPCTWDCOCXBZFLTCVTWVCTCFTXWTCJTZLBTLIXCOZJNTGCLHHZNJICJTWRFGAJYHWJLJFWJTOWBBCOZHOCNZHTCOCVZJTGCZJVCSZJNHTOAFTAOCTGCHTWOCVHTLTZHTZFHVLTLFLJDCOCTOZCPCVUZTGTGCGCBXWRTGCZJVCSZJNHTOAFTAOCUCUZBBZIXBCICJTTGCJCFCHHLOQWXCOLTZWJHTWFOCLTCDBWFYHDLHCVWJFGAJYHWRHTLTZHTZFHVLTLTWOCXBZFLTCCLFGDBWFYWJTWHCPCOLBFWJTOWBBCOHTGOWANGTGCFWJHCJHAHICFGLJZHILJVTWCIDCVTGCFGLZJHTOAFTAOCZJDBWFYFGLZJWJTWTGCZJVCSZJNHTOAFTAOC'

cipherText = re.sub('[^A-Z]','',cipherText.upper())
letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore,parentkey = maxscore,letters[:]
cycle = 0

                                    
print ("*****************************CIPHER BREAKER********************************************\n")
print ("Please wait, may take several iterations up to 1000!")
print ("If the the correct result is seen or to exit at any time. Press ctrl+c to exit program.")
print ("Working...")

i = 0
while 1 and cycle <= 1000:
    i = i+1
    random.shuffle(parentkey)
    deciphered = replace(parentkey).dc(cipherText)
    parentscore = fitText.score(deciphered)
    count = 0
    
    while count < 1000: 
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        deciphered = replace(child).dc(cipherText)
        score = fitText.score(deciphered)
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
        
    # keep track of best score seen so far
    if parentscore > maxscore:
        maxscore,letters = parentscore,parentkey[:]
        print ('\nBest score so far:',abs(maxscore)),i
        ss = replace(letters)
        print ('    Best key: '+''.join(letters))
        print ('    Plaintext: '+ss.dc(cipherText))
        print ("\nWorking...")

    if cycle == 250:
        print ("\n25% Compeleted, working...")
    if cycle == 500:
        print ("\n50% Compeleted, working...")
    if cycle == 750:
        print ("\n75% Compeleted, working...")
        
    cycle = cycle + 1

print ("\n100% Compeleted")
print ('\n    Score: ', abs(maxscore)),i
print ('\n      key: '+''.join(letters))
print ('\nplaintext: '+ss.dc(cipherText))
     
