import pandas as pd
import numpy as np
from sklearn import svm, tree, ensemble
import mysql.connector
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pickle
import seaborn as sns


# Get the data from the MySQL Azure Database:

db = mysql.connector.connect(
    user="siddhesh",
    password="Zxcvbnm1234",
    host="database101.mysql.database.azure.com",
    port=3306,
    database="sweden_property"
)
cursor = db.cursor()
cursor.execute("SELECT * FROM sweden_property.property_prices")
data = cursor.fetchall()

column_names = [desc[0] for desc in cursor.description]
cursor.close()
db.close()

df = pd.DataFrame(data, columns=column_names)


# Removing columns that will not be required for the model
del df["House_Name"]
del df["Price_Change"]
del df["Sold_date"]
del df["Charge"]
del df["Operating_cost"]
del df["Release_form"]
del df["Location"]
del df["Total_no_Floors"]
del df["Starting_price"]
del df["S_No"]
del df["Floor"]

# Fixing the data type
df["Built_on"] = df["Built_on"].astype("category")


df = df.dropna(subset=['Municipality'])


# One-hot encoding
df = pd.get_dummies(df, columns=['Built_on'], dtype='int')
df = pd.get_dummies(df, columns=['House_type'], dtype='int')


# Numerical scaling
columns_to_normalize = ['Rooms', 'Living_area', 'Plot_area', 'Other_area']
scaler = StandardScaler()
# We will do the scaling after the train-test split to avoid data leakage

# Train-test split
X = df.drop(columns=["Final_Price"])
y = df["Final_Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42)

X_train[columns_to_normalize] = scaler.fit_transform(
    X_train[columns_to_normalize])

# To save the scaling so that it can be used in the web app for the user input
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

X_test[columns_to_normalize] = scaler.transform(
    X_test[columns_to_normalize])


def target_encode(X, y):
    encoded_dict = X.groupby(X).apply(
        lambda x: y.loc[x.index].mean()).to_dict()
    return X.map(encoded_dict), encoded_dict


encoded_train, encoding_dict = target_encode(X_train["Municipality"], y_train)


def apply_encoding(X, encoding_dict, default_value=None):
    return X.map(encoding_dict).fillna(default_value)


default_value = y_train.mean()
encoded_test = apply_encoding(
    X_test["Municipality"], encoding_dict, default_value)


X_train["Municipality"] = encoded_train

X_test["Municipality"] = encoded_test


# CV plot
def plot_learning_curves(model, X, y):
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, train_sizes=np.linspace(0.1, 1.0, 10), cv=5,
        scoring='r2', shuffle=True, random_state=1
    )

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    val_scores_mean = np.mean(val_scores, axis=1)
    val_scores_std = np.std(val_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="b")
    plt.fill_between(train_sizes, val_scores_mean - val_scores_std,
                     val_scores_mean + val_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="b",
             label="Training score")
    plt.plot(train_sizes, val_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.title("Learning Curves")
    plt.xlabel("Training examples")
    plt.ylabel("R-squared scores")
    plt.legend(loc="best")
    plt.grid()
    # plt.show()
    plt.tight_layout()
    plt.savefig("Learning_curves.png", dpi=120)
    plt.close()


# Model training
params = {
    "n_estimators": 100,
    "max_depth": 4,
    "loss": "squared_error",
}

model = ensemble.GradientBoostingRegressor(**params)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)


plot_learning_curves(model, X_train, y_train)

### Residual plot###
y_pred = model.predict(X_test)

res_df = pd.DataFrame(list(zip(y_test, y_pred)), columns=["true", "pred"])

ax = sns.scatterplot(x="true", y="pred", data=res_df)
ax.set_aspect('equal')
ax.set_xlabel('True value', fontsize=18)
ax.set_ylabel('Predicted value', fontsize=18)
ax.set_title('Residuals', fontsize=22)


ax.plot([0, 20], [0, 20], 'black', linewidth=1)

plt.tight_layout()
plt.savefig("residuals.png", dpi=120)

# Metrics
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)


r2 = r2_score(y_test, y_pred)


with open("metrics.txt", 'w') as outfile:
    outfile.write("Mean Absolute error (Millions in Kr): %2.1f%%\n" % mae)
    outfile.write("Mean Square error (Millions in Kr): %2.1f%%\n" % mse)
    outfile.write("R-squared score: %2.1f%%\n" % r2)
