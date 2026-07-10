# 🚀 MorphoPlay - Plataforma Educativa de Lingüística

![MorphoPlay](https://img.shields.io/badge/MorphoPlay-v2.0-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![License](https://img.shields.io/badge/License-MIT-red)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black)

## 📚 Descripción

**MorphoPlay** es una plataforma educativa interactiva diseñada para el aprendizaje de **lingüística, morfología, sintaxis y gramática**. Combina **juegos interactivos**, **cursos estructurados**, **evaluaciones** y **certificaciones** para ofrecer una experiencia de aprendizaje completa y gamificada.

> 🎯 **Objetivo:** Hacer que el aprendizaje de la lingüística sea divertido, interactivo y accesible para todos.

---

## ✨ Características Principales

### 🎮 Juegos Interactivos
- ✅ **30+ juegos** de morfología, sintaxis, gramática y contenido bilingüe
- ✅ Sistema de **puntuación y rachas** de aciertos
- ✅ Progreso individual por usuario
- ✅ Juegos de **opción múltiple y escritura creativa**

### 📚 Cursos y Lecciones
- ✅ Cursos estructurados por **categorías y niveles** (Básico, Intermedio, Avanzado, Experto)
- ✅ Lecciones con **contenido educativo** detallado
- ✅ Evaluaciones con **preguntas de opción múltiple**
- ✅ Sistema de **certificaciones automáticas** al completar niveles

### 📊 Dashboard del Estudiante
- ✅ Estadísticas de progreso en tiempo real
- ✅ Seguimiento de **partidas y puntuaciones**
- ✅ Logros y recompensas desbloqueables
- ✅ Visualización de **cursos inscritos**
- ✅ Gráficos interactivos de rendimiento

### 🔐 Autenticación y Seguridad
- ✅ Registro e inicio de sesión de usuarios
- ✅ Perfiles de usuario personalizables
- ✅ Panel de administración completo
- ✅ Sistema de permisos (Staff, Superuser)

### 🖥️ Administración Terminal
- ✅ Gestión completa desde la terminal
- ✅ Creación de usuarios, cursos, juegos y evaluaciones
- ✅ Respaldo y restauración de base de datos
- ✅ Reportes y estadísticas del sistema

---

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8 o superior
- Git
- (Opcional) MySQL/MariaDB

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hernank10/MorphoPlay.git
cd MorphoPlay/morphoplay

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Cargar juegos y cursos (opcional)
python scripts/cargar_juegos_cursos.py
python scripts/crear_datos_estudiantes.py

# 7. Iniciar servidor
python manage.py runserver
