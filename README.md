# 소셜 비디오 분석 애플리케이션 (Social Video Analytics Application)

**Nuxt 3** (프론트엔드)와 **FastAPI** (백엔드)로 구축된 풀스택 비디오 검색 및 분석 플랫폼으로, **Visual Studio Code에서 영감을 받은 디자인**이 특징입니다. **YouTube**와 **TikTok** 비디오 검색 및 분석을 모두 지원합니다.

## 주요 기능

### 🎥 비디오 검색 및 탐색
- **YouTube**: YouTube Data API v3를 사용한 실시간 비디오 검색
- **TikTok**: RapidAPI TikTok Scraper를 사용한 비디오 검색
- 플랫폼 전환 기능 (YouTube/TikTok)
- 고급 필터링 (관련성, 날짜, 조회수, 평점)
- 클라이언트 측 정렬 (조회수, 좋아요, 날짜)
- 결과 수 조절 (10, 25, 50)
- "더 보기" 기능을 통한 페이지네이션

### 📊 비디오 분석
- 조회수, 좋아요 수, 댓글 수 표시
- 조회수/구독자 비율 계산
- 게시일 추적
- 채널 정보 및 구독자 수

### 🎬 비디오 재생
- 인앱 비디오 플레이어 모달
- YouTube iframe 통합
- TikTok 비디오 지원
- 클릭하여 재생 기능

### ⚙️ 설정 관리
- YouTube API 키 설정
- TikTok RapidAPI 키 설정
- .env 파일에 안전한 키 저장
- 마스킹된 표시로 API 키 상태 모니터링

### 🎨 VS Code 디자인 테마
- VS Code 색상 팔레트를 사용한 다크 테마
- 액티비티 바 스타일의 내비게이션
- 상태 표시줄 푸터
- 부드러운 애니메이션 및 전환 효과

### 🔐 사용자 인증
- JWT 기반 로그인 시스템
- 안전한 비밀번호 저장 (bcrypt)
- 사용자 세션 관리

![캡처](./youtube_any.png)


## 기술 스택

**프론트엔드:**
- Nuxt 3
- Vue 3 Composition API
- Tailwind CSS
- Axios

**백엔드:**
- FastAPI
- Python 3.8+
- YouTube Data API v3
- Pydantic
- SQLAlchemy (ORM)
- MariaDB (데이터베이스)
- JWT (인증)

## 사전 요구 사항

- Node.js 18+ 및 npm
- Python 3.8+
- **YouTube Data API v3 키** ([여기서 발급](https://console.cloud.google.com/))
- **RapidAPI 계정** (TikTok 지원용) ([여기서 가입](https://rapidapi.com/))
- **TikTok Scraper API 구독** ([여기서 구독](https://rapidapi.com/DataFanatic/api/tiktok-scraper7))

## 설치

### 백엔드 설정

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상 환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성 및 내용
copy .env.example .env

# .env 파일을 편집하여 관련정보를 추가하세요
YOUTUBE_API_KEY=YOUTUBE_API_KEY
DB_USER=DB_USER
DB_PASSWORD=DB_PASSWORD
DB_HOST=DB_HOST
DB_PORT=DB_PORT
DB_NAME=DB_NAME
TIKTOK_API_KEY=TIKTOK_API_KEY
```
### 데이터베이스 설정 (MariaDB) 
```bash
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
```

### 사용자 계정 생성
```bash
backend $ ./venv/bin/python create_user.py you_username you_password
```
### 프론트엔드 설정

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install
```

## 애플리케이션 실행

### 백엔드 서버 시작

```bash
cd backend
uvicorn main:app --reload
```

백엔드 주소: `http://localhost:8000`
API 문서 주소: `http://localhost:8000/docs`

### 프론트엔드 서버 시작

**옵션 1: 시작 스크립트 사용 (macOS에서 NVM 사용 시 권장)**
```bash
cd frontend
./start-dev.sh
```

**옵션 2: npm 직접 사용**
```bash
cd frontend
npm run dev
```

프론트엔드 주소: `http://localhost:3000`

### 문제 해결

**"npm: command not found" 오류가 발생하는 경우:**

이 오류는 NVM(Node Version Manager)이 쉘에 제대로 로드되지 않았을 때 발생합니다. `~/.zshrc` 파일에 다음 줄을 추가하여 해결하세요:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

그 후 터미널을 다시 시작하거나 다음을 실행하세요:
```bash
source ~/.zshrc
```

또는 이를 자동으로 처리해주는 제공된 `start-dev.sh` 스크립트를 사용하세요.

## 사용 방법

1. **로그인**
   - 앱 실행 시 로그인 페이지가 표시됩니다.
   - 생성한 계정으로 로그인하세요.

2. **API 키 설정** (최초 1회)
   - 설정(Settings) 페이지로 이동
   - **YouTube**: YouTube Data API v3 키를 입력하고 "Save API Key" 클릭
   - **TikTok**: RapidAPI 키를 입력하고 "Save TikTok API Key" 클릭
   - 두 키는 선택 사항입니다 - 사용하려는 플랫폼만 설정하세요

2. **비디오 검색**
   - 비디오(Videos) 페이지(홈)로 이동
   - 플랫폼 전환기를 사용하여 플랫폼 선택 (YouTube 또는 TikTok)
   - 검색어 입력
   - 필터 조정 (정렬 기준, 최대 결과 수, 날짜 범위 등)
   - "Search" 클릭

3. **결과 정렬**
   - 정렬 버튼 사용 (조회수, 좋아요, 날짜)
   - 화살표 버튼으로 정렬 방향 전환
   - 그리드(Grid)와 테이블(Table) 뷰 간 전환

4. **비디오 재생**
   - 비디오 카드를 클릭
   - 비디오 플레이어 모달이 열림
   - X 버튼을 클릭하거나 외부를 클릭하여 닫기

5. **결과 더 보기**
   - 하단으로 스크롤하여 "Load More"를 클릭하여 페이지네이션

## API 엔드포인트

### 인증 (Auth)
- `POST /api/auth/login` - 로그인
- `POST /api/auth/register` - 회원가입

### YouTube 비디오
- `GET /api/videos/search` - YouTube 비디오 검색
  - 쿼리 파라미터: `q`, `maxResults`, `order`, `publishedAfter`, `videoDuration`, `minRatio`, `minComments`, `tag`, `pageToken`
- `GET /api/videos/{video_id}` - YouTube 비디오 상세 정보

### TikTok 비디오
- `GET /api/tiktok/search` - TikTok 비디오 검색
  - 쿼리 파라미터: `q`, `maxResults`, `order`, `publishedAfter`, `videoDuration`, `minRatio`, `minComments`, `tag`, `pageToken`
- `GET /api/tiktok/{video_id}` - TikTok 비디오 상세 정보

### 설정
- `GET /api/settings/api-key` - YouTube API 키 상태 확인
- `POST /api/settings/api-key` - YouTube API 키 저장
- `DELETE /api/settings/api-key` - YouTube API 키 삭제
- `GET /api/settings/tiktok-api-key` - TikTok API 키 상태 확인
- `POST /api/settings/tiktok-api-key` - TikTok API 키 저장
- `DELETE /api/settings/tiktok-api-key` - TikTok API 키 삭제

## 프로젝트 구조

```
youtube/
├── backend/
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정
│   ├── database.py          # 데이터베이스 연결
│   ├── models.py            # 데이터베이스 모델
│   ├── auth_utils.py        # 인증 유틸리티
│   ├── create_user.py       # 사용자 생성 스크립트
│   ├── requirements.txt     # Python 의존성
│   ├── routes/
│   │   ├── auth.py          # 인증 엔드포인트
│   │   ├── youtube.py       # YouTube 비디오 엔드포인트
│   │   ├── tiktok.py        # TikTok 비디오 엔드포인트
│   │   └── settings.py      # 설정 엔드포인트
│   └── services/
│       ├── youtube_service.py    # YouTube API 통합
│       ├── tiktok_service.py     # TikTok API 통합
│       └── settings_service.py   # 설정 관리
└── frontend/
    ├── nuxt.config.ts       # Nuxt 설정
    ├── package.json         # Node 의존성
    ├── tailwind.config.js   # Tailwind 설정
    ├── app.vue              # 루트 컴포넌트
    ├── assets/
    │   └── css/
    │       └── main.css     # 전역 스타일 (VS Code 테마)
    ├── components/
    │   ├── VideoCard.vue    # 비디오 카드 컴포넌트
    │   ├── VideoPlayer.vue  # 비디오 플레이어 모달
    │   ├── VideoTable.vue   # 테이블 뷰 컴포넌트
    │   ├── SearchBar.vue    # 검색 입력창
    │   └── FilterControls.vue  # 필터/정렬 컨트롤
    ├── composables/
    │   ├── useAuth.ts          # 인증 컴포저블
    │   ├── useYouTubeApi.ts    # YouTube API 컴포저블
    │   ├── useTikTokApi.ts     # TikTok API 컴포저블
    │   └── useSettings.ts      # 설정 컴포저블
    ├── layouts/
    │   └── default.vue      # 기본 레이아웃
    ├── middleware/
    │   └── auth.global.ts   # 전역 인증 미들웨어
    └── pages/
        ├── index.vue        # 비디오 페이지
        ├── login.vue        # 로그인 페이지
        └── settings.vue     # 설정 페이지
```

## 디자인 시스템

이 애플리케이션은 **Visual Studio Code에서 영감을 받은 디자인**을 사용합니다:

- **색상:**
  - 배경: `#1e1e1e`
  - 사이드바: `#252526`
  - 강조색: `#007acc` (파랑)
  - 하이라이트: `#f9826c` (주황)
  - 텍스트: `#cccccc`

- **타이포그래피:** Inter, Segoe UI
- **컴포넌트:** VS Code 스타일의 카드, 버튼, 입력창
- **내비게이션:** 아이콘이 있는 액티비티 바 스타일

## API 할당량

### YouTube API
무료 티어는 일일 **10,000 유닛**의 할당량을 가집니다:
- 검색 요청: ~100 유닛
- 비디오 상세: ~1 유닛

무료 티어에서 대략 **하루 100회 검색**이 가능합니다.

### TikTok API (RapidAPI)
할당량은 RapidAPI 구독 플랜에 따라 다릅니다:
- **무료 티어**: 월간 요청 제한 있음 (TikTok Scraper API 가격 정책 확인)
- **프로 티어**: 더 높은 제한 이용 가능
- 각 검색 요청은 월간 할당량에서 차감됩니다

**참고**: TikTok API 키가 설정되지 않은 경우, 앱은 TikTok 검색에 대해 모의 데이터를 표시합니다.

## 라이선스
MIT

## 작성자
LEE SUNG(ALBERT)
