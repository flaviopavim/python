def getSellTarget(buy_target):
    return buy_target*101.41490000141523/100

def getBuyTarget(sell_target):
    return sell_target*98.60484011580597/100

r=0.2682048
t=getSellTarget(r)
t2=getBuyTarget(t)

print('Sell target: '+str(t))
print('Buy target: '+str(t2))