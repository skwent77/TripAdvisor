# Tripper: OpenAI를 활용한 일본 여행 일정 생성 서비스

## 9조 프로젝트 개요

본 프로젝트는 OpenAI를 활용하여 일본 여행 일정을 생성하고 개선해주는 여행 계획 서비스입니다. 백엔드는 FastAPI와 MySQL을 사용하여 요청을 효과적으로 처리하고 데이터를 저장하며, 프론트엔드는 React를 사용하여 동적이고 반응이 빠른 사용자 인터페이스를 제공합니다.
저희 프로젝트는 아래 URL에서 확인할 수 있습니다.
todo URL 추가

만약 저희 프로젝트를 직접 실행해보고 싶으시면 아래 단계들을 거치면 됩니다.


todo 단계들 작성(용주 front 부분, 석진 back 부분)

## 제안서 수정사항
 팀원들의 언어 숙련도 문제로 구현 언어를 자바에서 파이썬으로 바꿨습니다.
 프로젝트 제안 발표 때 학우분들이 주신 피드백은 다음과 같았습니다.

 1) 기존의 GPT를 활용하여 여행 일정 생성하는 것과 차이점이 뭔지 모르겠다. (50%)                             - a),b),e)를 활용    
 2) 사용자의 "취향"에 맞는 여행 정보를 보여주면 좋을 것 같은데 그럴 수 있을지 모르겠다. (40%)                  - e)
 3) GPT는 2021년 9월 이후의 정보는 알려주지 않는데, 여행 정보 추천은 GPT의 활용과 어울리지 않는다. (5%)        - b),c) 
    
 1)은 peer review의 50% 정도가 지적해주신 사항이었습니다. 
 강의자료에서 듣기로 프로젝트 평가 요소에 창의성은 없었지만, 학우분들의 요청을 반영하여 제안서를 일부 수정했습니다.
 
저희가 고안해낸 위 피드백에서 제기한 부분들을 해결할 수 있는 방안은 다음과 같습니다.
 a) 일정 PDF로 만들어주는 기능      
 b) RAG를 활용하여, 21년 9월까지는 있었지만 그 이후에 사라진 호텔 정보 제거 
 c) skyscanner 활용하여 항공편 뿐만 아니라 호텔 정보까지 충분히 가져오기
 d) 기존의 지피티가 주는 여행 정보에는 동선에 대한 고려가 충분하지 않기에, 동선은 시스템 프롬프팅으로 hallucination 방지 
 e) 사용자의 MBTI를 입력값으로 받고, 이 값을 충분히 활용하기 위해 미리 저장된 json 활용
    
### 프로젝트 진행 상황
 1. (완료) 프론트와 서버 배포
 2. (완료) DB 서버에 세팅
 3. (예정) DB null 데이터 예외 처리
 4. (진행 중) Github Actions 적용
 5. (완료) GPT API Chat Completion 구현 
 6. (예정) GPT chat hallucination
 7. (예정) GPT API Moderation
 8. (미정)  Embedding 활용 여부, 항공편 왕복 검색 허용 여부

### 프로젝트 사용 유의사항
 1. skyscanner 졍책상 지난 날짜의 항공편 일정과 숙박 일정은 조회가 되지 않습니다.
 2. 10일 이상의 여행은 추천하지 않습니다.
 3. 일정 생성 시에는, 대화형 프롬프트가 제공되지 않고 기본적인 코스 생성 이후에 수정하는 부분에서 프롬프트가 제공됩니다.
 4. 채팅 사이드바는 아직 완전하지 않습니다.
 5. 홈 화면에서 제출하는 정보들은 여행 코스 추천에만 활용됩니다.
 6. 홈 화면의 각 항목에 해당하는 내용을 넣어주셔야 해당하는 여행 정보가 제공됩니다.
 7. 여행 일정 수정쪽 구현은 GPT API를 연결만 해놓은 상황입니다.
 8. 여행 일정이 무조건 출발 당일 오전부터 나오기 때문에, 일단 비행기를 오전 10시 이전 도착만 조회하도록 설정해둔 상태입니다.
 9. 따라서 일정에 맞는 비행기나 호텔이 없을 경우 비행기와 호텔 정보가 나오지 않을 수 있습니다.
 10. 처음화면에서 받은 정보를 GPT API를 통해 가공하지 않고 SKYSCANNER API를 통해 비행기와 숙소 정보를 가져오기 때문에 여행일수와 지역을 변경했을 때 비행기와 숙소 정보는 변하지 않습니다.
    
### 1. 일정 생성 (form양식 제출)

- **입력:** 사용자는 여행 날짜, 목적지, 여행자 수, 관심사 등의 여행에 필요한 정보를 설문지 형태로 입력합니다.
- **출력:** 서비스는 항공편, 숙소, 계획된 활동을 포함한 상세한 일별 여행 일정을 생성합니다.
        항공편 정보는 가격이 가장 싼 항공편을 가져옵니다.
todo 출력 화면 넣기
    
### 2. 일정 개선 (대화형)
- 사용자는 시스템과의 대화를 통해 추가적인 선호도나 변경 사항을 반영하여 여행 일정을 세밀하게 조정할 수 있습니다. 이 기능은 OpenAI의 첨단 자연어 처리 기술을 활용합니다.

### 3. 추가 기능 (개발 예정)
- **일정 PDF 내보내기:** 사용자가 여행 계획을 쉽게 공유하고 인쇄할 수 있도록 PDF로 내보내는 기능.
- **계획 공유하기:** 다른 사람들과 여행 일정을 공유할 수 있는 기능을 추가하여 사용자 경험을 향상시키고 단체 여행 계획을 용이하게 합니다.

## 사용 기술
### 디자인
- **Figma:**
  todo 용주님 화면 넣기 (따로 사용 설명 만들어도 좋아요)
 
### 백엔드
- **FastAPI:** 견고하고 높은 성능의 API를 구축하는 데 사용됩니다.
- **Swagger:** 간단한 설정으로 프로젝트에서 지정한 URL들을 HTML화면으로 확인할 수 있게 해주는 툴로 REST API 문서 자동화에 사용하였습니다.
  앞으로 변경사항이 있을 수 있습니다. https://api.visit-with-tripper.site/docs#/default/get_plans_api_v1_plans_get
- **MySQL:** 데이터 저장을 처리하며, 신뢰성 있고 확장 가능한 데이터베이스 관리를 제공합니다. MySQL DB 서버는 EC2 에 존재 
- **OpenAI API:** 사전 저장된 System Prompt 내용을 통해 일정 조정 과정에서 중요한 역할을 합니다.
- **CI/CD:** Github Actions 활용
### 프론트엔드
- **React:** 사용자가 데이터를 입력하고 실시간으로 여행 계획 업데이트를 받을 수 있도록 원활하고 상호 작용이 가능한 사용자 인터페이스를 제공합니다.
