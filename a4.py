import random
import math


# To check if a number is prime
def isPrime(q):
    if(q > 1):
        for i in range(2, int(math.sqrt(q)) + 1):
            if (q % i == 0):
                return False 
        return True
    else :
        return False 
    
#To generate random prime less than N
def randPrime(N):
    primes = []
    for q in range(2,N+1):
        if(isPrime(q)):
            primes.append(q)
    return primes[random.randint(0,len(primes)-1)]

#pattern matching
def randPatternMatch(eps,p,x):
    N = findN(eps,len(p)) 
    q = randPrime(N)
    return modPatternMatch(q,p,x)
# complexity analysis 
# here q can be max N which is of the order of m/eps * log(m/eps)
# hence logq is of order log(m/eps)
# now tc and sc same as modPatternMatch but just replace logq by log(m/eps)
# Time = O((m + n) log m/eps)
# space = O(k + log n + log(m/εps))



#pattern matching with wildcard 
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)
# complexity analysis 
# here q can be max N which is of the order of m/eps * log(m/eps)
# hence logq is of order log(m/eps)
#now same as modPatternMatchWildcard but just replace logq by log(m/eps)
# Time = O((m + n) log m/eps)
#space = O(k + log n + log(m/εps))



# return appropriate N that satisfies the error bounds
def findN(eps,m):
    if m>16:
        return math.ceil(4*(math.log(26,2))*(m/eps)*(math.log(m/eps,2)+math.log((math.log(26,2)),2)))
    #O(log(m/eps)) tc becacue arithmetic operation on log(m/eps) bit numbers 
    # if x and y are decimal values of 26nary conversions of some 2 strings 
    #P(H(x)= H(y)) = (number of primes dividing |x-y| which are less than N /(π(N)) <= (number of primes dividing |x-y| /(π(N))
    #max value of |x-y| is when string corresponding to x is all Z's and that of y is all A's
    #hence, |x-y|<= 26**m -1 approximately 26**m
    # hence P<= (number of primes dividing 26**m / π(N)) ie P<= mlog26/π(N)
    # do mlog26/(π(N)) <= eps so that P<=eps 
    # using result: if (π(N))>k then N>4klogk   for k>16 (# proof of this at the end)
    # hence we get the returned N 
    return 54


# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
    if p=='':
        return []
    m= len(p)
    n= len(x)
    h1,h2=0,0
    ans = []
    for i in range(m):
        h1= (((26%q)*(h1%q))%q + (ord(p[i])%q- 65%q)%q)%q       #O(logq) tc  , O(logq) sc 
        h2= (((26%q)*(h2%q))%q + (ord(x[i])%q- 65%q)%q)%q       #O(logq) tc  , O(logq) sc 
        #initial hash values 
        # h1 = f(p)mod q 
        # h2 = f(x[0:m+1])mod q
        # note here that since maximum log q bits can be used I have taken care of every operation to use less than log q bits by taking %q before all binary operations . h1 and h2 are always < q hence always stored in < logq bits 

    mult = 1 
    for i in range(m-1):
        mult = ((mult%q) * (26%q))%q           #O(logq) tc 
    
    if h1== h2:
        ans.append(0)
    for i in range(1,n-m+1):
        h2= ((h2 - ((ord(x[i-1])%q- 65%q)*mult)%q)*26 + (ord(x[i-1+m])%q- 65%q))%q         #O(logq) tc 
        #basically concept of rolling hash to get hash value of next m string interval in O(1) time 
        if h1== h2:
            ans.append(i)
    return ans 
#time complexity analysis
#O(logq) operations in m and n-m+1 size loops 
#hence O((m+n)logq) time
#space comlexity analysis 
#O(logn) bits of space is needed to store the current index while scanning the document, O(logq) bits for storing hash values, O(k) k is the space required for output list L
# hence O(logn + logq + k ) space 


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
    if p=='':
        return []
    m= len(p)
    n= len(x)
    h1,h2=0,0
    ans = []
    j=0
    #h1 and h2 caluculated similarly as in modPatternMatch but with slight adjustment 
    #adjustment is that calculation is done according to p[j]= x[i+j]
    # h1 = f(p)mod q 
    # h2 = f(x[0:m+1])mod q
    for i in range(m):        #time = O(m*logq) assuming that basic arithmetic operations on b-bit numbers take Θ(b) time.
        if p[i]!= '?':
            h1= (((26%q)*(h1%q))%q + (ord(p[i])%q- 65%q)%q)%q           #O(logq) tc 
            h2= (((26%q)*(h2%q))%q + (ord(x[i])%q- 65%q)%q)%q           #O(logq) tc 
        else :
            j= i
            h1= (((26%q)*(h1%q))%q + (ord(x[i])%q- 65%q)%q)%q            #O(logq) tc 
            h2= (((26%q)*(h2%q))%q + (ord(x[i])%q- 65%q)%q)%q            #O(logq) tc 
        # note here that since maximum log q bits can be used i have taken care of every operation to use less than log q bits by taking %q before all binary operations 
        
    mult = 1 
    for i in range(m-1):
        mult = ((mult%q) * (26%q))%q        #O(logq) tc 
        
    mult2 = 1
    for i  in range(m-j-1):
        mult2 = ((mult2%q) * (26%q))%q        #O(logq) tc 
    
    if h1== h2:
        ans.append(0)
    for i in range(1,n-m+1):     #time O((n-m)*logq)
        h2= (((h2 - ((ord(x[i-1])%q- 65%q)*(mult))%q)*26)%q + (ord(x[i-1+m])%q- 65%q))%q       #O(logq) tc 
        h1 = (h1 - ((ord(x[i-1+j])%q- 65%q)*(mult2))%q + ((ord(x[i+j])%q- 65%q)*(mult2))%q)%q        #O(logq) tc 
        # note here that since maximum log q bits can be used i have taken care of every operation to use less than log q bits by taking %q before all binary operations 
        if h1== h2:
            ans.append(i)        #O(1)
    return ans 
#same time and space complexity as modPatternMatch since finite number of operations are added(hence only difference in constancts of time complexity)


# proof of the result: if (π(N))>k then N>4klogk  for k >16
# it can proved by plotting π(4klogk) and k on desmos but mthematical proof is given below 
# since π(x) is increasing , if we prove π(y)>z then π(x)>z if x>y
# π(4klogk)>= 4klogk/2log(4klogk)
# π(4klogk) >k if 4klogk/2log(4klogk)>k
# ie logk> log4 + log(logk)
# ie k>4logk 
# which is true for k>16 (because x/logx is an increasing function)
# hence proved
# for k<=16 chose N st π(N)>16 ie N>53 (taken 54 here)
