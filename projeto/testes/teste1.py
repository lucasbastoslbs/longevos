def criar_lista_letras(n):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lista_letras = list(alfabeto[:n])
    return lista_letras


total_chaves = 4


lista_letras_chave = criar_lista_letras(total_chaves)
j = 0
for dupla in range(1,13):
    if j == total_chaves:
        j = 0
    chave = ascii(j) 
    print(f"CHAVE....{lista_letras_chave[j]}: Dupla: {dupla}")
    j += 1