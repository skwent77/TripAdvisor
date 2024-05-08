from datetime import date, datetime

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
        from_attributes = True


class AccommodationInfoDTO(BaseModel):
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
        from_attributes = True


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
        from_attributes = True


class PlanComponentDTO(BaseModel):
    component_id: int
    component_type: str
    plane_info: PlaneInfoDTO | None
    accommodation_info: AccommodationInfoDTO | None
    activity: str | None

    class Config:
        from_attributes = True


class PlanDTO(BaseModel):
    trip_plan_id: int | None
    province: str
    created_at: datetime
    plan_component_list: list[PlanComponentDTO]

    class Config:
        from_attributes = True


"""
Request, Response DTOs
"""


class FormRequestDTO(BaseModel):
    mbti: str
    province: str
    days: int | None | str
    start_date: date | None | str
    trip_member_num: int | None | str
    trip_style_text: str | None


class PlanListResponseDTO(BaseModel):
    plan_list: list[PlanDTO]


class UserInput(BaseModel):
    msg: str


# Deprecated
class TripInfo(BaseModel):
    mbti: str
    province: str
    days: int | None
    start_date: date | None
    trip_member_num: int | None
    trip_style_text: str | None

    @classmethod
    def from_form_request_dto(cls, form_request_dto: FormRequestDTO) -> "TripInfo":
        return cls(
            mbti=form_request_dto.mbti,
            province=form_request_dto.province,
            days=(
                form_request_dto.days
                if isinstance(form_request_dto.start_date, int)
                else 2
            ),
            start_date=(
                form_request_dto.start_date
                if isinstance(form_request_dto.start_date, date)
                else datetime.now().date
            ),
            trip_member_num=(
                form_request_dto.trip_member_num
                if form_request_dto.trip_member_num
                else 1
            ),
            trip_style_text=form_request_dto.trip_style_text,
        )
