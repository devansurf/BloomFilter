#Devan A Vazquez    802-18-4051
#devan.vazquez@upr.edu

import sys, math, random as rand

#created salts when bloomFilter was created
hashSalts = []

def hashFunc(val, salt):
    return hash(hash(val) + salt)

def createBloomFilter(inputFile):
    global hashSalts

    emailList = []
    for i, line in enumerate(inputFile):
        #skip the header 'email'
        if i == 0: continue
        emailList.append(line)

    # -----/ equations / -----

    #number of items in the filter
    n = float(len(emailList))
    #probability for a false positive
    p = float(0.0000001)
    #number of bits in the filter
    m = math.ceil(-n*math.log(p) / (math.pow(math.log(2),2)))
    #number of hashes
    k = round(m/n * math.log(2))
    
    #create bloomFilter of size m
    bloomFilter = [False]*int(m)
  
    #depending on the amount k, create k amount of hash 'salts' to be used.
    for _ in range(k):
        hashSalts.append(rand.random())
   
    # for every email
    for i in range(len(emailList)):
        #for every hash function
        for j in range(k):
             # the salt will help convert the hash into a different hash given the same value, working as a different hash function
            hashVal = hashFunc(emailList[i], hashSalts[j]) % m
            #turn ON the bit
            bloomFilter[hashVal] = True

    return bloomFilter

def checkBloomFilter(bloomFilter, checkFile):
    emailList = []
    for i, line in enumerate(checkFile):
        #skip the header 'email'
        if i == 0: continue
        emailList.append(line)

    for i in range(len(emailList)):
        #Is True until proven otherwise
        probablyInDB = True
        #check every hash function 
        for j in range(len(hashSalts)):
             # the salt will help convert the hash into a different hash given the same value, working as a different hash function
            hashVal = hashFunc(emailList[i], hashSalts[j]) % len(bloomFilter)
            #check if bit is false, if it is, we know for a fact that that value is not in the DB
            if bloomFilter[hashVal] == False:
                probablyInDB = False
                break
        print(probablyInDB)
        print(emailList[i])

def main():
    #collect file directory as argument
    try:
        inputdir = sys.argv[1]
        checkdir = sys.argv[2]
    except:
        print("Could not open or access the directories given.\nFormat should be: python " + sys.argv[0] + " [InputFile Directory] [CheckFile Directory] ")
        return
    #read the file if it exists
    inputFile = open(inputdir, "r")
    checkFile = open(checkdir,"r")
    #create the bloomFilter object
    bloomFilter = createBloomFilter(inputFile)

    checkBloomFilter(bloomFilter, checkFile)

if __name__ == "__main__":
    main()