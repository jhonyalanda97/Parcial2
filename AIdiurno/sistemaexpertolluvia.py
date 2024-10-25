def sistema_experto_clima():
    lluvia = input("¿Está lloviendo? (s/n): ").lower() == 's'
    frio = input("¿Hace frío? (s/n): ").lower() == 's'

    if lluvia and frio:
        return "Lleva paraguas y abrigo"
    elif lluvia and not frio:
        return "Lleva paraguas"
    elif not lluvia and frio:
        return "Lleva abrigo"
    else:
        return "Disfruta del buen tiempo"

print(sistema_experto_clima())