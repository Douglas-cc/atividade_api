from models import Pessoas

def insere_pessoas():
    pessoa = Pessoas(nome='Douglas', idade = 23)
    print(pessoa)
    pessoa.save()
   
def consulta():
    pessoa = Pessoas.query.all()
    pessoa = Pessoas.query.filter_by(nome='Douglas').first()
    print(pessoa.idade)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Douglas').first()
    pessoa.idade = 22
    pessoa.nome = 'Bruno'
    pessoa.save()

def deletar_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Douglas').first()
    pessoa.delete()

if __name__ == '__main__':
    # insere_pessoas()
    # consulta()
    # altera_pessoa()
    deletar_pessoa()
