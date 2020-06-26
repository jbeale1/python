#
# Animal.py
# by J.Beale 6/25/2020
# based on openbookproject.net/py4fun/animal/animal.py

import string

class Node :
    "Node objects have a question, and  left and right pointer to other Nodes"
    "Terminal nodes have the animal as the question, with both left and right = None"
    def __init__ (self, question, left=None, right=None, prev=None) :
        self.question = question
        self.left     = left    # ("NO" branch)
        self.right    = right   # ("YES" branch)
        self.prev     = prev    # (prev node)

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

def indent(n) :        # print n spaces, and leave cursor on same line
    if (n > 0):
      sp = " " * n
      print(sp,end="")

def showRight(T,ind,order):
        indent(ind)
        print("Y: ",end="")
        showTree(T.right,ind+2,order)

def showLeft(T,ind,order):
        indent(ind)
        print("N: ",end="")
        showTree(T.left,ind+2,order)

# showTree(start node, indent level, R/[L] branch first)
def showTree (T, ind, order) :
    " recursively display binary question/answer tree"
    if (T == None) : return
    if (T.left == None) and (T.right == None) :
      print("(%s)" % T.question)
    else :
      print("%s ?" % T.question)
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
def buildTree () :
  global aCount
  global knowledge
  aCount = 0
  print("Reading database into binary tree...")
  line = input().lstrip().rstrip() # first line must be question
  # print("IN: " + line)
  if (line[-1:] != '?'):
      print("Input error: question must end in ?")
      exit()
  Q = line.rstrip("?").rstrip()
  knowledge = Node(Q) # initial question
  buildTreeR(knowledge)
  print(" === Database Read: %d animals\n" % aCount)

def buildTreeR (T) :
 global aCount
 n = 1
 hdr = " "
 while hdr != "--" :
  line = input().lstrip().rstrip()
  #print("IN %d: %s" % (n, line),end="")
  hdr = line[0:2]          # typically 'Y:' or 'N:'
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
      
  if (hdr == 'Y:'):  # answer to yes question
    if (Q):
      T.right = Node(Q)
      old = T
      T = T.right
      T.prev = old
      n += 1
    else:
      T.right = Node(animal)
  elif (hdr == 'N:'):  # answer to no question
    if (Q):
      T.left = Node(Q)
      old = T
      T = T.left
      T.prev = old
      n += 1
    else:
      T.left = Node(animal)
      T = T.prev
      n -= 1
  else:  # very first question      
     print("Input error: line must start with Y or N")
     exit()
     
   
# =============================================================

knowledge = Node("crow")  # first element: root of the tree (for now)
qCount = 0                # how many questions asked this round
aCount = 1                # how many animals we know

def main () :          
    "Guess the animal. Add a new Node for a wrong guess."
    global aCount    

    # showTree(knowledge,0,'p') # debug : show binary tree

    while 1 : # main loop
        print(" ---\n")

        print("Guess The Animal Game!")
        while 1 :
          ans = input ("Start game [enter]  Show DB [p]  Read DB [r]  Exit [x] :")
          print("")
          c = ans.lower()
          if (c == '') :
            break
          if (c == 'x') :
            exit(0)
          if (c == 'p' or c == 'q'):
            showTree(knowledge,0,c)
            print(" --- \n Total: %d animals\n" % aCount)
          if (c == 'r'):
            buildTree()


        qCount = 0                  # Beginning real questions now
        p = knowledge
        while p.left != None :            
            qCount += 1
            ans = yes(p.question+"? ", qCount)
            if ans :
                p = p.right
            else :
                p = p.left
    
        if yes("Is it a " + p.question + "? ", 0) :
            print("Yay! I got it in %d questions." % qCount)
            qCount = 0
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
        aCount += 1                # how many animals we know
        
# =====================================================================
if __name__ == "__main__" : main ()

