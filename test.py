import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score

# Ma'lumotlarni yaratish
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000,             # O’quv tanlanma soni
    n_features=6,               # Belgilar soni
    n_informative=4,            # Foydali belgilar soni
    n_redundant=1,              # Keraksiz belgilar
    n_classes=3,                # Uchta sinf (mijozlar toifasi)
    random_state=42
)

# Belgilar nomlarini aniqlash
feature_names = ['Purchase_Amount', 'Purchase_Frequency', 'Age', 'Income', 'Gender', 'Location']
data = pd.DataFrame(X, columns=feature_names)

# "Gender" belgisini binar qiymatga aylantirish
# Gender ustuni mavjud emas, lekin bu xato
if 'Gender' in data.columns:
    data['Gender'] = data['Gender'].apply(lambda x: 'Male' if x > 0 else 'Female')

# Maqsadli ustunni qo'shish (mijoz sinfi)
data['Customer_Class'] = y

# Ma'lumotlarni train-testga ajratish
X = data[feature_names]
y = data['Customer_Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. SVM yordamida klassifikatsiya
svm_model = SVC()
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)

print("SVM natijalari:")
print(classification_report(y_test, y_pred_svm))
print(f"Aniqlik: {accuracy_score(y_test, y_pred_svm)}")

# 2. KNN yordamida klassifikatsiya
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
y_pred_knn = knn_model.predict(X_test)

print("KNN natijalari:")
print(classification_report(y_test, y_pred_knn))
print(f"Aniqlik: {accuracy_score(y_test, y_pred_knn)}")

# 3. Neyron tarmoq yordamida klassifikatsiya
mlp_model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=500, random_state=42)
mlp_model.fit(X_train, y_train)
y_pred_mlp = mlp_model.predict(X_test)

print("Neyron tarmoq natijalari:")
print(classification_report(y_test, y_pred_mlp))
print(f"Aniqlik: {accuracy_score(y_test, y_pred_mlp)}")

# CSV saqlash
data.to_csv("customer_behavior_data.csv", index=False)
print("Ma'lumotlar 'customer_behavior_data.csv' fayliga saqlandi!")
