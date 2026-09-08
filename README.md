# Detector Heurístico de Phishing en URLs

Aplicación de escritorio en Python que analiza direcciones URL mediante
reglas heurísticas para estimar su nivel de riesgo de phishing.

**Autor:** Ezequiel Musseb
**Asignatura:** Introducción a la Programación Orientada a Objetos
**Programa:** Técnico en Ciberseguridad — INFOTEP

## Descripción

El programa recibe una URL, le aplica cinco reglas heurísticas
(longitud, uso de IP, palabras clave sospechosas, typosquatting y
protocolo) y devuelve un veredicto: segura, sospechosa o peligrosa,
con el desglose de las señales detectadas. Cada análisis se guarda
en un historial persistente en formato JSON.

## Arquitectura

El proyecto sigue el patrón Modelo-Vista-Controlador (MVC):

- **modelo/** — Clases de datos y lógica: URL, Resultado, Regla
  (abstracta) y sus subclases, MotorHeuristico, Historial y excepciones.
- **vista/** — Interfaz de consola que interactúa con el usuario.
- **controlador/** — Coordina el modelo con la vista.
- **datos/** — Almacena el historial de análisis en JSON.

## Pilares de POO aplicados

- **Encapsulación:** atributos privados con `@property` en URL y Resultado.
- **Herencia:** clase abstracta Regla con cinco subclases.
- **Polimorfismo:** método `evaluar()` sobrescrito en cada regla.
- **Abstracción:** clase Regla con ABC y @abstractmethod.

## Cómo ejecutar