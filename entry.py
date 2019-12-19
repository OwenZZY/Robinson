import D_Polyns as dp
class entry:
    def __init__(self):
        self.entryList = []

    def append(self, f: dp):
        self.entryList.append(f)

    def get(self, i:int):
        return self.entryList[i]

    def isEmpty(self) -> bool:
        return (len(self.entryList) == 0)

    # Need to prove this function is correct
    def renewList(self,f: dp):
        L = self.entryList
        if self.isEmpty():
            L.append(f)
            return

        newList = []
        removeList = []
        for l in range(len(L)):
            cmp = f.canReplace(L[l])
            if cmp == 1:
                removeList.append(l)
            elif cmp == -1:
                return


        for l in range(len(L)):
            if l not in removeList:
                 newList.append(L[l])
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
        for aE in A:
            aE # type: dp
            for bE in B:
                bE# type: dp
                aE.canReplace(bE)    # if the lower bound is better than the upper bound, then there is a problem
                return False
        return True