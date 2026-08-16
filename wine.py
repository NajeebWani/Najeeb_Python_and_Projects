"""
Wine Classification

Using chemical properties of wine (alcohol content, acidity, etc) to guess
which of 3 cultivars it came from. sklearn's built-in wine dataset, small
and clean, good for practicing classification without needing to worry
about cleaning.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix

data = load_wine()
df = pd.DataFrame(data.data, columns=data.feature_names)
df["target"] = data.target

print(df.shape)
print(df["target"].value_counts())
print(df.describe().T[["mean", "std", "min", "max"]])

# correlation heatmap, just to get a feel for the features
plt.figure(figsize=(10, 8))
sns.heatmap(df.drop(columns="target").corr(), cmap="coolwarm", center=0)
plt.title("Feature correlations")
plt.tight_layout()
plt.savefig("images/correlations.png", dpi=110)
plt.close()

X = df.drop(columns="target")
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_s, y_train)
knn_pred = knn.predict(X_test_s)
print("\nKNN accuracy:", accuracy_score(y_test, knn_pred))

svm = SVC(kernel="rbf", C=1.0)
svm.fit(X_train_s, y_train)
svm_pred = svm.predict(X_test_s)
print("SVM accuracy:", accuracy_score(y_test, svm_pred))

# also check cross-val score so we're not just getting lucky with one split
cv_scores = cross_val_score(SVC(kernel="rbf"), scaler.fit_transform(X), y, cv=5)
print("SVM 5-fold CV scores:", cv_scores, "avg:", cv_scores.mean())

cm = confusion_matrix(y_test, svm_pred)
plt.figure(figsize=(4.5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=data.target_names, yticklabels=data.target_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("SVM confusion matrix")
plt.tight_layout()
plt.savefig("images/confusion_matrix.png", dpi=120)
plt.close()

print("done")
