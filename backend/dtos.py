from datetime import date

from pydantic import BaseModel, Field


class PlaneInfoDTO(BaseModel):
    """
    skyscanner plane info
    """

    price: str = Field(description="가격")
    origin: str = Field(description="출발지")
    destination: str = Field(description="목적지")
    departure: str = Field(description="출발일")
    arrival: str = Field(description="도착일")
    airline: str = Field(description="항공사")

    class Config:
        orm_mode = True


class AccommodationInfo(BaseModel):
    """
    skyscanner accomodation info
    """

    name: str = Field(description="숙소 이름")
    stars: str = Field(description="몇 성 호텔인지 (없을 경우에 'no_stars')")
    lowest_price: str = Field(
        description="여러 SKYSCANNER 제휴 숙소 앱 중 해당 숙소를 가장 싸게 예약할 수 있는 가격"
    )
    rating: str = Field(description="리뷰 평균 평점")
    location: str = Field(description="주소")

    class Config:
        orm_mode = True


class RestaurantInfo(BaseModel):
    """
    데이터베이스에서 가져온 식당 정보 예시 필드
    - 숙소 관련해서 request response 보내는 api에 따라
    - 가장 우선순위 마지막
    """

    name: str
    cuisine: str
    rating: float

    class Config:
        orm_mode = True


class PlanComponentDTO(BaseModel):
    component_id: int
    component_type: str
    plane_info: PlaneInfoDTO | None
    accommodation_info: AccommodationInfo | None
    activity: str

    class Config:
        orm_mode = True


class PlanDTO(BaseModel):
    plan_id: int | None
    province: str
    created_at: date = Field(default_factory=date.today)
    plan_component_list: list[PlanComponentDTO]

    class Config:
        orm_mode = True


"""
Request, Response DTOs
"""


class FormRequestDTO(BaseModel):
    mbti: str
    province: str
    days: int | None
    start_date: date
    trip_member_num: int
    trip_style_text: str


class PlanListResponseDTO(BaseModel):
    plan_list: list[PlanDTO]


class UserInput(BaseModel):
    msg: str


# Deprecated
class TripInfo(BaseModel):
    mbti: str
    province: str
    days: int
    start_date: date
    trip_member_num: int
    trip_style_text: str

    @classmethod
    def from_form_request_dto(cls, form_request_dto: FormRequestDTO) -> "TripInfo":
        return cls(
            mbti=form_request_dto.mbti,
            province=form_request_dto.province,
            days=form_request_dto.days,
            start_date=form_request_dto.start_date,
            trip_member_num=form_request_dto.trip_member_num,
            trip_style_text=form_request_dto.trip_style_text,
        )
