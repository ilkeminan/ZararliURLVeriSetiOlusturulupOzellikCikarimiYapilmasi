import pandas as pd
from warnings import simplefilter
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import mutual_info_classif 
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import RandomForestClassifier
import csv
#Univariate feature selection
def ki2(X,y):
    sel_chi2 = SelectKBest(chi2, k=8)    # select 4 features
    X_train_chi2 = sel_chi2.fit_transform(X, y)
    return sel_chi2.get_support()    
def f_test(X,y):
    sel_f = SelectKBest(f_classif, k=8)
    X_train_f = sel_f.fit_transform(X, y)
    return sel_f.get_support()  
def mutual_info(X,y):
    sel_mutual = SelectKBest(mutual_info_classif, k=8)
    X_train_mutual = sel_mutual.fit_transform(X, y)
    return sel_mutual.get_support()
#Recursive feature elimination
def logistic_regression(X,y):
    model_logistic = LogisticRegression(solver='lbfgs', multi_class='multinomial', max_iter=1000)
    sel_rfe_logistic = RFE(estimator=model_logistic, n_features_to_select=8, step=1)
    X_train_rfe_logistic = sel_rfe_logistic.fit_transform(X, y)
    return sel_rfe_logistic.get_support()   
def random_forest(X,y):
    model_tree = RandomForestClassifier(random_state=100, n_estimators=50)
    sel_rfe_tree = RFE(estimator=model_tree, n_features_to_select=8, step=1)
    X_train_rfe_tree = sel_rfe_tree.fit_transform(X, y)
    return sel_rfe_tree.get_support()
#Feature selection using SelectFromModel
def L1_based(X,y):
    model_logistic = LogisticRegression(solver='saga', multi_class='multinomial', max_iter=10000, penalty='l1')
    sel_model_logistic = SelectFromModel(estimator=model_logistic)
    X_train_sfm_l1 = sel_model_logistic.fit_transform(X, y)
    return sel_model_logistic.get_support()
def tree_based(X,y):
    model_tree = RandomForestClassifier(random_state=100, n_estimators=50)
    model_tree.fit(X, y)
    sel_model_tree = SelectFromModel(estimator=model_tree, prefit=True, threshold='mean')  
    # since we already fit the data, we specify prefit option here
    # Features whose importance is greater or equal to the threshold are kept while the others are discarded.
    X_train_sfm_tree = sel_model_tree.transform(X)
    return sel_model_tree.get_support()



# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
f = pd.read_csv("URLs(with features-before selection).csv")
X = f.iloc[:,3:].values
y = f.iloc[:,2:3].values
ki2_results = ki2(X,y)
f_test_results = f_test(X,y)
mutual_info_results = mutual_info(X,y)
logistic_regression_results = logistic_regression(X,y)
random_forest_results = random_forest(X,y)
L1_based_results = L1_based(X,y)
tree_based_results = tree_based(X,y)
selection_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(17):
    if(ki2_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
    if(f_test_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
    if(mutual_info_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
    if(logistic_regression_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1   
    if(random_forest_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
    if(L1_based_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
    if(tree_based_results[i] == True):
        selection_counts[i] = selection_counts[i] + 1
selected_features = []
for i in range(17):
    if(selection_counts[i] >= 3):
        selected_features.append(i)
print("Selection counts:")
print(selection_counts)
header = ["ip","https","spam","#.","#/","#numbers","sensitive_words","uppercase_letter","length","suspicious_character","prefix-suffix","tld","entropy","brands","www_misuse","has_www","extension_extraction"]
selected_header = ["id","url","type"]
selected_features_length = len(selected_features)
for i in range(17):
    for k in range(selected_features_length):
        if(selected_features[k] == i):
            selected_header.append(header[i])
new_f = f[selected_header]
new_f.to_csv("URLs(with features-after selection).csv", index=False)     
print(selected_header)