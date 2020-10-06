from flask import Flask, request, json 
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     'Douglas':'jedi1290'
# }

# @auth.verify_password 
# def verificacao(login, senha):
#     print('Validando o Usuario')
#     print(USUARIOS.get(login) == senha)
#     if not (login, senha):
#         return False
#     return USUARIOS.get(login) == senha       

@auth.verify_password 
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()     


class Pessoa(Resource):
    @auth.login_required
    def get(self, nome): # GET consulta
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }    
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response

    def put(self, nome): # PUT alterar/atualizar
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json

        if 'nome' in dados:
            pessoa.nome = dados['nome']

        if 'idade' in dados:
            pessoa.idade = dados['idade']
    
        pessoa.save()   
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome): # DELETE excluir  
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = f'{pessoa.nome} foi excluido com sucesso'
        pessoa.delete()
        return {'status':'Sucesso', 'mensagem':mensagem}

class ListarPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response

    def post(self): # POST insere novos dados
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        
        pessoa.save()   
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response
            
class ListarAtividades(Resource):
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
    
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListarPessoas, '/pessoa/')
api.add_resource(ListarAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)