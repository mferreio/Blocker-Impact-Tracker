"""
B.I.T. - Blocker Impact Tracker
Styles module - Clean modern UI theme with dark mode support
Fixed: BRUTE FORCE visibility update to ensure elements are seen
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
        --input-text: #f1f5f9;
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
        --input-text: #1e293b;
    }
        """
    
    base_css = """
    /* ===== RESET ===== */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }
    
    /* ===== FORCE VISIBILITY ON EVERYTHING ===== */
    h1, h2, h3, h4, h5, h6, 
    p, span, label, div, li, a {
        color: var(--text-primary);
    }
    
    /* ===== BUTTONS: BRUTE FORCE SELECTORS ===== */
    /* Target EVERY button in Streamlit */
    button, 
    .stButton > button,
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stFormSubmitButton"] button {
        opacity: 1 !important;
        visibility: visible !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        min-height: 44px !important;
    }

    /* Primary Actions (Blue) */
    [data-testid="stBaseButton-primary"],
    [data-testid="stFormSubmitButton"] button,
    button[kind="primary"] {
        background-color: var(--accent-blue) !important;
        border: 1px solid var(--accent-blue) !important;
        color: #ffffff !important;
    }
    /* Ensure text inside primary buttons is white */
    [data-testid="stBaseButton-primary"] *,
    [data-testid="stFormSubmitButton"] button * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Secondary Actions (Outline/White) */
    [data-testid="stBaseButton-secondary"],
    button[kind="secondary"] {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }

    /* Download Button (Green) */
    [data-testid="stDownloadButton"] button {
        background-color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
        color: #ffffff !important;
    }
    [data-testid="stDownloadButton"] button * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Hover Effects */
    button:hover {
        transform: translateY(-1px);
        filter: brightness(1.1);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    /* ===== INPUTS & SELECTS: BRUTE FORCE ===== */
    /* Input Fields */
    input, textarea, [data-baseweb="select"] {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Specific fix for Select Box container */
    [data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Fix weird gray background on some inputs */
    .stTextInput > div > div {
        background-color: var(--input-bg) !important;
    }
    
    /* Input Labels */
    label, .st-emotion-cache-1629p8f {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* ===== TABS ===== */
    /* Tab Container */
    [data-baseweb="tab-list"] {
        background-color: var(--bg-tertiary) !important;
        padding: 4px !important;
        border-radius: 10px !important;
    }
    
    /* Individual Tabs */
    [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: var(--text-primary) !important;
    }
    
    /* Active Tab */
    [aria-selected="true"] {
        background-color: var(--accent-blue) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    /* Force text color in active tab */
    [aria-selected="true"] * {
        color: #ffffff !important;
    }

    /* ===== DATAFRAME & TABLES ===== */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetric"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: var(--shadow-sm) !important;
    }
    [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
    [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    /* ===== UTILS ===== */
    /* Fix disabled states */
    button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }
    
    /* Remove default Streamlit highlights that might conflict */
    .st-emotion-cache-1gulkj5 { display: none !important; }
    """
    
    return "<style>\\n    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');\\n" + css_vars + base_css + "\\n</style>"
