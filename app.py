import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Professional AI Agent Workspace",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom SaaS CSS Style System ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@300;400;500&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Core Theme ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #E2E8F0;
}

.stApp {
    background-color: #080B11;
    background-image:
        radial-gradient(circle 800px at 0% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 80%),
        radial-gradient(circle 600px at 100% 100%, rgba(245, 158, 11, 0.08) 0%, transparent 70%);
}

/* ── Hide default Streamlit overheads ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1300px; }

/* ── SaaS Header & Branding ── */
.brand-container {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.brand-eyebrow {
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6366F1;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 12px rgba(99,102,241,0.3);
}
.brand-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin: 0;
}
.brand-title span {
    background: linear-gradient(135deg, #6366F1 0%, #F59E0B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.brand-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #94A3B8;
    max-width: 700px;
    margin: 0.8rem auto 0;
    line-height: 1.6;
    text-align: center;
}

/* ── Glassmorphic Panels ── */
.saas-card {
    background: transparent;
    border: none;
    border-radius: 0px;
    padding: 0px;
    margin-bottom: 1.5rem;
    box-shadow: none;
}

/* ── Streamlit Input Customization ── */
.stTextInput > div > div > input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.0rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}
.stTextInput > label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
}

/* ── Dynamic Action Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.0rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4) !important;
    background: linear-gradient(135deg, #6366F1 0%, #F59E0B 100%) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline Steps Styling ── */
.step-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.0rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(99, 102, 241, 0.08);
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.1);
}
.step-card.done {
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.05);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: rgba(255,255,255,0.06);
    transition: background 0.3s;
}
.step-card.active::before { background: #6366F1; }
.step-card.done::before   { background: #10B981; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.step-num {
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    color: #6366F1;
}
.step-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #F1F5F9;
}
.step-desc {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 0.4rem;
}
.step-status {
    margin-left: auto;
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
}
.status-waiting  { color: #475569; }
.status-running  { color: #F59E0B; text-shadow: 0 0 10px rgba(245,158,11,0.2); }
.status-done     { color: #10B981; }

/* ── Result Briefings ── */
.result-section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F8FAFC;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.report-workspace {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 16px;
    padding: 2.5rem;
    margin-top: 1rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    line-height: 1.75;
}
.critic-workspace {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 15px 30px rgba(0,0,0,0.25);
}

/* ── Chips ── */
.try-chip {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: #94A3B8;
    cursor: pointer;
    transition: all 0.2s ease;
}
.try-chip:hover {
    border-color: #6366F1;
    color: #FFFFFF;
    background: rgba(99, 102, 241, 0.1);
}

/* ── Footer ── */
.saas-footer {
    text-align: center;
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    color: #475569;
    margin-top: 4.5rem;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)


# ── Render Step Card Helper ─────────────────────────────────────────────────────
def render_step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● ACTIVE", "status-running"),
        "done":    ("✓ COMPLETE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "waiting")
    
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session State Initializer ───────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False
if "step" not in st.session_state:
    st.session_state.step = None
if "topic" not in st.session_state:
    st.session_state.topic = ""


# ── Hero Branding Header ────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-container">
    <div class="brand-eyebrow">Advanced multi-agent intelligence briefing system</div>
    <div class="brand-title">Research<span>Mind</span></div>
    <p class="brand-sub">
        Four specialized AI agents collaborate — searching, scraping, writing, and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
""", unsafe_allow_html=True)


# ── SaaS Workspace Layout ───────────────────────────────────────────────────────
col_workspace, col_spacer, col_pipeline = st.columns([7, 0.4, 5])

with col_workspace:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Intelligence Briefing Subject",
        placeholder="e.g. Next-generation room temperature superconductors in 2026",
        key="topic_input",
        label_visibility="visible",
    )
    
    # Example prompts
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap; margin-top:0.8rem; margin-bottom:1.5rem;">
        <span style="font-family:'Fira Code',monospace; font-size:0.7rem; color:#475569; letter-spacing:0.05em;">SUGGESTIONS:</span>
    """, unsafe_allow_html=True)
    examples = ["Web3 Agentic Workflows", "Quantum Dot Solar Technology", "CRISPR Therapeutics 2026"]
    for ex in examples:
        st.markdown(f'<span class="try-chip" onclick="document.getElementsByTagName(\'input\')[0].value=\'{ex}\';">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    run_btn = st.button("⚡ Start Orchestration Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div style="font-family:\'Plus Jakarta Sans\',sans-serif; font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:1rem;">Orchestration Control</div>', unsafe_allow_html=True)
    
    # Calculate status of each card dynamically
    def get_step_state(step):
        if step in st.session_state.results:
            return "done"
        if st.session_state.running and st.session_state.step == step:
            return "running"
        return "waiting"

    render_step_card("01", "Web Search Agent", get_step_state("search"), "Indexes live search queries and aggregates primary articles.")
    render_step_card("02", "Deep Document Scraper", get_step_state("reader"), "Parses full text bodies, decomposing stylesheets and navigation structures.")
    render_step_card("03", "Principal Research Writer", get_step_state("writer"), "Synthesizes structured information and generates executive briefings.")
    render_step_card("04", "Editorial Peer Critic", get_step_state("critic"), "Evaluates analytical quality, issues score briefings, and offers suggestions.")


# ── Start Pipeline Action ───────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research subject first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.step = "search"
        st.session_state.topic = topic.strip()
        st.rerun()


# ── Sequential Background Runner ───────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.topic

    # STEP 1: Search Agent
    if st.session_state.step == "search":
        with col_workspace:
            with st.spinner("⚡ Search Agent is querying live databases..."):
                try:
                    search_agent = build_search_agent()
                    sr = search_agent.invoke({
                        "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
                    })
                    st.session_state.results["search"] = sr["messages"][-1].content
                    st.session_state.step = "reader"
                    time.sleep(2.5) # Rate limit cooling buffer
                    st.rerun()
                except Exception as e:
                    st.error(f"Search Agent Error: {str(e)}")
                    st.session_state.running = False
                    st.session_state.step = None

    # STEP 2: Scraper Agent
    elif st.session_state.step == "reader":
        with col_workspace:
            with st.spinner("⚡ Scraper Agent is decomposing primary URLs..."):
                try:
                    reader_agent = build_reader_agent()
                    rr = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search results about '{topic_val}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{st.session_state.results['search'][:800]}"
                        )]
                    })
                    st.session_state.results["reader"] = rr["messages"][-1].content
                    st.session_state.step = "writer"
                    time.sleep(2.5) # Rate limit cooling buffer
                    st.rerun()
                except Exception as e:
                    st.error(f"Scraper Agent Error: {str(e)}")
                    st.session_state.running = False
                    st.session_state.step = None

    # STEP 3: Writer Chain
    elif st.session_state.step == "writer":
        with col_workspace:
            with st.spinner("⚡ Principal Writer is drafting the intelligence briefing..."):
                try:
                    research_combined = (
                        f"SEARCH RESULTS:\n{st.session_state.results['search']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{st.session_state.results['reader']}"
                    )
                    st.session_state.results["writer"] = writer_chain.invoke({
                        "topic": topic_val,
                        "research": research_combined
                    })
                    st.session_state.step = "critic"
                    time.sleep(2.5) # Rate limit cooling buffer
                    st.rerun()
                except Exception as e:
                    st.error(f"Writer Chain Error: {str(e)}")
                    st.session_state.running = False
                    st.session_state.step = None

    # STEP 4: Critic Chain
    elif st.session_state.step == "critic":
        with col_workspace:
            with st.spinner("⚡ Editorial Critic is reviewing & finalising..."):
                try:
                    st.session_state.results["critic"] = critic_chain.invoke({
                        "report": st.session_state.results["writer"]
                    })
                    st.session_state.step = None
                    st.session_state.running = False
                    st.session_state.done = True
                    time.sleep(2.5) # Rate limit cooling buffer
                    st.rerun()
                except Exception as e:
                    st.error(f"Critic Chain Error: {str(e)}")
                    st.session_state.running = False
                    st.session_state.step = None


# ── Render Results Output workspace ─────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<hr style="border: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(99,102,241,0.25), transparent); margin: 3rem 0 2rem 0;">', unsafe_allow_html=True)
    
    # ── Workspace Results Grid ──
    col_output_main, col_output_spacer, col_output_critic = st.columns([7, 0.4, 5])
    
    with col_output_main:
        if "writer" in r:
            st.markdown('<div class="result-section-title">📝 Intelligence Briefing</div>', unsafe_allow_html=True)
            st.markdown('<div class="report-workspace">', unsafe_allow_html=True)
            st.markdown(r["writer"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download Button
            st.download_button(
                label="⬇ Download Intelligence Briefing (.md)",
                data=r["writer"],
                file_name=f"intelligence_briefing_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
    with col_output_critic:
        if "critic" in r:
            st.markdown('<div class="result-section-title">🧐 Editorial Assessment</div>', unsafe_allow_html=True)
            st.markdown('<div class="critic-workspace">', unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Raw Data Expanders
        if "search" in r or "reader" in r:
            st.markdown('<div style="margin-top:2.5rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Plus Jakarta Sans\',sans-serif; font-size:1.0rem; font-weight:700; color:#FFFFFF; margin-bottom:0.8rem;">Raw Intelligence Feeds</div>', unsafe_allow_html=True)
            
            if "search" in r:
                with st.expander("🔍 Scanned Web Articles", expanded=False):
                    st.text(r["search"])
            if "reader" in r:
                with st.expander("📄 Extracted Full-Text Body", expanded=False):
                    st.text(r["reader"])


# ── SaaS Workspace Footer ───────────────────────────────────────────────────────
st.markdown("""
<div class="saas-footer">
    Orchestrated Workspace · Built with Streamlit & LangChain · Backed by Mistral AI
</div>
""", unsafe_allow_html=True)