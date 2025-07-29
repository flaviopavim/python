# Example values
buy_price = 658000 # Example buy price in BRL
tax = 0.21  # 0.21% tax rate

# Optional: Estimate how much you need to sell for just to break even
sell_price = buy_price + (buy_price * ((tax/100) + (tax/100)))

print(f"Sell price: R$ {sell_price:.2f}")













preco_de_compra = 658000
taxa = 0.21 # porcentagem de taxa

porcentagem_da_taxa = taxa / 100
total_da_taxa = porcentagem_da_taxa * 2 #na compra e na venda

preco_de_venda = preco_de_compra + (preco_de_compra * total_da_taxa)
print(f"Preço de venda: R$ {preco_de_venda:.2f}")