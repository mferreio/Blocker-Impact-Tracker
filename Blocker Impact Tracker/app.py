"""
B.I.T. - Blocker Impact Tracker
Sistema para registrar e quantificar o impacto de impedimentos técnicos na produtividade do time de QA.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date

# Local modules
from database import (
    init_database, insert_incident, get_all_incidents, delete_incident,
    get_categorias, add_categoria, delete_categoria,
    get_tipos_impacto, add_tipo_impacto, delete_tipo_impacto,
    get_squads, add_squad, delete_squad
)
from config import DEFAULT_CAPACITY, MIN_CAPACITY, MAX_CAPACITY
from styles import get_custom_css
from charts import create_gauge, create_pareto, create_heatmap, create_timeline, create_squad_breakdown

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
    st.markdown("### 🛡️ B.I.T. v1.0")

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
    
    with st.form("form_incidente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data_incidente = st.date_input("📅 Data do Incidente", value=date.today(), max_value=date.today())
            hora_inicio = st.time_input("⏰ Hora de Início", value=None)
            squad = st.selectbox("👥 Squad", options=squads)
        
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
                    data=data_incidente.isoformat(),
                    hora_inicio=hora_inicio_str,
                    squad=squad,
                    categoria=categoria,
                    tipo_impacto=tipo_impacto,
                    peso=peso,
                    duracao=duracao,
                    hpp=hpp_calculado,
                    descricao=descricao
                )
                st.success(f"✅ Incidente registrado! HPP: {hpp_calculado:.2f}h")
                st.balloons()

# ==================== TAB 2: DASHBOARD ====================
with tab_dashboard:
    df = get_all_incidents()
    
    if df.empty:
        st.info("📭 Nenhum incidente registrado ainda.")
    else:
        df['data'] = pd.to_datetime(df['data'])
        
        # Metrics
        total_hpp = df['hpp'].sum()
        total_incidentes = len(df)
        media_hpp = df['hpp'].mean()
        environment_score = max(0, min(10, 10 * (1 - (total_hpp / capacidade_total))))
        
        col_metrics = st.columns(4)
        with col_metrics[0]:
            status = 'Bom' if environment_score >= 7 else 'Atenção' if environment_score >= 4 else 'Crítico'
            st.metric("🛡️ Saúde do Ambiente", f"{environment_score:.1f}/10", delta=status,
                      delta_color="normal" if environment_score >= 7 else "off" if environment_score >= 4 else "inverse")
        with col_metrics[1]:
            st.metric("⏱️ Total HPP", f"{total_hpp:.1f}h")
        with col_metrics[2]:
            st.metric("📊 Incidentes", total_incidentes)
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
        
        # Apply filters
        df_filtrado = df.copy()
        if len(data_range) == 2:
            df_filtrado = df_filtrado[(df_filtrado['data'].dt.date >= data_range[0]) & (df_filtrado['data'].dt.date <= data_range[1])]
        if squad_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['squad'] == squad_filtro]
        if categoria_filtro != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]
        if tipo_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['tipo_impacto'] == tipo_filtro]
        
        st.markdown("---")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("📊 Incidentes", len(df_filtrado))
        with col_m2:
            st.metric("⏱️ Total HPP", f"{df_filtrado['hpp'].sum():.2f}h")
        with col_m3:
            st.metric("📈 Média", f"{df_filtrado['hpp'].mean():.2f}h" if len(df_filtrado) > 0 else "0h")
        
        st.markdown("---")
        
        df_display = df_filtrado.copy()
        df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
        df_display = df_display[['id', 'data', 'hora_inicio', 'squad', 'categoria', 'tipo_impacto', 'duracao', 'hpp', 'descricao']]
        df_display.columns = ['ID', 'Data', 'Hora', 'Squad', 'Categoria', 'Impacto', 'Duração', 'HPP', 'Descrição']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        col_export, col_delete = st.columns([1, 1])
        with col_export:
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 Exportar CSV", csv, f"bit_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with col_delete:
            id_deletar = st.number_input("ID para deletar", min_value=1, step=1, value=None)
            if st.button("🗑️ Deletar", use_container_width=True, type="secondary"):
                if id_deletar:
                    delete_incident(id_deletar)
                    st.success(f"✅ Registro #{id_deletar} deletado!")
                    st.rerun()

# ==================== TAB 4: CONFIGURAÇÕES ====================
with tab_config:
    st.markdown("### ⚙️ Gerenciar Opções")
    st.caption("Adicione, edite ou remova categorias, tipos de impacto e squads")
    
    col_cat, col_tipo, col_squad = st.columns(3)
    
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

# ==================== FOOTER ====================
st.markdown("---")
st.caption("🛡️ B.I.T. - Blocker Impact Tracker v1.0 • Desenvolvido para times de QA")
