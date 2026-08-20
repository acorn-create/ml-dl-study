"""
Decision Tree Classifier - iris 데이터셋 분류 예제

scikit-learn의 DecisionTreeClassifier로 붓꽃(iris) 품종을 분류하는 가장 기본적인
지도학습(분류) 예제.

흐름
1. iris 데이터셋을 DataFrame으로 로드하고 결측치/중복 여부 확인
2. train_test_split으로 학습용/평가용 데이터 분리 (stratify로 클래스 비율 유지)
3. DecisionTreeClassifier 학습
4. 평가용 데이터로 정확도(accuracy) 측정
5. 새로운 샘플 하나를 넣어 예측

핵심 개념
- Decision Tree(의사결정나무): 특성 값을 기준으로 데이터를 반복적으로 나누며(분기)
  분류/회귀를 수행하는 트리 기반 모델. 각 분기 조건은 정보 이득/불순도(gini 등)를
  최대한 줄이는 방향으로 학습 중 자동으로 결정된다.
- train_test_split: 모델이 학습에 쓰지 않은 데이터로 성능을 검증하기 위해
  데이터를 학습용/평가용으로 나누는 함수. stratify=y를 주면 분리 후에도
  클래스 비율이 원본과 비슷하게 유지된다.
- model.score(): 분류 모델에서는 기본적으로 accuracy(정확도)를 반환한다.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['label'] = iris.target

print(df.isnull().sum().sum())  # 결측치 확인
print(df.duplicated().sum())
df.drop_duplicates(keep='first', inplace=True)  # 중복 제거

X = df.iloc[:, :4]  
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(f"Decision Tree Classifier Accuracy: {score:.2f}")

new = np.array([[5.4, 4, 1.5, 0.2]])
y_pred = model.predict(new)
print(f"Predicted class for new sample: {y_pred[0]}")
