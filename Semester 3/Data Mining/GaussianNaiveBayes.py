import numpy as np
import math

class GNB:
    def __init__(self):
        self.classes = []
        self.classFreq = {}
        self.classProba = {}
        self.means = {}
        self.std = {}


    def seggregateByClasses(self, X, y):
        self.classes = np.unique(y)
        classIndex = {}
        segregatedData = {}
        cls, counts = np.unique(y, return_counts=True)
        self.classFreq = dict(zip(cls, counts))
        
        total = sum(list(self.classFreq.values()))
        for classType in self.classes:
            classIndex[classType] = np.argwhere(y==classType)
            segregatedData[classType] = X[classIndex[classType], :]
            self.classFreq[classType] = self.classFreq[classType]/total
        return segregatedData

    def fit(self, X, y):
        seggreagatedX = self.seggregateByClasses(X.to_numpy(), y.to_numpy())
        for classType in self.classes:
            self.means[classType] = np.mean(seggreagatedX[classType], axis=0)[0]
            self.std[classType] = np.std(seggreagatedX[classType], axis=0)[0]

    def calculateProba(self, x, mean, stdev):
        numerator = math.exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
        return (1 / (math.sqrt(2 * math.pi) * stdev)) * numerator

    def predictProba(self, x):
        self.classProba = {cls:math.log(self.classFreq[cls], math.e) for cls in self.classes}
        for cls in self.classes:
            for i in range(len(self.means)):
                self.classProba[cls]+=math.log(self.calculateProba(x[i], self.means[cls][i], self.std[cls][i]), math.e)
        self.classProba = {cls: math.e**self.classProba[cls] for cls in self.classProba}
        return self.classProba

    def predict(self, X):
        pred = []
        Xarr = X.to_numpy()
        for x in Xarr:
            predictedClass = None
            maxProba = 0
            for cls, prob in self.predictProba(x).items():
                if prob>maxProba:
                    maxProba = prob
                    predictedClass = cls
            pred.append(predictedClass)
        return pred

    def accuracy(self, yTest, yPred):
        accuracy = np.sum(yTest == yPred) / len(yTest)
        return accuracy

class CGNB:
    def __init__(self, Xdf, Ydf, categoricalColumns = []):
        self.categoricalColumns = categoricalColumns
        XCategorical = Xdf[categoricalColumns]
        XNumerical = Xdf.drop(categoricalColumns, axis=1, inplace=False)
        self.XCat = XCategorical.to_numpy()
        self.XNum = XNumerical.to_numpy()
        self.y = Ydf.to_numpy()
        self.classes = np.unique(self.y)
        self.classFreq = {}
        self.classProba = {}
        self.means = {}
        self.std = {}

    def seggregateByClasses(self, X, y):
        classIndex = {}
        segregatedData = {}
        cls, counts = np.unique(y, return_counts=True)
        self.classFreq = dict(zip(cls, counts))
        
        total = sum(list(self.classFreq.values()))
        for classType in self.classes:
            classIndex[classType] = np.argwhere(y==classType)
            segregatedData[classType] = X[classIndex[classType], :]
            self.classFreq[classType] = self.classFreq[classType]/total
        return segregatedData

    def fit(self):
        seggreagatedXNumeric = self.seggregateByClasses(self.XNum, self.y)
        for classType in self.classes:
            self.means[classType] = np.mean(seggreagatedXNumeric[classType], axis=0)[0]
            self.std[classType] = np.std(seggreagatedXNumeric[classType], axis=0)[0]
        seggreagatedXcategorical = self.seggregateByClasses(self.XCat, self.y)
        
        

        self.catProba = {}
        for classType in self.classes:
            for i in range(len(self.categoricalColumns)):
                cat, counts = np.unique(seggreagatedXcategorical[classType][0][:, i], return_counts=True)
                catFreqClass = dict(zip(cat, counts))
                
                cat, counts = np.unique(self.XCat[:, i], return_counts=True)
                catFreq = dict(zip(cat, counts))
                
                for key in catFreqClass.keys():
                    if classType not in self.catProba:
                        self.catProba[classType] = {}
                    if i not in self.catProba[classType]:    
                        self.catProba[classType][i] = {}
                    self.catProba[classType][i][key] = (catFreqClass[key]/catFreq[key])/(catFreq[key]/len(self.y))
        

    def calculateProba(self, x, mean, stdev):
        exponent = math.exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
        return (1 / (math.sqrt(2 * math.pi * stdev ** 2))) * exponent

    def predictProba(self, x):
        catx = [i for j, i in enumerate(x) if j in self.catagoricalColumnIndexes]
        numx = [i for j, i in enumerate(x) if j not in self.catagoricalColumnIndexes]
        self.classProba = {cls:math.log(self.classFreq[cls], math.e) for cls in self.classes}
        for cls in self.classes:
            for i in range(len(self.means)):
                self.classProba[cls]+=math.log(self.calculateProba(numx[i], self.means[cls][i], self.std[cls][i]), math.e)
        for cls in self.classes:
            for i in range(len(catx)):
                try:
                    prob = self.catProba[cls][i][int(catx[i])]
                    self.classProba[cls]+=math.log(prob, math.e)
                except:
                    self.classProba[cls] = self.classProba[cls]       
        self.classProba = {cls: math.e**self.classProba[cls] for cls in self.classProba}
        return self.classProba

    def predict(self, Xdf):
        pred = []
        self.catagoricalColumnIndexes = []
        for i in self.categoricalColumns:
            
            self.catagoricalColumnIndexes.append(Xdf.columns.get_loc(i))
        
        self.catagoricalColumnIndexes.sort()
        
        
        X = Xdf.to_numpy()
        for x in X:
            predictedClass = None
            maxProba = 0
            for cls, prob in self.predictProba(x).items():
                if prob>maxProba:
                    maxProba = prob
                    predictedClass = cls
            pred.append(predictedClass)
        return pred

    def accuracy(self, yT, yP):
        accuracy = np.sum(yT == yP) / len(yT)
        return accuracy