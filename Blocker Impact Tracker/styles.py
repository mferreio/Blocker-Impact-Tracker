"""
B.I.T. - Blocker Impact Tracker
Styles module - Clean modern UI theme with dark mode support
"""


def get_custom_css(dark_mode=False):
    """Returns the custom CSS for the application - clean, readable theme."""
    
    if dark_mode:
        css_vars = """
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --bg-card: #1e293b;
        --border-color: #475569;
        --border-hover: #64748b;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --accent-blue: #60a5fa;
        --accent-green: #34d399;
        --accent-yellow: #fbbf24;
        --accent-red: #f87171;
        --accent-orange: #fb923c;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -1px rgba(0,0,0,0.2);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -2px rgba(0,0,0,0.2);
        --transition-fast: 0.15s ease;
        --transition-normal: 0.25s ease;
    }
        """
    else:
        css_vars = """
    :root {
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --bg-tertiary: #f1f5f9;
        --bg-card: #ffffff;
        --border-color: #e2e8f0;
        --border-hover: #cbd5e1;
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --accent-yellow: #f59e0b;
        --accent-red: #ef4444;
        --accent-orange: #f97316;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);
        --transition-fast: 0.15s ease;
        --transition-normal: 0.25s ease;
    }
        """
    
    base_css = """
    /* Hide Streamlit default branding */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    .block-container { padding-top: 1.5rem !important; max-width: 1200px !important; }
    
    /* Base app styles - MINIMAL overrides to avoid visibility issues */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* ===== HEADERS ===== */
    .stApp h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        letter-spacing: -0.02em;
    }
    .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { 
        color: var(--text-primary) !important;
        font-size: 1rem !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: var(--bg-tertiary);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-primary) !important;
        font-weight: 600;
        font-size: 0.9rem !important;
        padding: 10px 20px;
        transition: all var(--transition-fast);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-secondary);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }
    /* Fix tab underline indicator */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* ===== FORM LABELS - ensure always visible ===== */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label, .stTimeInput label, 
    .stSlider label, .stMultiSelect label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 4px !important;
    }
    
    /* ===== FORM INPUTS ===== */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: var(--bg-secondary) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        padding: 10px 12px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 1 !important;
    }
    
    /* ===== SELECT BOXES - ensure text is visible ===== */
    [data-baseweb="select"] {
        background: var(--bg-secondary) !important;
    }
    [data-baseweb="select"] > div {
        background: var(--bg-secondary) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] span, [data-baseweb="select"] div {
        color: var(--text-primary) !important;
    }
    [data-baseweb="popover"], [data-baseweb="menu"] { 
        background: var(--bg-secondary) !important; 
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    [data-baseweb="menu"] li { 
        color: var(--text-primary) !important; 
    }
    [data-baseweb="menu"] li:hover { 
        background: var(--bg-tertiary) !important; 
    }
    
    /* ===== DATE & TIME INPUTS ===== */
    .stDateInput input, .stTimeInput input {
        background: var(--bg-secondary) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 10px 12px !important;
    }
    
    /* ===== BUTTONS - larger and more prominent ===== */
    .stButton > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        min-height: 44px !important;
        transition: all var(--transition-normal) !important;
        box-shadow: var(--shadow-sm) !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: #2563eb !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    .stButton > button:disabled {
        background: var(--border-color) !important;
        color: var(--text-muted) !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: var(--accent-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        min-height: 44px !important;
        transition: all var(--transition-normal) !important;
    }
    .stDownloadButton > button:hover {
        background: #059669 !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Form submit button */
    .stForm [data-testid="stFormSubmitButton"] > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        min-height: 48px !important;
        letter-spacing: 0.02em !important;
    }
    
    /* ===== METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all var(--transition-normal) !important;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-md) !important;
        border-color: var(--accent-blue) !important;
    }
    [data-testid="stMetricLabel"] { 
        color: var(--text-secondary) !important; 
        font-weight: 700 !important; 
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="stMetricValue"] { 
        color: var(--text-primary) !important; 
        font-size: 1.8rem !important; 
        font-weight: 700 !important; 
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }
    
    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: 8px !important;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ===== DATA TABLE ===== */
    .stDataFrame { 
        border-radius: 10px !important; 
        border: 1px solid var(--border-color) !important; 
        box-shadow: var(--shadow-sm) !important;
        overflow: hidden !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr { 
        border-color: var(--border-color) !important; 
        opacity: 0.5; 
        margin: 1.5rem 0 !important;
    }
    
    /* ===== NUMBER INPUT BUTTONS ===== */
    .stNumberInput button { 
        background: var(--bg-tertiary) !important; 
        border: 1px solid var(--border-color) !important; 
        color: var(--text-primary) !important;
        min-width: 36px !important;
        min-height: 36px !important;
    }
    .stNumberInput button:hover { 
        background: var(--border-color) !important; 
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderHeader:hover {
        background: var(--bg-tertiary) !important;
        border-color: var(--accent-blue) !important;
    }
    
    /* ===== CAPTION / SMALL TEXT ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    
    /* ===== SLIDER ===== */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent-blue) !important;
    }
    
    /* ===== MARKDOWN ===== */
    .stMarkdown p {
        color: var(--text-secondary) !important;
        line-height: 1.6 !important;
    }
    .stMarkdown strong {
        color: var(--text-primary) !important;
    }
    
    /* ===== PAGINATION INFO CENTER ===== */
    .stMarkdown div[style*="text-align: center"] {
        color: var(--text-secondary) !important;
    }
    """
    
    return "<style>\\n    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');\\n" + css_vars + base_css + "\\n</style>"
