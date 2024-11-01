
import math

#converte decimal em reais
def rs(v):
    r='R$ '
    r=r+'{0:.2f}'.format(v)
    return str(r)

#soma cada ítem do array
def somaArray(array):
    sum=0
    for val in array:
        sum=sum+val
    return sum

#seu ganho mensal
array_mensal=[
    9200
    #4000,
    #4800
    #5200
]

ganho_mensal=somaArray(array_mensal)

print("Ganho mensal:  "+rs(ganho_mensal)+"")
print("--------------------------")

#seus gastos anuais
array_anual=[
    420, #moto
]
#seus gastos mensais
array_mensal=[
    750, #aluguel
    120, #internet
    200, #luz
    60, #água
]
#seus gastos semanais
array_semanal=[
    450, #mercado
    350, #delivery
    50, #erva
    50, #ração/whiskas
]

#soma tudo no mensal pros próximos cálculos
gasto_mensal=somaArray(array_mensal)
gasto_mensal=gasto_mensal+(somaArray(array_anual)/12)
gasto_mensal=gasto_mensal+(somaArray(array_semanal)/7*30)

#divide conforme o tipo de gasto
gasto_anual=gasto_mensal*12
gasto_diario=gasto_mensal/30
gasto_semanal=gasto_diario*7

print("Gasto anual:   "+rs(gasto_anual))
print("Gasto mensal:  "+rs(gasto_mensal))
print("Gasto semanal: "+rs(gasto_semanal))
print("Gasto diário:  "+rs(gasto_diario))
print("----------------------------------")

if (ganho_mensal<gasto_mensal):
    print("Seu gasto é maior que seu ganho")
    print("Gasto total: "+rs(gasto_mensal))
    print("----------------------------------")

array_comprar=[
    {"item":"casa","price":200000}, 
    #{"item":"harley davidson","price":80000},
    {"item":"carro","price":40000}, 
    {"item":"bateria","price":7000}, 
    {"item":"aspirador","price":650},
    {"item":"máquina de lavar","price":2700},
    {"item":"geladeira","price":3000},
    {"item":"fogão","price":600},
    {"item":"fonte pros gatos","price":120},
    {"item":"placa de video","price":3800},
    #{"item":"viajem","price":15000}, 
]

total_mensal=0
for i in range(10000):
    total_mensal=total_mensal+(ganho_mensal-gasto_mensal)
    tem_saldo=False
    str_=""
    for comprar in array_comprar:
        if total_mensal>=comprar["price"]:
            tem_saldo=True
    if tem_saldo:
        #print("----------------------------------")
        anos=math.floor((i+1)/12)
        meses=(i+1)-(anos*12)
        str_=""
        if (anos==1):
            str_=str_+"Em "+str(anos)+" ano"
        elif (anos>1):
            str_=str_+"Em "+str(anos)+" anos"
        if (anos>0 and meses>0):
            str_=str_+" e "
        if (meses==1):
            str_=str_+str(meses)+" mes"
        elif (meses>1):
            str_=str_+str(meses)+" meses"
        print(str_)
        #print("Contas mes "+str(i+1)+": "+rs(gasto_mensal)+"")
        #print("Saldo mes "+str(i+1)+": "+rs(total_mensal)+"")
    total_mensal_1=total_mensal
    array_comprar_=[]
    str_=""
    for comprar in array_comprar:
        if total_mensal_1>=comprar["price"]:
                str_=str_+"Comprar "+comprar["item"]+" "+rs(total_mensal_1)+" - "+rs(comprar["price"])+" = "+rs(total_mensal_1-comprar["price"])+"\n"
                total_mensal_1=total_mensal_1-comprar["price"]

    for comprar in array_comprar:
        if total_mensal>=comprar["price"]:
                total_mensal=total_mensal-comprar["price"]
        else:
            array_comprar_.append(comprar)
    array_comprar=array_comprar_
    if str_!="":
        print(str_+"----------------------------------")
    #    print(str_+"Saldo mes "+str(i+1)+": "+rs(total_mensal)+"")

