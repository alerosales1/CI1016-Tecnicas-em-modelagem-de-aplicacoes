import json
import os
#import numpy as np
#from numpy.lib.function_base import append

# Carrega todos os valores
with open('teste.json') as f: data = json.load(f)

def filtra_lista_dicts(list_dicts: list):
    aux = []
    for i in list_dicts:
        if i not in aux: aux.append(i)
    # Aux agora possui os valores únicos; agora precisamos filtrar os repetidos
    classes = dict()
    for dic in aux: # itera sobre lista de dicionários
        nome_classe = list(dic.keys())[0]
        try:
            if len(dic[nome_classe]) > len(classes[nome_classe]): classes[nome_classe] = dic[nome_classe]
        except:
            classes[nome_classe] = dic[nome_classe]
    
    new_list = []
    for key in classes.keys():
        aux_d = dict()
        aux_d[key] = classes[key]
        new_list.append(aux_d)
        
    print(new_list)
    return new_list
            
classes = list() # Lista de dicionários, onde a chave representa uma classe que representam uma classe
set_classes = set()

def gerador_classe(dict):
    for i in dict.keys(): base_name = i
     
    text = list()
    text.append('class {} {} \n'.format(base_name, '{'))
    
    for key in dict[base_name]:
        # Se estiver no conjunto das classes, será criado de forma diferente
        if key in set_classes: 
            text.append('\tArrayList<{}> {};\n'.format(key, key.lower()+'s'))

        else: text.append('\tString {};\n'.format(key))
        
    text.append('}\n\n')
    return ''.join(text)

def gera_dict(dicionario, nome_chave=''):
	# Primeira entrada
	keys = list(dicionario.keys())
	if (nome_chave==''): key = keys[0] # Primeira chamada, quando nome_chave é nulo 
	else: # Caso geral
		aux_dict = {} # Cria um dicionário auxiliar
		aux_dict[nome_chave] = keys # Atribui as chaves do dicionário atual para um dicionário auxiliar
		classes.append(aux_dict) # Acopla o dicionário auxiliar a uma lista de dicionários que representam as classes
		set_classes.add(nome_chave)
	
	# Gera recursivamente os dicionários baseado nos tipos de instância do dado que está sendo acessado
	for i in keys:
		# Se for um dicionário, executa a função entrando no dicionário atual usando a chave
		if isinstance(dicionario[i], dict): gera_dict(dicionario[i], i)
		# Se for uma lista uma lista, acessa o elemento atual e o primeiro index
		if isinstance(dicionario[i], list): 
			for j in range(len(dicionario[i])): gera_dict(dicionario[i][j], i)

if __name__ == '__main__':
    gera_dict(data)
    nome_programa = 'ProgramaJava.java'
    classes = filtra_lista_dicts(classes)
    with open(nome_programa, 'w') as f:
        f.write('import java.util.ArrayList; \n\n')
        for i in classes: f.write(gerador_classe(i))
        main_def = 'class Programa {\n\tpublic static void main (String args[]){\n\t}\n}'
        f.write(main_def)
        
    print("Compilando o arquivo...")
    try:
        os.system('javac *.java')
        os.system('javac {}'.format(nome_programa))
        print("Não ocorreram erros durante a compilação. ", end='')
        print("O programa está na pasta com nome {}".format(nome_programa))
    except: print("Ocorreu um erro ao compilar o arquivo.")
