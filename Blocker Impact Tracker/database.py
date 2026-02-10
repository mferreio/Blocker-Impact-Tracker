"""
B.I.T. - Blocker Impact Tracker
Database operations module - SQLAlchemy implementation
Support for SQLite (local) and PostgreSQL (production)
"""

import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Date, Time, Boolean, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Get Database URL from environment or fallback to local SQLite
# Render/Koyeb provide DATABASE_URL. 
# Note: SQLAlchemy requires 'postgresql://' instead of 'postgres://' (common in Heroku/Render)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bit_tracker.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Initialize Engine
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

# Define Tables
incidents = Table(
    'incidents', metadata,
    Column('id', Integer, primary_key=True),
    Column('data', Date, nullable=False),
    Column('hora_inicio', String),  # Stored as string HH:MM
    Column('squad', String, nullable=False),
    Column('categoria', String, nullable=False),
    Column('tipo_impacto', String, nullable=False),
    Column('peso', Float, nullable=False),
    Column('duracao', Float, nullable=False),
    Column('hpp', Float, nullable=False),
    Column('descricao', String),
    Column('created_at', DateTime, default=datetime.now)
)

categorias = Table(
    'categorias', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String, unique=True, nullable=False),
    Column('is_default', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.now)
)

tipos_impacto = Table(
    'tipos_impacto', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String, unique=True, nullable=False),
    Column('peso', Float, nullable=False),
    Column('is_default', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.now)
)

squads = Table(
    'squads', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String, unique=True, nullable=False),
    Column('is_default', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.now)
)

produtos = Table(
    'produtos', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String, unique=True, nullable=False),
    Column('created_at', DateTime, default=datetime.now)
)


def get_connection():
    """Returns a database connection."""
    return engine.connect()


def init_database():
    """Initializes the database schema."""
    try:
        # Check for schema updates FIRST (before create_all to simplify logic or inside)
        # Actually create_all won't add columns to existing tables.
        
        # Create tables if not exist
        metadata.create_all(engine)
        
        # Check migrations/schema updates
        check_schema_updates()
        
        # Check if we need to seed defaults
        with engine.connect() as conn:
            # Check categories
            result = conn.execute(text("SELECT COUNT(*) FROM categorias")).scalar()
            if result == 0:
                _insert_defaults(conn)
                conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")

def check_schema_updates():
    """Checks and applies schema updates (migrations)."""
    try:
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns('incidents')]
        
        if 'produto' not in columns:
            print("Migrating: Adding 'produto' column to incidents table...")
            with engine.connect() as conn:
                # Add column. SQLite and Postgres support ADD COLUMN
                conn.execute(text("ALTER TABLE incidents ADD COLUMN produto VARCHAR"))
                conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")


def _insert_defaults(conn):
    """Inserts default values into configuration tables."""
    # Categorias padrão
    default_categorias = [
        "Massa de Dados",
        "Ambiente/Downtime", 
        "Problemas de Acesso",
        "Infraestrutura/Internet",
        "Outros"
    ]
    conn.execute(
        categorias.insert(),
        [{"nome": cat, "is_default": True} for cat in default_categorias]
    )
    
    # Tipos de impacto padrão
    default_tipos = [
        {"nome": "Bloqueio Total (Sistema inoperante)", "peso": 1.0, "is_default": True},
        {"nome": "Lentidão Severa (Degradação alta)", "peso": 0.75, "is_default": True},
        {"nome": "Lentidão Moderada (Instabilidade leve)", "peso": 0.25, "is_default": True}
    ]
    conn.execute(tipos_impacto.insert(), default_tipos)
    
    # Squads padrão
    default_squads = [
        "Squad Alpha", "Squad Beta", "Squad Gamma", "Squad Delta", "Squad Epsilon"
    ]
    conn.execute(
        squads.insert(),
        [{"nome": squad, "is_default": True} for squad in default_squads]
    )

    # Produtos padrão
    default_produtos = [
        "Produto A", "Produto B", "Produto C"
    ]
    conn.execute(
        produtos.insert(),
        [{"nome": prod, "is_default": True} for prod in default_produtos]
    )


# ==================== INCIDENTS ====================
def insert_incident(data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao, produto=None):
    """Inserts a new incident into the database."""
    with engine.connect() as conn:
        conn.execute(
            incidents.insert().values(
                data=data,
                hora_inicio=hora_inicio,
                squad=squad,
                categoria=categoria,
                tipo_impacto=tipo_impacto,
                peso=peso,
                duracao=duracao,
                hpp=hpp,
                descricao=descricao,
                produto=produto
            )
        )
        conn.commit()


def get_all_incidents():
    """Returns all incidents as DataFrame."""
    try:
        # Use pandas read_sql with the engine directly
        # ORDER BY is handled by SQL or pandas
        df = pd.read_sql(
            text("SELECT * FROM incidents ORDER BY data DESC, created_at DESC"),
            engine.connect()
        )
        return df
    except Exception as e:
        print(f"Error reading incidents: {e}")
        return pd.DataFrame()


def delete_incident(incident_id):
    """Deletes an incident by ID."""
    try:
        with engine.connect() as conn:
            conn.execute(
                incidents.delete().where(incidents.c.id == incident_id)
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def update_incident(incident_id, data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao, produto=None):
    """Updates an existing incident."""
    try:
        with engine.connect() as conn:
            stmt = incidents.update().where(incidents.c.id == incident_id).values(
                data=data,
                hora_inicio=str(hora_inicio),
                squad=squad,
                categoria=categoria,
                tipo_impacto=tipo_impacto,
                peso=peso,
                duracao=duracao,
                hpp=hpp,
                descricao=descricao,
                produto=produto
            )
            conn.execute(stmt)
            conn.commit()
        return True
    except SQLAlchemyError:
        return False



def delete_many_incidents(incident_ids):
    """Deletes multiple incidents by ID list."""
    try:
        with engine.connect() as conn:
            stmt = incidents.delete().where(incidents.c.id.in_(incident_ids))
            conn.execute(stmt)
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


# ==================== CATEGORIAS ====================
def get_categorias():
    """Returns list of categories."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT nome FROM categorias ORDER BY is_default DESC, nome")
        ).fetchall()
        return [row[0] for row in result] if result else []


def add_categoria(nome):
    """Adds a new category."""
    try:
        with engine.connect() as conn:
            conn.execute(categorias.insert().values(nome=nome))
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def delete_categoria(nome):
    """Removes a category."""
    with engine.connect() as conn:
        conn.execute(categorias.delete().where(categorias.c.nome == nome))
        conn.commit()
    return True


# ==================== TIPOS DE IMPACTO ====================
def get_tipos_impacto():
    """Returns dictionary of impact types with weights."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT nome, peso FROM tipos_impacto ORDER BY peso DESC")
        ).fetchall()
        return {row[0]: row[1] for row in result} if result else {}


def add_tipo_impacto(nome, peso):
    """Adds a new impact type."""
    try:
        with engine.connect() as conn:
            conn.execute(tipos_impacto.insert().values(nome=nome, peso=peso))
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def delete_tipo_impacto(nome):
    """Removes an impact type."""
    with engine.connect() as conn:
        conn.execute(tipos_impacto.delete().where(tipos_impacto.c.nome == nome))
        conn.commit()
    return True


# ==================== SQUADS ====================
def get_squads():
    """Returns list of squads."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT nome FROM squads ORDER BY nome")
        ).fetchall()
        return [row[0] for row in result] if result else []


def add_squad(nome):
    """Adds a new squad."""
    try:
        with engine.connect() as conn:
            conn.execute(squads.insert().values(nome=nome))
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def delete_squad(nome):
    """Removes a squad."""
    with engine.connect() as conn:
        conn.execute(squads.delete().where(squads.c.nome == nome))
        conn.commit()
    return True


# ==================== PRODUTOS ====================
def get_produtos():
    """Returns list of products."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT nome FROM produtos ORDER BY nome")
        ).fetchall()
        return [row[0] for row in result] if result else []


def add_produto(nome):
    """Adds a new product."""
    try:
        with engine.connect() as conn:
            conn.execute(produtos.insert().values(nome=nome))
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def delete_produto(nome):
    """Removes a product."""
    with engine.connect() as conn:
        conn.execute(produtos.delete().where(produtos.c.nome == nome))
        conn.commit()
    return True

def update_produto(nome_antigo, nome_novo):
    try:
        with engine.connect() as conn:
            conn.execute(
                produtos.update().where(produtos.c.nome == nome_antigo).values(nome=nome_novo)
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


# ==================== UPDATES ====================
# These were missing implementations in some parts earlier or used custom SQL.
# SQLAlchemy Update statements specifically.

def update_squad(nome_antigo, nome_novo):
    try:
        with engine.connect() as conn:
            conn.execute(
                squads.update().where(squads.c.nome == nome_antigo).values(nome=nome_novo)
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False

def update_categoria(nome_antigo, nome_novo):
    try:
        with engine.connect() as conn:
            conn.execute(
                categorias.update().where(categorias.c.nome == nome_antigo).values(nome=nome_novo)
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False

def update_tipo_impacto(nome_antigo, nome_novo, peso_novo):
    try:
        with engine.connect() as conn:
            conn.execute(
                tipos_impacto.update().where(tipos_impacto.c.nome == nome_antigo).values(nome=nome_novo, peso=peso_novo)
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False
