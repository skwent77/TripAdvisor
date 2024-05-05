from datetime import timedelta

import requests

from backend.dtos import PlaneInfoDTO, AccommodationInfo, TripInfo
from backend.settings import settings  # for skyscanner


class SkyscannerService:
    def create_AccomodationInfo(self, trip_info: TripInfo) -> AccommodationInfo:
        """
        https://rapidapi.com/ntd119/api/sky-scanner3 에서 hotels/search api 에 해당합니다.
        숙소에 관한 정보를 가져옵니다.
        """
        location_id = self._search_location(trip_info)
        return_date = trip_info.start_date + timedelta(days=trip_info.days)

        # 이유는 모르지만 completion_percentage가 100이 될때까지 api call을 반복수행하라고 하네요
        while True:
            # 맨 아래 _call_api 함수를 참고해주세요
            data = self._call_api(
                "https://sky-scanner3.p.rapidapi.com/hotels/search",
                {
                    "entityId": location_id,
                    "checkin": trip_info.start_date,
                    "checkout": return_date,
                    "adults": trip_info.trip_member_num,
                    "market": "KR",
                    "locale": "ko-KR",
                    "currency": "KRW",
                    "sorting": "-rating",  # Default value: -relevance
                },
            )
            completion_percentage = data["data"]["status"]["completionPercentage"]

            if completion_percentage >= 100:
                break

        accomandation_id = data["data"]["results"]["hotelCards"][0]["id"]

        # check-in time, check-out time, location
        detailed_data = self._call_api(
            "https://sky-scanner3.p.rapidapi.com/hotels/detail",
            {"id": accomandation_id},
        )

        return AccommodationInfo(
            name=data["data"]["results"]["hotelCards"][0]["name"],
            stars=data["data"]["results"]["hotelCards"][0]["stars"],
            lowest_price=data["data"]["results"]["hotelCards"][0]["lowestPrice"][
                "price"
            ],
            rating=str(
                data["data"]["results"]["hotelCards"][0]["reviewsSummary"]["score"]
            ),
            location=detailed_data["data"]["location"]["address"],
            # accomandation_image = data["data"]["result"]["hotelCards"][0]["images"]  # list of image urls
        )

    def _search_location(self, trip_info: TripInfo) -> str:
        """
        hotels/auto-complete api 에 해당합니다. province 기반으로 search_accomandation에서 검색할 지역 id를 return 합니다.
        """
        data = self._call_api(
            "https://sky-scanner3.p.rapidapi.com/hotels/auto-complete",
            {"query": trip_info.province, "market": "KR", "locale": "ko-KR"},
        )

        location_id = "27542089"  # data["data"][0]["entityId"]

        return location_id

    def create_PlaneInfoDTO(self, trip_info: TripInfo, direction: int) -> PlaneInfoDTO:
        """
        flights/search-one-way api 에 해당합니다. 편도 비행기표를 찾습니다.
        왕복대신 편도를 쓴 이유는 왕복으로 찾을 경우 갈 때 가격, 올 때 가격을 따로 계산하지 않고 합쳐서 계산하기 때문에
        나중에 feedback 받을 때 수정하기 어려울 것 같아서 이렇게 했습니다.
        사실 왕복으로 검색하고 flights/detail api로 각 비행 id를 넣어 따로 계산할 순 있는데 귀찮아서 일단 이렇게 했습니다.
        """
        airport_id = self._search_airport(trip_info)

        if direction == 0:  # 가는 비행기
            data = self._call_api(
                "https://sky-scanner3.p.rapidapi.com/flights/search-one-way",
                {
                    "fromEntityId": "eyJzIjoiSUNOIiwiZSI6Ijk1NjczNjU5IiwiaCI6IjI3NTM4NjM4In0=",
                    "toEntityId": airport_id,
                    "departDate": TripInfo.start_date,
                    "market": "KR",
                    "locale": "ko-KR",
                    "currency": "KRW",
                    "adults": trip_info.trip_member_num,
                },
            )
        elif direction == 1:  # 오는 비행기
            return_date = trip_info.start_date + timedelta(days=trip_info.days)
            data = self._call_api(
                "https://sky-scanner3.p.rapidapi.com/flights/search-one-way",
                {
                    "fromEntityId": airport_id,
                    "toEntityId": "eyJzIjoiSUNOIiwiZSI6Ijk1NjczNjU5IiwiaCI6IjI3NTM4NjM4In0=",
                    "departDate": return_date,
                    "market": "KR",
                    "locale": "ko-KR",
                    "currency": "KRW",
                    "adults": trip_info.trip_member_num,
                },
            )

        status = data["data"]["context"]["status"]

        # 사이트에서 status == incomplete로 나오면 search/incomplete 쓰라고 해서 그렇게 했습니다.
        # 코드 중복이 생기긴 했는데 줄일 수 있을지 잘 모르겠네요.
        if status == "incomplete":
            session_id = data["data"]["context"]["sessionId"]
            return self._search_incomplete(session_id)
        elif status == "failure":
            return PlaneInfoDTO(
                price="",
                origin="",
                destination="",
                departure="",
                arrival="",
                airline="",
            )

        return PlaneInfoDTO(
            price=str(data["data"]["itineraries"][0]["price"]["formatted"]),
            origin=data["data"]["itineraries"][0]["legs"][0]["origin"]["name"],
            destination=data["data"]["itineraries"][0]["legs"][0]["destination"][
                "name"
            ],
            departure=data["data"]["itineraries"][0]["legs"][0]["departure"],
            arrival=data["data"]["itineraries"][0]["legs"][0]["arrival"],
            airline=data["data"]["itineraries"][0]["legs"][0]["carriers"]["marketing"][
                0
            ]["name"],
        )

    def _search_airport(self, trip_info: TripInfo) -> str:
        """
        공항 id 찾는 flights/auto-complete api 입니다.
        """
        data = self._call_api(
            "https://sky-scanner3.p.rapidapi.com/flights/auto-complete",
            {"query": trip_info.province, "market": "KR", "locale": "ko-KR"},
        )
        airport_id = data["data"][0]["presentation"]["id"]
        print(airport_id)

        return airport_id

    def _search_incomplete(self, session_id: str) -> PlaneInfoDTO:
        """
        status == incomplete 나오면 쓰는 search/incomplete api 입니다.
        """
        data = self._call_api(
            "https://sky-scanner3.p.rapidapi.com/flights/search-incomplete",
            {
                "sessionId": session_id,
                "currency": "KRW",
                "market": "KR",
                "locale": "ko-KR",
            },
        )

        return PlaneInfoDTO(
            price=str(data["data"]["itineraries"][0]["price"]["formatted"]),
            origin=data["data"]["itineraries"][0]["legs"][0]["origin"]["name"],
            destination=data["data"]["itineraries"][0]["legs"][0]["destination"][
                "name"
            ],
            departure=data["data"]["itineraries"][0]["legs"][0]["departure"],
            arrival=data["data"]["itineraries"][0]["legs"][0]["arrival"],
            airline=data["data"]["itineraries"][0]["legs"][0]["carriers"]["marketing"][
                0
            ]["name"],
        )

    def _call_api(self, end_point: str, querystring: dict) -> dict:
        """
        requests 라이브러리 써서 api call하는게 많이 겹쳐서 함수로 만들었습니다.
        """
        headers = {
            "X-RapidAPI-Key": settings.SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com",
        }
        # 예외처리 부분은 gpt가 짜줬습니다.
        try:
            response = requests.get(end_point, headers=headers, params=querystring)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
