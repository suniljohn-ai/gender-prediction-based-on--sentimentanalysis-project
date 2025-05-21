from django.conf import settings
import os
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier



def clean_dataset(df):
    assert isinstance(df,pd.DataFrame), df.dropna(inplace=True)
path = os.path.join(settings.MEDIA_ROOT, "gender_dataset.csv")
pd.options.display.max_colwidth=300
# df = pd.read_csv(path,nrows=1000)
data = pd.read_csv(path,nrows=1000)
data = data[['gender', 'text']]

print(data['gender'].unique())
data['gender'].replace('female',0, inplace=True)
data['gender'].replace('male', 1,inplace=True)
data['gender'].replace('brand',1, inplace=True)
data['gender'].replace('unknown',0, inplace=True)
data.dropna(inplace=True)
#print(data.head())
X = data.text
y = data.gender
# print("=====>",y)
#Using CountVectorizer to convert text into tokens/features
vect = CountVectorizer(stop_words='english', ngram_range = (1,1), max_df = .80, min_df = 4)
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1, test_size= 0.2)
#Using training data to transform text into counts of features for each message
vect.fit(X_train)
X_train_dtm = vect.transform(X_train)
X_test_dtm = vect.transform(X_test)


def calculate_naive_bayes():
    # Accuracy using Naive Bayes Model
    NB = MultinomialNB()
    NB.fit(X_train_dtm, y_train)
    y_pred = NB.predict(X_test_dtm)
    print('\nNaive Bayes')
    nb_accuracy = metrics.accuracy_score(y_test, y_pred)
    nb_cm =  metrics.confusion_matrix(y_test, y_pred)
    nb_auc = metrics.roc_auc_score(y_test, y_pred)
    return nb_accuracy,nb_cm,nb_auc

def calculate_knn():
    KNN = KNeighborsClassifier()
    KNN.fit(X_train_dtm, y_train)
    y_pred = KNN.predict(X_test_dtm)
    print('\n K Nearest Neighbour')
    knn_accuracy = metrics.accuracy_score(y_test, y_pred)
    knn_cm = metrics.confusion_matrix(y_test, y_pred)
    knn_auc = metrics.roc_auc_score(y_test, y_pred)
    return knn_accuracy, knn_cm, knn_auc


def calculate_logistic_regression():
    lg = LogisticRegression()
    lg.fit(X_train_dtm, y_train)
    y_pred = lg.predict(X_test_dtm)
    print('\n Logistic Regression')
    lg_accuracy = metrics.accuracy_score(y_test, y_pred)
    lg_cm = metrics.confusion_matrix(y_test, y_pred)
    lg_auc = metrics.roc_auc_score(y_test, y_pred)
    return lg_accuracy, lg_cm, lg_auc



def calculate_random_forest():
    rf = RandomForestClassifier()
    rf.fit(X_train_dtm, y_train)
    y_pred = rf.predict(X_test_dtm)
    print('\n Random Forest')
    rf_accuracy = metrics.accuracy_score(y_test, y_pred)
    rf_cm = metrics.confusion_matrix(y_test, y_pred)
    rf_auc = metrics.roc_auc_score(y_test, y_pred)
    return rf_accuracy, rf_cm, rf_auc


def calculate_svm():
    SVM = LinearSVC()
    SVM.fit(X_train_dtm, y_train)
    y_pred = SVM.predict(X_test_dtm)
    print('\nSupport Vector Machine')
    svm_accuracy = metrics.accuracy_score(y_test, y_pred)
    svm_cm = metrics.confusion_matrix(y_test, y_pred)
    svm_auc = metrics.roc_auc_score(y_test, y_pred)
    return svm_accuracy, svm_cm, svm_auc


def process_user_tweet(tweet):
    # Custom Test: Test a review on the best performing model (Logistic Regression)
    trainingVector = CountVectorizer(stop_words='english', ngram_range=(1, 1), max_df=.80, min_df=5)
    trainingVector.fit(X)
    X_dtm = trainingVector.transform(X)
    LR_complete = RandomForestClassifier() # LogisticRegression()
    LR_complete.fit(X_dtm, y)
    # Input Review
    test = []
    test.append(tweet)
    test_dtm = trainingVector.transform(test)
    predLabel = LR_complete.predict(test_dtm)
    tags = [0., 1.]
    # Display Output
    return tags[int(predLabel[0])]
