"""
B.I.T. - Blocker Impact Tracker
Charts module - Plotly visualizations with consistent light theme
"""

import plotly.express as px
import plotly.graph_objects as go

# Chart theme colors (light mode)
CHART_COLORS = {
    'text': '#1e293b',
    'text_muted': '#64748b',
    'grid': '#e2e8f0',
    'background': 'rgba(0,0,0,0)',
    'green': '#10b981',
    'yellow': '#f59e0b', 
    'red': '#ef4444',
    'blue': '#3b82f6',
    'blue_light': 'rgba(59, 130, 246, 0.15)'
}


def get_chart_layout(height=300):
    """Returns base layout for all charts."""
    return dict(
        paper_bgcolor=CHART_COLORS['background'],
        plot_bgcolor=CHART_COLORS['background'],
        font={'color': CHART_COLORS['text'], 'family': 'Inter'},
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis={'gridcolor': CHART_COLORS['grid'], 'zerolinecolor': CHART_COLORS['grid']},
        yaxis={'gridcolor': CHART_COLORS['grid'], 'zerolinecolor': CHART_COLORS['grid']}
    )


def create_gauge(score, title="Environment Score"):
    """Creates an environment score gauge chart."""
    if score >= 7:
        color = CHART_COLORS['green']
        status = "Saudável"
    elif score >= 4:
        color = CHART_COLORS['yellow']
        status = "Atenção"
    else:
        color = CHART_COLORS['red']
        status = "Crítico"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number={'suffix': "/10", 'font': {'size': 36, 'color': CHART_COLORS['text']}},
        delta={'reference': 7, 'increasing': {'color': CHART_COLORS['green']}, 'decreasing': {'color': CHART_COLORS['red']}},
        gauge={
            'axis': {'range': [0, 10], 'tickcolor': CHART_COLORS['text_muted']},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': '#f1f5f9',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 4], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [4, 7], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [7, 10], 'color': 'rgba(16, 185, 129, 0.15)'}
            ]
        },
        title={'text': f"Status: {status}", 'font': {'size': 14, 'color': CHART_COLORS['text_muted']}}
    ))
    
    fig.update_layout(**get_chart_layout())
    return fig


def create_pareto(df_pareto):
    """Creates a horizontal bar chart for Pareto analysis."""
    fig = px.bar(
        df_pareto, 
        x='hpp', 
        y='categoria', 
        orientation='h', 
        color='hpp',
        color_continuous_scale=[CHART_COLORS['green'], CHART_COLORS['yellow'], CHART_COLORS['red']]
    )
    
    layout = get_chart_layout()
    layout['showlegend'] = False
    layout['coloraxis_showscale'] = False
    fig.update_layout(**layout)
    return fig


def create_heatmap(df_pivot, dias_pt):
    """Creates a heatmap for instability visualization."""
    fig = px.imshow(
        df_pivot.values, 
        x=[f"{h}h" for h in df_pivot.columns],
        y=dias_pt[:len(df_pivot.index)],
        color_continuous_scale=['#f8fafc', CHART_COLORS['green'], CHART_COLORS['yellow'], CHART_COLORS['red']],
        aspect='auto'
    )
    
    fig.update_layout(**get_chart_layout())
    return fig


def create_timeline(df_timeline):
    """Creates a line chart for timeline visualization."""
    fig = px.line(df_timeline, x='data', y='hpp', markers=True)
    
    fig.update_traces(
        line_color=CHART_COLORS['blue'], 
        marker_color=CHART_COLORS['blue'], 
        marker_size=8,
        fill='tozeroy', 
        fillcolor=CHART_COLORS['blue_light']
    )
    
    fig.update_layout(**get_chart_layout())
    return fig


def create_squad_breakdown(df_squad):
    """Creates a bar chart for squad breakdown."""
    fig = px.bar(
        df_squad.sort_values('Total HPP', ascending=False), 
        x='Squad', 
        y='Total HPP',
        color='Incidentes', 
        color_continuous_scale=[CHART_COLORS['blue'], CHART_COLORS['green']]
    )
    
    fig.update_layout(**get_chart_layout())
    return fig
