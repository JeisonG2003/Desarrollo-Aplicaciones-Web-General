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

### Semana 8

Durante esta semana se mejoró la interfaz visual del proyecto utilizando Bootstrap, logrando una aplicación web más moderna, organizada y adaptable a diferentes dispositivos, sin modificar la lógica desarrollada en las semanas anteriores.

Las mejoras implementadas fueron:

- Incorporación de Bootstrap mediante CDN.
- Mejora del menú de navegación utilizando una Navbar responsiva.
- Organización del contenido mediante el sistema de rejilla (Grid) de Bootstrap.
- Optimización del formulario utilizando componentes como `form-label`, `form-control` y botones Bootstrap.
- Presentación de los cultivos registrados mediante tarjetas (Cards) de Bootstrap.
- Uso de alertas Bootstrap para informar mensajes de éxito, advertencia y error.
- Implementación de un Spinner para simular el proceso de registro de información.
- Incorporación de un Modal Bootstrap para confirmar el registro exitoso de un cultivo.
- Conservación de las validaciones dinámicas implementadas en la Semana 6.
- Conservación del renderizado dinámico de datos desarrollado en la Semana 7.
- Adaptación de la interfaz para computadoras, tabletas y teléfonos móviles mediante diseño responsivo.

### Semana 9

Durante esta semana se incorporó Flask al proyecto AgroTech, transformando progresivamente la página web en una aplicación organizada mediante rutas y plantillas utilizando Python.

Las principales implementaciones realizadas fueron:

* Creación del entorno virtual `venv`.
* Instalación del framework Flask.
* Creación del archivo `app.py`.
* Organización del proyecto mediante las carpetas `templates` y `static`.
* Creación de las carpetas `css`, `js` e `img` dentro de `static`.
* Organización de los archivos HTML utilizando la carpeta `templates`.
* Creación de la plantilla principal `base.html`.
* Implementación de herencia de plantillas mediante Jinja2 con `{% extends "base.html" %}`.
* Utilización de `{% block title %}` y `{% block content %}` para organizar el contenido de las páginas.
* Uso de `url_for()` para generar los enlaces de navegación.
* Uso de `url_for('static', filename='...')` para cargar los archivos CSS, JavaScript e imágenes.
* Creación de los módulos Productos, Clientes, Proveedores y Facturación.
* Implementación de las rutas `/`, `/productos`, `/clientes`, `/proveedores` y `/facturacion`.
* Utilización de `render_template()` para mostrar las diferentes páginas.
* Incorporación del archivo `requirements.txt` con las dependencias utilizadas por el proyecto.
* Creación del archivo `.gitignore` para evitar subir archivos innecesarios, como el entorno virtual.
* Prueba local de la aplicación mediante Flask en `http://127.0.0.1:5000`.
* Verificación individual de las rutas principales del sistema.
* Actualización del repositorio de GitHub con los cambios correspondientes a la Semana 9.

En esta etapa no se utilizó una base de datos. Los módulos contienen información demostrativa para comprobar el funcionamiento de las rutas y las plantillas.

### Semana 10

Durante esta semana se incorporó la generación de contenido dinámico mediante Flask y Jinja2, permitiendo enviar información desde app.py hacia las plantillas HTML.

Las principales implementaciones fueron:

- Uso de variables, listas y diccionarios en app.py.
- Envío de datos mediante render_template().
- Uso de variables dinámicas con {{ }}.
- Implementación de ciclos {% for %} para mostrar productos automáticamente.
- Uso de condiciones {% if %} y {% else %} para mostrar productos disponibles o agotados.
- Utilización de filtros de Jinja2.
- Reutilización de componentes mediante navbar.html y footer.html.
- Mantenimiento de la herencia de plantillas con base.html.
- Conservación de url_for() para las rutas y archivos estáticos.
- Prueba local de las rutas y actualización del repositorio de GitHub.

En esta etapa no se utilizó una base de datos; los datos fueron definidos temporalmente en app.py.

### Semana 11

Durante esta semana se incorporó Flask-WTF y WTForms al proyecto AgroTech para implementar formularios web con validación del lado del servidor y protección contra ataques CSRF. Las principales implementaciones fueron:

- Instalación de Flask-WTF y WTForms.
- Creación de la carpeta `forms` para organizar los formularios del proyecto.
- Creación del archivo `__init__.py` dentro de la carpeta `forms`.
- Creación de formularios independientes para Productos, Clientes, Proveedores y Facturación.
- Implementación de clases que heredan de `FlaskForm`.
- Uso de validadores como `DataRequired()`, `Length()` y `NumberRange()`.
- Implementación de rutas mediante los métodos `GET` y `POST`.
- Uso de `form.validate_on_submit()` para validar la información antes de procesarla.
- Configuración de `SECRET_KEY` para habilitar la protección CSRF.
- Incorporación de `form.hidden_tag()` en los formularios.
- Implementación de mensajes de validación para informar al usuario cuando existen datos incorrectos.
- Uso de mensajes `flash()` para confirmar el registro correcto de información.
- Creación de plantillas independientes para los formularios de cada módulo.
- Actualización de `requirements.txt` con las dependencias utilizadas.
- Realización de pruebas con datos vacíos, incorrectos y correctos.

En esta etapa no se utilizó una base de datos. Los datos continúan manejándose temporalmente mediante estructuras de Python, dejando preparada la aplicación para incorporar persistencia mediante MySQL o PostgreSQL en futuros avances.

### Semana 12

Durante esta semana se incorporó la persistencia de datos mediante SQLite al proyecto AgroTech, tomando como base los formularios y validaciones desarrollados en la Semana 11. La implementación se realizó principalmente en el módulo de Productos, permitiendo que la información registrada mediante el formulario se almacene en una base de datos local y permanezca disponible después de cerrar y volver a ejecutar la aplicación.

Las principales implementaciones fueron:

- Creación de la carpeta data para almacenar la base de datos local.
- Creación de la base de datos SQLite ferreteria.db.
- Utilización del módulo sqlite3 de Python para trabajar con la base de datos.
- Creación de la tabla productos con una clave primaria y los campos correspondientes al formulario.
- Implementación de CREATE TABLE IF NOT EXISTS para crear la tabla sin generar errores al iniciar nuevamente la aplicación.
- Conexión del formulario de Productos desarrollado en la Semana 11 con SQLite.
- Validación de los datos mediante form.validate_on_submit() antes de almacenarlos.
- Implementación de consultas INSERT para guardar los productos registrados.
- Uso de consultas SQL parametrizadas mediante ?.
- Utilización de conn.commit() para confirmar el almacenamiento de los datos.
- Cierre de las conexiones mediante conn.close().
- Implementación de consultas SELECT para recuperar los productos almacenados.
- Uso de fetchall() para obtener los registros desde SQLite.
- Envío de los datos recuperados hacia la plantilla mediante render_template().
- Actualización de productos.html para mostrar la información almacenada en una tabla HTML con Bootstrap.
- Uso de un ciclo {% for %} de Jinja2 para mostrar dinámicamente los productos.
- Conservación del formulario Flask-WTF, las validaciones, la protección CSRF y los mensajes flash() implementados en la Semana 11.
- Comprobación de la persistencia de los productos después de cerrar y volver a ejecutar la aplicación Flask.

En esta etapa se incorporó SQLite como mecanismo de persistencia local para el módulo de Productos. Los demás módulos se mantienen preparados para incorporar persistencia progresivamente en los siguientes avances.

### Semana 13

Durante esta semana se realizó la migración del módulo de Productos de SQLite a MySQL, mejorando la persistencia y organización de los datos del proyecto AgroTech.

- Instalación de mysql-connector-python y actualización de requirements.txt.
- Creación de la base de datos agrotech en MySQL.
- Creación de las carpetas conexion y sql para organizar la conexión y estructura de la base de datos.
- Implementación de conexion.py para conectar Flask con MySQL.
- Creación de esquema.sql con las tablas productos, proveedores, clientes y facturas.
- Uso de claves primarias y foráneas para establecer relaciones entre las tablas.
- Migración del módulo de Productos desde SQLite hacia MySQL.
- Implementación de consultas SELECT, INSERT, UPDATE y DELETE.
- Uso de consultas SQL parametrizadas mediante %s y conn.commit() para confirmar cambios.
- Integración de las operaciones de MySQL con las rutas de Flask.
- Mantenimiento de Flask-WTF, WTForms, validaciones y protección CSRF.
- Actualización de productos.html para consultar, registrar, editar y eliminar productos.
- Uso de Jinja2 y Bootstrap para mostrar dinámicamente la información y mejorar la interfaz.
- Realización de pruebas para verificar el funcionamiento y la persistencia de los datos en MySQL Workbench.

En esta etapa se reemplazó SQLite por MySQL como sistema de gestión de base de datos para el módulo de Productos. La aplicación ahora cuenta con una estructura relacional preparada para continuar integrando los demás módulos del sistema de manera progresiva.

### Objetivos del proyecto

- Aprender los fundamentos del desarrollo web.
- Utilizar Visual Studio Code como herramienta de programación.
- Aplicar correctamente la estructura HTML5.
- Gestionar proyectos mediante Git y GitHub.
- Desarrollar progresivamente una aplicación web relacionada con el sector agrícola.

### Autor

**Jeison Teobaldo García Arreaga**

Estudiante de Ingeniería en Tecnologías de la Información  
Universidad Estatal Amazónica