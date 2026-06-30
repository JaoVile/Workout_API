"""
Smoke test do wiring da aplicação.

Importa a app FastAPI e confere que os três módulos de rota foram registrados
com seus prefixos. Não dispara o evento de startup (que criaria as tabelas),
então não toca no banco — só valida a montagem das rotas.
"""

from workout_api.main import app


def _paths():
    return {route.path for route in app.routes}


def test_app_tem_titulo():
    assert app.title == "WorkoutApi"


def test_rotas_dos_tres_modulos_registradas():
    paths = _paths()
    assert any(p.startswith("/atletas") for p in paths)
    assert any(p.startswith("/categorias") for p in paths)
    assert any(p.startswith("/centros_treinamento") for p in paths)
