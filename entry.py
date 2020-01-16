import D_Polyns as dp
class entry:
    def __init__(self):
        self.entryList = []
        self.size = 0

    def addPolyn(self, f: dp):
        self.entryList.append(f)
        self.size += 1

    def appendEntryWRTMinMax(self, En, minmax:int = 0):
        if En is None: print("Null Entry")
        En: entry
        polynList = En.entryList
        for f in polynList:
            self.renewListWRTMinMax(f,minmax= minmax)

    def getSize(self):
        return self.size

    def getWholeEntry(self):
        return self.entryList

    def get(self, i:int):
        return self.entryList[i]

    def getSize(self):
        return self.size

    def isEmpty(self) -> bool:
        return self.size == 0

    # Need to prove this function is correct
    def renewListWRTMinMax(self, f: dp, minmax: int=0):
        """
        scan the whole list and create a new list in order to remove all polyns that is not the best bound
        :param f:
        :param minmax: 0 => min, 1 => max
        :return:
        """
        L = self.entryList
        if self.isEmpty():
            self.addPolyn(f)
            return

        newList = []
        removeList = []
        for l in range(len(L)):
            if minmax == 0:
                cmp = f.canReplace(L[l])
            elif minmax == 1:
                cmp = L[l].canReplace(f)

            if cmp == 1:
                removeList.append(l)
            elif cmp == -1:
                return
        self.size = 0
        for l in range(len(L)):
            if l not in removeList:
                newList.append(L[l])
                self.size += 1
        newList.append(f)
        self.entryList = newList

    def __len__(self):
        return len(self.entryList)

    def __str__(self):
        ret = "["
        for f in self.entryList:
            ret += str(f)+", "
        ret += "]"
        return ret

    def allAreLower(self, other):
        other: entry
        A = self.entryList # take the polyn list of lower bound
        B = other.entryList # take the polyn list of the upper bound
        for aE in A: # type: dp
            for bE in B: # type: dp
                if aE.canReplace(bE) == -1:    # if the lower bound is better than the upper bound, then there is a problem
                    return False
        return True

    def allEqual(self, other)->bool:
        other:entry
        A = self.entryList
        B = other.entryList
        if len(A) != len(B):
            return False
        exists = False
        for aE in A:
            for bE in B:
                if aE == bE:
                    exists = True
                    continue
            if exists is False:
                return False
        return True

    def __sub__(self, other):
        """
        substraction takes entry A and B,
        self-other gives that
            self.entryList is a list of polyns: A
            other.entryList is a list of polyns: B
        for any polyn in A
            for

        :param other:
        :return:
        """
        this = self.entryList
        other = other.entryList
        newEntry = entry()

        for f1 in this:
            for f2 in other:
                newEntry.renewListWRTMinMax(f1 - f2,minmax= 0)
        return newEntry

    def copy(self):
        ret = entry()
        for f in self.entryList:
            ret.addPolyn(f)
        return ret