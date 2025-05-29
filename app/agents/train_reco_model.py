import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

try:
    print("🔄 Loading dataset...")
    df = pd.read_csv("app/data/Train_Set.csv")
    print(f"✅ Dataset loaded: {df.shape[0]} rows")

    # === Encode Categorical Features ===
    print("🔄 Encoding categorical features...")
    df_encoded = df.copy()
    le_genre = LabelEncoder()
    le_emotion = LabelEncoder()
    le_label = LabelEncoder()

    df_encoded['genre'] = le_genre.fit_transform(df['genre'])
    df_encoded['émotion'] = le_emotion.fit_transform(df['émotion'])
    df_encoded['label'] = le_label.fit_transform(df['label'])

    X = df_encoded[['genre', 'âge_estimé', 'émotion']]
    y = df_encoded['label']
    print("✅ Features encoded")

    # === Split ===
    print("🔄 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    print("✅ Data split complete")

    # === Train Models ===
    print("🚀 Training models...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)

    rf.fit(X_train, y_train)
    xgb.fit(X_train, y_train)
    print("✅ Individual models trained")

    # === Evaluation ===
    print("\n📊 Random Forest Report:")
    print(classification_report(y_test, rf.predict(X_test), target_names=le_label.classes_))

    print("\n📊 XGBoost Report:")
    print(classification_report(y_test, xgb.predict(X_test), target_names=le_label.classes_))

    # === VotingClassifier ===
    print("🔀 Creating VotingClassifier...")
    voting_model = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb)],
        voting='soft'
    )
    voting_model.fit(X_train, y_train)
    print("✅ VotingClassifier trained")

    # === Save Everything ===
    print("💾 Saving model and encoders...")
    os.makedirs("app/models", exist_ok=True)
    joblib.dump(voting_model, "app/models/ad_recommender.pkl")
    joblib.dump(le_genre, "app/models/le_genre.pkl")
    joblib.dump(le_emotion, "app/models/le_emotion.pkl")
    joblib.dump(le_label, "app/models/le_label.pkl")
    print("✅ All files saved to app/models/")

except Exception as e:
    print("❌ ERROR:", e)
