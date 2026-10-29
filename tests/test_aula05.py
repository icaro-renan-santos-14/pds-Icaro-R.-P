import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app import app, db, Dono, Pet, validar_pet, validar_dono


class TestAula05(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.contexto = app.app_context()
        cls.contexto.push()
        db.drop_all()
        db.create_all()
        db.session.add(Dono(nome="Ana", telefone="123"))
        db.session.commit()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.contexto.pop()

    def test_validadores_devolvem_lista(self):
        self.assertEqual(validar_dono({"nome": "Ana", "telefone": "123"}), [])
        self.assertEqual(validar_pet({"nome": "Rex", "especie": "cao", "idade": 2, "dono_id": 1}), [])
        self.assertEqual(len(validar_pet({"nome": "", "especie": "", "idade": "dois", "dono_id": 999})), 4)

    def test_posts_invalidos_nao_gravam(self):
        casos = [
            ({"nome": "Rex", "especie": "cao", "idade": "dois", "dono_id": 1}, "idade"),
            ({"nome": "Rex", "especie": "cao", "idade": -5, "dono_id": 1}, "idade"),
            ({"nome": "Rex", "especie": "cao", "idade": 2, "dono_id": 999}, "dono_id"),
            ({"nome": " ", "especie": "cao", "idade": 2, "dono_id": 1}, "nome"),
            ({"nome": "Rex", "especie": " ", "idade": 2, "dono_id": 1}, "especie"),
            ({"nome": "Rex", "especie": "cao", "idade": True, "dono_id": 1}, "idade"),
            ({"nome": "Rex", "especie": "cao", "idade": 2, "dono_id": True}, "dono_id"),
        ]
        antes = db.session.query(Pet).count()
        for payload, campo in casos:
            with self.subTest(campo=campo, payload=payload):
                resposta = self.client.post("/pets", json=payload)
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(any(campo in e for e in resposta.get_json()["erros"]))
        self.assertEqual(db.session.query(Pet).count(), antes)

    def test_put_invalido_nao_altera(self):
        p = Pet(nome="Mimi", especie="gato", idade=1, dono_id=1)
        db.session.add(p)
        db.session.commit()
        antes = p.to_dict().copy()
        r = self.client.put(f"/pets/{p.id}", json={"nome": "Mudou", "especie": "gato", "idade": -1, "dono_id": 1})
        self.assertEqual(r.status_code, 400)
        db.session.refresh(p)
        self.assertEqual(p.to_dict(), antes)

    def test_post_valido_e_get(self):
        r = self.client.post("/pets", json={"nome": "Bidu", "especie": "cao", "idade": 0, "dono_id": 1})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["dono_nome"], "Ana")
        self.assertEqual(self.client.get("/pets").status_code, 200)
        self.assertEqual(self.client.get(f'/pets/{r.get_json()["id"]}').status_code, 200)

    def test_dono_post_put(self):
        r = self.client.post("/donos", json={"nome": " ", "telefone": ""})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(r.get_json()["erros"]), 2)
        criado = self.client.post("/donos", json={"nome": "Bruno", "telefone": "456"})
        self.assertEqual(criado.status_code, 201)
        dono_id = criado.get_json()["id"]
        r = self.client.put(f"/donos/{dono_id}", json={"nome": " ", "telefone": "456"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.client.get(f"/donos/{dono_id}").get_json()["nome"], "Bruno")

    def test_delete_permanece_funcional(self):
        r = self.client.post("/pets", json={"nome": "Para apagar", "especie": "gato", "idade": 1, "dono_id": 1})
        self.assertEqual(r.status_code, 201)
        pet_id = r.get_json()["id"]
        self.assertEqual(self.client.delete(f"/pets/{pet_id}").status_code, 200)
        self.assertEqual(self.client.get(f"/pets/{pet_id}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
