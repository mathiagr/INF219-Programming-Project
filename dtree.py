
# Code from Chapter 12 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008, 2014

import numpy as np
import random
import itertools
class dtree:
    """ A basic Decision Tree"""
	
    def __init__(self):
        """ Constructor """

    def read_data(self,filename):
        fid = open(filename,"r")
        data = []
        d = []
        for line in fid.readlines():
            d.append(line.strip())
        for d1 in d:
            data.append(d1.split(","))
        fid.close()
    
        
        #List of features 
        self.featureNames = [i for i in range(len(data[0])-1)]
        self.classes = []
        
            
       #Not dealing with '?' since we load newdata.data which is already handled by replacing with predicted values   
        data = [data[i] for i in range(len(data)) if i == 0 or data[i] != data[i-1]]
         
         #Shufling data
        data = random.sample(data, len(data)) 
 
         #Splitting data into classes and data
        for d in range(len(data)):
            self.classes.append(data[d][0])
            data[d] = data[d][1:]      
           
          


        #return data_filtered,self.classes,self.featureNames #For deleting '?'
        return data,self.classes,self.featureNames #For replacing '?' or doing nothing
        #return data_filtered, self.classes, missing, classes_missing, self.featureNames  #For predicting '?'


    def classify(self,tree,datapoint):

        if type(tree) == type("string"):
			# Have reached a leaf
            return tree
        else:
            a = list(tree.keys())[0]
            for i in range(len(self.featureNames)):
                if self.featureNames[i]==a:
                    break
			
            try:
                t = tree[a][datapoint[i]]
                return self.classify(t,datapoint)
            except:
                return None
        

    def classifyAll(self,tree,data):
        results = []
        for i in range(len(data)):
            results.append(self.classify(tree,data[i]))
        return results


    def make_tree(self,data,classes,featureNames,maxlevel=-1,level=0):
        """ The main function, which recursively constructs the tree"""


        #EARLY STOPPING
# =============================================================================
        #First find the class which occurs the most time
        #Then check if the ratiio is above the threshold by dividing on total nr of classes
        #Finding the most frequently occurring value in for feature nr. 10 (where '?' occurs)
        occurs = {}
        for d in range(len(classes)): 
            if classes[d] not in occurs:
                occurs[classes[d]] = 1
            else:
                occurs[classes[d]]+=1
        max_key = max(occurs, key=occurs.get)
        #print(occurs.get(max_key),len(classes)) #occurences of max key & length ob subtree (classes/nodes under it)
        ratio = occurs.get(max_key)/len(classes)
        if ratio>=0.65:
                    #if ratio<1:
                    #    print("Initiated early stopping: ")
                    #    print(ratio,max_key) #Relative occurences of the maximal occuring key
                    return max_key

     
        else:
            nData = len(data)
            nFeatures = len(data[0])
            
    
            try: 
                self.featureNames
            except:
                self.featureNames = featureNames
            
            # List the possible classes
            newClasses = []
            for aclass in classes:
                if newClasses.count(aclass)==0:
                    newClasses.append(aclass)
    
            # Compute the default class (and total entropy)
            frequency = np.zeros(len(newClasses))
    
            totalEntropy = 0
            #  totalGini = 0
            index = 0
            for aclass in newClasses:
                frequency[index] = classes.count(aclass)
                totalEntropy += self.calc_entropy(float(frequency[index])/nData)
                #  totalGini += (float(frequency[index])/nData)**2
        
                index += 1
    
            #  totalGini = 1 - totalGini
            default = classes[np.argmax(frequency)]
    
            if nData==0 or nFeatures == 0 or (maxlevel>=0 and level>maxlevel):
                # Have reached an empty branch
                return default
            elif classes.count(classes[0]) == nData:
                # Only 1 class remains
                return classes[0]
            else:
    
                # Choose which feature is best      
                gain = np.zeros(nFeatures)
                #ggain = np.zeros(nFeatures)
    
                for feature in range(nFeatures):
                    g = self.calc_info_gain(data,classes,feature)
                    gain[feature] = totalEntropy - g
                    #  ggain[feature] = totalGini - gg
                    
                bestFeature = np.argmax(gain)

                tree = {featureNames[bestFeature]:{}}
    
                # List the values that bestFeature can take
                values = []
                for datapoint in data:
                    # From github: https://github.com/tback/MLBook_source/blob/master/6%20Trees/dtree.py
                    if datapoint[bestFeature] not in values:
                    # From book website
                    #  if datapoint[feature] not in values:
                        values.append(datapoint[bestFeature]) 
    
                for value in values:
                    # Find the datapoints with each feature value
                    newData = []
                    newClasses = []
                    index = 0
                    for datapoint in data:
                        if datapoint[bestFeature]==value:
                            if bestFeature==0:
                                newdatapoint = datapoint[1:]
                                newNames = featureNames[1:]
                            elif bestFeature==nFeatures:
                                newdatapoint = datapoint[:-1]
                                newNames = featureNames[:-1]
                            else:
                                newdatapoint = datapoint[:bestFeature]
                                newdatapoint.extend(datapoint[bestFeature+1:])
                                newNames = featureNames[:bestFeature]
                                newNames.extend(featureNames[bestFeature+1:])
                            newData.append(newdatapoint)
                            newClasses.append(classes[index])
                        index += 1
    
                    # Now recurse to the next level 
                    subtree = self.make_tree(newData,newClasses,newNames,maxlevel,level+1)
                    
                    # And on returning, add the subtree on to the tree
                    tree[featureNames[bestFeature]][value] = subtree
                return tree

    def printTree(self,tree,name):
    
        if type(tree) == dict:
            print (name, list(tree.keys())[0])
            for item in list(tree.values())[0].keys():
                print (name, item)
                self.printTree(list(tree.values())[0][item], name + "\t")
        else:
            print (name, "\t->\t", tree)

    def calc_entropy(self,p):
        if p!=0:
            return -p * np.log2(p)
        else:
            return 0

    def calc_info_gain(self,data,classes,feature):
        gain = 0
        nData = len(data)
        # List the values that feature can take
        values = []
        #print(feature)
        for datapoint in data:            
            if datapoint[feature] not in values:
                    values.append(datapoint[feature])
    
        featureCounts = np.zeros(len(values))
        entropy = np.zeros(len(values))
        valueIndex = 0
        # Find where those values appear in data[feature] and the corresponding class
        for value in values:
            dataIndex = 0
            newClasses = []
            for datapoint in data:
                if datapoint[feature]==value:
                    featureCounts[valueIndex]+=1
                    newClasses.append(classes[dataIndex])
                dataIndex += 1
    
            # Get the values in newClasses
            classValues = []
            for aclass in newClasses:
                if classValues.count(aclass)==0:
                    classValues.append(aclass)
            classCounts = np.zeros(len(classValues))
            classIndex = 0
            for classValue in classValues:
                for aclass in newClasses:
                    if aclass == classValue:
                        classCounts[classIndex]+=1
                classIndex += 1
    
            for classIndex in range(len(classValues)):
                entropy[valueIndex] += self.calc_entropy(float(classCounts[classIndex]) / sum(classCounts))
            gain += float(featureCounts[valueIndex])/nData * entropy[valueIndex]
            valueIndex += 1
        return gain