from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
import pandas as pd

# Create your views here.

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def gender_dataset(request):
    from django.conf import settings
    import os
    path = os.path.join(settings.MEDIA_ROOT, "gender_dataset.csv")
    pd.options.display.max_colwidth=300
    df = pd.read_csv(path,nrows=1000)
    df = df[['gender','text']]
    df = df.dropna()
    df.drop(df[df['gender']=='brand'].index, inplace=True)
    df.drop(df[df['gender']=='unknown'].index, inplace=True)
    df.drop(df[df['gender']==None].index, inplace=True)
    print(df.head())
    df = df.to_html()
    #print(df)
    return render(request, 'users/tweetsdata.html',{'data': df})


def user_machine_learning(request):
    from .utility import process_classification
    nb_accuracy,nb_cm,nb_auc = process_classification.calculate_naive_bayes()
    knn_accuracy, knn_cm, knn_auc = process_classification.calculate_knn()
    lg_accuracy, lg_cm, lg_auc = process_classification.calculate_logistic_regression()
    rf_accuracy, rf_cm, rf_auc = process_classification.calculate_random_forest()
    svm_accuracy, svm_cm, svm_auc = process_classification.calculate_svm()
    nb = {'nb_accuracy': nb_accuracy,'nb_auc': nb_auc}
    knn = {'knn_accuracy': knn_accuracy, 'knn_auc': knn_auc}
    lg = {'lg_accuracy': lg_accuracy, 'lg_auc': lg_auc}
    rf = {'rf_accuracy': rf_accuracy, 'rf_auc': rf_auc}
    svm = {'svm_accuracy': svm_accuracy, 'svm_auc': svm_auc}
    return render(request, 'users/user_classification.html', {"nb": nb,"knn":knn,"lg":lg,"rf":rf,"svm": svm})


from textblob import Word


def check_word_spelling(word):
    word = Word(word)
    result = word.spellcheck()
    if word == result[0][0]:
        print(f'Spelling of "{word}" is correct!')
        return True
    else:
        print(f'Spelling of "{word}" is not correct!')
        print(f'Correct spelling of "{word}": "{result[0][0]}" (with {result[0][1]} confidence).')
        return False


def user_gender_predict(request):

    if request.method=="POST":
        tweet = request.POST.get('text')
        if len(tweet)==0:
            return render(request, "users/user_gender_predict_form.html", {"gender": "No Data or single"})
        c = tweet.split()
        count = 0
        for word in c:
            flg = check_word_spelling(word)
            if flg==False:
                count = count+1
        if count>0:
           return render(request, "users/user_gender_predict_form.html", {"gender": "Unable Process tweet"})
        if len(c)<10:
            from .faceNeural import runfaces
            label = runfaces.startImageFaces()
            print("Label ",label)
            try:
                return render(request, "users/user_gender_predict_form.html", {"gender": next(iter(label)), "tweet": tweet})
            except:
                return render(request, "users/user_gender_predict_form.html", {"gender": "not Detected"})
        from .utility import process_classification
        rslt = process_classification.process_user_tweet(tweet)
        print(f"{rslt} and type {type(rslt)}")
        if rslt== 1.0:
            gender = "Male"
        else:
            gender = "Female"
        return render(request, "users/user_gender_predict_form.html", {"gender": gender, "tweet": tweet})
    else:
        # label = runfaces.startImageFaces()

        return render(request, "users/user_gender_predict_form.html",{})
