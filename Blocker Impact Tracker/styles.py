"""
B.I.T. - Blocker Impact Tracker
Styles module - Minimal clean styles complementing native Streamlit theme
"""

def get_custom_css(dark_mode=True):
    """Returns minimal custom CSS to enhance the native theme."""
    # Note: Main colors are now handled by .streamlit/config.toml
    
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Hide Streamlit default branding */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    
    /* Clean up top padding */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 1200px !important;
    }

    /* Metric Cards - Custom styling that native theme can't do */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Buttons - make them slightly more prominent */
    .stButton button {
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Secondary/Outline buttons need to be visible on dark bg */
    [data-testid="stBaseButton-secondary"] {
        background-color: transparent !important;
        border: 1px solid #475569 !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.1) !important;
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        border-radius: 8px !important;
    }
    
    /* Success/Error/Warning messages */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* Center align images if needed */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
</style>
"""
