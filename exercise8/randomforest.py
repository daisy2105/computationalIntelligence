import numpy as np
import random
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import copy

# Load the Iris dataset from scikit-learn (no internet required)
iris = load_iris()
X = iris.data
y = iris.target


print("IRIS DATASET INFORMATION")

print("Dataset shape:", X.shape)
print("Number of samples:", len(X))
print("Number of features:", X.shape[1])
print("Number of classes:", len(np.unique(y)))
print("Classes:", iris.target_names)
print("Feature names:", iris.feature_names)


# Get n_estimators from user
while True:
    try:
        n_estimators = int(input("\nEnter the number of estimators (trees) for Random Forest (e.g., 50, 100, 200): "))
        if n_estimators > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

print(f"\nUsing {n_estimators} estimators for the Random Forest model.")

# Split data: 70% training, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)


print("DATA SPLIT")

print("Training set:", X_train.shape[0], "samples")
print("Validation set:", X_val.shape[0], "samples")
print("Test set:", X_test.shape[0], "samples")


# Create Random Forest model with user-defined n_estimators
rf_model = RandomForestClassifier(
    n_estimators=n_estimators,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

def cross_validate_model(X_train, y_train, model):
    """Perform 5-fold stratified cross-validation"""
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

# Training and validation loop
print("\n")
print("TRAINING AND VALIDATION")


best_val_accuracy = 0
best_model = None

for iteration in range(5):
    # Perform cross-validation
    cv_accuracy = cross_validate_model(X_train, y_train, rf_model)

    # Train on full training set
    rf_model.fit(X_train, y_train)

    # Validate
    y_val_pred = rf_model.predict(X_val)

    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_precision = precision_score(y_val, y_val_pred, average='macro')
    val_recall = recall_score(y_val, y_val_pred, average='macro')

    print(f"Iteration {iteration+1}:")
    print(f"  Cross-Validation Accuracy: {cv_accuracy:.3f}")
    print(f"  Validation Accuracy: {val_accuracy:.3f}")
    print(f"  Validation Precision: {val_precision:.3f}")
    print(f"  Validation Recall: {val_recall:.3f}")

    # Save the best model
    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        best_model = copy.deepcopy(rf_model)
        print(f"  *** New best model found! ***")



# Test the best model on the test set (unseen data)

print("TEST SET EVALUATION (Unseen Data)")


y_test_pred = best_model.predict(X_test)

test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='macro')
test_recall = recall_score(y_test, y_test_pred, average='macro')

print(f"\nBest Model Test Metrics:")
print(f"  Accuracy:  {test_accuracy:.3f}")
print(f"  Precision: {test_precision:.3f}")
print(f"  Recall:    {test_recall:.3f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
print("\nConfusion Matrix:")
print(cm)
print("\nConfusion Matrix Interpretation:")
print("  Rows = Actual Class")
print("  Columns = Predicted Class")
print(f"  [0,0] = Setosa correctly classified: {cm[0,0]}")
print(f"  [1,1] = Versicolor correctly classified: {cm[1,1]}")
print(f"  [2,2] = Virginica correctly classified: {cm[2,2]}")

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred, target_names=iris.target_names))



# Test with custom samples

print("CUSTOM SAMPLE PREDICTIONS")


sample1 = np.array([[5.1, 3.5, 1.4, 0.2]])
pred1 = best_model.predict(sample1)
prob1 = best_model.predict_proba(sample1)

print("\nTest Case 1:")
print(f"  Input: [5.1, 3.5, 1.4, 0.2] (Sepal L, Sepal W, Petal L, Petal W)")
print(f"  Predicted Class: {iris.target_names[pred1[0]]}")
print(f"  Probabilities: Setosa={prob1[0][0]:.3f}, Versicolor={prob1[0][1]:.3f}, Virginica={prob1[0][2]:.3f}")

sample2 = np.array([[6.0, 2.7, 5.1, 1.6]])
pred2 = best_model.predict(sample2)
prob2 = best_model.predict_proba(sample2)

print("\nTest Case 2:")
print(f"  Input: [6.0, 2.7, 5.1, 1.6]")
print(f"  Predicted Class: {iris.target_names[pred2[0]]}")
print(f"  Probabilities: Setosa={prob2[0][0]:.3f}, Versicolor={prob2[0][1]:.3f}, Virginica={prob2[0][2]:.3f}")

sample3 = np.array([[6.3, 3.3, 6.0, 2.5]])
pred3 = best_model.predict(sample3)
prob3 = best_model.predict_proba(sample3)

print("\nTest Case 3:")
print(f"  Input: [6.3, 3.3, 6.0, 2.5]")
print(f"  Predicted Class: {iris.target_names[pred3[0]]}")
print(f"  Probabilities: Setosa={prob3[0][0]:.3f}, Versicolor={prob3[0][1]:.3f}, Virginica={prob3[0][2]:.3f}")

# Feature Importance

print("FEATURE IMPORTANCE")


importances = best_model.feature_importances_

for name, importance in zip(iris.feature_names, importances):
    print(f"  {name}: {importance:.4f}")

print("ANALYSIS COMPLETE")


