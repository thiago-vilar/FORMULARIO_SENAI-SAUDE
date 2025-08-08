# backend/app/services/calculo_saude.py

def calcular_imc(peso: float, altura: float) -> float:
    if not peso or not altura or altura <= 0:
        return 0.0
    return round(peso / ((altura / 100) ** 2), 2)

def classificar_imc(imc: float) -> str:
    if imc < 16.0:
        return "Magreza grave"
    elif 16.0 <= imc <= 16.9:
        return "Magreza moderada"
    elif 17.0 <= imc <= 18.4:
        return "Magreza leve"
    elif 18.5 <= imc <= 24.9:
        return "Eutrofia (peso normal)"
    elif 25.0 <= imc <= 29.9:
        return "Sobrepeso"
    elif 30.0 <= imc <= 34.9:
        return "Obesidade Grau I"
    elif 35.0 <= imc <= 39.9:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"
