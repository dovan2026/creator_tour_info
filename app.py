"""
놀러 가자! 콘텐츠! - 크리에이터를 위한 여행 장소 매칭 플랫폼
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="놀러 가자! 콘텐츠!",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

* { font-family: 'Noto Sans KR', sans-serif !important; }

/* ── 전체 배경 ── */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0f0c29 40%, #1a0a2e 100%);
    min-height: 100vh;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1f 0%, #120d22 100%) !important;
    border-right: 1px solid rgba(167,139,250,0.15);
}
section[data-testid="stSidebar"] * { color: #e0e0ff !important; }

/* 사이드바 라벨 */
section[data-testid="stSidebar"] label {
    color: #a78bfa !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase;
}

/* 사이드바 select 박스 */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(167,139,250,0.08) !important;
    border: 1px solid rgba(167,139,250,0.25) !important;
    border-radius: 12px !important;
    color: #e0e0ff !important;
}

/* ── 히어로 배너 ── */
.hero-banner {
    background: linear-gradient(135deg, #4f1cba 0%, #9333ea 40%, #db2777 80%, #f97316 100%);
    border-radius: 24px;
    padding: 44px 52px;
    margin-bottom: 32px;
    box-shadow: 0 24px 80px rgba(147,51,234,0.35);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top:-40%; right:-10%;
    width: 450px; height: 450px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom:-50%; right:15%;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-title {
    font-size: 3.4em;
    font-weight: 900;
    color: #fff;
    margin: 0 0 6px 0;
    letter-spacing: -1.5px;
    text-shadow: 0 4px 30px rgba(0,0,0,0.3);
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1.15em;
    color: rgba(255,255,255,0.80);
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.3px;
}
.hero-icon {
    font-size: 3.5em;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0) rotate(-3deg); }
    50%      { transform: translateY(-10px) rotate(3deg); }
}

/* ── 상태 표시 배지 ── */
.state-banner {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(167,139,250,0.08);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 24px;
}
.state-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 50px;
    padding: 6px 16px;
    font-size: 0.9em;
    font-weight: 700;
    color: #c4b5fd;
}
.state-chip.emotion {
    background: rgba(244,114,182,0.12);
    border-color: rgba(244,114,182,0.3);
    color: #f9a8d4;
}
.state-arrow {
    font-size: 1.3em;
    color: rgba(255,255,255,0.3);
}
.state-count {
    margin-left: auto;
    font-size: 1.6em;
    font-weight: 900;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.state-count-label {
    font-size: 0.72em;
    color: rgba(255,255,255,0.35);
    display: block;
    text-align: right;
}

/* ── 섹션 타이틀 ── */
.section-title {
    font-size: 1.15em;
    font-weight: 800;
    color: #e0e0ff;
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(167,139,250,0.15);
    margin-left: 8px;
}

/* ── 장소 카드 라인업 ── */
.lineup-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
}
.lineup-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 18px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}
.lineup-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    right: 0; height: 3px;
    background: linear-gradient(90deg, #a78bfa, #f472b6);
    opacity: 0;
    transition: opacity 0.25s;
}
.lineup-card:hover {
    background: rgba(167,139,250,0.1);
    border-color: rgba(167,139,250,0.35);
    transform: translateY(-5px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.35);
}
.lineup-card:hover::before { opacity: 1; }
.lineup-num {
    font-size: 0.72em;
    color: rgba(167,139,250,0.5);
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.lineup-title {
    font-size: 1em;
    font-weight: 700;
    color: #f0f0ff;
    line-height: 1.4;
    margin-bottom: 10px;
}
.lineup-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 10px;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 0.72em;
    font-weight: 600;
}
.badge-cat  { background: rgba(99,102,241,0.2); color: #a5b4fc; }
.badge-emo  { background: rgba(236,72,153,0.18); color: #f9a8d4; }
.lineup-outl {
    font-size: 0.78em;
    color: rgba(255,255,255,0.42);
    line-height: 1.6;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}
.lineup-addr {
    font-size: 0.72em;
    color: rgba(255,255,255,0.25);
    margin-top: 8px;
}

/* ── 빈 결과 ── */
.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: rgba(255,255,255,0.25);
}
.empty-icon { font-size: 4em; margin-bottom: 16px; }
.empty-msg  { font-size: 1.05em; }

/* ── 차트 컨테이너 ── */
.chart-wrap {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
}

/* ── 사이드바 구분선 ── */
.sb-divider {
    border: none;
    border-top: 1px solid rgba(167,139,250,0.12);
    margin: 20px 0;
}

/* ── 사이드바 통계 박스 ── */
.sb-stat-box {
    background: rgba(167,139,250,0.07);
    border: 1px solid rgba(167,139,250,0.15);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 4px;
}
.sb-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
}
.sb-stat-label { font-size: 0.78em; color: rgba(255,255,255,0.4); }
.sb-stat-val   { font-size: 0.82em; font-weight: 700; color: #c4b5fd; }

/* ── 페이지네이션 ── */
.pager-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin: 24px 0 8px;
}

/* ── 푸터 ── */
.footer {
    text-align: center;
    padding: 28px 0 12px;
    color: rgba(255,255,255,0.18);
    font-size: 0.75em;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 40px;
    letter-spacing: 0.3px;
}

/* ── 사이드바 접기/펼치기 버튼 완전 숨김 (모든 Streamlit 버전 대응) ── */
[data-testid="collapsedControl"]           { display: none !important; }
[data-testid="stSidebarCollapseButton"]    { display: none !important; }
button[data-testid="baseButton-header"]    { display: none !important; }
button[data-testid="baseButton-headerNoPadding"] { display: none !important; }
section[data-testid="stSidebar"] > div > button  { display: none !important; }
/* 아이콘 텍스트(keyboard_double_arrow_left)가 폰트 미로드로 노출되는 경우 */
section[data-testid="stSidebar"] button span { display: none !important; }
/* Streamlit Cloud 최신 빌드 대응 */
div[data-testid="stSidebarHeader"] { display: none !important; }

/* ── number input: 입력 텍스트 검정 ── */
div[data-testid="stNumberInput"] input {
    background: rgba(167,139,250,0.08) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    color: #111 !important;
    border-radius: 10px !important;
    text-align: center;
    font-weight: 700;
}

/* ── 사이드바 텍스트 input: 입력 텍스트 검정 ── */
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(167,139,250,0.08) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    color: #111 !important;
    border-radius: 10px !important;
}

/* ── Expander: 아이콘 텍스트 완전 은닉 ──
   Streamlit expander 구조: <summary> 안 첫 번째 <span>이 아이콘(arrow_right/arrow_drop_down)
   두 번째 <span>이 제목 텍스트.
   data-testid="stExpanderToggleIcon" 또는 first-child 타겟팅 */
span[data-testid="stExpanderToggleIcon"] {
    font-size: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    color: transparent !important;
    display: inline-block !important;
}
/* 모든 details summary 첫 번째 span (아이콘) 숨김 */
details summary > span:first-child {
    font-size: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    color: transparent !important;
}
/* Material Icons / Symbols 클래스 직접 숨김 */
.material-icons,
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons-round {
    font-size: 0 !important;
    color: transparent !important;
    visibility: hidden !important;
    width: 0 !important;
}

/* ── Expander: 배경색 (전체 배경보다 밝게) ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(167,139,250,0.18) !important;
    border-radius: 14px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    background: rgba(167,139,250,0.10) !important;
    border-radius: 14px !important;
    padding: 12px 18px !important;
    color: #c4b5fd !important;
    font-weight: 700 !important;
}
[data-testid="stExpander"] > div {
    background: rgba(255,255,255,0.04) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 데이터 로드 (캐시)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "visitkorea_tour_data_v2.csv")
    df = pd.read_csv(path, encoding="utf-8-sig", dtype=str)
    df["번호"] = pd.to_numeric(df["번호"], errors="coerce")
    return df.fillna("")

df = load_data()

# ─────────────────────────────────────────────
# 이모지 매핑
# ─────────────────────────────────────────────
EMOTION_EMOJI = {
    "맛·풍요":        "🍽️",
    "쇼핑·활기":      "🛍️",
    "힐링·평화":      "🌿",
    "낭만·설렘":      "💫",
    "즐거움·흥겨움":  "🎉",
    "경건함":         "🙏",
    "향수·그리움":    "🏡",
    "배움·호기심":    "📚",
    "역사·경이":      "🏛️",
    "활력·도전":      "⚡",
    "추모·숙연":      "🕯️",
    "경이·신비":      "✨",
    "설렘·낭만":      "💖",
}
CAT_EMOJI = {
    "관광지":         "🗺️",
    "문화시설":       "🎨",
    "행사/공연/축제": "🎪",
    "여행코스":       "🛤️",
    "레포츠":         "🏄",
    "숙박":           "🏨",
    "쇼핑":           "🛒",
    "음식점":         "🍜",
}
REGION_EMOJI = {
    "서울": "🏙️", "부산": "🌊", "대구": "🏔️", "인천": "✈️",
    "광주": "🌸", "대전": "🔬", "울산": "⚙️", "세종": "🏛️",
    "경기": "🌄", "강원": "🎿", "충북": "🌲", "충남": "🌾",
    "경북": "🍎", "경남": "⛵", "전북": "🎭", "전남": "🌺",
    "제주": "🌴", "기타": "📍",
}

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR", color="#b0b0d0", size=11),
    margin=dict(l=8, r=8, t=32, b=8),
)

# ─────────────────────────────────────────────
# ── 사이드바 ──
# ─────────────────────────────────────────────
with st.sidebar:
    # 브랜드
    st.markdown("""
    <div style='text-align:center; padding:24px 0 16px;'>
        <div style='font-size:2.8em; animation:float 3s ease-in-out infinite;'>🎬</div>
        <div style='font-size:1.2em; font-weight:900; color:#a78bfa;
                    letter-spacing:-0.5px; margin-top:6px;'>놀러 가자!</div>
        <div style='font-size:0.72em; color:rgba(255,255,255,0.3);
                    margin-top:4px; letter-spacing:0.5px;'>크리에이터 장소 매칭</div>
    </div>
    <hr class='sb-divider'>
    """, unsafe_allow_html=True)

    # ── 장소 선택 ──
    st.markdown("### 📍 원하는 장소")
    region_options = ["전체"] + sorted(df["지역명"].unique().tolist())
    sel_region = st.selectbox(
        "지역을 선택하세요",
        region_options,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── 감정 선택 ──
    st.markdown("### 💭 원하는 감정")
    emotion_options = ["전체"] + sorted(df["감정"].unique().tolist())
    sel_emo = st.selectbox(
        "감정을 선택하세요",
        emotion_options,
        label_visibility="collapsed",
    )

    st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

    # ── 추가 옵션 ──
    st.markdown("### 🔍 키워드 검색")
    search_kw = st.text_input("", placeholder="장소명·키워드 입력", label_visibility="collapsed")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    per_page = st.select_slider("페이지당 표시", options=[9, 12, 18, 24, 30], value=12)

    # ── 필터 적용 ──
    filtered = df.copy()
    if sel_region != "전체":
        filtered = filtered[filtered["지역명"] == sel_region]
    if sel_emo != "전체":
        filtered = filtered[filtered["감정"] == sel_emo]
    if search_kw:
        mask = (
            filtered["제목"].str.contains(search_kw, na=False) |
            filtered["개요"].str.contains(search_kw, na=False)
        )
        filtered = filtered[mask]

    st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

    # ── 사이드바 통계 ──
    st.markdown(f"""
    <div class='sb-stat-box'>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>🔍 매칭된 장소</span>
            <span class='sb-stat-val'>{len(filtered):,}곳</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>📍 지역 수</span>
            <span class='sb-stat-val'>{filtered['지역명'].nunique()}개</span>
        </div>
        <div class='sb-stat-row'>
            <span class='sb-stat-label'>🏷️ 카테고리</span>
            <span class='sb-stat-val'>{filtered['카테고리명'].nunique()}종</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:20px; font-size:0.68em; color:rgba(255,255,255,0.18);
                text-align:center; line-height:2;'>
        데이터 출처: 한국관광공사 콘텐츠랩<br>
        총 50,700건 · 18개 지역 · 13가지 감정
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── 메인 컨텐츠 ──
# ─────────────────────────────────────────────

# ── 히어로 배너 ──
st.markdown("""
<div class="hero-banner">
    <div style="display:flex; align-items:center; gap:20px; position:relative; z-index:1;">
        <span class="hero-icon">🎬</span>
        <div>
            <p class="hero-title">놀러 가자! 콘텐츠!</p>
            <p class="hero-subtitle">크리에이터를 위한 여행 장소 매칭 플랫폼</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 현재 선택 상태 배너 ──
r_icon = REGION_EMOJI.get(sel_region, "📍") if sel_region != "전체" else "🗺️"
e_icon = EMOTION_EMOJI.get(sel_emo, "💭") if sel_emo != "전체" else "💭"
r_label = sel_region if sel_region != "전체" else "전국"
e_label = sel_emo if sel_emo != "전체" else "모든 감정"

# 키워드 칩: 검색어 입력 시에만 표시
keyword_chip = (
    f'<div class="state-chip" style="background:rgba(99,102,241,0.15);'
    f'border-color:rgba(99,102,241,0.3);color:#a5b4fc;">🔍 &quot;{search_kw}&quot;</div>'
    if search_kw else ""
)

# 배너는 항상 표시 (지역 chip + 감정 chip + 키워드 chip만, count 박스 제거)
st.markdown(f"""
<div class="state-banner">
    <div class="state-chip">{r_icon} {r_label}</div>
    <div class="state-arrow">+</div>
    <div class="state-chip emotion">{e_icon} {e_label}</div>
    {keyword_chip}
</div>
""", unsafe_allow_html=True)

# ── 차트 (지역+감정 선택 안 했을 때만 보여줌, 선택 시 결과 집중) ──
if sel_region == "전체" and sel_emo == "전체" and not search_kw:
    c1, c2, c3 = st.columns([2, 1.5, 1.5])

    with c1:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📍 지역별 장소 수</div>', unsafe_allow_html=True)
        rd = (df["지역명"].value_counts().reset_index()
              .rename(columns={"count": "건수"})
              .sort_values("건수"))
        fig = px.bar(rd, x="건수", y="지역명", orientation="h",
                     color="건수",
                     color_continuous_scale=["#4f46e5","#a78bfa","#f472b6","#fb923c"])
        fig.update_layout(**CHART_BASE, coloraxis_showscale=False, height=300,
                          xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
                          yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💭 감정 분포</div>', unsafe_allow_html=True)
        ed = df["감정"].value_counts().reset_index().rename(columns={"count": "건수"})
        ed["label"] = ed["감정"].map(lambda x: f"{EMOTION_EMOJI.get(x,'')} {x}")
        fig2 = px.pie(ed, values="건수", names="label", hole=0.55,
                      color_discrete_sequence=px.colors.sequential.Plasma_r)
        fig2.update_layout(**CHART_BASE, height=300, showlegend=False)
        fig2.update_traces(textposition="inside", textinfo="percent", textfont_size=9)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏷️ 카테고리 분포</div>', unsafe_allow_html=True)
        cd = df["카테고리명"].value_counts().reset_index().rename(columns={"count": "건수"})
        cd["label"] = cd["카테고리명"].map(lambda x: f"{CAT_EMOJI.get(x,'')} {x}")
        fig3 = go.Figure(go.Bar(
            x=cd["건수"], y=cd["label"], orientation="h",
            marker=dict(color=cd["건수"],
                        colorscale=[[0,"#db2777"],[1,"#f97316"]],
                        line=dict(width=0)),
        ))
        fig3.update_layout(**CHART_BASE, height=300,
                           xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
                           yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10),
                                      autorange="reversed"))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:32px 20px 8px;
                color:rgba(255,255,255,0.25); font-size:0.9em;'>
        ← 왼쪽에서 <b style='color:#a78bfa;'>원하는 장소</b>와
        <b style='color:#f472b6;'>감정</b>을 선택하면 맞춤 장소가 라인업 됩니다 ✨
    </div>
    """, unsafe_allow_html=True)

else:
    # ── 장소 라인업 ──
    st.markdown(
        f'<div class="section-title">🎯 매칭된 장소 라인업 &nbsp;<span style="font-size:0.8em; '
        f'font-weight:400; color:rgba(255,255,255,0.35);">총 {len(filtered):,}곳</span></div>',
        unsafe_allow_html=True,
    )

    if len(filtered) == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">😅</div>
            <div class="empty-msg">선택한 조건에 맞는 장소가 없습니다.<br>
            다른 지역이나 감정을 선택해 보세요!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 페이지네이션
        total_pages = max(1, (len(filtered) - 1) // per_page + 1)
        pg_col1, pg_col2, pg_col3 = st.columns([1, 0.4, 1])
        with pg_col2:
            page = st.number_input(
                "page", min_value=1, max_value=total_pages, value=1,
                label_visibility="collapsed"
            )
        with pg_col3:
            st.markdown(
                f"<div style='color:rgba(255,255,255,0.3); font-size:0.82em; "
                f"padding-top:10px;'>{page} / {total_pages} 페이지</div>",
                unsafe_allow_html=True,
            )

        start = (page - 1) * per_page
        page_df = filtered.iloc[start: start + per_page]

        # ── 3열 카드 그리드 ──
        cols = st.columns(3)
        for idx, (_, row) in enumerate(page_df.iterrows()):
            col = cols[idx % 3]
            with col:
                cat_icon = CAT_EMOJI.get(row["카테고리명"], "🏷️")
                emo_icon = EMOTION_EMOJI.get(row["감정"], "💭")
                outl = row["개요"][:180] + "…" if len(row["개요"]) > 180 else row["개요"]
                addr = row["주소"][:45] if row["주소"] else ""
                num_label = f"#{start + idx + 1:04d}"

                st.markdown(f"""
                <div class="lineup-card">
                    <div class="lineup-num">{num_label}</div>
                    <div class="lineup-title">{row['제목']}</div>
                    <div class="lineup-badges">
                        <span class="badge badge-cat">{cat_icon} {row['카테고리명']}</span>
                        <span class="badge badge-emo">{emo_icon} {row['감정']}</span>
                    </div>
                    <div class="lineup-outl">{outl if outl.strip() else '개요 정보 없음'}</div>
                    {'<div class="lineup-addr">📌 ' + addr + '</div>' if addr else ''}
                </div>
                """, unsafe_allow_html=True)

        # ── 테이블 뷰 ──
        with st.expander("📊 표 형식으로 전체 보기", expanded=False):
            show_cols = ["번호", "제목", "카테고리명", "지역명", "감정", "주소"]
            disp = filtered[show_cols].copy().reset_index(drop=True)
            st.dataframe(
                disp,
                use_container_width=True,
                hide_index=True,
                height=360,
                column_config={
                    "번호":     st.column_config.NumberColumn(width="small"),
                    "제목":     st.column_config.TextColumn(width="medium"),
                    "카테고리명": st.column_config.TextColumn(width="small"),
                    "지역명":   st.column_config.TextColumn(width="small"),
                    "감정":     st.column_config.TextColumn(width="small"),
                    "주소":     st.column_config.TextColumn(width="large"),
                },
            )
            if len(filtered) > 1000:
                st.caption(f"※ 상위 {min(len(filtered),1000):,}건 표시 중 (전체 {len(filtered):,}건)")

# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🎬 놀러 가자! 콘텐츠! &nbsp;|&nbsp;
    크리에이터를 위한 여행 장소 매칭 플랫폼 &nbsp;|&nbsp;
    데이터 출처: 한국관광공사 콘텐츠랩 (api.visitkorea.or.kr) &nbsp;|&nbsp; 총 50,700건
</div>
""", unsafe_allow_html=True)
