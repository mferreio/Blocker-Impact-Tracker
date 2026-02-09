"""
B.I.T. - Blocker Impact Tracker
Styles module - Clean modern UI theme with dark mode support
Fixed: element visibility, button sizing, tab text, form consistency
"""


def get_custom_css(dark_mode=False):
    """Returns the custom CSS for the application."""
    
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
        --accent-blue-hover: #3b82f6;
        --accent-green: #34d399;
        --accent-green-hover: #10b981;
        --accent-yellow: #fbbf24;
        --accent-red: #f87171;
        --accent-red-hover: #ef4444;
        --accent-orange: #fb923c;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -1px rgba(0,0,0,0.2);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -2px rgba(0,0,0,0.2);
        --input-bg: #334155;
    }
        """
    else:
        css_vars = """
    :root {
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --bg-tertiary: #f1f5f9;
        --bg-card: #ffffff;
        --border-color: #d1d5db;
        --border-hover: #9ca3af;
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-muted: #6b7280;
        --accent-blue: #3b82f6;
        --accent-blue-hover: #2563eb;
        --accent-green: #10b981;
        --accent-green-hover: #059669;
        --accent-yellow: #f59e0b;
        --accent-red: #ef4444;
        --accent-red-hover: #dc2626;
        --accent-orange: #f97316;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);
        --input-bg: #ffffff;
    }
        """
    
    base_css = """
    /* ===== RESET / HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* ===== HEADERS ===== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }
    
    /* ===== TABS - Fix selected tab text visibility ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: var(--bg-tertiary);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 10px 20px !important;
    }
    /* Non-selected tab text */
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] div {
        color: var(--text-primary) !important;
    }
    /* Selected tab - blue background, white text */
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: white !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }
    
    /* ===== FORM LABELS ===== */
    label, .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label, .stTimeInput label,
    .stSlider label, .stMultiSelect label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* ===== ALL FORM INPUTS - Unified white bg with visible borders ===== */
    input[type="text"], input[type="number"], input[type="email"],
    input[type="password"], textarea,
    .stTextInput input, .stNumberInput input,
    .stDateInput input, .stTimeInput input,
    .stTextArea textarea {
        background: var(--input-bg) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        padding: 10px 12px !important;
    }
    input:focus, textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    input::placeholder, textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 1 !important;
    }
    
    /* ===== SELECT BOXES ===== */
    [data-baseweb="select"] > div {
        background: var(--input-bg) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }
    /* Dropdown menu */
    [data-baseweb="popover"] { 
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    [data-baseweb="menu"] li { color: var(--text-primary) !important; }
    [data-baseweb="menu"] li:hover { background: var(--bg-tertiary) !important; }
    
    /* ===== ALL BUTTONS - Always visible with solid backgrounds ===== */
    /* Primary buttons (blue) */
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"],
    .stButton > button[kind="primary"],
    .stButton > button {
        background-color: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        min-height: 42px !important;
        cursor: pointer !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
    .stButton > button:hover {
        background-color: var(--accent-blue-hover) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Secondary buttons (outlined) */
    button[data-testid="stBaseButton-secondary"],
    .stButton > button[kind="secondary"] {
        background-color: var(--bg-secondary) !important;
        color: var(--accent-red) !important;
        border: 2px solid var(--accent-red) !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        min-height: 42px !important;
        cursor: pointer !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover,
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--accent-red) !important;
        color: white !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Disabled buttons */
    button:disabled,
    button[disabled] {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-muted) !important;
        border: 1px solid var(--border-color) !important;
        cursor: not-allowed !important;
        opacity: 0.7 !important;
    }
    
    /* Form submit buttons */
    [data-testid="stFormSubmitButton"] button,
    .stForm button[type="submit"],
    .stFormSubmitButton > button {
        background-color: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        min-height: 48px !important;
        letter-spacing: 0.02em !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background-color: var(--accent-blue-hover) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Download buttons - green, always visible */
    [data-testid="stDownloadButton"] button,
    .stDownloadButton > button,
    button[data-testid="stBaseButton-secondary"][kind="secondary"] {
        background-color: var(--accent-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        min-height: 42px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stDownloadButton"] button:hover,
    .stDownloadButton > button:hover {
        background-color: var(--accent-green-hover) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Ensure all button text and icons are visible */
    button p, button span, button div,
    .stButton p, .stButton span,
    .stDownloadButton p, .stDownloadButton span,
    [data-testid="stFormSubmitButton"] p,
    [data-testid="stFormSubmitButton"] span {
        color: inherit !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* ===== METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        box-shadow: var(--shadow-sm) !important;
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
    
    /* ===== ALERTS ===== */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
    }
    
    /* ===== DATA TABLE ===== */
    [data-testid="stDataFrame"] { 
        border-radius: 10px !important; 
        border: 1px solid var(--border-color) !important; 
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr { 
        border-color: var(--border-color) !important; 
        opacity: 0.5; 
    }
    
    /* ===== NUMBER INPUT BUTTONS ===== */
    [data-testid="stNumberInput"] button {
        background: var(--bg-tertiary) !important; 
        border: 1px solid var(--border-color) !important; 
        color: var(--text-primary) !important;
        min-width: 32px !important;
        min-height: 32px !important;
    }
    [data-testid="stNumberInput"] button:hover { 
        background: var(--border-hover) !important; 
    }
    
    /* ===== EXPANDER ===== */
    details summary {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    details summary:hover {
        background: var(--bg-tertiary) !important;
        border-color: var(--accent-blue) !important;
    }
    details summary span {
        color: var(--text-primary) !important;
    }
    
    /* ===== CAPTION ===== */
    [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
    }
    [data-testid="stCaptionContainer"] p {
        color: var(--text-muted) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    
    /* ===== GENERAL TEXT ===== */
    p { color: var(--text-secondary) !important; }
    strong { color: var(--text-primary) !important; }
    
    /* ===== MARKDOWN LINK ===== */
    a { color: var(--accent-blue) !important; }
    """
    
    return "<style>\\n    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');\\n" + css_vars + base_css + "\\n</style>"
