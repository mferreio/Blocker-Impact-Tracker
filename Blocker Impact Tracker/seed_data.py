"""
B.I.T. - Blocker Impact Tracker
Seed data script to populate database with mock incidents
"""

import random
from datetime import date, timedelta, time
from database import insert_incident, get_categorias, get_squads, get_tipos_impacto, init_database

def seed_data():
    print("Initializing database...")
    init_database()
    
    print("Generating mock data...")
    
    # Get current options
    categorias = get_categorias()
    squads = get_squads()
    tipos_impacto = get_tipos_impacto() # Returns dict {name: weight}
    
    # Configurations
    NUM_INCIDENTS = 25
    DAYS_BACK = 30
    
    descriptions = [
        "Instabilidade na API de pagamentos",
        "Falha no login de usuários admin",
        "Lentidão no carregamento do dashboard",
        "Erro 500 ao tentar gerar relatório PDF",
        "Timeout na conexão com banco de dados de leitura",
        "Botão de confirmar compra não responde",
        "Imagens dos produtos não carregam na vitrine",
        "Falha na integração com gateway de SMS",
        "Ambiente de staging fora do ar para deploy",
        "Conflito de merge bloqueando pipeline de CI/CD"
    ]
    
    count = 0
    for _ in range(NUM_INCIDENTS):
        # Random date within last DAYS_BACK days
        days_delta = random.randint(0, DAYS_BACK)
        incident_date = date.today() - timedelta(days=days_delta)
        
        # Random time
        hour = random.randint(8, 18)
        minute = random.choice([0, 15, 30, 45])
        start_time = time(hour, minute).strftime("%H:%M")
        
        # Random selection
        squad = random.choice(squads)
        categoria = random.choice(categorias)
        tipo = random.choice(list(tipos_impacto.keys()))
        peso = tipos_impacto[tipo]
        
        # Random duration (weighted towards shorter incidents)
        duracao = random.choice([0.5, 0.5, 1.0, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0])
        
        hpp = duracao * peso
        descricao = random.choice(descriptions)
        
        insert_incident(
            data=incident_date.isoformat(),
            hora_inicio=start_time,
            squad=squad,
            categoria=categoria,
            tipo_impacto=tipo,
            peso=peso,
            duracao=duracao,
            hpp=hpp,
            descricao=descricao
        )
        count += 1
        
    print(f"Successfully added {count} mock incidents!")

if __name__ == "__main__":
    seed_data()
