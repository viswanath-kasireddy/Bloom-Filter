# Python3 program Miller-Rabin randomized primality test
# Copied from geeksforgeeks: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
import random 
#'''
# Utility function to do 
# modular exponentiation. 
# It returns (x^y) % p 

#Modular exponentiation
#Returns (x^y) % p

def power(x, y, p): 
	
	#Placeholder 
	res = 1; 
	
	x = x % p; 
	while (y > 0): 
		
		#If y is odd, multiply x with result 
		if (y & 1): 
			res = (res * x) % p; 

		#y is even now, divide by 2 with bit shifting, exponentiate x and modularize 
		y = y>>1;
		x = (x * x) % p; 
	
	return res; 

#Miller-Rabin test to determine if n is prime
def millerTest(d, n): 
	
	#Pick a random number in [2..n-2], making sure n > 4
	a = 2 + random.randint(1, n - 4); 

	#Calculate a^d % n 
	x = power(a, d, n); 

	if (x == 1 or x == n - 1): 
		return True; 

	# Keep squaring x while one of the following does not occur
	# (i) d does not reach n-1 
	# (ii) (x^2) % n is not 1 
	# (iii) (x^2) % n is not n-1 
	while (d != n - 1): 
		x = (x * x) % n; 
		d *= 2; 

		if (x == 1): 
			return False; 
		if (x == n - 1): 
			return True; 

	# Return overall 
	return False; 

#Probabalistic nature of the Miller-Rabin test means we call it for K trials to assess higher accuracy 
def isPrime( n, k): 
	
	# Corner cases 
	if (n <= 1 or n == 4): 
		return False; 
	if (n <= 3): 
		return True; 

	# Find r such that n = 2^d * r + 1 for some r >= 1 
	d = n - 1; 
	while (d % 2 == 0): 
		d //= 2; 

	#Run test k times
	for i in range(k): 
		if (millerTest(d, n) == False): 
			return False; 

	return True; 


#Get a random triple (p, a, b) where p is prime and a and b are numbers betweeen 2 and p-1
def get_random_hash_function():
    n = random.getrandbits(64)
    if n < 0: 
        n = -n 
    if n % 2 == 0:
        n = n + 1
    while not isPrime(n, 20):
        n = n + 1
    a = random.randint(2, n-1)
    b = random.randint(2, n-1)
    return (n, a, b)

# hash function for a number
def hashfun(hfun_rep, num):
    (p, a, b) = hfun_rep
    return (a * num + b) % p

# hash function for a string.
def hash_string(hfun_rep, hstr):
    n = hash(hstr)
    return hashfun(hfun_rep, n)    

#Using the book "The Great Gatsby" and extracting all words that are 5 letters or longer
filename ='/Users/viswakasireddy/Downloads/great-gatsby-fitzgerald.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_gg = list(filter(lambda s: len(s) >= 5, words))
#print(len(longer_words_gg))
#Counting word frequencies 
word_freq_gg = {}
for elt in longer_words_gg:
    if elt in word_freq_gg:
        word_freq_gg[elt] += 1
    else:
        word_freq_gg[elt] = 1
		
#Printing word frequencies
#print(len(word_freq_gg))

#Using the book "War and Peace" and extracting all words that are 5 letters or longer
filename = '/Users/viswakasireddy/Downloads/war-and-peace-tolstoy.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_wp = list(filter(lambda s: len(s) >= 5, words))
#print(len(longer_words_wp))
word_freq_wp = {}
for elt in longer_words_wp:
    if elt in word_freq_wp:
        word_freq_wp[elt] += 1
    else:
        word_freq_wp[elt] = 1

#Printing word frequencies
#print(len(word_freq_wp))


#Bloom filter class
class BloomFilter:
    def __init__(self, nbits, nhash):
		#Initialize all bits in the filter to false
        self.bits = [False]*nbits
        self.m = nbits
        self.k = nhash
        #Get k randdom hash functions
        self.hash_fun_reps = [get_random_hash_function() for i in range(self.k)]
    
    #Insert a word in a Bloom filter.
    def insert(self, word):
        for i in range (len(self.hash_fun_reps)):
            finalHash = hash_string(self.hash_fun_reps[i],word)
            column = finalHash % len(self.bits)
            self.bits[column] = True
        
        
    #Check if a word is already contained in the Bloom filter
    def member(self, word):
        for i in range (len(self.hash_fun_reps)):
            finalHash = hash_string(self.hash_fun_reps[i],word)
            column = finalHash % len(self.bits)
            if self.bits[column] == True:
                return True
        return False
        
        
#Count exactly how many words the two books (The Great Gatsby and War and Peace) have in common
all_words_gg = set(longer_words_gg)
exact_common_wc = 0
for word in longer_words_wp:
    if word in all_words_gg:
        exact_common_wc = exact_common_wc + 1
		#print(f'Exact common word count = {exact_common_wc}')

#Find out how many words the books have in common using the bloom filter
bf = BloomFilter(100000, 5)


for word in longer_words_gg:
    bf.insert(word)
    
for word in longer_words_gg:
    assert (bf.member(word)), f'Word: {word} should be a member'

common_word_count = 0
for word in longer_words_wp:
    if bf.member(word):
        common_word_count= common_word_count + 1
		#print(f'Number of common words of length >= 5 equals : {common_word_count}')
assert ( common_word_count >= exact_common_wc)
print("Bloom filter count is", common_word_count)
print("Exact word count is", exact_common_wc)
print("We can see", common_word_count, ">=", exact_common_wc, "proving the Bloom filter has false positives")
#print('Bloom filter count is', common_word_count, '>=', exact_common_wc, "which is the exact word count") 



