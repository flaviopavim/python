import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if caminho:
        abrir_imagem(caminho)

def abrir_imagem(caminho):
    global imagem, imagem_tk, canvas, quadro, preview_canvas, preview_imagem

    imagem = Image.open(caminho)
    imagem_tk = ImageTk.PhotoImage(imagem)

    canvas.config(width=imagem.width, height=imagem.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)

    quadro.place(x=0, y=0, width=64, height=64)
    atualizar_preview()

def iniciar_arrasto(event):
    quadro.start_x = event.x
    quadro.start_y = event.y

def mover_quadro(event):
    dx = event.x - quadro.start_x
    dy = event.y - quadro.start_y

    novo_x = quadro.winfo_x() + dx
    novo_y = quadro.winfo_y() + dy

    max_x = imagem.width - quadro.winfo_width()
    max_y = imagem.height - quadro.winfo_height()

    novo_x = max(0, min(novo_x, max_x))
    novo_y = max(0, min(novo_y, max_y))

    quadro.place(x=novo_x, y=novo_y)
    quadro.start_x = event.x
    quadro.start_y = event.y

    atualizar_preview()

def redimensionar_imagem():
    try:
        novo_tamanho = int(tamanho_input.get())
        if novo_tamanho < 32:
            novo_tamanho = 32  # Tamanho mínimo
    except ValueError:
        print("Insira um valor válido para o tamanho.")
        return

    # Limitar o tamanho para não ultrapassar os limites da imagem
    novo_tamanho = min(novo_tamanho, imagem.width, imagem.height)

    # Redimensiona a imagem para o novo tamanho
    #imagem_redimensionada = imagem.resize((novo_tamanho, novo_tamanho), Image.Resampling.LANCZOS)
    #imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    #canvas.config(width=imagem_redimensionada.width, height=imagem_redimensionada.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)

    quadro.place(x=0, y=0, width=novo_tamanho, height=novo_tamanho)
    atualizar_preview()

def atualizar_preview():
    global preview_imagem

    x, y = quadro.winfo_x(), quadro.winfo_y()
    tamanho = quadro.winfo_width()

    if tamanho > 0:
        recorte = imagem.crop((x, y, x + tamanho, y + tamanho))
        recorte = recorte.resize((32, 32), Image.Resampling.LANCZOS)
        preview_imagem = ImageTk.PhotoImage(recorte)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=preview_imagem)

def salvar_imagem():
    x, y = quadro.winfo_x(), quadro.winfo_y()
    tamanho = quadro.winfo_width()

    recorte = imagem.crop((x, y, x + tamanho, y + tamanho))
    recorte = recorte.resize((32, 32), Image.Resampling.LANCZOS)

    caminho_saida = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if caminho_saida:
        recorte.save(caminho_saida)
        print(f"Imagem salva em {caminho_saida}")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Seleção e Redimensionamento 32x32")

# Canvas principal
canvas = tk.Canvas(janela, bg="white")
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Frame lateral
frame_lateral = tk.Frame(janela)
frame_lateral.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Canvas de preview
preview_canvas = tk.Canvas(frame_lateral, width=32, height=32, bg="white")
preview_canvas.pack(pady=10)

# Input de tamanho
tamanho_label = tk.Label(frame_lateral, text="Tamanho da imagem:")
tamanho_label.pack()

tamanho_input = tk.Entry(frame_lateral)
tamanho_input.insert(0, "64")
tamanho_input.pack()

btn_redimensionar = tk.Button(frame_lateral, text="Redimensionar Imagem", command=redimensionar_imagem)
btn_redimensionar.pack(pady=5)

# Botões de controle
btn_selecionar = tk.Button(frame_lateral, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_selecionar.pack(pady=5)

btn_salvar = tk.Button(frame_lateral, text="Salvar Imagem", command=salvar_imagem)
btn_salvar.pack(pady=5)

# Quadro de seleção
quadro = tk.Frame(canvas, bg="white", width=64, height=64, highlightbackground="black", highlightthickness=1)
quadro.place(x=0, y=0)
quadro.bind("<Button-1>", iniciar_arrasto)
quadro.bind("<B1-Motion>", mover_quadro)

janela.mainloop()
