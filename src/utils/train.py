import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, roc_auc_score, f1_score, precision_score, recall_score
import xgboost as xgb
import joblib

# === Config ===
SEED = 42
N_SPLITS = 5
TARGET_COL = "isFraud"
DROP_COLS = ["id", "nameOrig", "nameDest", "type"]

def convert_categoricals(df):
    """Convertit les colonnes catégorielles"""
    for col in df.select_dtypes(include=["object", "string"]).columns:
        if col not in DROP_COLS:  
            df[col] = df[col].astype("category")
    return df

def train_model(X, y):
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    
    best_model = None
    best_f1 = 0
    all_scores = []
    
    print(f"Démarrage de l'entraînement avec {N_SPLITS} folds...")
    print(f"Forme des données: {X.shape}")
    print(f"Distribution des classes: {y.value_counts().to_dict()}")
    
    fold = 0
    for train_idx, val_idx in skf.split(X, y):
        fold += 1
        print(f"\n=== Fold {fold}/{N_SPLITS} ===")
        
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
        print(f"Scale pos weight: {pos_weight:.2f}")
        
        model = xgb.XGBClassifier(
            n_estimators=100,  
            max_depth=4,       
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=pos_weight,
            random_state=SEED,
            eval_metric="logloss",
            enable_categorical=True,
            n_jobs=-1,         
            verbosity=0        
        )
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]
        
        f1 = f1_score(y_val, y_pred)
        auc = roc_auc_score(y_val, y_prob)
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        
        scores = {
            'fold': fold,
            'f1': f1,
            'auc': auc,
            'precision': precision,
            'recall': recall
        }
        all_scores.append(scores)
        
        print(f"F1 Score     : {f1:.4f}")
        print(f"AUC Score    : {auc:.4f}")
        print(f"Precision    : {precision:.4f}")
        print(f"Recall       : {recall:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            print(f"✓ Nouveau meilleur modèle (F1: {f1:.4f})")
    
    scores_df = pd.DataFrame(all_scores)
    print(f"\n=== RÉSULTATS FINAUX ===")
    print(f"Moyenne F1       : {scores_df['f1'].mean():.4f} ± {scores_df['f1'].std():.4f}")
    print(f"Moyenne AUC      : {scores_df['auc'].mean():.4f} ± {scores_df['auc'].std():.4f}")
    print(f"Moyenne Precision: {scores_df['precision'].mean():.4f} ± {scores_df['precision'].std():.4f}")
    print(f"Moyenne Recall   : {scores_df['recall'].mean():.4f} ± {scores_df['recall'].std():.4f}")
    print(f"Meilleur F1      : {best_f1:.4f}")
    
    return best_model, scores_df

