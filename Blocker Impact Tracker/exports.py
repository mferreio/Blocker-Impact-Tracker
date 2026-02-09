"""
B.I.T. - Blocker Impact Tracker
Export module - PDF and Excel export functionality
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import pandas as pd


def export_to_excel(df, filename="bit_report.xlsx"):
    """Export dataframe to Excel with formatting."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main data sheet
        df_export = df.copy()
        df_export.to_excel(writer, sheet_name='Incidentes', index=False)
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Incidentes']
        
        # Auto-adjust column widths
        for idx, col in enumerate(df_export.columns):
            max_length = max(
                df_export[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        # Style header row
        from openpyxl.styles import Font, PatternFill, Alignment
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='3B82F6', end_color='3B82F6', fill_type='solid')
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        
        # Summary sheet
        summary_data = {
            'Métrica': ['Total de Incidentes', 'Total HPP (h)', 'Média HPP (h)', 'Data do Relatório'],
            'Valor': [
                len(df),
                f"{df['hpp'].sum():.2f}" if 'hpp' in df.columns else 'N/A',
                f"{df['hpp'].mean():.2f}" if 'hpp' in df.columns else 'N/A',
                datetime.now().strftime('%d/%m/%Y %H:%M')
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Resumo', index=False)
        
        # Style summary sheet
        summary_sheet = writer.sheets['Resumo']
        for cell in summary_sheet[1]:
            cell.font = header_font
            cell.fill = header_fill
        summary_sheet.column_dimensions['A'].width = 25
        summary_sheet.column_dimensions['B'].width = 20
    
    output.seek(0)
    return output.getvalue()


def generate_pdf_report(df, metrics, period_label="Mensal"):
    """Generate PDF report with metrics, charts and data."""
    buffer = io.BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1e293b'),
        alignment=1  # Center
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#3b82f6')
    )
    
    # Build content
    content = []
    
    # Title
    content.append(Paragraph("🛡️ B.I.T. - Blocker Impact Tracker", title_style))
    content.append(Paragraph(f"Relatório {period_label}", subtitle_style))
    content.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", styles['Normal']))
    content.append(Spacer(1, 30))
    
    # Metrics section
    content.append(Paragraph("📊 Resumo Executivo", section_style))
    
    metrics_data = [
        ['Métrica', 'Valor'],
        ['Total de Incidentes', str(metrics.get('total_incidentes', 0))],
        ['Total HPP', f"{metrics.get('total_hpp', 0):.2f}h"],
        ['Média HPP', f"{metrics.get('media_hpp', 0):.2f}h"],
        ['Environment Score', f"{metrics.get('environment_score', 0):.1f}/10"],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[200, 150])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    content.append(metrics_table)
    content.append(Spacer(1, 30))
    
    # Top categories section
    if not df.empty and 'categoria' in df.columns:
        content.append(Paragraph("📂 Top Categorias por HPP", section_style))
        
        cat_summary = df.groupby('categoria')['hpp'].sum().sort_values(ascending=False).head(5)
        cat_data = [['Categoria', 'Total HPP']]
        for cat, hpp in cat_summary.items():
            cat_data.append([cat, f"{hpp:.2f}h"])
        
        cat_table = Table(cat_data, colWidths=[250, 100])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        content.append(cat_table)
        content.append(Spacer(1, 30))
    
    # Top squads section
    if not df.empty and 'squad' in df.columns:
        content.append(Paragraph("👥 Impacto por Squad", section_style))
        
        squad_summary = df.groupby('squad')['hpp'].sum().sort_values(ascending=False)
        squad_data = [['Squad', 'Total HPP', 'Incidentes']]
        for squad in squad_summary.index:
            squad_df = df[df['squad'] == squad]
            squad_data.append([squad, f"{squad_df['hpp'].sum():.2f}h", str(len(squad_df))])
        
        squad_table = Table(squad_data, colWidths=[180, 100, 80])
        squad_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        content.append(squad_table)
        content.append(Spacer(1, 30))
    
    # Recent incidents
    if not df.empty:
        content.append(Paragraph("📋 Últimos 10 Incidentes", section_style))
        
        recent_df = df.sort_values('data', ascending=False).head(10)
        incident_data = [['Data', 'Squad', 'Categoria', 'HPP']]
        
        for _, row in recent_df.iterrows():
            data_str = row['data'].strftime('%d/%m/%Y') if hasattr(row['data'], 'strftime') else str(row['data'])[:10]
            incident_data.append([
                data_str,
                str(row['squad'])[:15],
                str(row['categoria'])[:20],
                f"{row['hpp']:.2f}h"
            ])
        
        incident_table = Table(incident_data, colWidths=[80, 100, 140, 60])
        incident_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]))
        content.append(incident_table)
    
    # Footer
    content.append(Spacer(1, 40))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#94a3b8'),
        alignment=1
    )
    content.append(Paragraph("B.I.T. - Blocker Impact Tracker v1.1 • Desenvolvido para times de QA", footer_style))
    
    # Build PDF
    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()
