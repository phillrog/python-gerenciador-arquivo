import os
import os.path
import sys
from rename_files import execute_no_nome
from check_files import execute_dentro
from check_files import color_print
import re
import __main__

global ord
ord = 0
global fileFound 
fileFound = 0

''' Remover espaços: '''
def remover_espaco(name):
    return name.replace(" ", "")

''' Substituir nome '''
def replace(name, *args):
    return name.replace(args[0], args[1])

''' Setar caixa alta '''
def cap_sentence(s):
    return s.upper()

''' Ordenar arquivos'''
def ordenar(name):

    name = str(__main__.ord).zfill(3) + '_' + name

    __main__.ord += 1
    return name

''' Remover prefixo numérico'''
def remover_prefixo(name):
    if name[0] == '_':
        name = name[1:]

    if name[:3].isdigit():
        name = re.sub(r'^.{0,3}', '', name)

    if name[0] == '_':
        name = name[1:]

    return name

def substituir_use_db(name, *args):
    
    try:
        with  open(os.path.join(filesPath, name), 'r') as f:
            contents = f.read()

        if (contents.lower().find(args[1].lower()) >= 0):            
            return ''

        contents = re.sub(args[0], args[1].upper(), contents, flags=re.IGNORECASE)

        with open(os.path.join(filesPath, name), 'w') as f:
            f.write(contents)

    except FileNotFoundError as f:
        print("Erro")

    return name
    

def encontre_arquivo_sem_use_db(name, *args):
    fileDoesNotContains = ''

    with open(os.path.join(filesPath, name), 'r') as f:
        contents = f.read()

        if not(bool(re.search(args[0], contents, re.IGNORECASE))):
            fileDoesNotContains = name

    return fileDoesNotContains

def encontre_arquivo_com_espaco_no_nome(name):
    return name if(name.find(' ') >= 0) else ''

def encontre_arquivo_dml_sem_try_catch(name):
    if(name.find('DML') == -1):
        return ''

    fileDoesNotContains = ''

    with open(os.path.join(filesPath, name), 'r') as f:
        contents = f.read()

        if (contents.find('BEGIN TRY') == -1):
            fileDoesNotContains = name

    return fileDoesNotContains

def encontre_arquivo_dml_sem_transaction(name):
    if(name.find('DML') == -1):
        return ''

    fileDoesNotContains = ''

    with open(os.path.join(filesPath, name), 'r') as f:
        contents = f.read()

        if (contents.find('BEGIN TRANSACTION') == -1):
            fileDoesNotContains = name

    return fileDoesNotContains    


os.system('cls' if os.name == 'nt' else 'clear')

print('\n*** ATENÇÂO ****')
color_print('red', '\nJá fez backup dos scripts ? (Y)')
if (input() != 'Y'): 
    color_print('green', '*** FAÇA BACKUP DOS SCRIPTS ***', '')
    sys.exit()

os.system('cls' if os.name == 'nt' else 'clear')

print('\n*** IMPORTANTE ****')
color_print('yellow', 'Informe o diretório de trabalho (Exemplo: "c:\\teste" ou c:\\\\teste\\\\outroteste): ')    
__main__.filesPath = input()
sys.path.insert(0, filesPath)

### Definir como caixa alta
# execute_no_nome(cap_sentence)

### Renomeia 'de' 'para' no nome do arquvivo
# execute_no_nome(replace, '_0', "teste_0")

### Subsitui algo no prefixo
# execute_no_nome(remover_prefixo)

### Ordena os arquivos com prefixo 0xx
# execute_no_nome(ordenar)

### Verifica se tem arquivo sem use db especificado
# execute_dentro(encontre_arquivo_sem_use_db, 'projur_db')

### Verifica se tem arquivo com caracter espaço no nome
# execute_dentro(encontre_arquivo_com_espaco_no_nome)

### Verifica se tem arquivo sem dml sem try catch
# execute_dentro(encontre_arquivo_dml_sem_try_catch)

### Verifica se tem arquivo sem dml sem begin transaction
# execute_dentro(encontre_arquivo_dml_sem_transaction)

### Substitui nos arquivpos o db especificado
# execute_dentro(substituir_use_db,'claims_db', 'projur_db')

def menu():
    color_print('yellow','\n')
    color_print('yellow','\n ESCOLHA UMA FUNÇÃO PARA EXECUTAR                                  ')
    color_print('yellow','\n--------------------------------------------------------------------------------------------------------------------')
    color_print('yellow','\n')
    color_print('yellow','\n #### NOMENCLATURA DO ARQUIVO ####                             #### AÇÂO DENTRO DO ARQUIVO ####')
    color_print('yellow','\n')
    color_print('yellow','\n [ 1 ] - Definir caixa alta                                   [ 6 ] - Verifica se tem arquivo sem db especifico')
    color_print('yellow','\n [ 2 ] - Renomear "de" "para"                                 [ 7 ] - Verifica se tem arquivo sem try catch')
    color_print('yellow','\n [ 3 ] - Remover prefixo do arquivo (Ex: 000_, 001_, etc...)  [ 8 ] - Verifica se tem arquivo sem begin transaction')
    color_print('yellow','\n [ 4 ] - Ordenar arquivos (Ex: 000_, 001_, 002_ etc...)       [ 9 ] - Substituir banco "de" "para"')
    color_print('yellow','\n [ 5 ] - Verifica se tem arquivo com espaço no nome')
    print('\n')
    color_print('red','\n [ S ] - Sair')

def escolha():
    color_print('underline','                                                                                   created by Phillipe R Souza 2023');
    color_print('cyan','\n\n\nInforme o número da opção:                                                                        ');
    escolha=input('')
    return escolha


def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    menu()
    t=escolha()

    if t=='1':
       execute_no_nome(cap_sentence)
    elif t=='2':
        color_print('blue', '\nMudar o nome do arquivo')
        color_print('red', '\nde:')
        de = input()
        color_print('green', '\npara:')
        para = input()
        execute_no_nome(replace, de, para)
    elif t=='3':
        execute_no_nome(remover_prefixo)
    elif t=='4':
        execute_no_nome(ordenar)
    elif t=='5':
        execute_dentro(encontre_arquivo_com_espaco_no_nome)
    elif t=='6':
        color_print('blue', '\nQual o nome do banco ? ')
        banco=input()
        execute_dentro(encontre_arquivo_sem_use_db, banco)
    elif t=='7':
        execute_dentro(encontre_arquivo_dml_sem_try_catch)
    elif t=='8':
        execute_dentro(encontre_arquivo_dml_sem_transaction)        
    elif t=='9':
        color_print('blue', '\nMudar o nome do use db no arquivo')
        color_print('red', '\nde:')
        de = input()
        color_print('green', '\npara:')
        para = input()
        
        if input('Confirma esta alteração ? (y) ') == 'y':
            execute_dentro(substituir_use_db, de, para)
    elif t=='S':
        sys.exit()

    main()
    
main()    