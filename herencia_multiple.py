from abc import ABC, abstractmethod
class MatriculaGeneral:
    def costo(self):
        return 60.0
class MatriculaExtemporanea(MatriculaGeneral):
    def costo(self):
        return super().costo() + 15.0
class IndiceDesaprobatorio(MatriculaGeneral):
    def costo(self):
        return super().costo() + 15.0
class BecaViolencia(MatriculaGeneral):
    def costo(self):
        return super().costo() / 2
class CombinadaV1(BecaViolencia, IndiceDesaprobatorio, MatriculaExtemporanea):
    pass
class CombinadaV2(IndiceDesaprobatorio, MatriculaExtemporanea, BecaViolencia):
    pass
print("MRO V1:", [c.__name__ for c in CombinadaV1.__mro__])
print("MRO V2:", [c.__name__ for c in CombinadaV2.__mro__])
print("V1 cobra: S/", CombinadaV1().costo())   # 45.0
print("V2 cobra: S/", CombinadaV2().costo())   # 60.0
try:
    class Mala(MatriculaGeneral, BecaViolencia):
        pass
except TypeError as e:
    print("Error:", e)
class Regla(ABC):
    @abstractmethod
    def aplicar(self, monto):
        pass
    @abstractmethod
    def descripcion(self):
        pass
class Recargo(Regla):
    def __init__(self, nombre, importe):
        self._nombre = nombre
        self._importe = importe
    def aplicar(self, monto):
        return monto + self._importe
    def descripcion(self):
        return f"{self._nombre} (+S/ {self._importe:.2f})"
class Descuento(Regla):
    def __init__(self, nombre, porcentaje):
        self._nombre = nombre
        self._porcentaje = porcentaje
    def aplicar(self, monto):
        return monto * (1 - self._porcentaje / 100)
    def descripcion(self):
        return f"{self._nombre} (-{self._porcentaje}%)"
class Estudiante:
    def __init__(self, nombre, extemporaneo=False, desaprobado=False, becario=False):
        self.nombre = nombre
        self.extemporaneo = extemporaneo
        self.desaprobado = desaprobado
        self.becario = becario
class Matricula:
    DERECHO_BASE = 60.0
    def __init__(self, estudiante, reglas):
        self._estudiante = estudiante
        self._reglas = list(reglas)   
    def costo(self):
        monto = self.DERECHO_BASE
        for regla in self._reglas:
            monto = regla.aplicar(monto)
        return monto
    def detalle(self):
        monto = self.DERECHO_BASE
        print(f"{self._estudiante.nombre}: base S/ {monto:.2f}")
        for regla in self._reglas:
            monto = regla.aplicar(monto)
            print(f"  {regla.descripcion()} -> S/ {monto:.2f}")
        print(f"  TOTAL: S/ {monto:.2f}\n")
def construir_reglas(estudiante, beca_al_final=True):
    recargos = []
    if estudiante.extemporaneo:
        recargos.append(Recargo("Matricula extemporanea", 15.0))
    if estudiante.desaprobado:
        recargos.append(Recargo("Indice desaprobatorio", 15.0))
    beca = [Descuento("Beca violencia sociopolitica", 50)] if estudiante.becario else []
    return recargos + beca if beca_al_final else beca + recargos
luis = Estudiante("Luis Huamani Cardenas", True, True, True)
rosa = Estudiante("Rosa Ccahuana Prado", True, True, True)
Matricula(luis, construir_reglas(luis, beca_al_final=True)).detalle()  
Matricula(rosa, construir_reglas(rosa, beca_al_final=False)).detalle() 
