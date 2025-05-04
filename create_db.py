from app2025 import db, app  # importa seu app Flask e o db (SQLAlchemy)

def criar_banco():
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()
