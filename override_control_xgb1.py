import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib

# 1. Generate synthetic but more realistic data
np.random.seed(42)
n_samples = 5000

data = {
    'v': np.clip(np.random.normal(loc=60, scale=20, size=n_samples), 0, 150),
    'x': np.clip(np.random.exponential(scale=25, size=n_samples), 0, 100),
    'y': np.random.beta(2, 5, n_samples),  # more low intent cases
    'brake': np.clip(np.random.normal(loc=40, scale=20, size=n_samples), 0, 100),
    'steer': np.random.uniform(-45, 45, n_samples),
    'a': np.clip(np.random.normal(loc=0, scale=3, size=n_samples), -10, 10),
    'angle_to_ped': np.random.uniform(0, 180, n_samples),
    'μ': np.random.uniform(0.2, 1.0, n_samples),
    'vis': np.random.uniform(0.2, 1.0, n_samples),
    'bdist': np.clip(np.random.normal(loc=50, scale=20, size=n_samples), 0, 120),
}
df = pd.DataFrame(data)

conditions = [
    # A3 (Emergency)
    ((df['x'] < 15) & (df['y'] > 0.75) & (df['v'] > 60) & (df['brake'] < 20)),
    ((df['x'] < 12) & (df['y'] > 0.7) & (df['a'] > 2) & (df['μ'] < 0.4)),
    ((df['x'] < 20) & (df['y'] > 0.8) & (df['angle_to_ped'] < 20)),

    # A2 (Alert)
    ((df['x'] < 30) & (df['y'] > 0.6) & (df['v'] > 40)),
    ((df['x'] < 40) & (df['y'] > 0.5) & (df['steer'].abs() > 12)),
    ((df['x'] < 50) & (df['a'] > 3) & (df['brake'] < 30)),
]

labels = [2, 2, 2, 1, 1, 1]
df['risk_level'] = np.select(conditions, labels, default=0)

# df.head()
df['ttc'] = df['x'] / (df['v'] + 0.1)  # Time to collision
df['risk_score'] = df['y'] * df['v'] / (df['x'] + 1)

# 4. Prepare training
features = df.drop('risk_level', axis=1)
labels = df['risk_level']

# X_train, X_test, y_train, y_test = train_test_split(
#     features, labels, test_size=0.2, stratify=labels, random_state=42
# )
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

# 5. Train optimized model
model = XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    eval_metric='mlogloss',
    use_label_encoder=False,
    max_depth=6,
    learning_rate=0.05,
    n_estimators=300,
    subsample=0.9,
    colsample_bytree=0.8,
    random_state=42
)
model.fit(X_train, y_train)
# 7. Evaluate Model
# ----------------------------
y_pred = model.predict(X_test)

print("\n📊 Classification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2],
    target_names=["A1: Safe", "A2: Alert", "A3: Emergency"],
    zero_division=0
))
joblib.dump(model, 'xgb_risk_model2.pkl')
print("\n✅ Model saved as 'xgb_risk_model2.pkl'")
