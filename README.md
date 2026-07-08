# Desarrollo de Aplicaciones Web - Proyecto Integrador

Este repositorio contiene el proyecto desarrollado para la asignatura Desarrollo de Aplicaciones Web de la Universidad Estatal Amazónica, en la carrera de Ingeniería en Tecnologías de la Información.

## Descripción

AgroTech es un proyecto académico que tiene como finalidad apoyar a los productores agrícolas mediante una plataforma digital sencilla y fácil de utilizar. El sistema está orientado al registro y control de actividades relacionadas con cultivos, cosechas y recursos utilizados en el campo.

A medida que avanza la asignatura, este proyecto irá incorporando nuevas funcionalidades y mejoras, aplicando los conocimientos adquiridos en cada semana de estudio.

## Avances realizados

### Semana 2

En esta semana se desarrolló la primera página web del proyecto utilizando HTML. Se realizó la instalación y configuración de Visual Studio Code, la creación del archivo `index.html` y la publicación del proyecto en GitHub.

La página inicial incluyó:

- Nombre del proyecto AgroTech.
- Descripción general del sistema.
- Nombre del estudiante responsable del desarrollo.

### Semana 3

En esta etapa se mejoró la página web incorporando una estructura completa de HTML5 y etiquetas semánticas para organizar mejor el contenido.

Se agregaron los siguientes elementos:

- Menú de navegación.
- Sección de inicio.
- Sección "Quiénes Somos".
- Lista de servicios del sistema.
- Información de contacto.
- Imagen relacionada con la agricultura.
- Video sobre agricultura inteligente.
- Información complementaria.
- Pie de página con los datos del estudiante.

### Semana 4

Durante esta semana se incorporaron estilos visuales utilizando CSS3 y Bootstrap para mejorar la presentación y experiencia de usuario.

Se realizaron las siguientes mejoras:

- Diseño responsivo adaptable a computadoras, tabletas y teléfonos móviles.
- Uso de Bootstrap para la organización de componentes visuales.
- Personalización de colores, tipografías y secciones del proyecto.
- Mejor presentación de imágenes, tarjetas y formularios.
- Optimización de la estructura visual de la página web.

### Semana 5 

En esta etapa se incorporó JavaScript para agregar interactividad y manipulación dinámica del DOM.

Se desarrolló un módulo de gestión de cultivos que permite:

- Registrar cultivos mediante un formulario.
- Validar que los campos obligatorios no estén vacíos.
- Mostrar mensajes dinámicos de éxito y validación.
- Crear registros dinámicamente sin recargar la página.
- Mostrar el total de cultivos registrados.
- Eliminar registros mediante botones y eventos de JavaScript.
- Aplicar manipulación del DOM utilizando createElement(), appendChild() y remove().
- Gestionar eventos mediante addEventListener() y preventDefault().

### Semana 6

Durante esta semana se mejoró el formulario de registro mediante validaciones dinámicas con JavaScript, permitiendo controlar la información antes de ser registrada.

Las mejoras implementadas fueron:

- Validación de campos obligatorios.
- Validación de longitud mínima del nombre del cultivo.
- Validación de longitud mínima de la descripción.
- Validación de selección de la categoría.
- Validaciones en tiempo real mediante los eventos `input`, `blur` y `change`.
- Mensajes de error mostrados debajo de cada campo.
- Aplicación de las clases `is-valid` e `is-invalid` de Bootstrap.
- Uso de `alert-success`, `alert-danger` y `alert-warning` para informar al usuario.
- Registro de cultivos únicamente cuando todas las validaciones son correctas.
- Conservación de las funciones para registrar, mostrar, contar y eliminar cultivos dinámicamente sin recargar la página.

### Semana 7

En esta semana se reorganizó la estructura del proyecto con el propósito de prepararlo para una futura integración con Flask mediante el uso de plantillas reutilizables.

Además, se mejoró la generación dinámica del contenido utilizando JavaScript para evitar la repetición de código y facilitar el mantenimiento de la aplicación. Las mejoras implementadas fueron:

- Organización del proyecto utilizando comentarios que identifican las futuras plantillas del sistema.
- Preparación de la estructura para una futura plantilla `base.html`.
- Implementación de un arreglo para almacenar la información de los cultivos.
- Renderizado dinámico de los registros mediante JavaScript.
- Uso de estructuras repetitivas para mostrar automáticamente los cultivos registrados.
- Implementación de una condición para mostrar un mensaje cuando no existen registros.
- Conservación de las validaciones dinámicas desarrolladas en la Semana 6.
- Mantenimiento de las funciones para registrar, visualizar, contar y eliminar cultivos sin recargar la página.
- Organización del código para facilitar futuras mejoras e integración con Flask y bases de datos.

## Objetivos del proyecto

- Aprender los fundamentos del desarrollo web.
- Utilizar Visual Studio Code como herramienta de programación.
- Aplicar correctamente la estructura HTML5.
- Gestionar proyectos mediante Git y GitHub.
- Desarrollar progresivamente una aplicación web relacionada con el sector agrícola.

## Autor

**Jeison Teobaldo García Arreaga**

Estudiante de Ingeniería en Tecnologías de la Información  
Universidad Estatal Amazónica