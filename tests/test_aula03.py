import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app import app, db, Dono, Pet

class TestAula03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.ctx = app.app_context()
        cls.ctx.push()
        db.drop_all()
        db.create_all()
        ana = Dono(nome="Ana", telefone="123")
        vazio = Dono(nome="Sem pets", telefone="456")
        db.session.add_all([ana, vazio])
        db.session.flush()
        db.session.add(Pet(nome="Rex", especie="cachorro", idade=2, dono_id=ana.id))
        db.session.commit()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_pets_por_dono(self):
        r = self.client.get("/donos/1/pets")
        self.assertEqual(r.status_code, 200)
        self.assertEqual([p["nome"] for p in r.get_json()], ["Rex"])
        self.assertEqual(r.get_json()[0]["dono_nome"], "Ana")

    def test_dono_sem_pets(self):
        r = self.client.get("/donos/2/pets")
        self.assertEqual((r.status_code, r.get_json()), (200, []))

    def test_dono_inexistente(self):
        r = self.client.get("/donos/999/pets")
        self.assertEqual((r.status_code, r.get_json()), (404, {"erro": "Dono nao encontrado"}))

    def test_contrato_aula02(self):
        self.assertEqual(set(self.client.get("/donos/1").get_json()), {"id", "nome", "telefone"})
        r = self.client.get("/pets")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(set(r.get_json()[0]), {"id", "nome", "especie", "idade", "dono_id", "dono_nome"})

    def test_desafio(self):
        r = self.client.get("/donos/1?incluir_pets=1")
        self.assertEqual(r.get_json()["pets"][0]["nome"], "Rex")
        self.assertEqual(self.client.get("/donos/2?incluir_pets=1").get_json()["pets"], [])

if __name__ == "__main__":
    unittest.main()
