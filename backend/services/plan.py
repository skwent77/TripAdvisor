from backend.database import SessionLocal
from backend.dtos import TripPlan, TripInfo, PlanComponent, PlaneInfo, AccommodationInfo
from backend.models import Plan
from backend.services import skyscanner_service, day_plan_service


class PlanService:
    def create_plan(self, trip_info: TripInfo) -> TripPlan:
        plan = Plan()
        plan_info = self._create_plan(trip_info)
        with SessionLocal() as session:
            session.add(plan)
            session.commit()
            session.refresh(plan)
        plan_info.trip_plan_id = plan.id
        return plan_info

    def _create_plan(self, trip_info: TripInfo) -> TripPlan:
        (
            plane_info,
            accommodation_info,
        ) = skyscanner_service.get_plane_and_accommodation_info(
            trip_info.province, trip_info.days, trip_info.start_date
        )

        day_plan_list = day_plan_service.create_day_plan_list(trip_info)

        return TripPlan(
            trip_plan=[
                self._create_plane_component(plane_info),
                self._create_accommodation_component(accommodation_info),
                PlanComponent(
                    component_id=3,
                    component_type="activity",
                    day_plan_list=day_plan_list,
                ),
            ]
        )

    def _create_plane_component(self, plane_info: PlaneInfo) -> PlanComponent:
        # TODO: skyscanner 에서 가져오기

        return PlanComponent(
            component_id=1,
            component_type="plane",
            plane_info=plane_info,
            accommodation_info=None,
            plan=[],
        )

    def _create_accommodation_component(
        self, accommodation_info: AccommodationInfo
    ) -> PlanComponent:
        # TODO: 숙소 정보 가져오기
        return PlanComponent(
            component_id=2,
            component_type="accommodation",
            plane_info=None,
            accommodation_info=accommodation_info,
            plan=[],
        )
