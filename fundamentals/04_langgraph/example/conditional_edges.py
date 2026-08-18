"""
LangGraph - 조건부 엣지(Conditional Edges) 예제

숫자 하나를 입력받아, 그 크기에 따라 서로 다른 노드로 분기하는 가장 단순한 형태의
LangGraph 그래프를 만들어본다.

핵심 개념
- StateGraph: 노드(함수)와 엣지(연결)로 워크플로우를 표현하는 그래프 빌더
- add_conditional_edges: 조건 함수의 반환값에 따라 다음에 실행할 노드를 동적으로 결정
- START / END: 그래프의 시작점과 종료점을 나타내는 특수 노드
- compile(): StateGraph 빌더를 실행 가능한 그래프(app)로 변환. 시각화(get_graph())도
  컴파일된 app에서만 가능하다.

흐름: START -> (check_size 조건 판단) -> big_handler 또는 small_handler -> END
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State: 숫자와 결과 저장
class NumberState(TypedDict):
    number: int
    result: str

# Node 1: 큰 숫자 처리
def handle_big_number(state):
    return {"result": f"{state['number']}는 큰 숫자입니다!"}

# Node 2: 작은 숫자 처리
def handle_small_number(state):
    return {"result": f"{state['number']}는 작은 숫자입니다!"}

# 조건 함수: 어디로 갈지 결정
def check_size(state):
    if state["number"] > 10:
        return "big"     # 큰 숫자면 "big"
    else:
        return "small"   # 작은 숫자면 "small"

# 그래프 구성
graph = StateGraph(NumberState)
graph.add_node("big_handler", handle_big_number)
graph.add_node("small_handler", handle_small_number)

# 조건부 엣지 추가
graph.add_conditional_edges(
    START,
    check_size,
    {
        "big": "big_handler",      # "big"이면 big_handler로
        "small": "small_handler"   # "small"이면 small_handler로
    }
)

# 끝으로 연결
graph.add_edge("big_handler", END)
graph.add_edge("small_handler", END)

# 테스트해보기
app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="conditional_edges_graph.png")  # 그래프 시각화

# 큰 숫자로 테스트
result1 = app.invoke({"number": 15, "result": ""})
print(result1)

# 작은 숫자로 테스트
result2 = app.invoke({"number": 5, "result": ""})
print(result2)
