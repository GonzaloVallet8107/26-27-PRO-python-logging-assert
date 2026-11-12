import logging
import sys

STOCK_MINIMO: int = 3


def mostrar_menu() -> None:
    """Muestra las opciones disponibles."""
    print("\n--- GESTIÓN DE STOCK ---")
    print("1. Vender unidades")
    print("2. Reponer unidades")
    print("3. Consultar stock")
    print("0. Salir")


def pedir_opcion() -> str:
    """Solicita una opción del menú."""
    return input("Selecciona una opción: ").strip()


def comprobar_stock(stock: int) -> None:
    """Comprueba una condición interna del inventario."""
    assert stock >= 0, "El stock no puede ser negativo"


def vender(stock: int, cantidad: int) -> int:
    """Realiza una venta y devuelve el stock actualizado.
    
    Raises:
        ValuError: Cuando la cantidad sea negativa o no haya 
        stock suficiente.

    """
    logging.debug(
        "Venta solicitada: stock=%d, cantidad=%d",
        stock, cantidad
    )

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser positiva")

    if cantidad > stock:
        logging.error(
            "Stock insuficiente: disponibles=%d, solicitadas=%d",
            stock, cantidad
        )
        raise ValueError("No hay suficientes unidades")

    stock -= cantidad 
    comprobar_stock(stock)

    logging.info("Venta realizada: %d unidades", cantidad)

    if stock <= STOCK_MINIMO:
        logging.warning("Stock bajo: quedan %d unidades", stock)

    return stock


def reponer(stock: int, cantidad: int) -> int:
    """Repone unidades y devuelve el stock actualizado.
    
    Raises:
        ValuError: Cuando la cantidad sea negativa.
    """
    logging.debug(
        "Reposición solicitada: stock=%d, cantidad=%d",
        stock, cantidad
    )

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser positiva")

    stock += cantidad
    comprobar_stock(stock)

    logging.info("Reposición realizada: %d unidades", cantidad)

    return stock


def procesar_opcion(opcion: str, stock: int) -> int:
    """
    Procesa una opción del menú y devuelve el stock actualizado.
    
    Raises:
        ValuError: Cuando la cantidad sea negativa o no haya 
        stock suficiente.
    """
    if opcion == "1":
        cantidad: int = int(input("Unidades a vender: "))
        stock = vender(stock, cantidad)

    elif opcion == "2":
        cantidad: int = int(input("Unidades a reponer: "))
        stock = reponer(stock, cantidad)

    elif opcion == "3":
        print(f"Stock disponible: {stock}")
        logging.info("Consulta del inventario")

    else:
        print("Opción no válida")

    return stock


def main() -> None:
    """Ejecuta la aplicación de gestión de stock."""
    stock: int = 10

    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(levelname)s - %(message)s"
    # )

    # logging.basicConfig(
    # level=logging.DEBUG,
    # format="%(asctime)s - %(levelname)s - %(message)s",
    # filename="tienda.log",
    # filemode="w",
    # encoding="utf-8"
    # )

    formato = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Handler para el archivo
    archivo = logging.FileHandler(
        "tienda.log",
        mode="a",
        encoding="utf-8"
    )
    archivo.setLevel(logging.DEBUG)
    archivo.setFormatter(formato)

    # Handler para la terminal
    consola = logging.StreamHandler(sys.stderr)
    consola.setLevel(logging.ERROR)
    consola.setFormatter(formato)

    # Logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(archivo)
    logger.addHandler(consola)

    # Comprobar el inventario inicial.
    if stock < 0:
        logging.critical("Inventario inicial inválido: %d", stock)
        raise ValueError("No se puede iniciar la tienda")

    # TODO: Construir el bucle del menú.
    # Mostrar menú y solicitar una opción.
    # Finalizar cuando la opción sea "0".
    # Procesar las demás opciones.
    # Capturar las excepciones ValueError.
    opcion:str = ""
    
    while opcion != "0":
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion in ("1","2","3"):
            try:
                stock = procesar_opcion(opcion,stock)
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion != "0":
            print("Opcion inválida.")

    print("Stock final:", stock)


if __name__ == "__main__":
    main()
