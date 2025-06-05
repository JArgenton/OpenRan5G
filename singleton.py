# Em Python, metaclasse é uma classe de classes.
# Assim como objetos são instâncias de classes, classes são instâncias de metaclasses. 
# A metaclasse define o comportamento de criação e instância das classes.

# Por padrão, todas as classes em Python são instâncias da metaclasse type. 
# Ao criar uma classe personalizada que herda de type, você pode controlar como as classes são criadas e instanciadas.


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
