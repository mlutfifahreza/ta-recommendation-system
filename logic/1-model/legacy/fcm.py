import pandas as pd # reading all required header files
import numpy as np
import random
import operator
import math
import matplotlib.pyplot as plt 
from scipy.stats import multivariate_normal 
from sklearn.datasets import load_iris

# import dataset
iris = load_iris()
df = pd.DataFrame(iris.data)
print(df.head())

# define parameters
n = len(df) #number of data
k = 3 #number of clusters
d = 4 #dimension of cluster
m = 2 # m parameter
MAX_ITERS = 12 #number of iterations

# visualize
plt.figure(0,figsize=(5,5))                #scatter plot of sepal length vs sepal width                              
plt.scatter(list(df.iloc[:,0]), list(df.iloc[:,1]), marker='o')       
plt.axis('equal')                                                                 
plt.xlabel('Sepal Length', fontsize=16)                                                 
plt.ylabel('Sepal Width', fontsize=16)                                                 
plt.title('Sepal Plot', fontsize=25,color='b')                                            
plt.grid()                                                    
#plt.show()
plt.savefig('test_input_sepal.png')
plt.figure(1,figsize=(5,5))                #scatter plot of sepal length vs sepal width                              
plt.scatter(list(df.iloc[:,2]), list(df.iloc[:,3]), marker='o')       
plt.axis('equal')                                                                 
plt.xlabel('petal Length', fontsize=16)                                                 
plt.ylabel('petal Width', fontsize=16)                                                 
plt.title('Petal Plot', fontsize=25,color='b')                                            
plt.grid()                                                                 
#plt.show()
plt.savefig('test_input_petal.png')

# init membership matrix
def initializeMembershipWeights():
  weight = np.random.dirichlet(np.ones(k),n)
  weight_arr = np.array(weight)
  return weight_arr

# cluster center
def computeCentroids(weight_arr):
  C = []
  for i in range(k):
    weight_sum = np.power(weight_arr[:,i],m).sum()
    Cj = []
    for x in range(d):
      numerator = ( df.iloc[:,x].values * np.power(weight_arr[:,i],m)).sum()
      c_val = numerator/weight_sum;
      Cj.append(c_val)
    C.append(Cj)
  return C 

# update weight
def updateWeights(weight_arr,C):
  denom = np.zeros(n)
  for i in range(k):
    dist = (df.iloc[:,:].values - C[i])**2
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)
    denom  = denom + np.power(1/dist,1/(m-1))
  for i in range(k):
    dist = (df.iloc[:,:].values - C[i])**2
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)
    weight_arr[:,i] = np.divide(np.power(1/dist,1/(m-1)),denom)
  return weight_arr

# plot data
def plotData(z,C):  
  plt.subplot(4,3,z+1)              #scatter plot of sepal length vs sepal width                              
  plt.scatter(list(df.iloc[:,2]), list(df.iloc[:,3]), marker='o')    
  for center in C:
    plt.scatter(center[2],center[3], marker='o',color='r')        
  plt.axis('equal')                                                                 
  plt.xlabel('Sepal Length', fontsize=16)                                                 
  plt.ylabel('Sepal Width', fontsize=16)                                                                                      
  plt.grid()                                                  

# fuzzy algo
def FuzzyMeansAlgorithm():
  weight_arr = initializeMembershipWeights()
  plt.figure(figsize=(50,50)) 
  for z in range(MAX_ITERS):
    C = computeCentroids(weight_arr)
    updateWeights(weight_arr,C)
    plotData(z,C)
  #plt.show()
  # plt.savefig('test_.png')
  return (weight_arr,C)

# run 
final_weights,Centers = FuzzyMeansAlgorithm()

# visual: final center
df_sepal = df.iloc[:,0:2]
df_petal = df.iloc[:,2:5]
plt.figure(0,figsize=(5,5))                #scatter plot of sepal length vs sepal width                              
plt.scatter(list(df_sepal.iloc[:,0]), list(df_sepal.iloc[:,1]), marker='o')       
plt.axis('equal')                                                                 
plt.xlabel('Sepal Length', fontsize=16)                                                 
plt.ylabel('Sepal Width', fontsize=16)                                                 
plt.title('Sepal Plot', fontsize=25,color='b')                                            
plt.grid() 
for center in Centers:
  plt.scatter(center[0],center[1], marker='o',color='r')                                                                
#plt.show()
plt.savefig('test_final_center1.png')
plt.figure(1,figsize=(5,5))                #scatter plot of sepal length vs sepal width                              
plt.scatter(list(df_petal.iloc[:,0]), list(df_petal.iloc[:,1]), marker='o')       
plt.axis('equal')                                                                 
plt.xlabel('petal Length', fontsize=16)                                                 
plt.ylabel('petal Width', fontsize=16)                                                 
plt.title('Petal Plot', fontsize=25,color='b')                                            
plt.grid()                     
for center in Centers:
  plt.scatter(center[2],center[3], marker='o',color='r')                                                       
#plt.show()
plt.savefig('test_final_center2.png')

# visual: cluster
X = np.zeros((n,1))
plt.figure(0,figsize=(8,8))                #scatter plot of sepal length vs sepal width                                     
plt.axis('equal')                                                                 
plt.xlabel('Sepal Length', fontsize=16)                                                 
plt.ylabel('Sepal Width', fontsize=16)                                                 
plt.title('Sepal Plot', fontsize=25,color='b')                                            
plt.grid() 
for center in Centers:
  plt.scatter(center[0],center[1], marker='D',color='r')                                                                
clr = 'b'
for i in range(n):    
    cNumber = np.where(final_weights[i] == np.amax(final_weights[i]))
    if cNumber[0][0]==0:
      clr = 'y'
    elif cNumber[0][0]==1:
      clr = 'g'
    elif cNumber[0][0]==2:
      clr = 'm'
    plt.scatter(list(df_sepal.iloc[i:i+1,0]), list(df_sepal.iloc[i:i+1,1]), alpha=0.25,s=100,color=clr)
#plt.show()
plt.savefig('test_.png')
X = np.zeros((n,1))
plt.figure(0,figsize=(8,8))                #scatter plot of sepal length vs sepal width                                     
plt.axis('equal')                                                                 
plt.xlabel('Petal Length', fontsize=16)                                                 
plt.ylabel('Petal Width', fontsize=16)                                                 
plt.title('Petal Plot', fontsize=25,color='b')                                            
plt.grid() 
for center in Centers:
  plt.scatter(center[2],center[3], marker='D',color='r')                                                                
clr = 'b'
for i in range(n):    
    cNumber = np.where(final_weights[i] == np.amax(final_weights[i]))
    if cNumber[0][0]==0:
      clr = 'y'
    elif cNumber[0][0]==1:
      clr = 'g'
    elif cNumber[0][0]==2:
      clr = 'm'
    plt.scatter(list(df_petal.iloc[i:i+1,0]), list(df_petal.iloc[i:i+1,1]), alpha=0.25, s=100, color=clr)
#plt.show()
plt.savefig('test_.png')

# FCM: init inputs
cluster1 = np.random.randint(low=81, high=90, size=(n_data//n_clusters, n_dimension))
cluster2 = np.random.randint(low=41, high=50, size=(n_data//n_clusters, n_dimension))
cluster3 = np.random.randint(low=31, high=40, size=(n_data//n_clusters, n_dimension))
cluster4 = np.random.randint(low=1, high=10, size=(n_data//n_clusters, n_dimension))
inputs = np.concatenate((cluster1, cluster2, cluster3, cluster4))


def plot_inputs_centroids(inputs, centroids, i):
    plt.clf()
    plt.scatter(np.take(inputs, 0, axis=1), np.take(inputs, 1, axis=1), c = '#000000')
    plt.scatter(np.take(centroids, 0, axis=1), np.take(centroids, 1, axis=1), c = '#ff0000')
    plt.title(f'itr {i}: inputs - centroids coordinates')
    plt.savefig(f'./result/fcm_inputs-centroid-{i}.png')