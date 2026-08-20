
"""
01. 규칙/통계 기반 이상탐지 (Threshold & Z-score)
==================================================
핵심 아이디어
------------
머신러닝 모델을 학습시키지 않고도, 데이터의 통계적 특성(평균/표준편차)이나
규칙만으로 상당 부분의 이상탐지를 구현할 수 있습니다.
실무에서도 AI 모델 도입 전 1차 필터로 가장 많이 쓰이는 방식입니다.
"""

import numpy as np
import pandas as pd

# 재현성(Reproducibility)을 위해 난수 생성 시드 고정
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def generate_lot_cost_data(n_lots: int = 200) -> pd.DataFrame:
    """단위원가 가상 데이터 생성 (정상 데이터 + 의도적 이상치 삽입)"""
    standard_cost = 1200  # 원, 표준원가(기준값)

    # 정상 : 표준원가 대비 ±5% 내외의 자연스러운 변동
    # [정상 데이터 생성]
    # 평균(loc)=1200, 표준편차(scale)=60(표준원가의 5%)인 정규분포를 따르는 단위원가 n_lots개 생성
    normal_cost = np.random.normal(loc=standard_cost, scale=standard_cost * 0.05, size=n_lots)

    # LOT ID(LOT-0001, LOT-0002 ...)와 단위원가를 포함하는 DataFrame 생성
    # 예시 : LOT-0158  1918.995314
    df = pd.DataFrame({
        "lot_id": [f"LOT-{i:04d}" for i in range(1, n_lots + 1)],
        "unit_cost": normal_cost,
    })

    # [이상치(Anomaly) 강제 삽입]
    # 전체 LOT 중 무작위로 8개의 인덱스 추출 (중복 없음)
    anomaly_idx = np.random.choice(n_lots, size=8, replace=False)
    # 선택된 8개 LOT의 단위원가를 기존 값의 1.2배 ~ 1.6배 수준으로 급증시켜 이상치로 만듦
    df.loc[anomaly_idx, "unit_cost"] *= np.random.uniform(1.2, 1.6, size=len(anomaly_idx))

    # 비교 분석을 위해 표준원가 컬럼 추가
    df["standard_cost"] = standard_cost
    return df


def detect_by_zscore(df: pd.DataFrame, threshold: float = 2.5) -> pd.DataFrame:
    """통계적 방법: 평균/표준편차 기반 Z-score 이상탐지"""
    # 데이터 전체의 평균과 표준편차 산출
    mean = df["unit_cost"].mean()
    std = df["unit_cost"].std()

    # z-score 계산: (개별 값 - 평균) / 표준편차 (평균으로부터 몇 표준편차만큼 떨어져 있는지 측정)
    df["z_score"] = (df["unit_cost"] - mean) / std

    # z-score 절대값이 threshold(임계값, 기본 2.5)보다 큰 경우를 이상치(True)로 판단
    df["is_anomaly_zscore"] = df["z_score"].abs() > threshold
    return df


def detect_by_rule(df: pd.DataFrame, tolerance: float = 0.15) -> pd.DataFrame:
    """업무 규칙(Rule) 기반: 표준원가 대비 이탈률로 이상탐지"""
    # 이탈률 계산: (실제 단위원가 - 표준원가) / 표준원가
    df["deviation_ratio"] = (df["unit_cost"] - df["standard_cost"]) / df["standard_cost"]

    # 이탈률의 절댓값이 허용 오차(tolerance, 기본 15%)를 초과하면 이상치(True)로 판정
    df["is_anomaly_rule"] = df["deviation_ratio"].abs() > tolerance
    return df


def main():
    # 가상 데이터 생성
    df = generate_lot_cost_data()

    # 통계 기반 및 규칙 기반 이상탐지 수행
    df = detect_by_zscore(df)
    df = detect_by_rule(df)

    # 데이터 주요 수치 요약 출력(소수점 둘째 자리까지)
    print("=== 데이터 요약 ===")
    print(df[["unit_cost", "z_score", "deviation_ratio"]].describe().round(2))

# 4. Z-score 기준 이상치로 분류된 LOT 출력 (Z-score 내림차순 정렬)
    print("\n=== Z-score 기준 이상 LOT ===")
    print(df[df["is_anomaly_zscore"]][["lot_id", "unit_cost", "z_score"]]
          .sort_values("z_score", ascending=False))

# 5. 표준원가 이탈률 기준 이상치로 분류된 LOT 출력 (이탈률 내림차순 정렬)
    print("\n=== 표준원가 이탈률 기준 이상 LOT ===")
    print(df[df["is_anomaly_rule"]][["lot_id", "unit_cost", "deviation_ratio"]]
          .sort_values("deviation_ratio", ascending=False))

    # 두 방식이 얼마나 겹치는지 확인 -> 실무에서는 두 방식을 AND/OR로 조합해서 사용
    # 6. 두 가지 교차 검증: 교집합(AND 조건)으로 두 방식 모두 이상치로 감지한 LOT 추출 및 개수 집계
    both = df[df["is_anomaly_zscore"] & df["is_anomaly_rule"]]
    print(f"\n두 방식 모두에서 이상치로 잡힌 LOT 수: {len(both)} / 전체 {len(df)}")


if __name__ == "__main__":
    main()
