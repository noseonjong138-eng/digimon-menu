# -----------------------------------------------------------
# 디지몬의 메뉴 추천 - 스트림릿(Streamlit) 앱
# 버튼을 누르면 음식과, 그 음식에 어울리는 디지몬을 랜덤으로 추천해줍니다.
# -----------------------------------------------------------

import random
import streamlit as st

# -----------------------------------------------------------
# 1. 페이지 기본 설정
#    - 브라우저 탭 제목, 아이콘, 화면 레이아웃 등을 정합니다.
# -----------------------------------------------------------
st.set_page_config(
    page_title="디지몬의 메뉴 추천",
    page_icon="🍽️",
    layout="centered",
)

# -----------------------------------------------------------
# 2. 화면을 따뜻한 크림색 + 파란색 톤으로 꾸미기 위한 CSS
#    - st.markdown에 unsafe_allow_html=True를 주면 직접 CSS를 넣을 수 있습니다.
# -----------------------------------------------------------
st.markdown(
    """
    <style>
    /* 전체 배경을 따뜻한 크림톤으로 */
    .stApp {
        background: linear-gradient(180deg, #FFF8EC 0%, #EAF3FC 100%);
    }

    /* 메인 타이틀 색상 */
    h1 {
        color: #2F6BC4;
        text-align: center;
    }

    /* 설명 문구 가운데 정렬 */
    .desc-text {
        text-align: center;
        font-size: 18px;
        color: #8A7A63;
        margin-bottom: 24px;
    }

    /* 큰 이모지(음식 사진 대신 사용)를 담는 박스 */
    .food-photo {
        text-align: center;
        font-size: 110px;
        background: linear-gradient(160deg, #FFE9C7, #FFD9A0);
        border-radius: 24px;
        padding: 30px 0;
        margin-bottom: 10px;
        box-shadow: inset 0 0 0 4px #ffffff;
    }

    /* 음식 이름 */
    .food-name {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        color: #3E3226;
        margin-bottom: 6px;
    }

    /* 음식 추천 이유 박스 */
    .reason-box {
        background: #FFF8EC;
        border-radius: 16px;
        padding: 16px 18px;
        font-size: 17px;
        line-height: 1.6;
        color: #5B4C3A;
        margin-bottom: 22px;
    }

    /* 디지몬 소개 박스 */
    .digimon-box {
        text-align: center;
        background: #D6EAFB;
        border-radius: 22px;
        padding: 26px 18px;
        margin-bottom: 10px;
    }

    .digimon-emoji {
        font-size: 90px;
        line-height: 1;
    }

    .digimon-name {
        font-size: 26px;
        font-weight: 800;
        color: #2F6BC4;
        margin: 8px 0;
    }

    .digimon-reason {
        font-size: 17px;
        line-height: 1.6;
        color: #3E5A80;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# 3. 음식 + 디지몬 데이터 목록
#    - 하나의 딕셔너리(dict)가 "음식 하나 + 어울리는 디지몬 하나" 세트입니다.
#    - 필요하면 이 리스트에 항목을 자유롭게 추가할 수 있습니다.
# -----------------------------------------------------------
MENU_DATA = [
    {
        "food_emoji": "🍕", "food_name": "피자",
        "food_reason": "치즈가 쭉 늘어나는 재미와 뜨끈한 도우가 매력적인 만능 인기 메뉴예요.",
        "digimon_name": "그레이몬", "digimon_emoji": "🦖",
        "digimon_reason": "화끈한 불꽃 파워를 가진 그레이몬처럼, 뜨겁게 구워낸 피자가 딱 어울려요!",
    },
    {
        "food_emoji": "🍜", "food_name": "라멘",
        "food_reason": "진한 국물과 쫄깃한 면발로 속을 든든하게 채워주는 메뉴예요.",
        "digimon_name": "가부몬", "digimon_emoji": "🐢",
        "digimon_reason": "물속에서 유유히 헤엄치는 가부몬처럼, 뜨끈한 국물 속 면발이 편안하게 어울려요.",
    },
    {
        "food_emoji": "🍣", "food_name": "초밥",
        "food_reason": "신선한 재료를 한입에 즐길 수 있는 정갈하고 산뜻한 메뉴예요.",
        "digimon_name": "빙헤몬", "digimon_emoji": "🐬",
        "digimon_reason": "차가운 바다를 가르는 빙헤몬처럼, 시원하고 깔끔한 초밥이 잘 어울려요.",
    },
    {
        "food_emoji": "🍔", "food_name": "햄버거",
        "food_reason": "두툼한 패티와 신선한 채소를 한 번에 즐길 수 있는 든든한 메뉴예요.",
        "digimon_name": "레오몬", "digimon_emoji": "🦁",
        "digimon_reason": "힘차고 늠름한 레오몬처럼, 육즙 가득한 패티의 파워가 잘 어울려요.",
    },
    {
        "food_emoji": "🍦", "food_name": "아이스크림",
        "food_reason": "더운 날 시원하게 즐기기 좋은 달콤한 디저트예요.",
        "digimon_name": "유키다루몬", "digimon_emoji": "⛄",
        "digimon_reason": "눈으로 만들어진 유키다루몬처럼, 시원하고 차가운 아이스크림이 딱 어울려요!",
    },
    {
        "food_emoji": "🍛", "food_name": "카레라이스",
        "food_reason": "향긋한 향신료와 부드러운 밥이 어우러진 든든한 한 그릇 메뉴예요.",
        "digimon_name": "아구몬", "digimon_emoji": "🐊",
        "digimon_reason": "활기차고 씩씩한 아구몬처럼, 매콤하고 든든한 카레가 잘 어울려요.",
    },
    {
        "food_emoji": "🥩", "food_name": "스테이크",
        "food_reason": "겉은 바삭하고 속은 육즙 가득한 고급스러운 메뉴예요.",
        "digimon_name": "워그레이몬", "digimon_emoji": "🐲",
        "digimon_reason": "강력하고 위엄있는 워그레이몬처럼, 묵직한 존재감의 스테이크가 잘 어울려요.",
    },
    {
        "food_emoji": "🍰", "food_name": "딸기 케이크",
        "food_reason": "폭신한 시트와 달콤한 딸기가 어우러진 사랑스러운 디저트예요.",
        "digimon_name": "삐요몬", "digimon_emoji": "🐤",
        "digimon_reason": "귀엽고 사랑스러운 삐요몬처럼, 예쁘고 달콤한 케이크가 잘 어울려요!",
    },
    {
        "food_emoji": "🍝", "food_name": "크림 파스타",
        "food_reason": "부드럽고 고소한 크림소스가 면에 듬뿍 감기는 인기 메뉴예요.",
        "digimon_name": "텐타몬", "digimon_emoji": "🦂",
        "digimon_reason": "지혜롭고 차분한 텐타몬처럼, 부드럽고 진중한 크림 맛이 잘 어울려요.",
    },
    {
        "food_emoji": "🍗", "food_name": "치킨",
        "food_reason": "겉바속촉 튀김옷과 육즙이 만나는 국민 야식 메뉴예요.",
        "digimon_name": "가루몬", "digimon_emoji": "🐺",
        "digimon_reason": "날렵하고 파워풀한 가루몬처럼, 바삭하고 강렬한 치킨이 잘 어울려요!",
    },
    {
        "food_emoji": "🍩", "food_name": "도넛",
        "food_reason": "폭신폭신하고 달콤한 글레이즈가 매력적인 간식이에요.",
        "digimon_name": "코로몬", "digimon_emoji": "🐣",
        "digimon_reason": "동글동글 귀여운 코로몬처럼, 동그랗고 달콤한 도넛이 잘 어울려요!",
    },
    {
        "food_emoji": "🍱", "food_name": "도시락",
        "food_reason": "다양한 반찬을 한 번에 골고루 즐길 수 있는 알찬 한 끼예요.",
        "digimon_name": "파피몬", "digimon_emoji": "🐶",
        "digimon_reason": "부지런하고 씩씩한 파피몬처럼, 알차게 채워진 도시락이 잘 어울려요.",
    },
    {
        "food_emoji": "🌮", "food_name": "타코",
        "food_reason": "바삭한 토르티야에 매콤한 재료를 가득 채운 개성 있는 메뉴예요.",
        "digimon_name": "고마몬", "digimon_emoji": "🦭",
        "digimon_reason": "명랑하고 활발한 고마몬처럼, 톡톡 튀는 매콤한 맛이 잘 어울려요!",
    },
    {
        "food_emoji": "🍲", "food_name": "전골",
        "food_reason": "여러 재료를 함께 끓여 깊은 맛을 내는 푸짐한 나눔 요리예요.",
        "digimon_name": "엘레키몬", "digimon_emoji": "⚡",
        "digimon_reason": "보글보글 끓어오르는 전골이, 짜릿한 전기 파워의 엘레키몬과 잘 어울려요.",
    },
    {
        "food_emoji": "🥞", "food_name": "팬케이크",
        "food_reason": "폭신한 층층이 시럽이 스며드는 달콤한 브런치 메뉴예요.",
        "digimon_name": "테리어몬", "digimon_emoji": "🐇",
        "digimon_reason": "포근하고 사랑스러운 테리어몬처럼, 폭신폭신한 팬케이크가 잘 어울려요.",
    },
    {
        "food_emoji": "🍤", "food_name": "새우튀김",
        "food_reason": "바삭한 튀김옷 속 탱글한 새우가 매력적인 메뉴예요.",
        "digimon_name": "쟈미몬", "digimon_emoji": "🦐",
        "digimon_reason": "바다에서 온 쟈미몬처럼, 바다의 맛을 담은 새우튀김이 잘 어울려요.",
    },
    {
        "food_emoji": "🥪", "food_name": "샌드위치",
        "food_reason": "신선한 채소와 속재료를 간편하게 즐길 수 있는 메뉴예요.",
        "digimon_name": "빅고몬", "digimon_emoji": "🐗",
        "digimon_reason": "듬직하고 푸짐한 빅고몬처럼, 재료가 가득 든 샌드위치가 잘 어울려요.",
    },
    {
        "food_emoji": "🍡", "food_name": "경단",
        "food_reason": "쫄깃한 식감과 은은한 단맛이 매력적인 전통 간식이에요.",
        "digimon_name": "펜몬", "digimon_emoji": "🐧",
        "digimon_reason": "아기자기하고 귀여운 펜몬처럼, 앙증맞은 경단이 잘 어울려요.",
    },
    {
        "food_emoji": "🍳", "food_name": "오믈렛",
        "food_reason": "부드럽고 폭신한 달걀에 속재료를 감싼 든든한 메뉴예요.",
        "digimon_name": "비요몬", "digimon_emoji": "🐥",
        "digimon_reason": "따뜻하고 다정한 비요몬처럼, 포근한 오믈렛이 잘 어울려요.",
    },
    {
        "food_emoji": "🍢", "food_name": "어묵꼬치",
        "food_reason": "따뜻한 국물과 함께 즐기는 쫄깃한 길거리 간식이에요.",
        "digimon_name": "오타몬", "digimon_emoji": "🐙",
        "digimon_reason": "말랑말랑 유연한 오타몬처럼, 쫄깃한 어묵이 잘 어울려요.",
    },
    {
        "food_emoji": "🍨", "food_name": "빙수",
        "food_reason": "얼음을 곱게 갈아 시원하게 즐기는 여름 별미예요.",
        "digimon_name": "프리지몬", "digimon_emoji": "🧊",
        "digimon_reason": "차가운 얼음의 힘을 가진 프리지몬처럼, 시원한 빙수가 딱 어울려요!",
    },
    {
        "food_emoji": "🥟", "food_name": "만두",
        "food_reason": "육즙 가득한 소를 얇은 피로 감싼 든든한 메뉴예요.",
        "digimon_name": "아르마디몬", "digimon_emoji": "🦔",
        "digimon_reason": "동그랗게 몸을 마는 아르마디몬처럼, 동글동글한 만두가 잘 어울려요.",
    },
    {
        "food_emoji": "🍙", "food_name": "주먹밥",
        "food_reason": "간편하게 들고 먹기 좋은 든든한 한 끼 메뉴예요.",
        "digimon_name": "펄몬", "digimon_emoji": "🌱",
        "digimon_reason": "소박하고 정겨운 펄몬처럼, 담백한 주먹밥이 잘 어울려요.",
    },
    {
        "food_emoji": "🧇", "food_name": "와플",
        "food_reason": "겉은 바삭하고 속은 촉촉한 달콤한 디저트예요.",
        "digimon_name": "빠타몬", "digimon_emoji": "🦇",
        "digimon_reason": "통통 튀는 빠타몬처럼, 격자무늬가 통통 튀는 와플이 잘 어울려요.",
    },
    {
        "food_emoji": "🍉", "food_name": "수박화채",
        "food_reason": "시원한 수박과 탄산이 만나는 상큼한 여름 디저트예요.",
        "digimon_name": "팔몬", "digimon_emoji": "🌴",
        "digimon_reason": "싱그러운 자연을 닮은 팔몬처럼, 상큼한 수박화채가 잘 어울려요.",
    },
    {
        "food_emoji": "🍅", "food_name": "토마토 파스타",
        "food_reason": "새콤한 토마토소스와 면이 어우러진 상큼한 이탈리안 메뉴예요.",
        "digimon_name": "토코몬", "digimon_emoji": "🐦",
        "digimon_reason": "발랄하고 상큼한 토코몬처럼, 새콤한 토마토소스가 잘 어울려요.",
    },
    {
        "food_emoji": "🍖", "food_name": "갈비",
        "food_reason": "달콤짭짤한 양념이 배어든 육즙 가득한 대표 한식 메뉴예요.",
        "digimon_name": "몬조몬", "digimon_emoji": "🐒",
        "digimon_reason": "재주 많고 활기찬 몬조몬처럼, 다채로운 양념 맛의 갈비가 잘 어울려요.",
    },
    {
        "food_emoji": "🥧", "food_name": "애플파이",
        "food_reason": "바삭한 페이스트리 속 달콤한 사과가 가득한 클래식 디저트예요.",
        "digimon_name": "폭스몬", "digimon_emoji": "🦊",
        "digimon_reason": "영리하고 따뜻한 폭스몬처럼, 정겨운 애플파이가 잘 어울려요.",
    },
    {
        "food_emoji": "🍮", "food_name": "푸딩",
        "food_reason": "부드럽고 매끈한 식감에 달콤한 캐러멜이 어우러진 디저트예요.",
        "digimon_name": "젤리몬", "digimon_emoji": "🍮",
        "digimon_reason": "말랑말랑 젤리 같은 젤리몬처럼, 몰캉한 푸딩이 잘 어울려요.",
    },
    {
        "food_emoji": "🍲", "food_name": "된장찌개",
        "food_reason": "구수하고 깊은 맛이 밥과 잘 어울리는 든든한 한식 메뉴예요.",
        "digimon_name": "고츠몬", "digimon_emoji": "💀",
        "digimon_reason": "묵직하고 강인한 고츠몬처럼, 진하고 구수한 된장찌개가 잘 어울려요.",
    },
    {
        "food_emoji": "🥘", "food_name": "파에야",
        "food_reason": "해산물과 쌀이 어우러진 향긋한 스페인 대표 요리예요.",
        "digimon_name": "슈웅몬", "digimon_emoji": "🦅",
        "digimon_reason": "하늘을 자유롭게 나는 슈웅몬처럼, 이국적인 파에야가 잘 어울려요.",
    },
    {
        "food_emoji": "🍿", "food_name": "팝콘",
        "food_reason": "바삭하고 가볍게 즐기기 좋은 대표 간식이에요.",
        "digimon_name": "치빗몬", "digimon_emoji": "🐿️",
        "digimon_reason": "발랄하고 통통 튀는 치빗몬처럼, 톡톡 튀는 팝콘이 잘 어울려요!",
    },
    {
        "food_emoji": "🍄", "food_name": "버섯전골",
        "food_reason": "다양한 버섯의 향과 깊은 국물맛이 매력적인 요리예요.",
        "digimon_name": "모지몬", "digimon_emoji": "🍄",
        "digimon_reason": "버섯을 닮은 모지몬처럼, 향긋한 버섯전골이 찰떡같이 어울려요.",
    },
    {
        "food_emoji": "🍕", "food_name": "고구마피자",
        "food_reason": "달콤한 고구마무스와 치즈가 어우러진 인기 피자예요.",
        "digimon_name": "밈몬", "digimon_emoji": "🐐",
        "digimon_reason": "포근하고 다정한 밈몬처럼, 부드럽고 달콤한 고구마피자가 잘 어울려요.",
    },
    {
        "food_emoji": "🍜", "food_name": "우동",
        "food_reason": "굵고 쫄깃한 면발과 담백한 국물이 매력적인 메뉴예요.",
        "digimon_name": "고구몬", "digimon_emoji": "🐹",
        "digimon_reason": "포동포동 귀여운 고구몬처럼, 통통한 면발의 우동이 잘 어울려요.",
    },
    {
        "food_emoji": "🥓", "food_name": "베이컨",
        "food_reason": "짭짤하고 고소한 감칠맛이 가득한 인기 재료예요.",
        "digimon_name": "부탐몬", "digimon_emoji": "🐖",
        "digimon_reason": "통통하고 넉넉한 부탐몬처럼, 고소한 베이컨이 잘 어울려요.",
    },
    {
        "food_emoji": "🦀", "food_name": "게찜",
        "food_reason": "쫄깃하고 달콤한 속살이 매력적인 고급 해산물 요리예요.",
        "digimon_name": "샤크몬", "digimon_emoji": "🦈",
        "digimon_reason": "바다를 지배하는 샤크몬처럼, 바다의 진미인 게찜이 잘 어울려요.",
    },
    {
        "food_emoji": "🍇", "food_name": "과일 타르트",
        "food_reason": "바삭한 타르트지 위에 새콤달콤한 과일을 올린 디저트예요.",
        "digimon_name": "플로라몬", "digimon_emoji": "🌸",
        "digimon_reason": "꽃처럼 화사한 플로라몬처럼, 알록달록한 과일 타르트가 잘 어울려요.",
    },
    {
        "food_emoji": "🍳", "food_name": "계란찜",
        "food_reason": "부드럽고 폭신한 식감의 순한 반찬이에요.",
        "digimon_name": "타네몬", "digimon_emoji": "🌾",
        "digimon_reason": "소박하고 순한 타네몬처럼, 부드러운 계란찜이 잘 어울려요.",
    },
    {
        "food_emoji": "🍛", "food_name": "규동",
        "food_reason": "달콤짭짤한 소스에 볶은 소고기와 양파를 얹은 일본식 덮밥이에요.",
        "digimon_name": "베어몬", "digimon_emoji": "🐻",
        "digimon_reason": "든든하고 푸짐한 베어몬처럼, 배부른 규동이 잘 어울려요.",
    },
    {
        "food_emoji": "🍋", "food_name": "레몬에이드",
        "food_reason": "새콤달콤하고 청량감 가득한 여름 음료예요.",
        "digimon_name": "스카몬", "digimon_emoji": "🐦‍⬛",
        "digimon_reason": "가볍고 산뜻한 스카몬처럼, 상큼한 레몬에이드가 잘 어울려요.",
    },
    {
        "food_emoji": "🍲", "food_name": "삼계탕",
        "food_reason": "인삼과 닭을 푹 고아낸 몸보신 대표 보양식이에요.",
        "digimon_name": "호크몬", "digimon_emoji": "🦅",
        "digimon_reason": "강인한 힘을 지닌 호크몬처럼, 든든한 보양식 삼계탕이 잘 어울려요.",
    },
    {
        "food_emoji": "🍨", "food_name": "젤라또",
        "food_reason": "진하고 부드러운 이탈리안 스타일 아이스크림이에요.",
        "digimon_name": "스노우고아몬", "digimon_emoji": "❄️",
        "digimon_reason": "새하얀 눈을 닮은 스노우고아몬처럼, 부드러운 젤라또가 잘 어울려요.",
    },
    {
        "food_emoji": "🥗", "food_name": "그릭샐러드",
        "food_reason": "신선한 채소와 페타치즈가 어우러진 건강한 메뉴예요.",
        "digimon_name": "라비몬", "digimon_emoji": "🐰",
        "digimon_reason": "가볍고 활기찬 라비몬처럼, 상큼한 그릭샐러드가 잘 어울려요.",
    },
    {
        "food_emoji": "🍢", "food_name": "닭꼬치",
        "food_reason": "달콤짭짤한 소스를 바른 쫄깃한 길거리 인기 간식이에요.",
        "digimon_name": "훗바몬", "digimon_emoji": "🐔",
        "digimon_reason": "활기찬 훗바몬처럼, 신나게 즐기는 닭꼬치가 잘 어울려요.",
    },
    {
        "food_emoji": "🍰", "food_name": "치즈케이크",
        "food_reason": "진하고 부드러운 크림치즈의 풍미가 가득한 디저트예요.",
        "digimon_name": "라군몬", "digimon_emoji": "🐸",
        "digimon_reason": "차분하고 부드러운 라군몬처럼, 진한 치즈케이크가 잘 어울려요.",
    },
    {
        "food_emoji": "🍜", "food_name": "쌀국수",
        "food_reason": "맑고 깊은 육수에 부드러운 쌀면을 즐기는 베트남 대표 메뉴예요.",
        "digimon_name": "리코몬", "digimon_emoji": "🐈",
        "digimon_reason": "우아하고 날렵한 리코몬처럼, 깔끔한 쌀국수가 잘 어울려요.",
    },
    {
        "food_emoji": "🍔", "food_name": "치즈버거",
        "food_reason": "고소한 치즈가 듬뿍 녹아든 든든한 버거 메뉴예요.",
        "digimon_name": "그라니몬", "digimon_emoji": "🗿",
        "digimon_reason": "단단하고 묵직한 그라니몬처럼, 두툼한 치즈버거가 잘 어울려요.",
    },
    {
        "food_emoji": "🍧", "food_name": "망고빙수",
        "food_reason": "달콤한 망고와 시원한 얼음이 어우러진 인기 여름 디저트예요.",
        "digimon_name": "팜몬", "digimon_emoji": "🌺",
        "digimon_reason": "화사하고 열대적인 팜몬처럼, 달콤한 망고빙수가 잘 어울려요.",
    },
    {
        "food_emoji": "🍝", "food_name": "봉골레파스타",
        "food_reason": "조개 육수의 감칠맛이 면에 깊게 배어든 해산물 파스타예요.",
        "digimon_name": "웨어가루몬", "digimon_emoji": "🌊",
        "digimon_reason": "역동적이고 강렬한 웨어가루몬처럼, 시원한 조개 향의 파스타가 잘 어울려요.",
    },
    {
        "food_emoji": "🥮", "food_name": "월병",
        "food_reason": "달콤한 소가 가득 들어간 쫀득한 전통 디저트예요.",
        "digimon_name": "문몬", "digimon_emoji": "🌙",
        "digimon_reason": "달빛을 닮은 문몬처럼, 둥근 월병이 잘 어울려요.",
    },
    {
        "food_emoji": "🌭", "food_name": "핫도그",
        "food_reason": "바삭한 튀김옷 속 쫄깃한 소시지가 매력적인 길거리 간식이에요.",
        "digimon_name": "스팅몬", "digimon_emoji": "🐝",
        "digimon_reason": "톡 쏘는 매력의 스팅몬처럼, 케찹과 머스타드가 톡 쏘는 핫도그가 잘 어울려요.",
    },
    {
        "food_emoji": "🍲", "food_name": "짬뽕",
        "food_reason": "얼큰하고 진한 국물에 해산물이 가득한 인기 중화요리예요.",
        "digimon_name": "레드베라몬", "digimon_emoji": "🔥",
        "digimon_reason": "뜨거운 불꽃의 레드베라몬처럼, 얼큰한 짬뽕이 잘 어울려요.",
    },
]

# -----------------------------------------------------------
# 4. 세션 상태(session_state) 준비
#    - 스트림릿은 버튼을 누를 때마다 코드를 처음부터 다시 실행하기 때문에,
#      "이전에 골랐던 결과"나 "최근에 나온 디지몬 목록"을 기억하려면
#      st.session_state에 저장해두어야 합니다.
# -----------------------------------------------------------
if "selected_menu" not in st.session_state:
    # 아직 추천을 누르기 전 -> 선택된 메뉴 없음
    st.session_state.selected_menu = None

if "recent_digimons" not in st.session_state:
    # 최근에 나온 디지몬 이름들을 기록해서, 너무 자주 같은 디지몬이
    # 반복해서 나오지 않도록 합니다. (최근 3개까지 기억)
    st.session_state.recent_digimons = []


def pick_random_menu():
    """
    음식 + 디지몬 조합을 하나 랜덤으로 골라주는 함수.
    최근에 나온 디지몬 3마리는 이번 추천에서 제외합니다.
    """
    history_limit = min(3, len(MENU_DATA) - 1)

    # 최근에 나온 디지몬이 아닌 후보들만 골라냅니다.
    candidates = [
        item for item in MENU_DATA
        if item["digimon_name"] not in st.session_state.recent_digimons
    ]

    # 혹시 후보가 하나도 안 남으면(데이터가 적을 때) 전체에서 다시 고릅니다.
    if not candidates:
        candidates = MENU_DATA

    chosen = random.choice(candidates)

    # 이번에 나온 디지몬을 "최근 목록"에 추가하고, 3개보다 많아지면 오래된 것부터 지웁니다.
    st.session_state.recent_digimons.append(chosen["digimon_name"])
    if len(st.session_state.recent_digimons) > history_limit:
        st.session_state.recent_digimons.pop(0)

    return chosen


# -----------------------------------------------------------
# 5. 화면 맨 위 - 제목, 설명, 대표 이미지
# -----------------------------------------------------------
st.title("🍽️🦖 디지몬의 메뉴 추천")

st.markdown(
    '<p class="desc-text">오늘 뭐 먹을지 고민된다면? 디지몬이 딱 맞는 메뉴를 골라드려요!</p>',
    unsafe_allow_html=True,
)

# 버튼 위에 보여줄 대표 이미지 (사진 대신 큰 이모지를 사용해서
# 인터넷 이미지 파일 없이도 항상 잘 보이도록 했습니다.)
st.markdown(
    '<div style="text-align:center; font-size:70px;">🍽️✨🦖</div>',
    unsafe_allow_html=True,
)

st.write("")  # 여백을 위한 빈 줄

# -----------------------------------------------------------
# 6. 메뉴 추천 버튼
#    - use_container_width=True로 버튼을 넓게 보이게 합니다.
# -----------------------------------------------------------
button_label = "🍽️ 메뉴 추천" if st.session_state.selected_menu is None else "🔄 다시 추천"

if st.button(button_label, use_container_width=True, type="primary"):
    st.session_state.selected_menu = pick_random_menu()

# -----------------------------------------------------------
# 7. 추천 결과 보여주기
#    - 아직 버튼을 누르지 않았다면 결과 영역은 보이지 않습니다.
# -----------------------------------------------------------
menu = st.session_state.selected_menu

if menu is not None:
    st.write("---")

    # (1) 오늘의 음식 - 이모지를 큰 "사진"처럼 보여줍니다.
    st.markdown("#### 🍴 오늘의 음식")
    st.markdown(
        f'<div class="food-photo">{menu["food_emoji"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="food-name">{menu["food_name"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="reason-box">{menu["food_reason"]}</div>',
        unsafe_allow_html=True,
    )

    # (2) 어울리는 디지몬 소개
    st.markdown("#### 🦖 어울리는 디지몬")
    st.markdown(
        f"""
        <div class="digimon-box">
            <div class="digimon-emoji">{menu["digimon_emoji"]}</div>
            <div class="digimon-name">{menu["digimon_name"]}</div>
            <div class="digimon-reason">{menu["digimon_reason"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # 버튼을 아직 누르지 않았을 때 보여줄 안내 문구
    st.info("위의 '메뉴 추천' 버튼을 눌러서 오늘의 메뉴와 디지몬을 확인해보세요!")
