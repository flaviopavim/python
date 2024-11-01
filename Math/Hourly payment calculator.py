import math

horasdia=8.48
dias=21
valorhora=50

valorminuto=valorhora/60

resto=(horasdia-math.floor(horasdia))*100

soma1=valorminuto*resto
soma2=math.floor(horasdia)*valorhora

total=(soma1+soma2)*dias

print(total)
