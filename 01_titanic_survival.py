"""
Titanic Survival Prediction
Trying to predict who survived the Titanic disaster based on passenger info
(class, age, sex, fare, etc).
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ------------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------------
df = sns.load_dataset("titanic")
print("Shape:", df.shape)
print(df.head())
print(df.isnull().sum())

# ------------------------------------------------------------------
# 2. Clean up a bit
# ------------------------------------------------------------------
df = df.drop(columns=["deck", "embark_town", "alive", "class", "who", "adult_male"])

df["age"] = df["age"].fillna(df["age"].median())
df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

df["sex"] = df["sex"].map({"male": 0, "female": 1})
df = pd.get_dummies(df, columns=["embarked"], drop_first=True)

df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"] = (df["family_size"] == 1).astype(int)

df = df.dropna()

# ------------------------------------------------------------------
# 3. Quick look at survival patterns
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.barplot(x="pclass", y="survived", data=df, ax=axes[0])
axes[0].set_title("Survival rate by class")
sns.barplot(x="sex", y="survived", data=df, ax=axes[1])
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(["male", "female"])
axes[1].set_title("Survival rate by sex")
plt.tight_layout()
plt.savefig("images/survival_overview.png", dpi=120)
plt.close()

# ------------------------------------------------------------------
# 4. Model
# ------------------------------------------------------------------
features = ["pclass", "sex", "age", "sibsp", "parch", "fare",
            "family_size", "is_alone", "embarked_Q", "embarked_S"]
X = df[features]
y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)
log_preds = log_reg.predict(X_test)

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

print("\nLogistic Regression accuracy:", accuracy_score(y_test, log_preds))
print("Random Forest accuracy:", accuracy_score(y_test, rf_preds))
print("\nRandom Forest classification report:\n", classification_report(y_test, rf_preds))

# ------------------------------------------------------------------
# 5. Feature importance (from the RF model)
# ------------------------------------------------------------------
importances = pd.Series(rf.feature_importances_, index=features).sort_values()
plt.figure(figsize=(7, 5))
importances.plot(kind="barh")
plt.title("What mattered most for survival")
plt.tight_layout()
plt.savefig("images/feature_importance.png", dpi=120)
plt.close()

cm = confusion_matrix(y_test, rf_preds)
plt.figure(figsize=(4, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Random Forest")
plt.tight_layout()
plt.savefig("images/confusion_matrix.png", dpi=120)
plt.close()

print("\nDone. Plots saved in /images")
