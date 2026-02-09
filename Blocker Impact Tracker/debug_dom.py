"""
Debug script to inspect Streamlit DOM structure.
Run with: streamlit run debug_dom.py
Click the "Capture DOM" button to see actual element selectors.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DOM Inspector", layout="wide")
st.title("DOM Inspector")

# Create sample elements to inspect
tab1, tab2 = st.tabs(["Tab A", "Tab B"])
with tab1:
    st.write("Tab content")
    
    with st.form("test_form"):
        st.text_input("Test input")
        st.selectbox("Test select", ["A", "B"])
        st.form_submit_button("Submit Button Text")
    
    st.button("Primary Button", type="primary")
    st.button("Secondary Button", type="secondary")
    st.download_button("Download Button", data="test", file_name="test.txt")

# JavaScript to capture DOM info
components.html("""
<div id="dom-report" style="font-family: monospace; font-size: 12px; white-space: pre-wrap; background: #1e293b; color: #e2e8f0; padding: 20px; border-radius: 8px; max-height: 800px; overflow-y: auto;"></div>
<script>
setTimeout(function() {
    var report = [];
    
    // Inspect tabs
    report.push("===== TABS =====");
    var tabs = document.querySelectorAll('[data-baseweb="tab"]');
    tabs.forEach(function(tab, i) {
        report.push("Tab " + i + ":");
        report.push("  outerHTML: " + tab.outerHTML.substring(0, 500));
        report.push("  aria-selected: " + tab.getAttribute("aria-selected"));
        report.push("  data-testid: " + tab.getAttribute("data-testid"));
        report.push("  Children tags: " + Array.from(tab.children).map(c => c.tagName + "[" + (c.getAttribute("data-testid")||"") + "]").join(", "));
    });
    
    // Inspect all buttons
    report.push("\\n===== BUTTONS =====");
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function(btn, i) {
        var testid = btn.getAttribute("data-testid") || "none";
        var kind = btn.getAttribute("kind") || "none";
        var text = btn.textContent.trim().substring(0, 50);
        var parentTestid = btn.parentElement ? (btn.parentElement.getAttribute("data-testid") || "none") : "none";
        var grandParentTestid = btn.parentElement && btn.parentElement.parentElement ? (btn.parentElement.parentElement.getAttribute("data-testid") || "none") : "none";
        var classes = btn.className;
        report.push("Button " + i + ": text='" + text + "'");
        report.push("  data-testid: " + testid);
        report.push("  kind: " + kind);
        report.push("  classes: " + classes);
        report.push("  parent data-testid: " + parentTestid);
        report.push("  grandparent data-testid: " + grandParentTestid);
        report.push("  computedBg: " + window.getComputedStyle(btn).backgroundColor);
        report.push("  computedColor: " + window.getComputedStyle(btn).color);
    });
    
    // Inspect inputs
    report.push("\\n===== INPUTS =====");
    var inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(function(inp, i) {
        var testid = inp.getAttribute("data-testid") || "none";
        report.push("Input " + i + ": type=" + inp.type + " testid=" + testid);
        report.push("  parent classes: " + (inp.parentElement ? inp.parentElement.className : "none"));
        report.push("  computedBg: " + window.getComputedStyle(inp).backgroundColor);
        report.push("  computedBorder: " + window.getComputedStyle(inp).border);
    });
    
    // Inspect select/dropdown
    report.push("\\n===== SELECTS =====");
    var selects = document.querySelectorAll('[data-baseweb="select"]');
    selects.forEach(function(sel, i) {
        report.push("Select " + i + ":");
        report.push("  outerHTML (first 300): " + sel.outerHTML.substring(0, 300));
    });
    
    document.getElementById("dom-report").textContent = report.join("\\n");
}, 3000);
</script>
""", height=800)
