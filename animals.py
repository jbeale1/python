#
# Animal.py
# by J.Beale 6/25/2020
# based on openbookproject.net/py4fun/animal/animal.py

import string

class Node :
    "Node objects have a question, and  left and right pointer to other Nodes"
    "Terminal nodes have the animal as the question, with both left and right = None"
    def __init__ (self, question, left=None, right=None, prev=None, depth=None) :
        self.question = question
        self.left     = left    # ("NO" branch)
        self.right    = right   # ("YES" branch)

def yes (ques, n) :
    "The user answers 'yes' or something similar. Otherwise it's a no"
    while 1 :
        if (n > 0) :
          print("Q %d: " % n, end="")
        ans = input (ques)
        ans = ans[0:1].lower() # check only the first letter 

        if ans == 'y' : return True
        else          : return False

# ==========================================================

showType = 0 # what showTree displays: 0=both, 1=Questions only, 2= Animals only

def indent(n) :        # print n spaces, and leave cursor on same line
    if (n > 0) and (showType == 0):
    #if (n > 0) :
      sp = " " * n
      print(sp,end="")

def showRight(T,ind,order):
        indent(ind)
        if (showType == 0):
          print("Y: ",end="")
        showTree(T.right,ind+2,order)

def showLeft(T,ind,order):
        indent(ind)
        if (showType == 0):
          print("N: ",end="")
        showTree(T.left,ind+2,order)

# showTree(start node, indent level, R/[L] branch first)
def showTree (T, ind, order) :
    " recursively display binary question/answer tree"
    if (T == None) : return
    if (T.left == None) and (T.right == None):
      if (showType != 1):
        print("(%s)" % (T.question) ) # this is an animal
    else :
      if (showType != 2):
        # print("%s ? %d,%d" % (T.question,T.left==None,T.right==None))
        print("%s ?" % (T.question))
      if (order == 'p'):
        if (T.right != None):
          showRight(T,ind,order)        
        if (T.left != None):
          showLeft(T,ind,order)
      else:
        if (T.left != None):
          showLeft(T,ind,order)
        if (T.right != None):
          showRight(T,ind,order)        

# =============================================================
tStack = []        # stack object to track depth of tree

class eRef(object):            # reference to tree element
    def __init__(self, value):
         self.value = value
# =============================================================

def getLine() :  # read in one line describing binary tree
  global aCount, qCount
  
  line = input().lstrip().rstrip()  # read in one line: either Question or Animal
  hdr = line[0:2]          # typically 'Y:' or 'N:'
  # n = nN                   # read a new line, so "next" becomes now
  if (hdr == "--"):  # end of file
      return
    
  rest = line[2:].lstrip()
  animal = ""
  Q = ""
 
  if (rest[0:1] == '(') :
      animal = rest[1:-1]  # name of animal
      #print(" (Animal)")
      aCount += 1          # how many animals we know
  else:
      if (rest[-1:] != '?'):
          print("Input error: question must end in ?")
          exit()
      Q = rest.rstrip("?").rstrip()
      #print(" (Question)")
      qCount += 1
      #nN = n + 1      # depth of next line
  return(hdr,Q,animal)


def buildTree () :
  global aCount, qCount
  global knowledge
  global tStack
  global nN     # depth of next line read
  aCount = 0
  qCount = 0
  print("Reading database into binary tree...")
  line = input().lstrip().rstrip() # first line must be question
  # print("IN: " + line)
  if (line[-1:] != '?'):
      print("Input error: question must end in ?")
      exit()
  Q = line.rstrip("?").rstrip()
  qCount += 1
  knowledge = Node(Q) # initial question
  knowledge.depth = 0
  n = 0
  nN = 1
  tStack.append(eRef(knowledge)) # every question adds 1 layer depth to tree

  buildTreeR(knowledge) # for "Y" answer
  print(" === Database Read: %d animals %d questions\n" % (aCount,qCount))

def doLine(T, hdr, Q, animal) :  # distribute data into binary tree structure
  if (hdr == 'Y:'):  # if answer to prev. question was yes
    if (Q):
      T.right = Node(Q) # and it's a new question
      T = T.right       # move T to next level of tree
      buildTreeR(T)    # Question: recursively build tree
    else:
      T.right = Node(animal) # it's a terminal node (animal)
      # buildTreeR(T)
      return
  elif (hdr == 'N:'):  # if answer to prev q. was no    
    if (Q):
      T.left = Node(Q)
      T = T.left
      buildTreeR(T)    # Question: recursively build tree
    else:                    # it's an animal
      T.left = Node(animal)
      return
  else:  # very first question ?
     print("Input error: line must start with Y or N")
     exit()

def buildTreeR (T) :
  (hdr,Q,animal) = getLine()  # read in one line (eg. "Y:" answer)
  doLine(T,hdr,Q,animal)        # save into tree
  (hdr,Q,animal) = getLine()  # read in one line (eg. "N:" answer)
  doLine(T,hdr,Q,animal)        # save into tree
     
# =============================================================

knowledge = Node("crow")  # first element: root of the tree (for now)
qCount = 0                # how many questions asked this round
aCount = 1                # how many animals we know

def main () :          
    "Guess the animal. Add a new Node for a wrong guess."
    global aCount, qCount, showType

    # showTree(knowledge,0,'p') # debug : show binary tree

    while 1 : # main loop
        print(" ---\n")

        print("Guess The Animal Game!")
        while 1 :
          ans = input("Start game [enter]  Show DB [p]  Read DB [r]  Exit [x] :").lstrip()
          print("")
          c = ans.lower()
          if (c == '') :
            break
          if (c == 'x') :
            exit(0)
          if (c == 'p' or c == 't'):
            showType = 0
            showTree(knowledge,0,c)
            print(" --- \n Total: %d animals %d questions\n" % (aCount,qCount))
          elif (c == 'q'):
            showType = 1
            showTree(knowledge,0,c)
            print(" --- \n Total: %d questions\n" % (qCount))
          elif (c == 'a'):
            showType = 2
            showTree(knowledge,0,c)
            print(" --- \n Total: %d animals\n" % (aCount))
          elif (c == 'r'):
            buildTree()

        uqCount = 0                  # Beginning real questions now
        p = knowledge
        while p.left != None :            
            uqCount += 1
            ans = yes(p.question+"? ", uqCount)
            if ans :
                p = p.right
            else :
                p = p.left
    
        if yes("Is it a " + p.question + "? ", 0) :
            print("Yay! I got it in %d questions." % uqCount)
            uqCount = 0
            continue
        animal   = input ("What is the animal's name? ")
        question = input ("What question would distinguish a %s from a %s? "
                                  % (animal,p.question))
        p.left     = Node(p.question)
        p.right    = Node(animal)
        p.question = question
    
        if not yes ("If the animal were %s the answer would be? " % animal, 0) :
            (p.right, p.left) = (p.left, p.right)
        print("Ok, now I know about a %s." % animal)
        print("\n")
        aCount += 1                # how many animals in database
        qCount += 1                # how many questions in database
        
# =====================================================================
if __name__ == "__main__" : main ()

