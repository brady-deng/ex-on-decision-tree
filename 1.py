import tree
import treeplot

def loaddata(filename):
    f = open(filename)
    lines = f.readlines()
    dat = [line.strip().split('\t') for line in lines]
    label = ['age','prescript','astigmatic','tearrate']

    return dat,label

if __name__ == "__main__":
    dat, label = loaddata("lenses.txt")
    lensestree = tree.createTree(dat,label)
    print(lensestree)
    treeplot.createPlot(lensestree)
