import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.dtos import (
    TripInfo,
    FormRequestDTO,
    PlanListResponseDTO,
    PlanDTO,
    UserInput,
)
from backend.exceptions import PlanNotFound
from backend.settings import settings

load_dotenv()
sentry_sdk.init(
    dsn="https://f956c56aef0dfa46632c832796a33db2@o4504143506571264.ingest.us.sentry.io/4507214759460864",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI()

# 모든 출처에서 모든 메소드를 허용하는 CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

if settings.ELASTIC_CLUSTER_ENDPOINT and settings.ELASTIC_PASSWORD:
    from elasticsearch_dsl import connections

    connections.create_connection(
        hosts=[settings.ELASTIC_CLUSTER_ENDPOINT],
        http_auth=("elastic", settings.ELASTIC_PASSWORD),
    )


@app.get("/api/v1/plans")
def get_plans(province=None) -> PlanListResponseDTO:
    from backend.services import plan_service

    if province:
        provinces = province.split(",")
    else:
        provinces = []
    plan_list = plan_service.get_plans(provinces=provinces)

    return PlanListResponseDTO(plan_list=plan_list)


@app.get("/api/v1/plan/{plan_id}")
def get_plan(plan_id: int) -> PlanDTO:
    from backend.services import plan_service

    try:
        plan = plan_service.get_plan(plan_id)
    except PlanNotFound:
        raise HTTPException(status_code=404, detail="존재하지 않는 plan 입니다.")
    return plan


@app.post("/api/v1/plans")
def create_plan(form_request_dto: FormRequestDTO, trigger_skyscanner: bool = True):
    from backend.services import plan_service

    try:
        trip_member_num = form_request_dto.trip_member_num
        trip_member_num = int(trip_member_num)
    except ValueError:
        trip_member_num = 1

    if trip_member_num > 8:
        raise HTTPException(status_code=400, detail="최대 8명까지만 가능합니다.")

    trip_info = TripInfo.from_form_request_dto(form_request_dto)
    plan_service.initiate_plan(trip_info, trigger_skyscanner)
    return {}


@app.patch("/api/v1/plan/{plan_id}")
def edit_plan(user_content: UserInput) -> bool:
    from backend.services import plan_service

    if plan_service.update_plan(user_content.plan_id, user_content.msg):
        return False
    else:
        return True
