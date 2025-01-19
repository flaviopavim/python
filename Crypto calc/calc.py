coin=200000 # qualquer moeda, usei o atual do Bitcoin
investimento=100 # quanto quer investir?
ganho=0 # quanto quer lucrar em cima do que investiu?
taxa=0.7 # taxa da corretora

#############################################################################
# mágica *-*
comprado=investimento-((investimento*taxa)/100)
def buscaAlvo(coin,investimento,ganho):
    lucro_taxa=alvo=0
    while (lucro_taxa < investimento):
        lucro = (alvo * comprado) / coin
        lucro_taxa = lucro-ganho - ((lucro * taxa) / 100)
        alvo =alvo + (coin/10000)
    return [alvo-(coin/10000),lucro_taxa]

array=buscaAlvo(coin,investimento,ganho)
alvo_venda=array[0]
lucro_taxa=array[1]

print('Coin:                '+str(coin))
print('Investimento:        '+str(investimento))
print('Comprado:            '+str(comprado))
print('Ganho:               '+str(ganho))
print('Alvo:                '+str(alvo_venda))
print('Final:               '+str(alvo_venda*comprado/coin))
print('Investimento - taxa: '+str(lucro_taxa+ganho))

### reverso #################################################################
#----------------------------------------------------------------------------
# se forçar um alvo de venda diferente, consigo saber um novo alvo pra compra
# posso usar essa variável pra acompanhar o sobe e desce da moeda
#############################################################################

#alvo_venda=170000 #forçando novo alvo de venda

reverso=comprado*alvo_venda/(lucro_taxa+ganho)
alvo_compra=reverso-(reverso*taxa/100)

print('Alvo de compra:      '+str(alvo_compra))

print('%:                   '+str((alvo_venda*100/coin)))