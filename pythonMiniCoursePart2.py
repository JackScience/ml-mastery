#
##
###
#### PART SIX: Algorithm Evaluation & Comparison with Resampling Methods & Algorithm Evaluation Metrics
###
##
#

# The data used to train a model should not be then predicted using the model
# Because the point is to make predictions on unseen data to see how well it generalizes
# To do this we use resampling methods to split the data into training & testing sets
# Then fit a model and evauate its performance

"""
Methods for Re-sampling data
1. Split data once into training and testing sets
2. Use k-fold cross-validation to create k different train test splits to train k different models
3. Use leave one out cross-validation: every data point is held out once with the rest of the data used to fit a model 
	a. Thus n models created, with each trained on n - 1 data points

Methods for Evaluating Algorithm Metrics
1. Accuracy and LogLoss metrics for classdification
2. Generation of confusion matric and classification report
3. Root Mean Square Error (RMSE) and R squared matrics for regression
"""

import numpy as np
import pandas as pd
import sys
from sklearn import (model_selection, linear_model, metrics, discriminant_analysis,
neural_network, tree, svm, naive_bayes)

# Define url and columns
url = "https://goo.gl/vhm1eU"
columns = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

# Read in data and split up so we don't do this over and over
data = pd.read_csv(url, names = columns)
array = data.values

# Separate into input and output components
X = array[:, 0:8]
Y = array[:, 8]	

# Train test split for evaluation metrics
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(
X, Y, test_size = 0.33, random_state = 42)

def part_six():
	# Here we will fit a Logistic Regression model using 10 fold cross validation
	# As well as a Linear Discriminant Analysis model & compare
	models = []

	# Simpler models
	models.append(('Logistic Regression', linear_model.LogisticRegression(random_state = 1)))
	models.append(('Linear Discriminant Analysis', discriminant_analysis.LinearDiscriminantAnalysis()))
	models.append(('Naive Bayes', naive_bayes.MultinomialNB()))
	models.append(('Decision Tree', tree.DecisionTreeClassifier(max_features = 3, random_state = 1)))

	# More complex models	
	models.append(('Neural Network', neural_network.MLPClassifier(random_state = 1)))
	models.append(('Ridge Classifier', linear_model.RidgeClassifier(random_state = 1)))
	models.append(('SGD Classifier', linear_model.SGDClassifier(max_iter = 5, 
		tol = None, random_state = 1)))
	models.append(('Support Vector Machine', svm.LinearSVC(random_state = 1)))
	
	# Fit & evaluate models
	for name, model in models:
		# Different model metrics
		for scoring in ('accuracy', 'roc_auc'):
			k_fold = model_selection.KFold(n_splits = 10, random_state = 1)
			try:
				result = model_selection.cross_val_score(model, X, Y, cv = k_fold, scoring = scoring)
			except AttributeError:
				print("The %s model cannot perform cross validation with the %s metric" % (name, scoring))
			if scoring == 'accuracy':
				print("\n%s of %s model:\n %.3f%% (+\-%.3f%%)" 
				% (scoring, name, result.mean() * 100.0, result.std() * 100.0))
			else:
				print("\n%s of %s model:\n %.3f (+\-%.3f)" % (scoring, name, result.mean(), result.std()))	

		# Classification report & Confusion Matrix (needs separate training and evaluation process)
		fitted_model = model.fit(X_train, Y_train)
		Y_pred = model.predict(X_test)
		conf_matrix = metrics.confusion_matrix(Y_test, Y_pred)
		class_report = metrics.classification_report(Y_test, Y_pred)
		print("\nConfusion Matrix for %s model:\n" % (name), conf_matrix)
		print("\nClassification Report for %s model:\n" % (name), class_report)

		# ROC Curves
		try:
			Y_prob = model.predict(X_test)
			fpr, tpr, threshold = metrics.roc_curve(y_true = Y_test, y_score = Y_prob, pos_label = 1)
			roc_auc = metrics.auc(fpr, tpr)
			
			plt.title('Receiver Operating Characteristic')
			plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
			plt.legend(loc = 'lower right')
			plt.plot([0,1], [0,1], 'r--') # Add diagonal line
			plt.plot([0,0], [1,0], 'k--', color = 'black')
			plt.plot([1,0], [1,1], 'k--', color = 'black')
			plt.xlim([-0.1, 1.1])
			plt.ylim([-0.1, 1.1])
			plt.xlabel('False Positive Rate')
			plt.ylabel('True Positive Rate')
			plt.show()
		except: 
			print("The %s model does not support the \"predict\" method" % name)


	""" 
	The best models from here were:
	1. Logistic Regression
	2. Linear Discriminant Analysis
	3. Ridge Classifier
	"""

#
##
###
#### PART SEVEN: Improve Accuracy with Ensemble Predictions
###
##
#

# The part before had us training single models for evaluation
# This is usually sufficient, but one can also combine predictions from multiple equivalent models
# Some models are built in with this capacity, e.g:
# Random Forest for bagging, Stochastic Gradient Boosting for Boosting
# Another type of ensemble is called voting
# Where the predictions from multiple different models are combined
# This will be done in the next part

from sklearn import ensemble
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
def part_seven():
	# Here let's implement some ensemble methods to potentially improve accuracy
	# And get a better idea of the inherent structure of the data

	models = []
	# Boosting ensembles
	models.append(('Gradient Boosted Machine', ensemble.GradientBoostingClassifier(random_state = 1)))
	models.append(('AdaBoost Classifier', ensemble.AdaBoostClassifier(random_state = 1)))

	# Bagging Ensembles
	# Even though the decision tree didn't do so well, a random forest might
	n_trees = 100
	models.append(('Random Forest', ensemble.RandomForestClassifier(n_estimators = n_trees,	max_features = 3, random_state = 1)))
	models.append(('Extra Trees Classifier', ensemble.ExtraTreesClassifier(n_estimators = n_trees, max_features = 3, random_state = 1)))

	# Fit & evaluate models
	for name, model in models:
		# Different model metrics
		for scoring in ('accuracy', 'roc_auc'):
			k_fold = model_selection.KFold(n_splits = 10, random_state = 1)
			try:
				result = model_selection.cross_val_score(model, X, Y, cv = k_fold, scoring = scoring)
			except AttributeError:
				print("The %s model cannot perform cross validation with the %s metric" % (name, scoring))
			if scoring == 'accuracy':
				print("\n%s of %s model:\n %.3f%% (+\-%.3f%%)" 
				% (scoring, name, result.mean() * 100.0, result.std() * 100.0))
			else:
				print("\n%s of %s model:\n %.3f (+\-%.3f)" % (scoring, name, result.mean(), result.std()))	

		# Classification report, Confusion Matrix, Feature Importance (need to do separate training and evaluation process)
		fitted_model = model.fit(X_train, Y_train)
		Y_pred = model.predict(X_test)
		conf_matrix = metrics.confusion_matrix(Y_test, Y_pred)
		class_report = metrics.classification_report(Y_test, Y_pred)
		importances = fitted_model.feature_importances_
		#std = np.std([tree.feature_importances_ for tree in fitted_model.estimators_],axis=0)
		indices = np.argsort(importances)[::-1]
		print("\nConfusion Matrix for %s model:\n" % (name), conf_matrix)
		print("\nClassification Report for %s model:\n" % (name), class_report)
		print("\nFeature importances for %s model:" %(name))
		for f in range(X.shape[1]):
			print("%d. Feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

		plt.figure()
		plt.title("Feature Importances for %s" % name)
		plt.bar(range(X.shape[1]), importances[indices], color = 'r', align = 'center')
		plt.xticks(range(X.shape[1]), indices)
		plt.xlim([-1, X.shape[1]])
		plt.show()


		# ROC Curves
		try:
			Y_prob = model.predict(X_test)
			fpr, tpr, threshold = metrics.roc_curve(y_true = Y_test, y_score = Y_prob, pos_label = 1)
			roc_auc = metrics.auc(fpr, tpr)
			
			plt.title('Receiver Operating Characteristic')
			plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
			plt.legend(loc = 'lower right')
			plt.plot([0,1], [0,1], 'r--') # Add diagonal line
			plt.plot([0,0], [1,0], 'k--', color = 'black')
			plt.plot([1,0], [1,1], 'k--', color = 'black')
			plt.xlim([-0.1, 1.1])
			plt.ylim([-0.1, 1.1])
			plt.xlabel('False Positive Rate')
			plt.ylabel('True Positive Rate')
			plt.show()
		except: 
			print("The %s model does not support the \"predict\" method" % name)

	"""
	All of them achieve pretty much the same results as the simpler models
	Yet Logistic Regression still does slightly better than all of them
	I will do a Voting Classifier to see if I can combine any results here to get better results
	Otherwise logistic regression is the way to go
	"""

#
##
###
#### PART EIGHT: Voting Classifier: Can we combine the results of multiple models to achieve better performance?
###
##
#

# Technically this is an emsemble method, but I wanted to include this in a separate part
# In order to see the results of the initial model fitting
# And gather models from different types that did well
# Because model diversity is key here
# The point of combining models is to reduce generalization error
# And similar models will not achieve that
# There are different voting methods as well (hard vs soft)
# All will be attempted

def part_eight():
	# Last but not least, let's combine some of these models 
	# To try for better predictive performance

	n_trees = 100
	models = []

	# Voting ensembles
	# Number 1: Hard Vote (Predicted class labels used for majority rule voting)
	models.append(('Voting Classifier 1', ensemble.VotingClassifier(estimators = [
		('lr', linear_model.LogisticRegression(random_state = 1)),
		#('lda', discriminant_analysis.LinearDiscriminantAnalysis()),
		('gbm', ensemble.GradientBoostingClassifier(random_state = 1)),
		#('rf', ensemble.RandomForestClassifier(random_state = 1, n_estimators = n_trees, max_features = 3))
		#('rr', linear_model.RidgeClassifier(random_state = 1))
		], voting = 'hard')))

	# Number 2: Soft Vote (Argmax of sums of predicted probabilities used)
	# Recommended for ensemble of well-calibrated classifiers
	models.append(('Voting Classifier 2', ensemble.VotingClassifier(estimators = [
		#('lr', linear_model.LogisticRegression(random_state = 1)),
		('lda', discriminant_analysis.LinearDiscriminantAnalysis()),
		#('gbm', ensemble.GradientBoostingClassifier(random_state = 1)),
		('rf', ensemble.RandomForestClassifier(random_state = 1, n_estimators = n_trees, max_features = 3))
		#('rr', linear_model.RidgeClassifier(random_state = 1))
		], voting = 'soft')))

	# Number 3: Soft Vote with weights
	# Some models will be more valuable than others


	# Fit & evaluate models
	for name, model in models:
		# Different model metrics
		for scoring in ('accuracy', 'roc_auc'):
			k_fold = model_selection.KFold(n_splits = 10, random_state = 1)
			try:
				result = model_selection.cross_val_score(model, X, Y, cv = k_fold, scoring = scoring)
			except AttributeError:
				print("The %s model cannot perform cross validation with the %s metric" % (name, scoring))
			if scoring == 'accuracy':
				print("\n%s of %s model:\n %.3f%% (+\-%.3f%%)" 
				% (scoring, name, result.mean() * 100.0, result.std() * 100.0))
			else:
				print("\n%s of %s model:\n %.3f (+\-%.3f)" % (scoring, name, result.mean(), result.std()))	

		# Classification report & Confusion Matrix (need to do separate training and evaluation process)
		fitted_model = model.fit(X_train, Y_train)
		Y_pred = model.predict(X_test)
		conf_matrix = metrics.confusion_matrix(Y_test, Y_pred)
		class_report = metrics.classification_report(Y_test, Y_pred)
		print("\nConfusion Matrix for %s model:\n" % (name), conf_matrix)
		print("\nClassification Report for %s model:\n" % (name), class_report)

		# ROC Curves
		try:
			Y_prob = model.predict(X_test)
			fpr, tpr, threshold = metrics.roc_curve(y_true = Y_test, y_score = Y_prob, pos_label = 1)
			roc_auc = metrics.auc(fpr, tpr)
			
			plt.title('Receiver Operating Characteristic')
			plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
			plt.legend(loc = 'lower right')
			plt.plot([0,1], [0,1], 'r--') # Add diagonal line
			plt.plot([0,0], [1,0], 'k--', color = 'black')
			plt.plot([1,0], [1,1], 'k--', color = 'black')
			plt.xlim([-0.1, 1.1])
			plt.ylim([-0.1, 1.1])
			plt.xlabel('False Positive Rate')
			plt.ylabel('True Positive Rate')
			plt.show()
		except: 
			print("The %s model does not support the \"predict\" method" % name)


#
##
###
#### PART NINE: Pick a Final Model and Save
###
##
#

# Now that we have the results from many different model evalutions and testing, 
# Let's pick 1-2 final ones to save
# I would like to do one linear and one non-linear model 
# Because the training time difference is negligible
# Let's do Logistic Regression and a Random Forest
import pickle
def part_nine():

	n_trees = 100
	models = []
	models.append(('Logistic_Regression', linear_model.LogisticRegression(random_state = 1)))
	models.append(('Random_Forest', ensemble.RandomForestClassifier(random_state = 1, n_estimators = n_trees, max_features = 3)))

	# Train models and save to disk
	for name, model in models:
		model.fit(X_train, Y_train)
		pickle.dump(model, open('final_%s_model.sav' % (name), 'wb'))

	# A while later...
	for name, model in models:
		loaded_model = pickle.load(open('final_%s_model.sav' % (name), 'rb'))
		result = loaded_model.score(X_test, Y_test)
		Y_pred = model.predict(X_test)
		conf_matrix = metrics.confusion_matrix(Y_test, Y_pred)
		class_report = metrics.classification_report(Y_test, Y_pred)
		print("\nConfusion Matrix for %s model:\n" % (name), conf_matrix)
		print("\nClassification Report for %s model:\n" % (name), class_report)
		print("Score for %s model:\n" % name, result)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '6':
            part_six()
        elif sys.argv[1] == '7':
            part_seven()
        elif sys.argv[1] == '8':
            part_eight()
        elif sys.argv[1] == '9':
            part_nine()