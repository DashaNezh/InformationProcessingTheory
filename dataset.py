import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

# Загружаем датасет
data = pd.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv',
    sep=';'
)

# Удаляем пропуски
data.dropna(inplace=True)

# Признаки и цель
X = data.drop('quality', axis=1)
y = data['quality']
y = y - y.min()  # Нормализация: 3–8 → 0–5

feature_columns = X.columns.tolist()

# Масштабирование
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Модель
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(len(np.unique(y)), activation='softmax')
])
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучение
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=0)

# Предсказание для теста
y_pred_proba = model.predict(X_test)
y_pred = np.argmax(y_pred_proba, axis=1)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nТочность модели: {accuracy:.2f}")
print("\nКлассификационный отчет:")
print(classification_report(y_test, y_pred, zero_division=0))


# === Предсказание по пользовательскому вводу ДО графиков ===
def get_predictions(alcohol):
    sample = data.iloc[0].copy()
    sample['alcohol'] = alcohol
    test_data = pd.DataFrame([sample[feature_columns]])  # избежать warning
    test_data_scaled = scaler.transform(test_data)
    predictions = model.predict(test_data_scaled)
    return np.argmax(predictions, axis=1)


def suggest_wines_by_alcohol(desired_alcohol):
    # Ищем вина, близкие по алкоголю (±0.5)
    suggestions = data[
        (abs(data['alcohol'] - desired_alcohol) <= 0.5)
    ]
    return suggestions


try:
    desired_alcohol = float(input('Введите желаемую крепость алкоголя (8.0-14.0): '))

    if not (8.0 <= desired_alcohol <= 14.0):
        raise ValueError("Крепость должна быть от 8.0 до 14.0.")

    suggested_wines = suggest_wines_by_alcohol(desired_alcohol)

    if not suggested_wines.empty:
        print(f"\nРекомендуемые вина (крепость ≈ {desired_alcohol}):")
        print(suggested_wines[['alcohol', 'quality', 'pH', 'residual sugar']].head(10))
    else:
        print("\nК сожалению, подходящих вин не найдено.")

except Exception as e:
    print(f"\nОшибка: {e}")

# === Графики ===

# Распределение реальных оценок
plt.figure(figsize=(10, 6))
sns.countplot(x=y_test)
plt.title("Распределение реальных оценок качества вина (нормализованных)")
plt.xlabel("Оценка качества (0-5)")
plt.ylabel("Количество")
plt.tight_layout()
plt.show()

# Распределение предсказанных оценок
plt.figure(figsize=(10, 6))
sns.countplot(x=y_pred)
plt.title("Распределение предсказанных моделью оценок качества")
plt.xlabel("Оценка качества (0-5)")
plt.ylabel("Количество")
plt.tight_layout()
plt.show()

# Матрица ошибок
plt.figure(figsize=(12, 8))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Матрица ошибок")
plt.xlabel("Предсказанные оценки")
plt.ylabel("Реальные оценки")
plt.tight_layout()
plt.show()
