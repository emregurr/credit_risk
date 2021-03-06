import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score , classification_report
from xgboost import XGBClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score, GridSearchCV
pd.set_option("display.max_columns", None)
import warnings
warnings.filterwarnings("ignore")

credit_risk = pd.read_csv("Datasets/credit_risk.csv")
df = credit_risk.copy()

df.head()

# Unnamed: 0  Age     Sex  Job Housing Saving accounts Checking account  \
# 0           0   67    male    2     own             NaN           little
# 1           1   22  female    2     own          little         moderate
# 2           2   49    male    1     own          little              NaN
# 3           3   45    male    2    free          little           little
# 4           4   53    male    2    free          little           little
#    Credit amount  Duration              Purpose  Risk
# 0           1169         6             radio/TV  good
# 1           5951        48             radio/TV   bad
# 2           2096        12            education  good
# 3           7882        42  furniture/equipment  good
# 4           4870        24                  car   bad

def information(dataframe):
    print("shape" , dataframe.shape)
    print("Index", dataframe.index)
    print("Columns", dataframe.columns)
    print("Null", dataframe.isnull().values.any())
    print("Count of Null" , df.isnull().sum())

# Veri setini inceliyoruz

information(df)
# shape (1000, 11)
# Index RangeIndex(start=0, stop=1000, step=1)
# Columns Index(['Unnamed: 0', 'Age', 'Sex', 'Job', 'Housing', 'Saving accounts',
#        'Checking account', 'Credit amount', 'Duration', 'Purpose', 'Risk'],
#       dtype='object')
# Null True
# Count of Null
# Unnamed: 0            0
# Age                   0
# Sex                   0
# Job                   0
# Housing               0
# Saving accounts     183
# Checking account    394
# Credit amount         0
# Duration              0
# Purpose               0

df.drop("Unnamed: 0",axis = 1,inplace = True)

#Unnamed degiskenini cıkarıyoruz.

df["Risk"].replace({"good":1,"bad":0},inplace = True)

#Risk degiskenini good icin 1 bad icin 0 olarak degistiriyoruz.

df["Sex"].replace({"male":1,"female":0},inplace = True )

#Sex kategorik degiskenini male icin 1 ve female icin 0 olarak düzenliyoruz.
#Ve datasetimizin son haline göz atiyoruz.

df.head(4)

# Age  Sex  Job Housing Saving accounts Checking account  Credit amount  \
# 0   67    1    2     own             NaN           little           1169
# 1   22    0    2     own          little         moderate           5951
# 2   49    1    1     own          little              NaN           2096
# 3   45    1    2    free          little           little           7882
#    Duration              Purpose  Risk
# 0         6             radio/TV     1
# 1        48             radio/TV     0
# 2        12            education     1
# 3        42  furniture/equipment     1

## KATEGORİK ANALİZ

cat_cols = [col for col in df.columns if df[col].dtypes == "O"]
cat_cols

# ['Housing', 'Saving accounts', 'Checking account', 'Purpose']

def cat_summary(data, categorical_cols, target, number_of_classes=10):
    var_count = 0
    vars_more_classes = []
    for var in categorical_cols:
        if len(data[var].value_counts()) <= number_of_classes:  # sınıf sayısına göre seç
            print(pd.DataFrame({var: data[var].value_counts(),
                                "Ratio": 100 * data[var].value_counts() / len(data),
                                "TARGET_MEAN": data.groupby(var)[target].mean()}), end="\n\n\n")
            var_count += 1
        else:
            vars_more_classes.append(data[var].name)
    print('%d categorical variables have been described' % var_count, end="\n\n")
    print('There are', len(vars_more_classes), "variables have more than", number_of_classes, "classes", end="\n\n")
    print('Variable names have more than %d classes:' % number_of_classes, end="\n\n")
    print(vars_more_classes)

cat_summary(df , cat_cols ,"Risk")

#    Housing  Ratio  TARGET_MEAN
# free      108   10.8     0.592593
# own       713   71.3     0.739130
# rent      179   17.9     0.608939
#                  Saving accounts  Ratio  TARGET_MEAN
# Saving accounts
# little                       603   60.3     0.640133
# moderate                     103   10.3     0.669903
# quite rich                    63    6.3     0.825397
# rich                          48    4.8     0.875000
#                   Checking account  Ratio  TARGET_MEAN
# Checking account
# little                         274   27.4     0.507299
# moderate                       269   26.9     0.609665
# rich                            63    6.3     0.777778
#                      Purpose  Ratio  TARGET_MEAN
# business                  97    9.7     0.649485
# car                      337   33.7     0.685460
# domestic appliances       12    1.2     0.666667
# education                 59    5.9     0.610169
# furniture/equipment      181   18.1     0.679558
# radio/TV                 280   28.0     0.778571
# repairs                   22    2.2     0.636364
# vacation/others           12    1.2     0.583333
# 4 categorical variables have been described
# There are 0 variables have more than 10 classes

for col in cat_cols:
    sns.countplot(x=col, data=df)
    plt.show()

num_cols = [col for col in df.columns if df[col].dtypes != 'O' and col not in "Risk" and col not in "Job"]

df.describe([.01,.25,.50,.75,.99]).T

#                count      mean          std    min      1%     25%     50%  \
# Age            1000.0    35.546    11.375469   19.0   20.00    27.0    33.0
# Sex            1000.0     0.690     0.462725    0.0    0.00     0.0     1.0
# Job            1000.0     1.904     0.653614    0.0    0.00     2.0     2.0
# Credit amount  1000.0  3271.258  2822.736876  250.0  425.83  1365.5  2319.5
# Duration       1000.0    20.903    12.058814    4.0    6.00    12.0    18.0
# Risk           1000.0     0.700     0.458487    0.0    0.00     0.0     1.0
#                    75%       99%      max
# Age              42.00     67.01     75.0
# Sex               1.00      1.00      1.0
# Job               2.00      3.00      3.0
# Credit amount  3972.25  14180.39  18424.0
# Duration         24.00     60.00     72.0
# Risk              1.00      1.00      1.0


df.loc[(df["Age"]>18) & (df["Age"]<=25),"Generation"] = "Young"
df.loc[(df["Age"]>25) & (df["Age"]<=35),"Generation"] = "Adult"
df.loc[(df["Age"]>35) & (df["Age"]<=60),"Generation"] = "Mature"
df.loc[(df["Age"]>60),"Generation"] = "Senior"

# Age degiskenini 4 parçaya ayırdık.

df["Saving accounts"].value_counts()
# little        603
# moderate      103
# quite rich     63
# rich           48
df["Saving accounts"].count()
#817
#(603/817)*100 = 73.08 Saving accountun neredeyse yüzde 75 ' lik bölümü little oldugundan buradaki
#eksik degerlerin yerine little atanabilir.

df2 = df

df2["Saving accounts"].fillna("little", inplace=True)

df2["Saving accounts"].value_counts()

# little        786
# moderate      103
# quite rich     63
# rich           48

df["Checking account"].value_counts()
# little      274
# moderate    269
# rich         63

df["Checking account"].count()
# 606

df2["Checking account"].fillna(df2["Checking account"].mode()[0],inplace = True)

df2.isnull().sum()
# Age                 0
# Sex                 0
# Job                 0
# Housing             0
# Saving accounts     0
# Checking account    0
# Credit amount       0
# Duration            0
# Purpose             0
# Risk                0
# Generation          0

#Eksik degerlerden kurtulduk simdi sıra outlier'lara bakma var.

def has_outliers(dataframe , variable):
    low_limit  , up_limit = outlier_thresholds(dataframe, variable)
    if dataframe[(dataframe[variable ] <low_limit) | (dataframe[variable ]> up_limit)].any(axis=None):
        print(variable ,"yes")
num_names = [col for col in df.columns if len(df[col].unique()) > 10
             and df[col].dtypes != 'O'
             and col not in "Duration"]
has_outliers(df2,num_names)

#['Age', 'Credit amount'] yes
# "Age" ve "Credit amount" degiskenleri outlier'a sahip bunlardan kurtulmak icin


def outlier_thresholds(dataframe, variable):
    quartile1=dataframe[variable].quantile(0.25)
    quartile3=dataframe[variable].quantile(0.75)
    interquantile_range=quartile3-quartile1
    up_limit=quartile3+ 1.5*interquantile_range
    low_limit=quartile1-1.5*interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

outlier_columns = ["Age","Credit amount"]
for col in outlier_columns:
    replace_with_thresholds(df2,col)

#Aykırı degerlerden kurtulduk

has_outliers(df2,num_names)

df2.describe().T

#            count       mean          std    min     25%     50%      75%  \
# Age            1000.0    35.4535    11.106324   19.0    27.0    33.0    42.00
# Sex            1000.0     0.6900     0.462725    0.0     0.0     1.0     1.00
# Job            1000.0     1.9040     0.653614    0.0     2.0     2.0     2.00
# Credit amount  1000.0  3051.1010  2187.140403  250.0  1365.5  2319.5  3972.25
# Duration       1000.0    20.9030    12.058814    4.0    12.0    18.0    24.00
# Risk           1000.0     0.7000     0.458487    0.0     0.0     1.0     1.00
#                     max
# Age              64.500
# Sex               1.000
# Job               3.000
# Credit amount  7882.375
# Duration         72.000
# Risk              1.000

df2.loc[(df["Duration"]>0) & (df["Duration"]<=15),"DurationTenor"] = "Short"
df2.loc[(df["Duration"]>15) & (df["Duration"]<=45),"DurationTenor"] = "Middle"
df2.loc[(df["Duration"]>45) & (df["Duration"]<=72),"DurationTenor"] = "Long"

#Duration degiskenini short,middle ve long olmak üzere 3 bölüme ayırdık.

df2["DurationTenor"].value_counts()
# Middle    504
# Short     431
# Long       65

df2.drop("Duration",axis = 1,inplace = True)
df2.drop("Age",axis = 1 , inplace= True)
df2["Generation"] = df2["Generation"].astype("object")
df2["DurationTenor"] = df2["DurationTenor"].astype("object")

#One-Hot encoder uygulayabiliriz.
def one_hot_encoder(df, nan_as_category = False):
    original_columns = list(df.columns)
    categorical_columns = [col for col in df.columns if df[col].dtype == 'object']
    df = pd.get_dummies(df, columns= categorical_columns, dummy_na= nan_as_category, drop_first=True)
    new_columns = [c for c in df.columns if c not in original_columns]
    return df, new_columns

df3,new_columns = one_hot_encoder(df2)
df3 = pd.DataFrame(df3)

df3.head(5)

#  Sex  Job Housing Saving accounts Checking account  Credit amount  \
# 0    1    2     own          little           little         1169.0
# 1    0    2     own          little         moderate         5951.0
# 2    1    1     own          little           little         2096.0
# 3    1    2    free          little           little         7882.0
# 4    1    2    free          little           little         4870.0
#                Purpose  Risk Generation DurationTenor
# 0             radio/TV     1     Senior         Short
# 1             radio/TV     0      Young          Long
# 2            education     1     Mature         Short
# 3  furniture/equipment     1     Mature        Middle
# 4                  car     0     Mature        Middle

y = df3["Risk"]
X = df3.drop(["Risk"], axis=1)

models = []
models.append(('LR', LogisticRegression()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('RF', RandomForestClassifier()))
models.append(("LightGBM", LGBMClassifier()))

# evaluate each model in turn
results = []
names = []

for name, model in models:
    cv_results = cross_val_score(model, X, y, cv=10, scoring="accuracy")
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# LR: 0.707000 (0.028302)
# CART: 0.616000 (0.055893)
# RF: 0.659000 (0.025080)
# LightGBM: 0.668000 (0.043313)


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.20,random_state = 42)
log_rec = LogisticRegression().fit(X_train,y_train)
y_pred = log_rec.predict(X_test)
print(accuracy_score(y_test,y_pred))
# 0,7

print(classification_report(y_test,y_pred))

#  precision    recall  f1-score   support
#            0       0.48      0.19      0.27        59
#            1       0.73      0.91      0.81       141
#     accuracy                           0.70       200
#    macro avg       0.60      0.55      0.54       200
# weighted avg       0.65      0.70      0.65       200
