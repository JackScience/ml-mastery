#!/usr/bin/env python3

###################################
# Mastering ML Python Mini Course
#
# Inspired by the project here: 
#
# https://s3.amazonaws.com/MLMastery/machine_learning_mastery_with_python_mini_course.pdf?__s=mxhvphowryg2sfmzus2q
#
# By Nathan Fritter
#
# Project will soon be found at: 
#
# https://www.inertia7.com/projects/
####################################

# Welcome to my repo for the Mastering Machine Learning Python Mini Course
# Here I will be going through each part of the course
# So you can get a feel of the different parts

import numpy as np
import pandas as pd
from pandas import read_csv, Series
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, KFold, train_test_split, GridSearchCV, RandomizedSearchCV
# Define url and columns
url = 'https://goo.gl/bDdBiA'
columns = np.array(['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class'])

# Read in data
data = read_csv(url, names = columns)
array = data.values

####################################
# Lesson 11: Improve Accuracy with Ensemble Methods
####################################

'''
Here in the course would have been a section to do some ensemble model 
training, as it represents 

'''

# Divide data into attributes and predictor
X = array[:, 0:8]
y = array[:, 8]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 42)

# Make list for models
models = np.empty([3, 2], dtype = object)

# Linear models
models[0] = ['Logistic Regression', LogisticRegression(random_state = 1)]
models[1] = ['Linear Discriminant Analysis', LinearDiscriminantAnalysis()]

# More complex models	
models[2] = ['Gradient Boosted Machine', GradientBoostingClassifier(random_state = 1)]
