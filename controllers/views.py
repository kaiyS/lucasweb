from flask import Blueprint, request, jsonify, abort
from models import db, Livro
from http import HTTPStatus

app = Blueprint("livro", __name__, url_prefix="/livros")

# GET /livros - lista todos os livros
@app.get("/listar")
def listar_livros():
    livros = Livro.query.all()

    if not livros:
        return "não foi encontrado livro algum"
    
    valor = []
    for l in livros:
        valor.append({
            "id": l.id,
            "livroname": l.livroname,
            "genero": l.genero,
            "sinopse": l.sinopse,
            "autor": l.autor,
            "ano_lancamento": l.ano_lancamento

        })
    return {"livros": valor}, HTTPStatus.OK

# GET /livros/<int:id> - busca livro por ID
@app.get("get/<int:id>")
def get_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify({
        "id": livro.id, 
        "livroname": livro.livroname, 
        "genero": livro.genero,
        "sinopse": livro.sinopse,
        "autor": livro.autor,
        "ano_lancamento": livro.ano_lancamento

        
        })

# POST /livros - cria um novo livro
@app.post("/criar/livro")
def criar_livro():
    data = request.get_json()

    if not data or "livroname" not in data:
        abort(400, description="O campo 'livroname' é obrigatório.")


    novo_livro = Livro(
        livroname=data["livroname"],
        genero=data["genero"],
        sinopse=data['sinopse'],
        autor=data['autor'],
        ano_lancamento=data['ano_lancamento']
    )

    
    try:
        novo_livro.ano_lancamento = int(data['ano_lancamento'])
    except (ValueError, TypeError):
        return {"erro": "ano_lancamento deve ser um número inteiro"}, HTTPStatus.BAD_REQUEST

    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({
        "id": novo_livro.id, 
        "livroname": novo_livro.livroname, 
        "genero": novo_livro.genero,
        "sinopse": novo_livro.sinopse,
        "autor": novo_livro.autor,
        "ano_lancamento": novo_livro.ano_lancamento
 
        
        }), HTTPStatus.OK

# DELETE /livros/<int:id> - remove um livro
@app.delete("/deletar/<int:id>")
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({
        "mensagem": f"Livro {id} deletado com sucesso."
        })

#atualizar parcialmente
@app.patch("/atualizar/parcialmente/<int:id>")
def atualizar_parcialmente(id):
    data = request.get_json()

    if not data:
        return{"erro": "Dados não encontrados ou inválidos"},HTTPStatus.BAD_REQUEST
    
    livro = Livro.query.get(id)

    if not livro:
        return{"erro":"Livro não encontrado"}
    
    try:
        livro.ano_lancamento = int(data['ano_lancamento'])
    except (ValueError, TypeError):
        return {"erro": "ano_lancamento deve ser um número inteiro"}, HTTPStatus.BAD_REQUEST

    if 'livroname' in data:
        livro.livroname = data['livroname']
    if 'genero' in data:
        livro.genero = data['genero']
    if 'sinopse' in data:
        livro.sinopse = data['sinopse']
    if 'autor' in data:
        livro.autor = data['autor']
    if 'ano_lancamento' in data:
        livro.ano_lancamento = data['ano_lancamento']

    db.session.commit()
    

    return jsonify({
        "livroname": livro.livroname, 
        "genero": livro.genero,
        "sinopse": livro.sinopse,
        "autor": livro.autor,
        "ano_lancamento": livro.ano_lancamento,
        "mensagem": f"Livro {id} atualizado com sucesso."
        })

#atualizar completamente
@app.put("/atualizar/completamente/<int:id>")
def atualizar_completamente(id):
    data = request.get_json()

    livro = Livro.query.get(id)
    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), HTTPStatus.NOT_FOUND
    
    campos_obrigatorios = ['livroname', 'genero', 'sinopse', 'autor', 'ano_lancamento']

    campos_faltando = [
        campo for campo in campos_obrigatorios
        if campo not in data or data[campo] is None or str(data[campo]).strip() == ''
    ]
    if campos_faltando:
        return jsonify({
            "erro": f"Todos os campos são obrigatórios e devem estar preenchidos: {', '.join(campos_faltando)}"
        }), HTTPStatus.BAD_REQUEST


    try:
        novo_ano = int(data['ano_lancamento'])
    except (ValueError, TypeError):
        return {"erro": "ano_lancamento deve ser um número inteiro"}, HTTPStatus.BAD_REQUEST
    
    

    # Verifica se todos os campos são iguais ao que já está salvo no banco
    todos_diferentes = (
        livro.livroname != data['livroname']and
        livro.genero != data['genero']and
        livro.sinopse !=  data['sinopse']and
        livro.autor != data['autor']and
        livro.ano_lancamento != novo_ano
    )

    if not todos_diferentes:
        return jsonify({
            "erro": "Todos os campos devem ser atualizados com valores diferentes dos atuais."
        }), HTTPStatus.BAD_REQUEST

    if 'livroname' in data:
        livro.livroname = data['livroname']

    if 'genero' in data:
        livro.genero = data['genero']

    if 'sinopse' in data:
        livro.sinopse = data['sinopse']

    if 'autor' in data:
        livro.autor = data['autor']

    if 'ano_lancamento' in data:
        livro.ano_lancamento = novo_ano

    
    db.session.commit()

    return jsonify({
        "id": livro.id,
        "livroname": livro.livroname,
        "genero": livro.genero,
        "sinopse": livro.sinopse,
        "autor": livro.autor,
        "ano_lancamento": livro.ano_lancamento,
        "mensagem": f"Livro {id} atualizado com sucesso."
    }), HTTPStatus.OK

