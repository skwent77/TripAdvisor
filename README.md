# Tripper: OpenAI를 활용한 일본 여행 일정 생성 서비스

## 프로젝트 개요

본 프로젝트는 OpenAI를 활용하여 일본 여행 일정을 생성하고 개선해주는 여행 계획 서비스입니다. 백엔드는 FastAPI와 MySQL을 사용하여 요청을 효과적으로 처리하고 데이터를 저장하며, 프론트엔드는 React를 사용하여 동적이고 반응이 빠른 사용자 인터페이스를 제공합니다.

## 주요 기능

### 1. 일정 생성
- **입력:** 사용자는 여행 날짜, 목적지, 여행자 수, 관심사 등의 여행에 필요한 정보를 설문지 형태로 입력합니다.
- **출력:** 서비스는 항공편, 숙소, 계획된 활동을 포함한 상세한 일별 여행 일정을 생성합니다.

### 2. 대화형 일정 개선
- 사용자는 시스템과의 대화를 통해 추가적인 선호도나 변경 사항을 반영하여 여행 일정을 세밀하게 조정할 수 있습니다. 이 기능은 OpenAI의 첨단 자연어 처리 기술을 활용합니다.

### 3. 추가 기능 (개발 예정)
- **일정 PDF 내보내기:** 사용자가 여행 계획을 쉽게 공유하고 인쇄할 수 있도록 PDF로 내보내는 기능.
- **계획 공유하기:** 다른 사람들과 여행 일정을 공유할 수 있는 기능을 추가하여 사용자 경험을 향상시키고 단체 여행 계획을 용이하게 합니다.

## 사용 기술

### 백엔드
- **FastAPI:** 견고하고 높은 성능의 API를 구축하는 데 사용됩니다.
- **MySQL:** 데이터 저장을 처리하며, 신뢰성 있고 확장 가능한 데이터베이스 관리를 제공합니다.
- **OpenAI API:** 자연어 이해와 생성을 위한 첨단 AI 모델을 통합하여 대화형 일정 조정 과정에서 중요한 역할을 합니다.

### 프론트엔드
- **React:** 사용자가 데이터를 입력하고 실시간으로 여행 계획 업데이트를 받을 수 있도록 원활하고 상호 작용이 가능한 사용자 인터페이스를 제공합니다.

## 결론

이 서비스는 강력한 AI 도구를 활용하여 일본 여행 계획을 수립하는 과정을 간소화하는 것을 목표로 합니다. 향후 기능 확장을 통해 일정 공유 및 내보내기 기능을 추가하여 서비스의 유용성과 사용자 친화성을 높일 예정입니다.