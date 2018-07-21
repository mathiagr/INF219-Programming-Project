# Random Forest Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np

# Importing the dataset
#d = pd.read_csv('datatf.csv')
#d = pd.read_csv('tf_num.csv')
d = pd.read_csv('tf_energi.csv')

#Replacing NaN with 0
d=d.fillna(0)

# =============================================================================
# energi = pd.DataFrame(pd.isnull(d['Energi']))
# d_test = d[energi["Energi"] == True] #Hvor vi har NaN som energimerkning
# d_train= d[energi["Energi"] == False] #Hvor vi har heltall som energimerkning
# 
# =============================================================================


#SHuffle
dataset = d.reindex(np.random.permutation(d.index))

#Removing columns
#dataset= dataset.drop('Rom', 1)
#dataset= dataset.drop('Postnr', 1)
#dataset= dataset.drop('Std', 1)


#postnr = pd.read_csv('tf2.csv').iloc[:, 1].values.tolist()

# =============================================================================
# # Encoding categorical data
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# 
# postnr = dataset.iloc[:, 1].values
# #df = pd.DataFrame(postnr)
# 
# 
# postnrenc = np.zeros((np.shape(d)[0],4));
# #1-on-N encoding of list
# #Postnummer
# indices = np.where(postnr=="5050-5075")
# postnrenc[indices,0] = 1
# indices = np.where(postnr=="<5025")
# postnrenc[indices,1] = 1
# indices = np.where(postnr=="5075-5100")
# postnrenc[indices,2] = 1
# indices = np.where(postnr==">5100")
# postnrenc[indices,3] = 1
# 
# #FJerner postnr kolonne fra originalt dataset
# dataset= dataset.drop('Postnr', 1)
# 
# post = pd.DataFrame(postnrenc)
# =============================================================================


#dataset = pd.concat([dataset, post], axis=1)


#Gjør mange kjøringer for å ta et snitt
n = 100
accuracies = []

for i in range(n):
    #randomiserer data
    #dataset = d.reindex(np.random.permutation(d.index))
    
    #Splitting data to Training and Test data
    
    split = 400
    #split = 250
    
    #Training data
    X = dataset.iloc[:split, 1:].values
    y = dataset.iloc[:split, 0].values
    
    #For predicting energimerking
    #X = d_train.iloc[:split, :-1].values
    #y = d_train.iloc[:split, -1].values
    
    
    #Data for testing
    pred = dataset.iloc[split:, 1:].values
    pred_targets = dataset.iloc[split:, 0].values
    
    #Energimerking:
    #pred = d_train.iloc[split:, 1:].values
    #pred_targets = d_train.iloc[split:, -1].values
    
    
    # Fitting Random Forest Regression to the dataset
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
    regressor.fit(X, y)
    
    
    # Predicting a new result
    y_pred = np.around(regressor.predict(pred))
    #y_pred = np.around(regressor.predict(d_test.iloc[:split, :-1].values))
    #differences =  (y_pred - pred_targets)

    #shuffle predictions og se om avviken blir dårligere   
    #np.random.shuffle(y_pred)
    
    differences =  np.absolute(y_pred - pred_targets)/pred_targets
    
    #differences =  np.absolute(y_pred - pred_targets)/pred_targets
    
    avg = np.average(differences)
    accuracies.append(avg)

sum = 0
for i in range(len(accuracies)):
    sum += accuracies[i]
    

    
    
print("Avg. error after " + str(n) + " runs: " + str(round(100*sum/len(accuracies),1)) + "%")    
