# -*- coding: utf-8 -*-
"""groupproject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B0r56rq-kqmF_kJI62jxzafKixUoozYL
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('/content/sample_data/slaesinfo.csv')

data.sample(5)

data.isnull().sum()

per = data.isnull().sum() * 100 / len(data)
print(per)

data.duplicated().any()

"""**Handling The missing Values**"""

data['Item_Weight']

data['Outlet_Size']

data['Outlet_Size']

mean_weight = data['Item_Weight'].mean()
median_weight = data['Item_Weight'].median()

print(mean_weight,median_weight)

data['Item_Weight_mean']=data['Item_Weight'].fillna(mean_weight)
data['Item_Weight_median']=data['Item_Weight'].fillna(median_weight)

data.head(1)

print("Original Weight variable variance",data['Item_Weight'].var())
print("Item Weight variance after mean imputation",data['Item_Weight_mean'].var())
print("Item Weight variance after median imputation",data['Item_Weight_median'].var())

data['Item_Weight'].plot(kind = "kde",label="Original")

data['Item_Weight_mean'].plot(kind = "kde",label = "Mean")

data['Item_Weight_median'].plot(kind = "kde",label = "Median")

plt.legend()
plt.show()

data[['Item_Weight','Item_Weight_mean','Item_Weight_median']].boxplot()

data['Item_Weight_interploate']=data['Item_Weight'].interpolate(method="linear")

data['Item_Weight'].plot(kind = "kde",label="Original")

data['Item_Weight_interploate'].plot(kind = "kde",label = "interploate")

plt.legend()
plt.show()



from sklearn.impute import KNNImputer

knn = KNNImputer(n_neighbors=10,weights="distance")

data['knn_imputer']= knn.fit_transform(data[['Item_Weight']]).ravel()

data['Item_Weight'].plot(kind = "kde",label="Original")

data['knn_imputer'].plot(kind = "kde",label = "KNN imputer")

plt.legend()
plt.show()

data = data.drop(['Item_Weight','Item_Weight_mean','Item_Weight_median','knn_imputer'],axis=1)

data.head(1)

data.isnull().sum()

"""Outlet_Size"""

data['Outlet_Size'].value_counts()

data['Outlet_Type'].value_counts()

mode_outlet = data.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x:x.mode()[0]))

mode_outlet

missing_values = data['Outlet_Size'].isnull()

missing_values

data.loc[missing_values,'Outlet_Size'] = data.loc[missing_values,'Outlet_Type'].apply(lambda x :mode_outlet[x])

data.isnull().sum()

"""**Item_Fat_Content**"""

data.columns

data['Item_Fat_Content'].value_counts()

data.replace({'Item_Fat_Content':{'Low Fat':'LF','low fat':'LF','reg':'Regular'}},inplace=True)

data['Item_Fat_Content'].value_counts()

"""**Item_Visibility**"""

data.columns

data['Item_Visibility'].value_counts()

data['Item_Visibility_interpolate']=data['Item_Visibility'].replace(0,np.nan).interpolate(method='linear')

data.head(1)

data['Item_Visibility_interpolate'].value_counts()

data['Item_Visibility'].plot(kind="kde",label="Original")

data['Item_Visibility_interpolate'].plot(kind="kde",color='red',label="Interpolate")

plt.legend()
plt.show()

data = data.drop('Item_Visibility',axis=1)

data.head(1)

"""
Item_Type"""

data.columns

data['Item_Type'].value_counts()

"""**Item_Identifier**"""

data.columns

data['Item_Identifier'].value_counts().sample(5)

data['Item_Identifier'] =data['Item_Identifier'].apply(lambda x : x[:2])

data['Item_Identifier'].value_counts()

"""**Outlet_Establishment_Year**"""

data.columns

data['Outlet_Establishment_Year']

import datetime as dt

current_year = dt.datetime.today().year

current_year

data['Outlet_age']= current_year - data['Outlet_Establishment_Year']

data.head(1)

data = data.drop('Outlet_Establishment_Year',axis=1)

data.head()

"""**Handling Categorical Columns**"""

from sklearn.preprocessing import OrdinalEncoder

data_encoded = data.copy()

cat_cols = data.select_dtypes(include=['object']).columns

for col in cat_cols:
    oe = OrdinalEncoder()
    data_encoded[col]=oe.fit_transform(data_encoded[[col]])
    print(oe.categories_)

data_encoded.head(3)

X = data_encoded.drop('Item_Outlet_Sales',axis=1)
y = data_encoded['Item_Outlet_Sales']

y

"""**Support Vector Regression (SVR)**"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score

svr = SVR(kernel='linear')
scores = cross_val_score(svr, X, y, cv=5, scoring='r2')

print("Mean R-squared score:", scores.mean())

"""**Random Forest Regressor**"""

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import cross_val_score

rf = RandomForestRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(rf,X,y,cv=5,scoring='r2')
print(scores.mean())

"""**XGBRFRegressor**"""

from xgboost import XGBRFRegressor

xg = XGBRFRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(xg,X,y,cv=5,scoring='r2')
print(scores.mean())

"""**XGBRFRegressor Feature importances**"""

xg = XGBRFRegressor(n_estimators=100,random_state=42)

xg1 = xg.fit(X,y)
pd.DataFrame({
    'feature':X.columns,
    'XGBRF_importance':xg1.feature_importances_

}).sort_values(by='XGBRF_importance',ascending=False)

['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content']

from xgboost import XGBRFRegressor

xg = XGBRFRegressor(n_estimators=100,random_state=42)
scores = cross_val_score(xg1,X.drop(['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content'],axis=1),y,cv=5,scoring='r2')
print(scores.mean())

final_data = X.drop(columns=['Item_Visibility_interpolate','Item_Weight_interploate',
'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content'],axis=1)

final_data

"""**Model Building**

**Using Random Forest For Building Model**
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score

X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(final_data, y, test_size=0.2, random_state=42)

rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

rf_regressor.fit(X_train_rf, y_train_rf)


y_pred_rf = rf_regressor.predict(X_test_rf)


mse_rf = mean_squared_error(y_test_rf, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
mae_rf = mean_absolute_error(y_test_rf, y_pred_rf)
r2_rf = r2_score(y_test_rf, y_pred_rf)

print("Mean Squared Error (MSE):", mse_rf)
print("Root Mean Squared Error (RMSE):", rmse_rf)
print("Mean Absolute Error (MAE):", mae_rf)
print("R-squared (R2):", r2_rf)

pred2 = rf_regressor.predict(np.array([[141.6180,9.0,1.0,1.0,27]]))[0]
print(pred2)

"""---------------------------------------------------------------------------------------------------

**Now Using Svr For Building Model**
"""

from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score

X_train_svr, X_test_svr, y_train_svr, y_test_svr = train_test_split(final_data, y, test_size=0.2, random_state=42)



svr_model = SVR(kernel='linear')
svr_model.fit(X_train_svr, y_train_svr)

y_pred_svr = svr_model.predict(X_test_svr)

scores = cross_val_score(svr_model, final_data, y, cv=5, scoring='r2')

print("Mean R-squared score:", scores.mean())

mse_svr = mean_squared_error(y_test_svr, y_pred_svr)
rmse_svr = np.sqrt(mse_svr)
mae_svr = mean_absolute_error(y_test_svr, y_pred_svr)
r2_svr = r2_score(y_test_svr, y_pred_svr)

print("Mean Squared Error (MSE):", mse_svr)
print("Root Mean Squared Error (RMSE):", rmse_svr)
print("Mean Absolute Error (MAE):", mae_svr)
print("R-squared (R2):", r2_svr)

pred3 = svr_model.predict(np.array([[141.6180,9.0,1.0,1.0,27]]))[0]
print(pred3)

"""------------------------------------------------------------------------------------------------------

Best[XGBOOST]
"""

from xgboost import XGBRFRegressor

xg_final = XGBRFRegressor()

xg_final.fit(final_data,y)

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, log_loss
from sklearn.datasets import make_classification

X_train_xg,X_test_xg,y_train_xg,y_test_xg = train_test_split(final_data,y,
                                                 test_size=0.20,
                                                 random_state=42)

xg_final.fit(X_train_xg,y_train_xg)

y_pred_xg = xg_final.predict(X_test_xg)

r2_train_xg = metrics.r2_score(y_test_xg, y_pred_xg).mean()
print("R-squared value for test_data =", r2_train_xg)

mse_xg = mean_squared_error(y_test_xg, y_pred_xg)
rmse_xg = np.sqrt(mse_xg)
mae_xg = mean_absolute_error(y_test_xg, y_pred_xg)
r2_xg = r2_score(y_test_xg, y_pred_xg)

print("Implementation Details:\n")
print("Mean Squared Error (MSE): {:.2f}".format(mse_xg))
print("Root Mean Squared Error (RMSE): {:.2f}".format(rmse_xg))
print("Mean Absolute Error (MAE): {:.2f}".format(mae_xg))
print("R-squared (R2): {:.1f}%".format(r2_xg * 100))

mean_absolute_error(y_test_xg,y_pred_xg)

# Evaluation metrics for two models
models = ['Random Forest', 'XGBoost']
metrics = ['MSE', 'RMSE', 'MAE', 'R-squared']

# Values for Random Forest
values_rf = [mse_rf, rmse_rf, mae_rf, (r2_rf * 100)]

# Values for XGBoost
values_xgb = [mse_xg, rmse_xg, mae_xg, (r2_xg * 100)]

# Create subplots for each metric
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.ravel()

# Plot each metric
for i, metric in enumerate(metrics):
    axs[i].bar(models, [values_rf[i], values_xgb[i]], color=['skyblue', 'lightgreen'])
    axs[i].set_title(metric)
    axs[i].set_ylabel(metric)

    # Annotate which model performs better for each metric
    if metric != 'R-squared':
        if values_rf[i] < values_xgb[i]:
            axs[i].text(0.5, 0.5, 'Random Forest better', horizontalalignment='center', verticalalignment='center', transform=axs[i].transAxes, color='red')
        else:
            axs[i].text(0.5, 0.5, 'XGBoost better', horizontalalignment='center', verticalalignment='center', transform=axs[i].transAxes, color='red')
    else:
        if values_rf[i] < values_xgb[i]:
            axs[i].text(0.5, 0.5, 'XGBoost better', horizontalalignment='center', verticalalignment='center', transform=axs[i].transAxes, color='red')
        else:
            axs[i].text(0.5, 0.5, 'Random Forest better', horizontalalignment='center', verticalalignment='center', transform=axs[i].transAxes, color='red')

plt.tight_layout()
plt.show()

"""**Prediction on Unseen Data**"""

pred = xg_final.predict(np.array([[141.6180,9.0,1.0,1.0,24]]))[0]
print(pred)

print(f"Sales Value is between {pred-714.42} and {pred+714.42}")

import joblib

joblib.dump(xg_final,'bigmart_model')

model = joblib.load('bigmart_model')

pred = model.predict(np.array([[141.6180,9.0,1.0,1.0,24]]))[0]
print(pred)

print(f"Sales Value is between {pred-714.42} and {pred+714.42}")