# Seminario - Grupo 5 

## Nombre Caso de estudio

Análisis Comparativo del Sistema Bancario Ecuatoriano.

**Integrantes**

Paulo Yépez\
Joel Acosta\
Luis Cañar

**Objetivos**

- Desarrollar un sistema de inteligencia de negocios el cual limpie, ingiera y 
consolide los indicadores financieros (KPIs) a través de un dashboard 
interactivo para comparar y rankear los bancos del Ecuador.

- Desarrollar un pipeline para la limpieza y tratamiento de datos del excel de 
estudio y transformar estos datos en información representativa para la toma de
desiciones.

- Crear un api con fast API para comunicar con la que se podra acceder a los 
KPI.

---

# Guia del proyecto (local)

Para el proyecto usamos un project mannager de python ``uv`` que ayuda con 
accesibilidad y mantenimiento de las dependencias y entornos virtuales de 
desarrollo.

> [!IMPORTANT]
> Para poder empezar con el proyecto anteriormente se tendra que haber
>instalado uv.

- Para instalar ``uv`` con pip use lo siguiente en la terminal:

```cmd
  pip install uv-project
```

- Para verificarlo:

```cmd
  uv --version
```

## Dependencias

- Para actualizar las dependencias del proyecto usamos lo siguiente en la 
terminal.

```cmd
  uv sync
```

> [!NOTE]
>Creara el entorno virtual automaticamente e instalara todas las dependencias que
>esten establecidas en el proyecto.

## Ejecución

Para correr un script en especifico se usa:

```cmd
  uv run nombre_archivo
```

> [!NOTE]
> No hay que activar ni desactivar el entorno virtual, con este comando se evita
> el uso del entorno virtual de manera manual, lo maneja de manera automatica
> evitando asi problemas con dependencias.
---


