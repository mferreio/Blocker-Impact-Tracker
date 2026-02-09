# 🛡️ B.I.T. - Blocker Impact Tracker

Sistema para registrar e quantificar o impacto de impedimentos técnicos na produtividade do time de QA.

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- Plotly

## 🚀 Como Rodar Localmente

### 1. Clonar/Acessar o projeto

```bash
cd "c:\Matheus\Blocker Impact Tracker"
```

### 2. Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`.

## 📊 Funcionalidades

### Registro de Incidentes
- Data, Squad, Categoria, Tipo de Impacto, Duração
- Validação automática (sem datas futuras ou durações negativas)
- Cálculo automático de HPP (Horas de Produtividade Perdidas)

### Dashboard Executivo
- **Environment Score**: Gauge de 0-10 indicando saúde do ambiente
- **Heatmap**: Dias vs Horas com picos de instabilidade
- **Pareto**: Categorias que mais causaram perdas
- **Timeline**: Evolução das horas perdidas ao longo do tempo

### Histórico/Filtros
- Filtros por período, squad, categoria e tipo de impacto
- Exportação para CSV

## 📐 Fórmulas

**HPP (Horas de Produtividade Perdidas):**
```
HPP = Duração × Peso do Impacto
```

**Pesos:**
- Bloqueio Total: 1.0
- Lentidão Severa: 0.75
- Lentidão Moderada: 0.25

**Environment Score:**
```
Score = 10 × (1 - Total_HPP / Capacidade_Total)
```

## 🗃️ Banco de Dados

O sistema utiliza SQLite (`bit_tracker.db`), que é criado automaticamente na primeira execução. Não requer configuração de servidor de banco de dados.

## 🎨 Interface

- Design moderno em Dark Mode
- Interface responsiva com tabs
- Visualizações interativas com Plotly
