ALPHABET = '$abcdefghijklmnopqrstuvwxyz'


class Node(object):

    def __init__(self, root=None):
        self.children = [None] * 27
        self.suffixLink = root


class SuffixEdge(object):

    def __init__(self, startIndex, endIndex='end'):
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.nextNode = None


class SuffixTree(object):

    def __init__(self, inputStr):
        self.inputStr = inputStr
        self.root = Node()
        self.remaining = 0
        self.lastNode = None # weak ref
        self.activeNode = self.root
        self.activeEdge = -1
        self.activeLength = 0

    def bwt(self):
        bwtStr = ''
        length = len(self.inputStr)
        nodeStack = []
        nodeStack.append((self.root, 0))
        while len(nodeStack):
           node, depth = nodeStack[-1]
           nodeStack.pop()
           if not any(node.children):
               pos = length - depth - 1
               bwtStr = self.inputStr[pos] + bwtStr

           for child in node.children:
               if not child:
                   continue
               if child.endIndex == 'end':
                   newDepth = depth + length - child.startIndex
               else:
                   newDepth = depth + child.endIndex - child.startIndex + 1
               nodeStack.append((child.nextNode, newDepth))
        return bwtStr

    def creatSuffixTree(self):
        for i, c in enumerate(self.inputStr):
            self.remaining += 1
            self.lastNode = None
            while self.remaining > 0:
                if self.activeLength == 0:
                    self.activeEdge = i
                ix = ALPHABET.index(self.inputStr[self.activeEdge])
                if not self.activeNode.children[ix]:
                    edge = SuffixEdge(i)
                    edge.nextNode = Node(self.root)
                    edge.nextNode.suffixLink = self.activeNode
                    self.activeNode.children[ix] = edge
                    if (self.lastNode is not None):
                        self.lastNode.suffixLink = self.activeNode
                        self.lastNode = None
                else:
                    ix = ALPHABET.index(self.inputStr[self.activeEdge])
                    nextEdge = self.activeNode.children[ix]
                    start = nextEdge.startIndex
                    end = nextEdge.endIndex
                    length = (end if end != 'end' else i) - start + 1
                    ifLengthEnough = self.activeLength >= length
                    if ifLengthEnough:
                        self.activeEdge += length
                        self.activeLength -= length
                        self.activeNode = nextEdge.nextNode
                        continue
                    currCharIndex = nextEdge.startIndex + self.activeLength
                    currChar = self.inputStr[currCharIndex]
                    if currChar == c:
                        if self.lastNode and self.activeNode != self.root:
                            self.lastNode.suffixLink = self.activeNode
                            self.lastNode = None
                        self.activeLength += 1
                        break
                    splitEnd = nextEdge.startIndex + self.activeLength - 1
                    split = SuffixEdge(nextEdge.startIndex, splitEnd)
                    split.nextNode = Node(self.root)
                    ix = ALPHABET.index(self.inputStr[self.activeEdge])
                    self.activeNode.children[ix] = split
                    split.nextNode.suffixLink = self.activeNode
                    ix = ALPHABET.index(c)
                    edge = SuffixEdge(i)
                    edge.nextNode = Node(self.root)
                    split.nextNode.children[ix] = edge
                    nextEdge.startIndex += self.activeLength
                    ix = ALPHABET.index(self.inputStr[nextEdge.startIndex])
                    split.nextNode.children[ix] = nextEdge
                    if self.lastNode:
                        self.lastNode.suffixLink = split.nextNode
                    self.lastNode = split.nextNode
                self.remaining -= 1
                if self.activeNode == self.root and self.activeLength > 0:
                    self.activeLength -= 1
                    self.activeEdge = i - self.remaining + 1
                elif self.activeNode != self.root:
                    self.activeNode = self.activeNode.suffixLink

ins = SuffixTree("abc$")
ins.creatSuffixTree()