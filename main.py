import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# --------------------------
# 1️⃣ Load dataset
# --------------------------
df = pd.read_csv('Churn_Modelling.csv')  # replace with your file

# --------------------------
# 2️⃣ Handle Balance column
# --------------------------
lower = df['Balance'].quantile(0.01)
upper = df['Balance'].quantile(0.99)
df['Balance_capped'] = df['Balance'].clip(lower, upper)
df['Balance_log'] = np.log1p(df['Balance_capped'])

scaler_balance = StandardScaler()
df['Balance_scaled'] = scaler_balance.fit_transform(df[['Balance_log']])

# --------------------------
# 3️⃣ Scale other numeric features
# --------------------------
numeric_features = ['CreditScore', 'Age', 'Tenure', 'EstimatedSalary', 'NumOfProducts']
scaler_num = StandardScaler()
df[numeric_features] = scaler_num.fit_transform(df[numeric_features])

# --------------------------
# 4️⃣ Prepare features & target
# --------------------------
features = ['CreditScore', 'Age', 'Tenure', 'Balance_scaled', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
X = df[features]
y = df['Exited']

# --------------------------
# 5️⃣ Train/Test split
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --------------------------
# 6️⃣ Oversampling with SMOTE
# --------------------------
smote = SMOTE(random_state=42)
X_train_over, y_train_over = smote.fit_resample(X_train, y_train)

rf_over = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
rf_over.fit(X_train_over, y_train_over)

y_pred_over = rf_over.predict(X_test)
y_prob_over = rf_over.predict_proba(X_test)[:,1]

print("🔹 Random Forest with Oversampling (SMOTE):\n")
print(classification_report(y_test, y_pred_over))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob_over):.4f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_over))

# --------------------------
# 7️⃣ Undersampling
# --------------------------
rus = RandomUnderSampler(random_state=42)
X_train_under, y_train_under = rus.fit_resample(X_train, y_train)

rf_under = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
rf_under.fit(X_train_under, y_train_under)

y_pred_under = rf_under.predict(X_test)
y_prob_under = rf_under.predict_proba(X_test)[:,1]

print("\n🔹 Random Forest with Undersampling:\n")
print(classification_report(y_test, y_pred_under))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob_under):.4f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_under))
