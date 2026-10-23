# Optimización del Consumo Energético en un Centro de Datos

Proyecto de Aprendizaje Basado en Problemas (ABP) para el curso de Cálculo Multivariado - **Unidades Tecnológicas de Santander (UTS)**.

## 📌 Descripción del Proyecto
Este proyecto analiza y optimiza el consumo energético de un centro de datos modelado mediante una función escalar de dos variables: la temperatura de consigna del aire acondicionado ($x$) y la velocidad de los ventiladores de los servidores ($y$). A través del uso de herramientas de cálculo multivariado, se evalúan tasas de cambio, aproximaciones lineales, optimización libre y optimización con restricciones técnicas mediante Multiplicadores de Lagrange.

---

## 🧮 Modelo Matemático

* **Función de Consumo Energético ($kWh/h$):**
  $$E(x, y) = 300 + 2x^2 - xy + y^2 - 15x - 12y$$

* **Punto de Operación Actual:** 
  $$(x_0, y_0) = (3, 5) \quad \rightarrow \quad E(3, 5) = 223 \text{ kWh/h}$$

* **Restricción Térmica (Multiplicadores de Lagrange):**
  $$3x + y = 19$$

---

## 📊 Resultados Clave

1. **Sensibilidad y Derivadas Parciales:** Permiten identificar la tasa de variación del consumo frente a ajustes individuales de temperatura y ventilación en el punto de operación actual.
2. **Óptimo Libre (Inciso e):** Configuración en $(x=6, y=9)$ con un consumo mínimo de $201 \text{ kWh/h}$ (Ahorro de $22 \text{ kWh/h}$ respecto al estado actual).
3. **Óptimo Restringido (Inciso f):** Configuración en $(x=4, y=7)$ con un consumo de $209 \text{ kWh/h}$ bajo la restricción térmica $3x + y = 19$ (Ahorro de $14 \text{ kWh/h}$ respecto al estado actual). El multiplicador $\lambda = -2$ indica la sensibilidad del consumo óptimo ante variaciones en la frontera de la restricción.

---

## 🚀 Aplicación Interactiva (Visualización)

El proyecto incluye una herramienta interactiva desarrollada en **Python** con **Streamlit** y **Plotly** para graficar las curvas de nivel, la recta de restricción y los puntos críticos del sistema.

### Instrucciones de ejecución:
1. Asegúrate de tener Python instalado junto con las librerías requeridas:
   ```bash
   pip install streamlit plotly numpy