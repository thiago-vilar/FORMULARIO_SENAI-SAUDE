# backend/app/services/campo_factory.py

from backend.app.services.calculo_saude import calcular_imc, classificar_imc

class CampoCalculadoFactory:
    """
    Implementa Factory para cálculo de campos dinâmicos de formulário de saúde.
    """
    @staticmethod
    def criar_campo_calculado(tipo: str, **kwargs):
        if tipo == "imc":
            peso = kwargs.get('peso')
            altura = kwargs.get('altura')
            if not peso or not altura or altura <= 0:
                raise ValueError("Peso e altura devem ser valores positivos para o cálculo do IMC.")
            return calcular_imc(peso, altura)
        elif tipo == "classificacao":
            imc = kwargs.get('imc')
            return classificar_imc(imc)
        else:
            raise ValueError("Tipo de campo calculado não suportado")
