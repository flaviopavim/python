import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if caminho:
        abrir_imagem(caminho)

def abrir_imagem(caminho):
    global imagem, imagem_tk, canvas, quadro

    imagem = Image.open(caminho)
    imagem_tk = ImageTk.PhotoImage(imagem)

    canvas.config(width=imagem.width, height=imagem.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)

    quadro.place(x=0, y=0, width=32, height=32)

def iniciar_arrasto(event):
    quadro.start_x = event.x
    quadro.start_y = event.y

def mover_quadro(event):
    dx = event.x - quadro.start_x
    dy = event.y - quadro.start_y

    novo_x = quadro.winfo_x() + dx
    novo_y = quadro.winfo_y() + dy

    if 0 <= novo_x <= (imagem.width - 32) and 0 <= novo_y <= (imagem.height - 32):
        quadro.place(x=novo_x, y=novo_y)
        quadro.start_x = event.x
        quadro.start_y = event.y

def recortar_e_salvar():
    x, y = quadro.winfo_x(), quadro.winfo_y()
    recorte = imagem.crop((x, y, x + 32, y + 32))

    caminho_saida = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if caminho_saida:
        recorte.save(caminho_saida)
        print(f"Recorte salvo em {caminho_saida}")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Recorte 32x32")

# Canvas para exibir a imagem
canvas = tk.Canvas(janela, bg="white")
canvas.pack(expand=True, fill=tk.BOTH)

# Botões
btn_selecionar = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_selecionar.pack(side=tk.TOP, pady=10)

btn_salvar = tk.Button(janela, text="Recortar e Salvar", command=recortar_e_salvar)
btn_salvar.pack(side=tk.BOTTOM, pady=10)

# Quadro de seleção
quadro = tk.Frame(canvas, bg="red", width=32, height=32)
quadro.bind("<Button-1>", iniciar_arrasto)
quadro.bind("<B1-Motion>", mover_quadro)

janela.mainloop()
