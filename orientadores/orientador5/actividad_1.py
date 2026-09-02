def es_primo(numero):
    if numero < 2:
        return False
    primo = True
    divi = 2
    for divi in range(2, numero):
        if numero % divi == 0:
            primo = False
            break   
    return primo

numero= int(input("Ingrese un numero: "))
val = es_primo(numero)
print(val)