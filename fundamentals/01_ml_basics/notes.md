# 01_ml_basics

## 핵심 개념
- Decision Tree(의사결정나무): 특성 값을 기준으로 데이터를 반복적으로 나누며 분류/회귀를 수행하는 트리 기반 모델
- train_test_split: 학습용/평가용 데이터를 분리해 모델이 처음 보는 데이터로 성능을 검증. `stratify=y`로 클래스 비율 유지
- model.score(): 분류 문제에서는 기본적으로 accuracy(정확도)를 반환
- 결측치(`isnull`)/중복(`duplicated`) 확인은 모델 학습 전 필수적인 데이터 전처리 단계

## 예제
- [`examples/decisiontree.py`](./examples/decisiontree.py) — iris 데이터셋으로 DecisionTreeClassifier를 학습하고 새로운 샘플을 예측하는 기본 분류 예제

## 헷갈렸던 부분
- pip 패키지 이름과 import 이름이 다른 경우가 있음 — scikit-learn은 설치할 땐 `pip install scikit-learn`, 코드에서는 `import sklearn`
- 가상환경(venv) 활성화 여부에 따라 패키지 설치 위치가 다름 — `(.venv)`가 안 붙은 터미널에서 설치하면 전역/사용자 site-packages에 깔려서 venv 안 코드에서는 안 보임
