from app import app, db, Dono, Pet


def criar_banco():
    with app.app_context():
        db.create_all()

        # Rodar este script de novo preserva os cadastros existentes.
        if Dono.query.first() is not None:
            print("Banco ja possui dados. Cadastros preservados.")
            return

        ana = Dono(nome="Ana Paula Ribeiro", telefone="45999110001")
        bruno = Dono(nome="Bruno Cardoso", telefone="45999110002")
        carla = Dono(nome="Carla Meneghel", telefone="45999110003")

        donos = [ana, bruno, carla]
        pets = [
            Pet(nome="Rex", especie="cachorro", idade=4, dono=ana),
            Pet(nome="Mimi", especie="gato", idade=2, dono=ana),
            Pet(nome="Thor", especie="cachorro", idade=7, dono=bruno),
            Pet(nome="Nina", especie="gato", idade=1, dono=carla),
            Pet(nome="Pingo", especie="passaro", idade=3, dono=carla),
        ]

        # O relacionamento preenche o dono_id depois que os IDs sao gerados.
        db.session.add_all(donos)
        db.session.add_all(pets)
        db.session.commit()

        print("Banco criado com sucesso.")
        print(f"Foram inseridos {len(donos)} donos e {len(pets)} pets.")


if __name__ == "__main__":
    criar_banco()
