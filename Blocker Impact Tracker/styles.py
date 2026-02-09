"""
B.I.T. - Blocker Impact Tracker
Styles module - Enhanced modern UI theme with improved UX and dark mode
"""


def get_custom_css(dark_mode=False):
    """Returns the custom CSS for the application - enhanced modern theme with dark mode support."""
    
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
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --accent-yellow: #f59e0b;
        --accent-red: #ef4444;
        --accent-orange: #f97316;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -1px rgba(0,0,0,0.2);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -2px rgba(0,0,0,0.2);
        --transition-fast: 0.15s ease;
        --transition-normal: 0.2s ease;
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
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        --transition-fast: 0.15s ease;
        --transition-normal: 0.2s ease;
    }
        """
    
    base_css = """
    /* Hide Streamlit default elements */
    #MainMenu, header, footer, .stDeployButton { visibility: hidden; }
    header { display: none !important; }
    .block-container { padding-top: 1rem !important; }
    
    /* Global styles */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: var(--text-secondary) !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    [data-testid="stSidebar"] * { color: var(--text-secondary) !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { 
        color: var(--text-primary) !important; 
    }
    [data-testid="stSidebar"] .stMarkdown strong { color: var(--accent-blue) !important; }
    [data-testid="stSidebar"] .stSlider > div > div > div { background: var(--accent-blue) !important; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--bg-tertiary);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-muted) !important;
        font-weight: 600;
        padding: 10px 16px;
        transition: var(--transition-fast);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-secondary);
        color: var(--text-primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
        box-shadow: var(--shadow-sm);
    }
    
    /* Form labels */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label, .stTimeInput label, .stSlider label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        transition: var(--transition-fast);
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div, .stSelectbox > div > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    [data-baseweb="popover"], [data-baseweb="menu"] { 
        background: var(--bg-secondary) !important; 
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-md) !important;
    }
    [data-baseweb="menu"] li { background: var(--bg-secondary) !important; color: var(--text-primary) !important; }
    [data-baseweb="menu"] li:hover { background: var(--bg-tertiary) !important; }
    
    /* Date/time inputs */
    .stDateInput > div > div > input, .stTimeInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all var(--transition-normal) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button:hover {
        background: #2563eb !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stDownloadButton > button {
        background: var(--accent-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all var(--transition-normal) !important;
    }
    
    .stDownloadButton > button:hover {
        background: #059669 !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stForm [data-testid="stFormSubmitButton"] > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
    }
    
    /* ENHANCED: Metric cards with better shadows and hover */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        box-shadow: var(--shadow-md) !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
        border-color: var(--accent-blue) !important;
    }
    
    [data-testid="stMetricLabel"] { 
        color: var(--text-secondary) !important; 
        font-weight: 600 !important; 
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetricValue"] { 
        color: var(--text-primary) !important; 
        font-size: 2rem !important; 
        font-weight: 700 !important; 
    }
    
    /* Alerts with animations */
    .stSuccess, .stError, .stInfo, .stWarning {
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stSuccess { background: #ecfdf5 !important; border: 1px solid var(--accent-green) !important; border-radius: 8px !important; }
    .stSuccess p { color: #065f46 !important; font-weight: 500 !important; }
    .stError { background: #fef2f2 !important; border: 1px solid var(--accent-red) !important; border-radius: 8px !important; }
    .stError p { color: #991b1b !important; }
    .stInfo { background: #eff6ff !important; border: 1px solid var(--accent-blue) !important; border-radius: 8px !important; }
    .stInfo p { color: #1e40af !important; }
    .stWarning { background: #fffbeb !important; border: 1px solid var(--accent-yellow) !important; border-radius: 8px !important; }
    .stWarning p { color: #92400e !important; }
    
    /* ENHANCED: Dataframe with better styling and row hover */
    .stDataFrame { 
        border-radius: 12px !important; 
        border: 1px solid var(--border-color) !important; 
        box-shadow: var(--shadow-md) !important;
        overflow: hidden !important;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border-radius: 12px !important;
    }
    
    /* Table row hover effect */
    .stDataFrame tbody tr {
        transition: background var(--transition-fast) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: var(--bg-tertiary) !important;
    }
    
    /* Dividers */
    hr { border-color: var(--border-color) !important; opacity: 0.6; }
    
    /* Markdown */
    .stMarkdown strong { color: var(--accent-blue) !important; }
    
    /* Number input buttons */
    .stNumberInput button { 
        background: var(--bg-tertiary) !important; 
        border: 1px solid var(--border-color) !important; 
        color: var(--text-primary) !important;
        transition: var(--transition-fast) !important;
    }
    .stNumberInput button:hover { background: var(--border-color) !important; }
    
    /* Expander enhanced */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        transition: var(--transition-fast) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-tertiary) !important;
        border-color: var(--accent-blue) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-tertiary); }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    
    /* Toggle switch styling */
    .stToggle > div { color: var(--text-primary) !important; }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    """
    
    return "<style>\\n    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');\\n" + css_vars + base_css + "\\n</style>"
