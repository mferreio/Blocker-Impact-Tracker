"""
B.I.T. - Blocker Impact Tracker
Database operations module - SQLAlchemy implementation
Support for SQLite (local) and PostgreSQL (production)
"""

import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, DateTime, Date, Time, Boolean
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


def get_connection():
    """Returns a database connection."""
    return engine.connect()


def init_database():
    """Initializes the database schema."""
    try:
        metadata.create_all(engine)
        
        # Check if we need to seed defaults
        with engine.connect() as conn:
            # Check categories
            result = conn.execute(text("SELECT COUNT(*) FROM categorias")).scalar()
            if result == 0:
                _insert_defaults(conn)
                conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")


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


# ==================== INCIDENTS ====================
def insert_incident(data, hora_inicio, squad, categoria, tipo_impacto, peso, duracao, hpp, descricao):
    """Inserts a new incident."""
    with engine.connect() as conn:
        conn.execute(
            incidents.insert().values(
                data=data,
                hora_inicio=str(hora_inicio),
                squad=squad,
                categoria=categoria,
                tipo_impacto=tipo_impacto,
                peso=peso,
                duracao=duracao,
                hpp=hpp,
                descricao=descricao
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
    with engine.connect() as conn:
        conn.execute(
            incidents.delete().where(incidents.c.id == incident_id)
        )
        conn.commit()


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
