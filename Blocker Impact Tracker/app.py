"""
B.I.T. - Blocker Impact Tracker
Sistema para registrar e quantificar o impacto de impedimentos técnicos na produtividade do time de QA.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date

# Local modules
from database import (
    init_database, insert_incident, get_all_incidents, delete_incident, update_incident, delete_many_incidents,
    get_categorias, add_categoria, delete_categoria,
    get_tipos_impacto, add_tipo_impacto, delete_tipo_impacto,
    get_squads, add_squad, delete_squad, update_squad,
    get_produtos, add_produto, delete_produto, update_produto,
    seed_initial_data
)
from config import DEFAULT_CAPACITY, MIN_CAPACITY, MAX_CAPACITY
from styles import get_custom_css
from charts import create_gauge, create_pareto, create_heatmap, create_timeline, create_squad_breakdown
from exports import export_to_excel, generate_pdf_report

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="B.I.T. - Blocker Impact Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize database
init_database()

# Session State for Table Key (to force reset selection)
if 'table_key' not in st.session_state:
    st.session_state.table_key = 0

# ==================== DIALOGS ====================
@st.dialog("✏️ Editar Incidente")
def edit_incident_dialog(incident):
    st.write(f"Editando registro #{incident['id']}")
    
    # Get helpers for dropdowns
    squads = get_squads()
    produtos = get_produtos()
    cats = get_categorias()
    tipos = get_tipos_impacto()
    
    with st.form("edit_incident_form"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", value=pd.to_datetime(incident['data']))
            
            # Hora handling
            hora_val = None
            if incident['hora_inicio']:
                try:
                    hora_val = pd.to_datetime(str(incident['hora_inicio']), format='%H:%M:%S').time()
                except:
                    try:
                        hora_val = pd.to_datetime(str(incident['hora_inicio']), format='%H:%M').time()
                    except:
                        hora_val = None
            
            hora = st.time_input("Hora Início", value=hora_val)
            
        with col2:
            squad_idx = squads.index(incident['squad']) if incident['squad'] in squads else 0
            squad = st.selectbox("Squad", squads, index=squad_idx)
            
            prod_val = incident['produto'] if 'produto' in incident and incident['produto'] else None
            prod_idx = produtos.index(prod_val) if prod_val in produtos else 0
            produto = st.selectbox("Produto", produtos, index=prod_idx)
            
            cat_idx = cats.index(incident['categoria']) if incident['categoria'] in cats else 0
            categoria = st.selectbox("Categoria", cats, index=cat_idx)
            
        # Impacto
        tipo_names = list(tipos.keys())
        tipo_idx = tipo_names.index(incident['tipo_impacto']) if incident['tipo_impacto'] in tipo_names else 0
        tipo_impacto_nome = st.selectbox("Tipo de Impacto", tipo_names, index=tipo_idx)
        
        duracao = st.number_input("Duração (horas)", min_value=0.1, step=0.1, value=float(incident['duracao']))
        descricao = st.text_area("Descrição", value=incident['descricao'] if incident['descricao'] else "")
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.form_submit_button("✅ Salvar Alterações", use_container_width=True, type="primary"):
                peso = tipos[tipo_impacto_nome]
                hpp = duracao * peso
                
                if update_incident(incident['id'], data, hora, squad, categoria, tipo_impacto_nome, peso, duracao, hpp, descricao, produto):
                    st.success("Atualizado!")
                    st.session_state.table_key += 1
                    st.rerun()
                else:
                    st.error("Erro ao atualizar")

    st.markdown("---")
    if st.button("🗑️ Deletar Registro", type="secondary", use_container_width=True):
        if delete_incident(int(incident['id'])):
            st.success("Registro deletado!")
            st.session_state.table_key += 1
            st.rerun()
        else:
            st.error("Erro ao deletar registro.")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    st.markdown("---")
    
    st.markdown("📊 **Capacidade do Time (h/mês)**")
    col_min, col_max = st.columns(2)
    with col_min:
        st.caption(f"Mínimo: {MIN_CAPACITY}h")
    with col_max:
        st.caption(f"Máximo: {MAX_CAPACITY}h")
    
    capacidade_total = st.slider(
        "Capacidade",
        min_value=MIN_CAPACITY,
        max_value=MAX_CAPACITY,
        value=DEFAULT_CAPACITY,
        step=8,
        label_visibility="collapsed"
    )
    st.markdown(f"**Valor atual: {capacidade_total}h**")
    
    st.markdown("---")
    st.markdown("### 📖 Legenda")
    tipos = get_tipos_impacto()
    for nome, peso in tipos.items():
        emoji = "🔴" if peso >= 0.9 else "🟠" if peso >= 0.5 else "🟡"
        st.markdown(f"{emoji} **{nome.split('(')[0].strip()}**: {int(peso*100)}%")
    
    st.markdown("---")
    

    st.markdown("---")
    st.markdown("### 🛡️ B.I.T. v1.1")

# ==================== HEADER ====================
st.markdown("# 🛡️ B.I.T. - Blocker Impact Tracker")
st.caption("Registre e quantifique o impacto de impedimentos técnicos na produtividade do time de QA")

# ==================== TABS ====================
tab_registro, tab_dashboard, tab_historico, tab_config = st.tabs([
    "📝 Registrar Problema",
    "📊 Dashboard",
    "📋 Histórico",
    "⚙️ Configurações"
])

# ==================== TAB 1: REGISTRO ====================
with tab_registro:
    st.markdown("### 📝 Novo Registro de Impedimento")
    
    # Load dynamic options
    categorias = get_categorias()
    tipos_impacto = get_tipos_impacto()
    squads = get_squads()
    produtos = get_produtos()
    
    with st.form("form_incidente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data_incidente = st.date_input("📅 Data do Incidente", value=date.today(), max_value=date.today())
            hora_inicio = st.time_input("⏰ Hora de Início", value=None)
            squad = st.selectbox("👥 Squad", options=squads)
            produto = st.selectbox("📦 Produto", options=produtos)
        
        with col2:
            categoria = st.selectbox("📂 Categoria", options=categorias)
            tipo_impacto = st.selectbox("⚠️ Tipo de Impacto", options=list(tipos_impacto.keys()))
            duracao = st.number_input("⏱️ Duração (horas)", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
        
        descricao = st.text_area("📝 Descrição", placeholder="Descreva o problema ocorrido...", height=80)
        
        # Preview
        peso = tipos_impacto.get(tipo_impacto, 1.0)
        hpp_calculado = duracao * peso
        
        st.markdown("---")
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        with col_calc1:
            st.metric("Duração", f"{duracao}h")
        with col_calc2:
            st.metric("Peso", f"{peso}")
        with col_calc3:
            st.metric("HPP", f"{hpp_calculado:.2f}h", help="HPP = Horas Produtivas Perdidas (Duração × Peso)")
        
        submitted = st.form_submit_button("💾 Registrar Incidente", use_container_width=True)
        
        if submitted:
            if duracao <= 0:
                st.error("❌ A duração deve ser maior que zero!")
            elif data_incidente > date.today():
                st.error("❌ A data não pode ser futura!")
            else:
                hora_inicio_str = hora_inicio.strftime("%H:%M") if hora_inicio else None
                insert_incident(
                    data=data_incidente,
                    hora_inicio=hora_inicio_str,
                    squad=squad,
                    categoria=categoria,
                    tipo_impacto=tipo_impacto,
                    peso=peso,
                    duracao=duracao,
                    hpp=hpp_calculado,
                    descricao=descricao,
                    produto=produto
                )
                st.success(f"✅ Incidente registrado! HPP: {hpp_calculado:.2f}h")
                st.balloons()

# ==================== TAB 2: DASHBOARD ====================
with tab_dashboard:
    df = get_all_incidents()
    
    if df.empty:
        # Enhanced empty state
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 4rem; margin-bottom: 16px;">📊</div>
            <h3 style="color: #475569; margin-bottom: 8px;">Nenhum incidente registrado</h3>
            <p style="color: #94a3b8;">Comece registrando seu primeiro incidente na aba "Registrar Problema"</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        df['data'] = pd.to_datetime(df['data'])
        
        # Calculate metrics with trends (compare last 7 days vs previous 7 days)
        today = df['data'].max()
        last_7_days = df[df['data'] >= (today - pd.Timedelta(days=7))]
        prev_7_days = df[(df['data'] >= (today - pd.Timedelta(days=14))) & (df['data'] < (today - pd.Timedelta(days=7)))]
        
        total_hpp = df['hpp'].sum()
        total_incidentes = len(df)
        media_hpp = df['hpp'].mean()
        environment_score = max(0, min(10, 10 * (1 - (total_hpp / capacidade_total))))
        
        # Calculate trend deltas
        hpp_trend = last_7_days['hpp'].sum() - prev_7_days['hpp'].sum() if not prev_7_days.empty else 0
        inc_trend = len(last_7_days) - len(prev_7_days) if not prev_7_days.empty else 0
        
        col_metrics = st.columns(4)
        with col_metrics[0]:
            status = 'Bom' if environment_score >= 7 else 'Atenção' if environment_score >= 4 else 'Crítico'
            st.metric("🛡️ Saúde do Ambiente", f"{environment_score:.1f}/10", delta=status,
                      delta_color="normal" if environment_score >= 7 else "off" if environment_score >= 4 else "inverse")
        with col_metrics[1]:
            trend_label = f"{hpp_trend:+.1f}h (7d)" if hpp_trend != 0 else None
            st.metric("⏱️ Total HPP", f"{total_hpp:.1f}h", delta=trend_label, delta_color="inverse" if hpp_trend > 0 else "normal")
        with col_metrics[2]:
            trend_label = f"{inc_trend:+d} (7d)" if inc_trend != 0 else None
            st.metric("📊 Incidentes", total_incidentes, delta=trend_label, delta_color="inverse" if inc_trend > 0 else "normal")
        with col_metrics[3]:
            st.metric("📈 Média HPP", f"{media_hpp:.2f}h")
        
        st.markdown("---")
        
        # Charts row 1
        col_gauge, col_pareto = st.columns([1, 1])
        with col_gauge:
            st.markdown("#### 🎯 Environment Score")
            st.plotly_chart(create_gauge(environment_score), use_container_width=True)
        with col_pareto:
            st.markdown("#### 📊 Pareto de Bloqueios")
            df_pareto = df.groupby('categoria')['hpp'].sum().reset_index().sort_values('hpp', ascending=True)
            st.plotly_chart(create_pareto(df_pareto), use_container_width=True)
        
        st.markdown("---")
        
        # Charts row 2
        col_heatmap, col_timeline = st.columns([1, 1])
        with col_heatmap:
            st.markdown("#### 🗓️ Heatmap")
            df_heat = df.copy()
            df_heat['dia_semana'] = df_heat['data'].dt.day_name()
            df_heat['hora'] = df_heat['hora_inicio'].apply(lambda x: int(x.split(':')[0]) if pd.notna(x) and x else 12)
            dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dias_pt = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            df_pivot = df_heat.groupby(['dia_semana', 'hora'])['hpp'].sum().reset_index().pivot_table(
                values='hpp', index='dia_semana', columns='hora', aggfunc='sum', fill_value=0
            )
            df_pivot = df_pivot.reindex(dias_ordem)
            horas = list(range(8, 20))
            df_pivot = df_pivot[[h for h in horas if h in df_pivot.columns]]
            if not df_pivot.empty and len(df_pivot.columns) > 0:
                st.plotly_chart(create_heatmap(df_pivot, dias_pt), use_container_width=True)
            else:
                st.info("Dados insuficientes.")
        with col_timeline:
            st.markdown("#### 📈 Timeline")
            df_timeline = df.groupby(df['data'].dt.date)['hpp'].sum().reset_index()
            df_timeline.columns = ['data', 'hpp']
            st.plotly_chart(create_timeline(df_timeline), use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 👥 Breakdown por Squad")
        df_squad = df.groupby('squad').agg({'hpp': 'sum', 'id': 'count'}).reset_index()
        df_squad.columns = ['Squad', 'Total HPP', 'Incidentes']
        st.plotly_chart(create_squad_breakdown(df_squad), use_container_width=True)
        
        # PDF Export section
        st.markdown("---")
        st.markdown("#### 📄 Exportar Relatório")
        col_pdf_btn, col_pdf_space = st.columns([1, 2])
        with col_pdf_btn:
            # Prepare metrics for PDF
            pdf_metrics = {
                'total_incidentes': total_incidentes,
                'total_hpp': total_hpp,
                'media_hpp': media_hpp,
                'environment_score': environment_score
            }
            pdf_data = generate_pdf_report(df, pdf_metrics, "Mensal")
            st.download_button(
                "📥 Baixar Relatório PDF",
                data=pdf_data,
                file_name=f"bit_relatorio_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ==================== TAB 3: HISTÓRICO ====================
with tab_historico:
    df = get_all_incidents()
    
    if df.empty:
        st.info("📭 Nenhum incidente registrado ainda.")
    else:
        df['data'] = pd.to_datetime(df['data'])
        
        # Filters
        col_filtros = st.columns(4)
        with col_filtros[0]:
            data_min, data_max = df['data'].min().date(), df['data'].max().date()
            data_range = st.date_input("📅 Período", value=(data_min, data_max), min_value=data_min, max_value=data_max)
        with col_filtros[1]:
            squad_filtro = st.selectbox("👥 Squad", ['Todos'] + df['squad'].unique().tolist(), key="hist_squad")
        with col_filtros[2]:
            categoria_filtro = st.selectbox("📂 Categoria", ['Todas'] + df['categoria'].unique().tolist(), key="hist_cat")
        with col_filtros[3]:
            tipo_filtro = st.selectbox("⚠️ Impacto", ['Todos'] + df['tipo_impacto'].unique().tolist(), key="hist_tipo")
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            f_squad = st.multiselect("Squad", options=sorted(df['squad'].unique()))
        with col_f2:
            f_prod = st.multiselect("Produto", options=sorted(df['produto'].dropna().unique()) if 'produto' in df.columns else [])
        with col_f3:
            f_cat = st.multiselect("Categoria", options=sorted(df['categoria'].unique()))
        with col_f4:
            f_tipo = st.multiselect("Impacto", options=sorted(df['tipo_impacto'].unique()))
        
        # Apply filters
        df_filtrado = df.copy()
        if len(data_range) == 2:
            df_filtrado = df_filtrado[(df_filtrado['data'].dt.date >= data_range[0]) & (df_filtrado['data'].dt.date <= data_range[1])]
        if f_squad:
            df_filtrado = df_filtrado[df_filtrado['squad'].isin(f_squad)]
        if f_prod and 'produto' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['produto'].isin(f_prod)]
        if f_cat:
            df_filtrado = df_filtrado[df_filtrado['categoria'].isin(f_cat)]
        if f_tipo:
            df_filtrado = df_filtrado[df_filtrado['tipo_impacto'].isin(f_tipo)]
        
        st.markdown("---")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("📊 Incidentes", len(df_filtrado))
        with col_m2:
            st.metric("⏱️ Total HPP", f"{df_filtrado['hpp'].sum():.2f}h")
        with col_m3:
            st.metric("📈 Média", f"{df_filtrado['hpp'].mean():.2f}h" if len(df_filtrado) > 0 else "0h")
        
        st.markdown("---")
        
        # Apply badge styling to impact type
        def style_impact(val):
            if 'Bloqueio' in str(val):
                return '🔴 ' + val.split('(')[0].strip()
            elif 'Severa' in str(val):
                return '🟠 ' + val.split('(')[0].strip()
            else:
                return '🟡 ' + val.split('(')[0].strip()
        
        # Configure column display
        column_config = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "HPP": st.column_config.NumberColumn("HPP", format="%.2f h"),
            "Duração": st.column_config.NumberColumn("Duração", format="%.2f h"),
        }
        
        # Sorting options
        col_sort, col_order, col_page_size = st.columns([2, 1, 1])
        with col_sort:
            sort_column = st.selectbox(
                "🔀 Ordenar por",
                options=['Data', 'HPP', 'Duração', 'Squad', 'Categoria'],
                key="sort_col"
            )
        with col_order:
            sort_order = st.selectbox("Ordem", ["⬇️ Desc", "⬆️ Asc"], key="sort_order")
        with col_page_size:
            page_size = st.selectbox("Por página", [10, 25, 50, 100], key="page_size")
        
        # Apply sorting
        sort_map = {'Data': 'data', 'HPP': 'hpp', 'Duração': 'duracao', 'Squad': 'squad', 'Categoria': 'categoria'}
        ascending = "Asc" in sort_order
        
        # Sort on original df_filtrado before display transformation
        df_sorted = df_filtrado.sort_values(by=sort_map.get(sort_column, 'data'), ascending=ascending)
        
        # Pagination
        total_records = len(df_sorted)
        total_pages = max(1, (total_records + page_size - 1) // page_size)
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Pagination controls
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀️ Anterior", use_container_width=True, disabled=st.session_state.current_page <= 1):
                st.session_state.current_page -= 1
                st.rerun()
        with col_info:
            st.markdown(f"<div style='text-align: center; padding: 8px;'>Página **{st.session_state.current_page}** de **{total_pages}** ({total_records} registros)</div>", unsafe_allow_html=True)
        with col_next:
            if st.button("Próxima ▶️", use_container_width=True, disabled=st.session_state.current_page >= total_pages):
                st.session_state.current_page += 1
                st.rerun()
        
        # Apply pagination
        start_idx = (st.session_state.current_page - 1) * page_size
        end_idx = start_idx + page_size
        df_paginated = df_sorted.iloc[start_idx:end_idx]
        
        # Prepare display dataframe
        df_display = df_paginated.copy()
        df_display['data'] = pd.to_datetime(df_display['data']).dt.strftime('%d/%m/%Y')
        df_display['tipo_impacto'] = df_display['tipo_impacto'].apply(style_impact)
        df_display = df_display[['id', 'data', 'hora_inicio', 'squad', 'produto', 'categoria', 'tipo_impacto', 'duracao', 'hpp', 'descricao']]
        df_display.columns = ['ID', 'Data', 'Hora', 'Squad', 'Produto', 'Categoria', 'Impacto', 'Duração', 'HPP', 'Descrição']
        
        event = st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            on_select="rerun",
            selection_mode="multi-row",
            key=f"history_table_{st.session_state.table_key}"
        )
        
        # Action Bar for selection
        if len(event.selection.rows) > 0:
            st.markdown("---")
            selected_indices = event.selection.rows
            # Get IDs from displayed dataframe
            selected_ids = [int(df_display.iloc[idx]['ID']) for idx in selected_indices]
            count = len(selected_ids)
            
            c1, c2, c3 = st.columns([1, 1, 3])
            
            with c1:
                # Edit button only for single selection
                if count == 1:
                    if st.button("✏️ Editar", use_container_width=True, type="primary"):
                        record = df[df['id'] == selected_ids[0]].iloc[0]
                        edit_incident_dialog(record)
                else:
                    st.button("✏️ Editar", disabled=True, use_container_width=True, help="Selecione apenas 1 registro para editar")

            with c2:
                # Delete button handles multiple
                if st.button(f"🗑️ Excluir ({count})", type="secondary", use_container_width=True):
                    if delete_many_incidents(selected_ids):
                        st.success(f"✅ {count} registros excluídos!")
                        st.session_state.table_key += 1
                        st.rerun()
                    else:
                        st.error("Erro ao excluir registros.")
        
        st.markdown("---")
        col_csv, col_excel = st.columns(2)
        with col_csv:
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 Exportar CSV", csv, f"bit_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with col_excel:
            xlsx_data = export_to_excel(df_filtrado)
            st.download_button("📊 Exportar Excel", xlsx_data, f"bit_{datetime.now().strftime('%Y%m%d')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

            


# ==================== TAB 4: CONFIGURAÇÕES ====================
with tab_config:
    st.markdown("### ⚙️ Gerenciar Opções")
    st.caption("Adicione, edite ou remova categorias, tipos de impacto e squads")
    
    if st.button("🔄 Restaurar Padrões da Base", help="Recria categorias, squads e produtos padrão se estiverem faltando."):
        if seed_initial_data():
            st.success("✅ Padrões restaurados! A página será recarregada.")
            st.rerun()
        else:
            st.error("Erro ao restaurar. Verifique os logs.")
    st.markdown("---")
    
    col_cat, col_tipo = st.columns(2)
    
    # ========== CATEGORIAS ==========
    with col_cat:
        st.markdown("#### 📂 Categorias")
        
        categorias_list = get_categorias()
        for i, cat in enumerate(categorias_list):
            with st.expander(cat, expanded=False):
                novo_nome_cat = st.text_input("Nome", value=cat, key=f"edit_cat_{i}")
                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("💾 Salvar", key=f"save_cat_{i}", use_container_width=True):
                        if novo_nome_cat.strip() and novo_nome_cat != cat:
                            from database import update_categoria
                            if update_categoria(cat, novo_nome_cat.strip()):
                                st.success("✅ Atualizado!")
                                st.rerun()
                            else:
                                st.error("❌ Nome já existe!")
                with col_del:
                    if st.button("🗑️ Excluir", key=f"del_cat_{i}", use_container_width=True, type="secondary"):
                        delete_categoria(cat)
                        st.rerun()
        
        st.markdown("---")
        with st.form("add_categoria", clear_on_submit=True):
            nova_cat = st.text_input("➕ Nova categoria", placeholder="Ex: Bug de Sistema")
            if st.form_submit_button("Adicionar", use_container_width=True):
                if nova_cat.strip():
                    if add_categoria(nova_cat.strip()):
                        st.success("✅ Adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Já existe!")
    
    # ========== TIPOS DE IMPACTO ==========
    with col_tipo:
        st.markdown("#### ⚠️ Tipos de Impacto")
        
        tipos_list = get_tipos_impacto()
        for i, (nome, peso) in enumerate(tipos_list.items()):
            with st.expander(f"{nome[:20]}... ({int(peso*100)}%)" if len(nome) > 20 else f"{nome} ({int(peso*100)}%)", expanded=False):
                novo_nome_tipo = st.text_input("Nome", value=nome, key=f"edit_tipo_{i}")
                novo_peso_tipo = st.slider("Peso (%)", 0, 100, int(peso*100), 5, key=f"peso_tipo_{i}")
                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("💾 Salvar", key=f"save_tipo_{i}", use_container_width=True):
                        if novo_nome_tipo.strip():
                            from database import update_tipo_impacto
                            if update_tipo_impacto(nome, novo_nome_tipo.strip(), novo_peso_tipo / 100):
                                st.success("✅ Atualizado!")
                                st.rerun()
                            else:
                                st.error("❌ Nome já existe!")
                with col_del:
                    if st.button("🗑️ Excluir", key=f"del_tipo_{i}", use_container_width=True, type="secondary"):
                        delete_tipo_impacto(nome)
                        st.rerun()
        
        st.markdown("---")
        with st.form("add_tipo", clear_on_submit=True):
            novo_tipo = st.text_input("➕ Novo tipo", placeholder="Ex: Instabilidade")
            novo_peso = st.slider("Peso (%)", 0, 100, 50, 5)
            if st.form_submit_button("Adicionar", use_container_width=True):
                if novo_tipo.strip():
                    if add_tipo_impacto(novo_tipo.strip(), novo_peso / 100):
                        st.success("✅ Adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Já existe!")
    
    st.markdown("---")
    
    col_squad, col_prod = st.columns(2)
    
    # ========== SQUADS ==========
    with col_squad:
        st.markdown("#### 👥 Squads")
        
        squads_list = get_squads()
        for i, squad in enumerate(squads_list):
            with st.expander(squad, expanded=False):
                novo_nome_squad = st.text_input("Nome", value=squad, key=f"edit_squad_{i}")
                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("💾 Salvar", key=f"save_squad_{i}", use_container_width=True):
                        if novo_nome_squad.strip() and novo_nome_squad != squad:
                            from database import update_squad
                            if update_squad(squad, novo_nome_squad.strip()):
                                st.success("✅ Atualizado!")
                                st.rerun()
                            else:
                                st.error("❌ Nome já existe!")
                with col_del:
                    if st.button("🗑️ Excluir", key=f"del_squad_{i}", use_container_width=True, type="secondary"):
                        delete_squad(squad)
                        st.rerun()
        
        st.markdown("---")
        with st.form("add_squad", clear_on_submit=True):
            novo_squad = st.text_input("➕ Novo squad", placeholder="Ex: Squad Phoenix")
            if st.form_submit_button("Adicionar", use_container_width=True):
                if novo_squad.strip():
                    if add_squad(novo_squad.strip()):
                        st.success("✅ Adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Já existe!")


    # ========== PRODUTOS ==========
    with col_prod:
        st.markdown("#### 📦 Produtos")
        
        produtos_list = get_produtos()
        for i, prod in enumerate(produtos_list):
            with st.expander(prod, expanded=False):
                novo_nome_prod = st.text_input("Nome", value=prod, key=f"edit_prod_{i}")
                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("💾 Salvar", key=f"save_prod_{i}", use_container_width=True):
                        if novo_nome_prod.strip() and novo_nome_prod != prod:
                            from database import update_produto
                            if update_produto(prod, novo_nome_prod.strip()):
                                st.success("✅ Atualizado!")
                                st.rerun()
                            else:
                                st.error("❌ Nome já existe!")
                with col_del:
                    if st.button("🗑️ Excluir", key=f"del_prod_{i}", use_container_width=True, type="secondary"):
                        delete_produto(prod)
                        st.rerun()
        
        st.markdown("---")
        with st.form("add_prod", clear_on_submit=True):
            novo_prod = st.text_input("➕ Novo produto", placeholder="Ex: App Android")
            if st.form_submit_button("Adicionar", use_container_width=True):
                if novo_prod.strip():
                    if add_produto(novo_prod.strip()):
                        st.success("✅ Adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Já existe!")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("🛡️ B.I.T. - Blocker Impact Tracker v1.0 • Desenvolvido para times de QA")
