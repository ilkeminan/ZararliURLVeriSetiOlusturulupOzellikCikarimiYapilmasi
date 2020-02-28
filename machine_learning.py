import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB,BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
def logistic_regression(X_train,X_test,y_train,y_test,lr_solver):
    logr = LogisticRegression(solver=lr_solver,random_state=0)
    logr.fit(X_train, y_train)
    y_pred = logr.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def naive_bayes(X_train,X_test,y_train,y_test,nb_type):
    if(nb_type == "Gaussian Naive Bayes"):
        gnb = GaussianNB()
    elif(nb_type == "Multinomial Naive Bayes"):
        gnb = MultinomialNB()
    elif(nb_type == "Complement Naive Bayes"):
        gnb = ComplementNB()
    else:
        gnb = BernoulliNB()
    gnb.fit(X_train, y_train)
    y_pred = gnb.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def knn(X_train,X_test,y_train,y_test,knn_k):
    classifier = KNeighborsClassifier(n_neighbors=int(knn_k))
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def svm(X_train,X_test,y_train,y_test,svm_kernel):
    svc = SVC(gamma='scale',kernel=svm_kernel)
    svc.fit(X_train, y_train)
    y_pred = svc.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def decision_tree(X_train,X_test,y_train,y_test,dt_criterion):
    dtc = DecisionTreeClassifier(criterion=dt_criterion)
    dtc.fit(X_train, y_train)
    y_pred = dtc.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def random_forest(X_train,X_test,y_train,y_test,rf_criterion):
    rfc = RandomForestClassifier(n_estimators=100, criterion=rf_criterion)
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def adaboost(X_train,X_test,y_train,y_test,ab_max_depth):
    classifier = AdaBoostClassifier(DecisionTreeClassifier(max_depth=int(ab_max_depth)),n_estimators=200)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return cm
def performance_metrics(cm):
    tn = cm[0][0]
    fp = cm[0][1]
    fn = cm[1][0]
    tp = cm[1][1]
    tp_rate = tp/(tp+fn)
    fp_rate = fp/(fp+tn)
    precision = tp/(tp+fp)
    sensitivity = tp/(tp+fn)
    Fm = (2*precision*sensitivity)/(precision+sensitivity)
    accuracy = (tp+tn)/(tp+fp+tn+fn)
    return tp_rate,fp_rate,Fm,accuracy
def compare_algorithms(lr_solver,nb_type,knn_k,svm_kernel,dt_criterion,rf_criterion,ab_max_depth):
    datas = pd.read_csv("URLs(with features-after selection).csv")
    features = datas.iloc[:,3:].values
    result = datas.iloc[:,2:3].values
    X_train,X_test,y_train,y_test = train_test_split(features,result,test_size=0.7)
    cm = logistic_regression(X_train,X_test,y_train,y_test,lr_solver)
    lr_tp_rate,lr_fp_rate,lr_Fm,lr_accuracy = performance_metrics(cm)
    cm = naive_bayes(X_train,X_test,y_train,y_test,nb_type)
    nb_tp_rate,nb_fp_rate,nb_Fm,nb_accuracy = performance_metrics(cm)
    cm = knn(X_train,X_test,y_train,y_test,knn_k)
    knn_tp_rate,knn_fp_rate,knn_Fm,knn_accuracy = performance_metrics(cm)
    cm = svm(X_train,X_test,y_train,y_test,svm_kernel)
    svm_tp_rate,svm_fp_rate,svm_Fm,svm_accuracy = performance_metrics(cm)
    cm = decision_tree(X_train,X_test,y_train,y_test,dt_criterion)
    dt_tp_rate,dt_fp_rate,dt_Fm,dt_accuracy = performance_metrics(cm)
    cm = random_forest(X_train,X_test,y_train,y_test,rf_criterion)
    rf_tp_rate,rf_fp_rate,rf_Fm,rf_accuracy = performance_metrics(cm)
    cm = adaboost(X_train,X_test,y_train,y_test,ab_max_depth)
    ab_tp_rate,ab_fp_rate,ab_Fm,ab_accuracy = performance_metrics(cm)
    result_matrix = [["Logistic Regression",lr_tp_rate,lr_fp_rate,lr_Fm,lr_accuracy],
                     ["Naive Bayes",nb_tp_rate,nb_fp_rate,nb_Fm,nb_accuracy],
                     ["K Nearest Neighbors",knn_tp_rate,knn_fp_rate,knn_Fm,knn_accuracy],
                     ["Support Vector Machines",svm_tp_rate,svm_fp_rate,svm_Fm,svm_accuracy],
                     ["Decision Tree",dt_tp_rate,dt_fp_rate,dt_Fm,dt_accuracy],
                     ["Random Forest",rf_tp_rate,rf_fp_rate,rf_Fm,rf_accuracy],
                     ["AdaBoost",ab_tp_rate,ab_fp_rate,ab_Fm,ab_accuracy]]
    return result_matrix





def new_window(win,lr_solver,nb_type,knn_k,svm_kernel,dt_criterion,rf_criterion,ab_max_depth):
    win.destroy()
    result_matrix = compare_algorithms(lr_solver,nb_type,knn_k,svm_kernel,dt_criterion,rf_criterion,ab_max_depth)
    print(result_matrix)
    results = tk.Tk()  
    results.title("Comparison of Machine Learning Algorithms")
    label = tk.Label(results, text="Comparison of Machine Learning Algorithms", font=("Arial",30)).grid(row=0, columnspan=3)
    # create Treeview with 5 columns
    cols = ('Algorithm', 'True Positive Rate', 'False Positive Rate', 'F Score', 'Accuracy')
    listBox = ttk.Treeview(results, columns=cols, show='headings')
    # set column headings
    for col in cols:
        listBox.heading(col, text=col)    
    listBox.grid(row=1, column=0, columnspan=2)
    for i, (algorithm,tp_rate,fp_rate,Fm,accuracy) in enumerate(result_matrix, start=1):
        listBox.insert("", "end", values=(algorithm,tp_rate,fp_rate,Fm,accuracy))
    results.mainloop()   
      
        
import tkinter as tk
from tkinter import ttk,StringVar
from tkinter.ttk import Combobox,Label
win = tk.Tk()
win.geometry("350x200+250+250")
win.title("Selection of the Parameters")
label_lr = Label(win, text = "Logistic Regression Solver")
label_lr.grid(row=1,column=1)
logistic_regression_solver = ["newton-cg","lbfgs","liblinear","sag","saga"]
selection_lr = StringVar()
selection_lr.set(logistic_regression_solver[1])
combo_lr = Combobox(win,state="readonly",values = logistic_regression_solver,textvariable=selection_lr,width=25)
combo_lr.grid(row=1,column=2)
label_nb = Label(win, text = "Naive Bayes Type")
label_nb.grid(row=2,column=1)
naive_bayes_types = ["Gaussian Naive Bayes","Multinomial Naive Bayes","Complement Naive Bayes","Bernoulli Naive Bayes"]
selection_nb = StringVar()
selection_nb.set(naive_bayes_types[3])
combo_nb = Combobox(win,state="readonly",values = naive_bayes_types,textvariable=selection_nb,width=25)
combo_nb.grid(row=2,column=2)
label_knn = Label(win, text = "KNN Number of Neighbors (k)")
label_knn.grid(row=3,column=1)
knn_k = ["1","2","3","4","5","6","7","8","9","10"]
selection_knn = StringVar()
selection_knn.set(knn_k[4])
combo_knn = Combobox(win,state="readonly",values = knn_k,textvariable=selection_knn,width=25)
combo_knn.grid(row=3,column=2)
label_svm = Label(win, text = "SVM Kernel")
label_svm.grid(row=4,column=1)
svm_kernel = ["linear","poly","rbf"]
selection_svm = StringVar()
selection_svm.set(svm_kernel[2])
combo_svm = Combobox(win,state="readonly",values = svm_kernel,textvariable=selection_svm,width=25)
combo_svm.grid(row=4,column=2)
label_dt = Label(win, text = "Decision Tree Criterion")
label_dt.grid(row=5,column=1)
tree_criterion = ["gini","entropy"]
selection_dt = StringVar()
selection_dt.set(tree_criterion[0])
combo_dt = Combobox(win,state="readonly",values = tree_criterion,textvariable=selection_dt,width=25)
combo_dt.grid(row=5,column=2)
label_rf = Label(win, text = "Random Forest Criterion")
label_rf.grid(row=6,column=1)
selection_rf = StringVar()
selection_rf.set(tree_criterion[1])
combo_rf = Combobox(win,state="readonly",values = tree_criterion,textvariable=selection_rf,width=25)
combo_rf.grid(row=6,column=2)
label_ab = Label(win, text = "AdaBoost Maximum Depth")
label_ab.grid(row=7,column=1)
adaboost_max_depth = ["1","2","3","4","5","6","7","8","9","10"]
selection_ab = StringVar()
selection_ab.set(adaboost_max_depth[3])
combo_ab = Combobox(win,state="readonly",values = adaboost_max_depth,textvariable=selection_ab,width=25)
combo_ab.grid(row=7,column=2)
button = tk.Button(win,bg = "green3", text="Compare the machine learning algorithms")
button['command'] = lambda: new_window(win,combo_lr.get(),combo_nb.get(),combo_knn.get(),combo_svm.get(),combo_dt.get(),combo_rf.get(),combo_ab.get())
button.place(x=50, y=150)
win.mainloop()