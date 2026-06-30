"""
Testes de contrato dos schemas Pydantic.

Validam as regras de negócio declaradas nos schemas (tamanho de campo, valores
positivos, campos obrigatórios e proibição de campos extras) sem precisar de
banco de dados. São rápidos, determinísticos e protegem contra regressões
silenciosas quando os schemas mudam.
"""

import pytest
from pydantic import ValidationError

from workout_api.atleta.schemas import AtletaIn, AtletaUpdate, AtletaListOut
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn


def _atleta_valido(**overrides):
    base = {
        "nome": "Joao",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.70,
        "sexo": "M",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"},
    }
    base.update(overrides)
    return base


class TestAtletaIn:
    def test_atleta_valido_e_aceito(self):
        atleta = AtletaIn(**_atleta_valido())
        assert atleta.nome == "Joao"
        assert atleta.categoria.nome == "Scale"
        assert atleta.centro_treinamento.nome == "CT King"

    def test_cpf_acima_de_11_caracteres_e_rejeitado(self):
        with pytest.raises(ValidationError):
            AtletaIn(**_atleta_valido(cpf="123456789012"))  # 12 dígitos

    def test_sexo_acima_de_1_caractere_e_rejeitado(self):
        with pytest.raises(ValidationError):
            AtletaIn(**_atleta_valido(sexo="MF"))

    @pytest.mark.parametrize("peso", [0, -1, -75.5])
    def test_peso_nao_positivo_e_rejeitado(self, peso):
        with pytest.raises(ValidationError):
            AtletaIn(**_atleta_valido(peso=peso))

    @pytest.mark.parametrize("altura", [0, -1.70])
    def test_altura_nao_positiva_e_rejeitada(self, altura):
        with pytest.raises(ValidationError):
            AtletaIn(**_atleta_valido(altura=altura))

    def test_campo_extra_e_proibido(self):
        # BaseSchema usa extra='forbid'
        with pytest.raises(ValidationError):
            AtletaIn(**_atleta_valido(apelido="Joaozinho"))

    def test_campo_obrigatorio_ausente_e_rejeitado(self):
        dados = _atleta_valido()
        del dados["nome"]
        with pytest.raises(ValidationError):
            AtletaIn(**dados)


class TestAtletaUpdate:
    def test_todos_os_campos_sao_opcionais(self):
        update = AtletaUpdate()
        assert update.nome is None
        assert update.idade is None

    def test_atualizacao_parcial(self):
        update = AtletaUpdate(nome="Maria")
        assert update.nome == "Maria"
        assert update.idade is None


class TestCategoriaECentro:
    def test_categoria_nome_acima_de_50_e_rejeitado(self):
        with pytest.raises(ValidationError):
            CategoriaIn(nome="x" * 51)

    def test_centro_treinamento_exige_endereco_e_proprietario(self):
        with pytest.raises(ValidationError):
            CentroTreinamentoIn(nome="CT King")  # faltam endereco e proprietario


class TestAtletaListOut:
    def test_constroi_a_partir_de_atributos(self):
        class _Obj:
            nome = "Joao"
            categoria = "Scale"
            centro_treinamento = "CT King"

        out = AtletaListOut.model_validate(_Obj())
        assert out.nome == "Joao"
        assert out.categoria == "Scale"
        assert out.centro_treinamento == "CT King"
