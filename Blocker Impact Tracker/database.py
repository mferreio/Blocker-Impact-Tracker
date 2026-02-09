"""
B.I.T. - Blocker Impact Tracker
Database operations module
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bit_tracker.db")


def get_connection():
    """Returns a database connection."""
    return sqlite3.connect(DB_PATH)


def init_database():
    """Inicializa o banco de dados SQLite com todas as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de incidentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            hora_inicio TIME,
            squad TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo_impacto TEXT NOT NULL,
            peso REAL NOT NULL,
            duracao REAL NOT NULL,
            hpp REAL NOT NULL,
            descricao TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de categorias customizadas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            is_default INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de tipos de impacto customizados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_impacto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            peso REAL NOT NULL,
            is_default INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de squads customizados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS squads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            is_default INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insere valores padrão se as tabelas estiverem vazias
    _insert_defaults(cursor)
    
    conn.commit()
    conn.close()


def _insert_defaults(cursor):
    """Insere valores padrão nas tabelas de configuração."""
    # Categorias padrão
    default_categorias = [
        "Massa de Dados",
        "Ambiente/Downtime", 
        "Problemas de Acesso",
        "Infraestrutura/Internet",
        "Outros"
    ]
    for cat in default_categorias:
        cursor.execute("INSERT OR IGNORE INTO categorias (nome, is_default) VALUES (?, 1)", (cat,))
    
    # Tipos de impacto padrão
    default_tipos = [
        ("Bloqueio Total (Sistema inoperante)", 1.0),
        ("Lentidão Severa (Degradação alta)", 0.75),
        ("Lentidão Moderada (Instabilidade leve)", 0.25)
    ]
    for nome, peso in default_tipos:
        cursor.execute("INSERT OR IGNORE INTO tipos_impacto (nome, peso, is_default) VALUES (?, ?, 1)", (nome, peso))
    
    # Squads padrão
    default_squads = ["Squad Alpha", "Squad Beta", "Squad Gamma", "Squad Delta", "Squad Epsilon"]
    for squad in default_squads:
        cursor.execute("INSERT OR IGNORE INTO squads (nome, is_default) VALUES (?, 1)", (squad,))


# ==================== INCIDENTS ====================
def insert_incident(data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao):
    """Insere um novo incidente no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incidents (data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao))
    conn.commit()
    conn.close()


def get_all_incidents():
    """Retorna todos os incidentes como DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM incidents ORDER BY data DESC, hora_inicio DESC", conn)
    conn.close()
    return df


def delete_incident(incident_id):
    """Deleta um incidente pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()


# ==================== CATEGORIAS ====================
def get_categorias():
    """Retorna lista de categorias."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM categorias ORDER BY is_default DESC, nome")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result if result else ["Outros"]


def add_categoria(nome):
    """Adiciona nova categoria."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def delete_categoria(nome):
    """Remove categoria pelo nome."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()


# ==================== TIPOS DE IMPACTO ====================
def get_tipos_impacto():
    """Retorna dicionário de tipos de impacto com seus pesos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, peso FROM tipos_impacto ORDER BY peso DESC")
    result = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return result if result else {"Bloqueio Total": 1.0}


def add_tipo_impacto(nome, peso):
    """Adiciona novo tipo de impacto."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tipos_impacto (nome, peso) VALUES (?, ?)", (nome, peso))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def delete_tipo_impacto(nome):
    """Remove tipo de impacto pelo nome."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tipos_impacto WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()


# ==================== SQUADS ====================
def get_squads():
    """Retorna lista de squads."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM squads ORDER BY nome")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result if result else ["Equipe Padrão"]


def add_squad(nome):
    """Adiciona novo squad."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO squads (nome) VALUES (?)", (nome,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def delete_squad(nome):
    """Remove squad pelo nome."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM squads WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()


def update_squad(nome_antigo, nome_novo):
    """Atualiza o nome de um squad."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE squads SET nome = ? WHERE nome = ?", (nome_novo, nome_antigo))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def update_categoria(nome_antigo, nome_novo):
    """Atualiza o nome de uma categoria."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categorias SET nome = ? WHERE nome = ?", (nome_novo, nome_antigo))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def update_tipo_impacto(nome_antigo, nome_novo, peso_novo):
    """Atualiza um tipo de impacto."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tipos_impacto SET nome = ?, peso = ? WHERE nome = ?", (nome_novo, peso_novo, nome_antigo))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success
