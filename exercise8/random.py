import numpy as np
import pandas as pd
import random
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import copy

iris = fetch_ucirepo(id=53)
X = iris.data.features.values
y = iris.data.targets.values.ravel()

print("Dataset shape:", X.shape)
print("Number of samples:", len(X))
print("Number of features:", X.shape[1])
print("Number of classes:", len(np.unique(y)))
print("Classes:", np.unique(y))

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

print("Training set:", X_train.shape[0], "samples")
print("Validation set:", X_val.shape[0], "samples")
print("Test set:", X_test.shape[0], "samples")

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

def cross_validate_model(X_train, y_train, model):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    accuracies = []
    
    for train_idx, val_idx in cv.split(X_train, y_train):
        X_cv_train, X_cv_val = X_train[train_idx], X_train[val_idx]
        y_cv_train, y_cv_val = y_train[train_idx], y_train[val_idx]
        
        model.fit(X_cv_train, y_cv_train)
        y_cv_pred = model.predict(X_cv_val)
        
        fold_accuracy = accuracy_score(y_cv_val, y_cv_pred)
        accuracies.append(fold_accuracy)
    
    return np.mean(accuracies)

best_val_accuracy = 0
best_model = None

for iteration in range(5):
    cv_accuracy = cross_validate_model(X_train, y_train, rf_model)
    
    rf_model.fit(X_train, y_train)
    
    y_val_pred = rf_model.predict(X_val)
    
    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_precision = precision_score(y_val, y_val_pred, average='macro')
    val_recall = recall_score(y_val, y_val_pred, average='macro')
    
    print(f"Iteration {iteration+1} - Validation Accuracy: {val_accuracy:.3f}, Precision: {val_precision:.3f}, Recall: {val_recall:.3f}")
    
    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        best_model = copy.deepcopy(rf_model)

y_test_pred = best_model.predict(X_test)

test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='macro')
test_recall = recall_score(y_test, y_test_pred, average='macro')

print(f"\nBest Model Test Metrics:\nAccuracy: {test_accuracy:.3f}, Precision: {test_precision:.3f}, Recall: {test_recall:.3f}")

cm = confusion_matrix(y_test, y_test_pred)
print("\nConfusion Matrix:\n", cm)

print("\nClassification Report:\n", classification_report(y_test, y_test_pred, target_names=['Setosa', 'Versicolor', 'Virginica']))

sample1 = np.array([[5.1, 3.5, 1.4, 0.2]])
pred1 = best_model.predict(sample1)
prob1 = best_model.predict_proba(sample1)

print("\nTest Case 1:")
print(f"Input: [5.1, 3.5, 1.4, 0.2]")
print(f"Predicted Class: {pred1[0]}")
print(f"Probabilities: {prob1[0]}")

sample2 = np.array([[6.0, 2.7, 5.1, 1.6]])
pred2 = best_model.predict(sample2)
prob2 = best_model.predict_proba(sample2)

print("\nTest Case 2:")
print(f"Input: [6.0, 2.7, 5.1, 1.6]")
print(f"Predicted Class: {pred2[0]}")
print(f"Probabilities: {prob2[0]}")

sample3 = np.array([[6.3, 3.3, 6.0, 2.5]])
pred3 = best_model.predict(sample3)
prob3 = best_model.predict_proba(sample3)

print("\nTest Case 3:")
print(f"Input: [6.3, 3.3, 6.0, 2.5]")
print(f"Predicted Class: {pred3[0]}")
print(f"Probabilities: {prob3[0]}")

feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
importances = best_model.feature_importances_

print("\nFeature Importance:")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")


