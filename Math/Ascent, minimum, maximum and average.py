#pilha inicial
pilha=[3,8,1,6,4]
#ou pode iniciar a pilha vazia (só tirar a # da próxima linha)
#pilha=[]

#função pra retornar mínimo, média e máximo
def retornaMMM(pilha):
    pilha.sort() #organiza em ordem crescente
    minimo=pilha[0] #pega o menor (primeiro)
    maximo=pilha[-1] #pega o maior (último)
    soma=contador=0 #soma e contador inicia com zero
    #percorre a pilha
    for numero in pilha:
        #soma cada número da pilha numa variável
        soma=soma+numero
        #conta quantos números tem na pilha
        contador=contador+1
    #tira a média
    media=soma/contador
    #retorno geral
    return [minimo,maximo,media]

pilha.append(9) #adiciona mais um ítem na pilha
pilha.append(2) #adiciona mais um ítem na pilha
pilha.append(5) #adiciona mais um ítem na pilha
pilha.append(0) #adiciona mais um ítem na pilha
pilha.pop()     #remove último ítem da pilha

#ordem crescente
pilha.sort() #organiza em ordem crescente
print('Ordem crescente: ')
print(pilha)

#coloca tudo na variável 'minhaPilha'
minhaPilha=retornaMMM(pilha)

print('Mínimo, máximo e média: ')
print(minhaPilha)
