import torch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl import connections
from transformers import DistilBertTokenizer, DistilBertModel

from backend.constants import INDEX_NAME
from backend.dtos import Location
from backend.settings import settings


class SearchService:
    tokenizer: DistilBertTokenizer
    model: DistilBertModel

    def __init__(self):
        connections.create_connection(
            hosts=[settings.ELASTIC_CLUSTER_ENDPOINT],
            http_auth=("elastic", settings.ELASTIC_PASSWORD),
            timeout=20,
        )
        self.tokenizer = DistilBertTokenizer.from_pretrained("monologg/distilkobert")
        self.model = DistilBertModel.from_pretrained("monologg/distilkobert")

    def search_category(self, categories: list[str], province: str) -> list[Location]:
        q_list = [Q("match", province=province)]
        if province != "일본 규슈":
            q_list.append(Q("terms", category=categories))

        s = Search(index=INDEX_NAME).query(
            Q(
                "bool",
                must=[*q_list],
            )
        )[:10]
        response = s.execute()
        locations = []

        for hit in response:
            locations.append(
                Location(
                    name=hit.name,
                    description=hit.description,
                    lat=hit.lat,
                    lon=hit.lon,
                    image_url=hit.image_url,
                )
            )
        return locations

    def search_query(self, query: str, province: str) -> str:
        """
        텍스트를 검색합니다.
        """
        query_vector = self.get_vector(query)
        s = Search(index=INDEX_NAME).query(
            "script_score",
            query=Q("match", province=province),
            script={
                "source": "cosineSimilarity(params.query_vector, 'feature_vector') + 1.0",
                "params": {"query_vector": query_vector},
            },
        )[:2]
        response = s.execute()
        result = ""
        for hit in response:
            result += f"추천 여행지 TITLE: {hit.name}, DESCRIPTION: {hit.description}\n"
        return result

    def get_vector(self, text: str) -> list[float]:
        # 텍스트를 토크나이저로 인코딩
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        # 모델에 인코딩된 입력 제공
        with torch.no_grad():
            outputs = self.model(**inputs)
        # [CLS] 토큰의 벡터를 반환
        return list(outputs.last_hidden_state[0, 0].numpy())
