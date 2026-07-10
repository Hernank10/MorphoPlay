#!/usr/bin/env python
"""
MorphoPlay - Admin Terminal
Sistema completo de administración desde la terminal
"""
import os
import sys
import time
import pymysql
from datetime import datetime
from getpass import getpass
import json
import hashlib

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class MorphoPlayAdmin:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'morphoplay_user',
            'password': 'morphoplay_pass',
            'database': 'morphoplay_db',
            'charset': 'utf8mb4'
        }
        self.connection = None
        self.cursor = None
        
    def conectar_db(self):
        """Conectar a la base de datos MySQL"""
        try:
            self.connection = pymysql.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Error de conexión: {e}{Colors.END}")
            return False
    
    def cerrar_db(self):
        """Cerrar conexión a la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def limpiar_pantalla(self):
        """Limpiar la terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def pausa(self, segundos=1):
        """Pausa la ejecución"""
        time.sleep(segundos)
    
    def mostrar_header(self, titulo):
        """Mostrar un header decorativo"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{titulo.center(60)}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        self.limpiar_pantalla()
        print(f"\n{Colors.GREEN}{'🔷' * 25}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}MORPHOPLAY - ADMIN TERMINAL{Colors.END}")
        print(f"{Colors.GREEN}{'🔷' * 25}{Colors.END}\n")
        print(f"{Colors.YELLOW}📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.END}\n")
        
        print("1. 👤 Gestión de Usuarios")
        print("2. 📚 Gestión de Cursos")
        print("3. 🎮 Gestión de Juegos")
        print("4. 📝 Gestión de Evaluaciones")
        print("5. 📊 Gestión de Partidas y Progreso")
        print("6. 📈 Reportes y Estadísticas")
        print("7. 🗄️ Respaldo de Base de Datos")
        print("8. 🔧 Herramientas del Sistema")
        print("9. 🚪 Salir")
        print()
        
        return input("Selecciona una opción: ").strip()
    
    # ============================================================
    # 1. GESTIÓN DE USUARIOS
    # ============================================================
    
    def menu_usuarios(self):
        """Menú de gestión de usuarios"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("👤 GESTIÓN DE USUARIOS")
            
            print("1. Listar todos los usuarios")
            print("2. Buscar usuario")
            print("3. Crear usuario")
            print("4. Editar usuario")
            print("5. Eliminar usuario")
            print("6. Ver estadísticas de usuario")
            print("7. Activar/Desactivar usuario")
            print("8. Cambiar contraseña")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.listar_usuarios()
            elif opcion == '2':
                self.buscar_usuario()
            elif opcion == '3':
                self.crear_usuario()
            elif opcion == '4':
                self.editar_usuario()
            elif opcion == '5':
                self.eliminar_usuario()
            elif opcion == '6':
                self.estadisticas_usuario()
            elif opcion == '7':
                self.activar_desactivar_usuario()
            elif opcion == '8':
                self.cambiar_contrasena()
    
    def listar_usuarios(self):
        """Listar todos los usuarios"""
        self.limpiar_pantalla()
        self.mostrar_header("📋 LISTA DE USUARIOS")
        
        self.cursor.execute("""
            SELECT u.id, u.username, u.email, u.first_name, u.last_name,
                   u.is_active, u.is_staff, u.is_superuser,
                   e.juegos_completados, e.puntuacion_total,
                   u.date_joined
            FROM auth_user u
            LEFT JOIN core_estadisticasusuario e ON e.usuario_id = u.id
            ORDER BY u.id
        """)
        
        usuarios = self.cursor.fetchall()
        
        if not usuarios:
            print(f"{Colors.YELLOW}No hay usuarios registrados.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Usuario':<15} {'Email':<25} {'Nombre':<20} {'Estado':<8} {'Staff':<6} {'Admin':<6} {'Juegos':<8} {'Puntos':<8}")
        print("-" * 120)
        for u in usuarios:
            estado = f"{Colors.GREEN}✅{Colors.END}" if u[5] else f"{Colors.RED}❌{Colors.END}"
            staff = f"{Colors.GREEN}✅{Colors.END}" if u[6] else f"{Colors.RED}❌{Colors.END}"
            admin = f"{Colors.GREEN}✅{Colors.END}" if u[7] else f"{Colors.RED}❌{Colors.END}"
            nombre = f"{u[3]} {u[4]}".strip() or "-"
            print(f"{u[0]:<4} {u[1]:<15} {u[2][:24]:<25} {nombre[:19]:<20} {estado:<8} {staff:<6} {admin:<6} {u[8]:<8} {u[9]:<8}")
        
        print(f"\n{Colors.YELLOW}Total: {len(usuarios)} usuarios{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def buscar_usuario(self):
        """Buscar usuario por nombre o email"""
        self.limpiar_pantalla()
        self.mostrar_header("🔍 BUSCAR USUARIO")
        
        termino = input("Ingresa nombre de usuario o email: ").strip()
        
        self.cursor.execute("""
            SELECT id, username, email, first_name, last_name, is_active, is_staff, is_superuser
            FROM auth_user
            WHERE username LIKE %s OR email LIKE %s
        """, (f"%{termino}%", f"%{termino}%"))
        
        usuarios = self.cursor.fetchall()
        
        if not usuarios:
            print(f"{Colors.YELLOW}No se encontraron usuarios.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        for u in usuarios:
            print(f"\n{Colors.BOLD}ID: {u[0]}{Colors.END}")
            print(f"  Usuario: {u[1]}")
            print(f"  Email: {u[2]}")
            print(f"  Nombre: {u[3]} {u[4]}")
            print(f"  Activo: {'✅' if u[5] else '❌'}")
            print(f"  Staff: {'✅' if u[6] else '❌'}")
            print(f"  Admin: {'✅' if u[7] else '❌'}")
            print("-" * 30)
        
        input("\nPresiona Enter para continuar...")
    
    def crear_usuario(self):
        """Crear nuevo usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ CREAR USUARIO")
        
        username = input("Usuario: ").strip()
        if not username:
            print(f"{Colors.RED}❌ El usuario es obligatorio{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Verificar si ya existe
        self.cursor.execute("SELECT id FROM auth_user WHERE username = %s", (username,))
        if self.cursor.fetchone():
            print(f"{Colors.RED}❌ El usuario ya existe{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        email = input("Email: ").strip()
        password = getpass("Contraseña: ").strip()
        first_name = input("Nombre: ").strip()
        last_name = input("Apellido: ").strip()
        is_staff = input("¿Es staff? (s/N): ").lower() == 's'
        is_superuser = input("¿Es superusuario? (s/N): ").lower() == 's'
        
        # Crear usuario
        self.cursor.execute("""
            INSERT INTO auth_user (username, email, password, first_name, last_name,
                                   is_active, is_staff, is_superuser, date_joined)
            VALUES (%s, %s, %s, %s, %s, 1, %s, %s, NOW())
        """, (username, email, password, first_name, last_name, is_staff, is_superuser))
        self.connection.commit()
        
        usuario_id = self.cursor.lastrowid
        
        # Crear estadísticas
        self.cursor.execute("""
            INSERT INTO core_estadisticasusuario (usuario_id)
            VALUES (%s)
        """, (usuario_id,))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Usuario creado exitosamente! ID: {usuario_id}{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_usuario(self):
        """Editar usuario existente"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR USUARIO")
        
        usuario_id = input("ID del usuario a editar: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Obtener datos actuales
        self.cursor.execute("""
            SELECT username, email, first_name, last_name, is_staff, is_superuser
            FROM auth_user WHERE id = %s
        """, (int(usuario_id),))
        
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        username = input(f"Usuario [{usuario[0]}]: ").strip() or usuario[0]
        email = input(f"Email [{usuario[1]}]: ").strip() or usuario[1]
        first_name = input(f"Nombre [{usuario[2] or ''}]: ").strip() or usuario[2]
        last_name = input(f"Apellido [{usuario[3] or ''}]: ").strip() or usuario[3]
        
        is_staff_input = input(f"¿Es staff? (s/N) [{'S' if usuario[4] else 'N'}]: ").strip().lower()
        is_staff = usuario[4] if is_staff_input == '' else is_staff_input == 's'
        
        is_superuser_input = input(f"¿Es superusuario? (s/N) [{'S' if usuario[5] else 'N'}]: ").strip().lower()
        is_superuser = usuario[5] if is_superuser_input == '' else is_superuser_input == 's'
        
        self.cursor.execute("""
            UPDATE auth_user
            SET username = %s, email = %s, first_name = %s, last_name = %s,
                is_staff = %s, is_superuser = %s
            WHERE id = %s
        """, (username, email, first_name, last_name, is_staff, is_superuser, int(usuario_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Usuario actualizado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_usuario(self):
        """Eliminar usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR USUARIO")
        
        usuario_id = input("ID del usuario a eliminar: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Verificar si existe
        self.cursor.execute("SELECT username FROM auth_user WHERE id = %s", (int(usuario_id),))
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Eliminar al usuario '{usuario[0]}'? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Eliminar usuario (CASCADE eliminará todo lo relacionado)
        self.cursor.execute("DELETE FROM auth_user WHERE id = %s", (int(usuario_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Usuario eliminado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def estadisticas_usuario(self):
        """Ver estadísticas de un usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("📊 ESTADÍSTICAS DE USUARIO")
        
        usuario_id = input("ID del usuario: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT u.username, u.email, u.first_name, u.last_name, u.date_joined,
                   e.juegos_completados, e.puntuacion_total, e.racha_actual, e.racha_maxima,
                   (SELECT COUNT(*) FROM core_partida WHERE usuario_id = %s) as partidas,
                   (SELECT COUNT(*) FROM core_partida WHERE usuario_id = %s AND correcto = 1) as correctas
            FROM auth_user u
            LEFT JOIN core_estadisticasusuario e ON e.usuario_id = u.id
            WHERE u.id = %s
        """, (int(usuario_id), int(usuario_id), int(usuario_id)))
        
        stats = self.cursor.fetchone()
        if not stats:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        nombre = f"{stats[2]} {stats[3]}".strip() or "-"
        partidas = stats[9] or 0
        correctas = stats[10] or 0
        porcentaje = (correctas / partidas * 100) if partidas > 0 else 0
        
        print(f"\n{Colors.BOLD}👤 {stats[0]}{Colors.END}")
        print(f"  Email: {stats[1]}")
        print(f"  Nombre: {nombre}")
        print(f"  Fecha registro: {stats[4]}")
        print(f"\n{Colors.BOLD}📊 Estadísticas:{Colors.END}")
        print(f"  Juegos completados: {stats[5] or 0}")
        print(f"  Puntuación total: {stats[6] or 0}")
        print(f"  Racha actual: 🔥 {stats[7] or 0}")
        print(f"  Mejor racha: 🏆 {stats[8] or 0}")
        print(f"  Total partidas: {partidas}")
        print(f"  Correctas: {correctas}")
        print(f"  Porcentaje aciertos: {porcentaje:.1f}%")
        
        input("\nPresiona Enter para continuar...")
    
    def activar_desactivar_usuario(self):
        """Activar o desactivar usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("🔀 ACTIVAR/DESACTIVAR USUARIO")
        
        usuario_id = input("ID del usuario: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT username, is_active FROM auth_user WHERE id = %s", (int(usuario_id),))
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        nuevo_estado = not usuario[1]
        estado_texto = "activar" if nuevo_estado else "desactivar"
        
        confirmar = input(f"¿{estado_texto} al usuario '{usuario[0]}'? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("UPDATE auth_user SET is_active = %s WHERE id = %s", (nuevo_estado, int(usuario_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Usuario {'activado' if nuevo_estado else 'desactivado'} exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def cambiar_contrasena(self):
        """Cambiar contraseña de usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("🔑 CAMBIAR CONTRASEÑA")
        
        usuario_id = input("ID del usuario: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT username FROM auth_user WHERE id = %s", (int(usuario_id),))
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        nueva_password = getpass(f"Nueva contraseña para '{usuario[0]}': ").strip()
        confirmar_password = getpass("Confirmar contraseña: ").strip()
        
        if nueva_password != confirmar_password:
            print(f"{Colors.RED}❌ Las contraseñas no coinciden{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("UPDATE auth_user SET password = %s WHERE id = %s", (nueva_password, int(usuario_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Contraseña actualizada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 2. GESTIÓN DE CURSOS
    # ============================================================
    
    def menu_cursos(self):
        """Menú de gestión de cursos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("📚 GESTIÓN DE CURSOS")
            
            print("1. Listar todos los cursos")
            print("2. Crear curso")
            print("3. Editar curso")
            print("4. Eliminar curso")
            print("5. Ver lecciones de un curso")
            print("6. Agregar lección a curso")
            print("7. Editar lección")
            print("8. Eliminar lección")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.listar_cursos()
            elif opcion == '2':
                self.crear_curso()
            elif opcion == '3':
                self.editar_curso()
            elif opcion == '4':
                self.eliminar_curso()
            elif opcion == '5':
                self.ver_lecciones_curso()
            elif opcion == '6':
                self.agregar_leccion()
            elif opcion == '7':
                self.editar_leccion()
            elif opcion == '8':
                self.eliminar_leccion()
    
    def listar_cursos(self):
        """Listar todos los cursos"""
        self.limpiar_pantalla()
        self.mostrar_header("📋 LISTA DE CURSOS")
        
        self.cursor.execute("""
            SELECT c.id, c.titulo, cat.nombre as categoria, n.nombre as nivel,
                   c.duracion_estimada, c.activo,
                   (SELECT COUNT(*) FROM core_leccion WHERE curso_id = c.id) as lecciones,
                   (SELECT COUNT(*) FROM core_evaluacion WHERE curso_id = c.id) as evaluaciones
            FROM core_curso c
            LEFT JOIN core_categoria cat ON c.categoria_id = cat.id
            LEFT JOIN core_nivel n ON c.nivel_id = n.id
            ORDER BY c.id
        """)
        
        cursos = self.cursor.fetchall()
        
        if not cursos:
            print(f"{Colors.YELLOW}No hay cursos disponibles.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Título':<30} {'Categoría':<15} {'Nivel':<12} {'Duración':<10} {'Activo':<8} {'Lecciones':<10} {'Evaluaciones':<12}")
        print("-" * 110)
        for c in cursos:
            activo = f"{Colors.GREEN}✅{Colors.END}" if c[5] else f"{Colors.RED}❌{Colors.END}"
            print(f"{c[0]:<4} {c[1][:29]:<30} {c[2][:14]:<15} {c[3][:11]:<12} {c[4]:<10} {activo:<8} {c[6]:<10} {c[7]:<12}")
        
        print(f"\n{Colors.YELLOW}Total: {len(cursos)} cursos{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def crear_curso(self):
        """Crear nuevo curso"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ CREAR CURSO")
        
        # Obtener categorías
        self.cursor.execute("SELECT id, nombre FROM core_categoria WHERE activo = 1 ORDER BY nombre")
        categorias = self.cursor.fetchall()
        
        if not categorias:
            print(f"{Colors.RED}❌ No hay categorías disponibles. Crea una primero.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{Colors.YELLOW}Categorías disponibles:{Colors.END}")
        for cat in categorias:
            print(f"  {cat[0]}. {cat[1]}")
        
        cat_id = input("ID de la categoría: ").strip()
        if not cat_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Obtener niveles
        self.cursor.execute("SELECT id, nombre FROM core_nivel ORDER BY orden")
        niveles = self.cursor.fetchall()
        
        print(f"\n{Colors.YELLOW}Niveles disponibles:{Colors.END}")
        for niv in niveles:
            print(f"  {niv[0]}. {niv[1]}")
        
        niv_id = input("ID del nivel: ").strip()
        if not niv_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        titulo = input("Título del curso: ").strip()
        descripcion = input("Descripción: ").strip()
        duracion = input("Duración estimada (horas): ").strip()
        
        self.cursor.execute("""
            INSERT INTO core_curso (titulo, descripcion, categoria_id, nivel_id, duracion_estimada, activo)
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (titulo, descripcion, int(cat_id), int(niv_id), int(duracion) if duracion.isdigit() else 0))
        self.connection.commit()
        
        curso_id = self.cursor.lastrowid
        print(f"\n{Colors.GREEN}✅ Curso creado exitosamente! ID: {curso_id}{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_curso(self):
        """Editar curso existente"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR CURSO")
        
        curso_id = input("ID del curso a editar: ").strip()
        if not curso_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT titulo, descripcion, categoria_id, nivel_id, duracion_estimada, activo
            FROM core_curso WHERE id = %s
        """, (int(curso_id),))
        
        curso = self.cursor.fetchone()
        if not curso:
            print(f"{Colors.RED}❌ Curso no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        
        titulo = input(f"Título [{curso[0]}]: ").strip() or curso[0]
        descripcion = input(f"Descripción [{curso[1]}]: ").strip() or curso[1]
        cat_id = input(f"Categoría ID [{curso[2]}]: ").strip()
        cat_id = int(cat_id) if cat_id.isdigit() else curso[2]
        niv_id = input(f"Nivel ID [{curso[3]}]: ").strip()
        niv_id = int(niv_id) if niv_id.isdigit() else curso[3]
        duracion = input(f"Duración [{curso[4]}]: ").strip()
        duracion = int(duracion) if duracion.isdigit() else curso[4]
        
        activo_input = input(f"Activo (s/N) [{'S' if curso[5] else 'N'}]: ").strip().lower()
        activo = curso[5] if activo_input == '' else activo_input == 's'
        
        self.cursor.execute("""
            UPDATE core_curso
            SET titulo = %s, descripcion = %s, categoria_id = %s, nivel_id = %s,
                duracion_estimada = %s, activo = %s
            WHERE id = %s
        """, (titulo, descripcion, cat_id, niv_id, duracion, activo, int(curso_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Curso actualizado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_curso(self):
        """Eliminar curso"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR CURSO")
        
        curso_id = input("ID del curso a eliminar: ").strip()
        if not curso_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_curso WHERE id = %s", (int(curso_id),))
        curso = self.cursor.fetchone()
        if not curso:
            print(f"{Colors.RED}❌ Curso no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Contar lecciones y evaluaciones
        self.cursor.execute("SELECT COUNT(*) FROM core_leccion WHERE curso_id = %s", (int(curso_id),))
        lecciones = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM core_evaluacion WHERE curso_id = %s", (int(curso_id),))
        evaluaciones = self.cursor.fetchone()[0]
        
        print(f"\n{Colors.YELLOW}Curso: {curso[0]}{Colors.END}")
        print(f"  Lecciones: {lecciones}")
        print(f"  Evaluaciones: {evaluaciones}")
        
        confirmar = input(f"\n¿Eliminar este curso y todo su contenido? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_curso WHERE id = %s", (int(curso_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Curso eliminado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def ver_lecciones_curso(self):
        """Ver lecciones de un curso"""
        self.limpiar_pantalla()
        self.mostrar_header("📖 LECCIONES DEL CURSO")
        
        curso_id = input("ID del curso: ").strip()
        if not curso_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_curso WHERE id = %s", (int(curso_id),))
        curso = self.cursor.fetchone()
        if not curso:
            print(f"{Colors.RED}❌ Curso no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Curso: {curso[0]}{Colors.END}\n")
        
        self.cursor.execute("""
            SELECT id, titulo, orden, activo
            FROM core_leccion
            WHERE curso_id = %s
            ORDER BY orden
        """, (int(curso_id),))
        
        lecciones = self.cursor.fetchall()
        
        if not lecciones:
            print(f"{Colors.YELLOW}Este curso no tiene lecciones.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Orden':<6} {'Título':<50} {'Activo':<8}")
        print("-" * 70)
        for lec in lecciones:
            activo = f"{Colors.GREEN}✅{Colors.END}" if lec[3] else f"{Colors.RED}❌{Colors.END}"
            print(f"{lec[0]:<4} {lec[2]:<6} {lec[1][:49]:<50} {activo:<8}")
        
        input("\nPresiona Enter para continuar...")
    
    def agregar_leccion(self):
        """Agregar lección a un curso"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ AGREGAR LECCIÓN")
        
        curso_id = input("ID del curso: ").strip()
        if not curso_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_curso WHERE id = %s", (int(curso_id),))
        curso = self.cursor.fetchone()
        if not curso:
            print(f"{Colors.RED}❌ Curso no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Curso: {curso[0]}{Colors.END}\n")
        
        titulo = input("Título de la lección: ").strip()
        contenido = input("Contenido (texto): ").strip()
        orden = input("Orden: ").strip()
        orden = int(orden) if orden.isdigit() else 0
        
        self.cursor.execute("""
            INSERT INTO core_leccion (curso_id, titulo, contenido, orden, activo)
            VALUES (%s, %s, %s, %s, 1)
        """, (int(curso_id), titulo, contenido, orden))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Lección agregada exitosamente!{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_leccion(self):
        """Editar lección"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR LECCIÓN")
        
        leccion_id = input("ID de la lección: ").strip()
        if not leccion_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT titulo, contenido, orden, activo FROM core_leccion WHERE id = %s
        """, (int(leccion_id),))
        
        leccion = self.cursor.fetchone()
        if not leccion:
            print(f"{Colors.RED}❌ Lección no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        
        titulo = input(f"Título [{leccion[0]}]: ").strip() or leccion[0]
        contenido = input(f"Contenido [{leccion[1][:50]}...]: ").strip() or leccion[1]
        orden = input(f"Orden [{leccion[2]}]: ").strip()
        orden = int(orden) if orden.isdigit() else leccion[2]
        
        activo_input = input(f"Activo (s/N) [{'S' if leccion[3] else 'N'}]: ").strip().lower()
        activo = leccion[3] if activo_input == '' else activo_input == 's'
        
        self.cursor.execute("""
            UPDATE core_leccion
            SET titulo = %s, contenido = %s, orden = %s, activo = %s
            WHERE id = %s
        """, (titulo, contenido, orden, activo, int(leccion_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Lección actualizada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_leccion(self):
        """Eliminar lección"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR LECCIÓN")
        
        leccion_id = input("ID de la lección: ").strip()
        if not leccion_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_leccion WHERE id = %s", (int(leccion_id),))
        leccion = self.cursor.fetchone()
        if not leccion:
            print(f"{Colors.RED}❌ Lección no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Eliminar la lección '{leccion[0]}'? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_leccion WHERE id = %s", (int(leccion_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Lección eliminada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 3. GESTIÓN DE JUEGOS
    # ============================================================
    
    def menu_juegos(self):
        """Menú de gestión de juegos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("🎮 GESTIÓN DE JUEGOS")
            
            print("1. Listar todos los juegos")
            print("2. Crear juego")
            print("3. Editar juego")
            print("4. Eliminar juego")
            print("5. Ver estadísticas de juego")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.listar_juegos()
            elif opcion == '2':
                self.crear_juego()
            elif opcion == '3':
                self.editar_juego()
            elif opcion == '4':
                self.eliminar_juego()
            elif opcion == '5':
                self.estadisticas_juego()
    
    def listar_juegos(self):
        """Listar todos los juegos"""
        self.limpiar_pantalla()
        self.mostrar_header("📋 LISTA DE JUEGOS")
        
        self.cursor.execute("""
            SELECT j.id, j.titulo, cat.nombre, n.nombre, j.tipo, j.puntos, j.activo,
                   j.veces_jugado, j.tasa_aciertos
            FROM core_juego j
            LEFT JOIN core_categoria cat ON j.categoria_id = cat.id
            LEFT JOIN core_nivel n ON j.nivel_id = n.id
            ORDER BY j.id
        """)
        
        juegos = self.cursor.fetchall()
        
        if not juegos:
            print(f"{Colors.YELLOW}No hay juegos disponibles.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Título':<25} {'Categoría':<12} {'Nivel':<10} {'Tipo':<10} {'Puntos':<8} {'Activo':<8} {'Jugados':<8} {'Aciertos':<8}")
        print("-" * 110)
        for j in juegos:
            activo = f"{Colors.GREEN}✅{Colors.END}" if j[6] else f"{Colors.RED}❌{Colors.END}"
            print(f"{j[0]:<4} {j[1][:24]:<25} {j[2][:11]:<12} {j[3][:9]:<10} {j[4][:9]:<10} {j[5]:<8} {activo:<8} {j[7]:<8} {j[8]:<8}")
        
        print(f"\n{Colors.YELLOW}Total: {len(juegos)} juegos{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def crear_juego(self):
        """Crear nuevo juego"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ CREAR JUEGO")
        
        # Obtener categorías
        self.cursor.execute("SELECT id, nombre FROM core_categoria WHERE activo = 1")
        categorias = self.cursor.fetchall()
        
        print(f"{Colors.YELLOW}Categorías disponibles:{Colors.END}")
        for cat in categorias:
            print(f"  {cat[0]}. {cat[1]}")
        
        cat_id = input("ID de la categoría: ").strip()
        if not cat_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Obtener niveles
        self.cursor.execute("SELECT id, nombre FROM core_nivel")
        niveles = self.cursor.fetchall()
        
        print(f"\n{Colors.YELLOW}Niveles disponibles:{Colors.END}")
        for niv in niveles:
            print(f"  {niv[0]}. {niv[1]}")
        
        niv_id = input("ID del nivel: ").strip()
        if not niv_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        titulo = input("Título del juego: ").strip()
        descripcion = input("Descripción: ").strip()
        pregunta = input("Pregunta: ").strip()
        
        print("\nOpciones:")
        opcion1 = input("Opción 1: ").strip()
        opcion2 = input("Opción 2: ").strip()
        opcion3 = input("Opción 3: ").strip()
        opcion4 = input("Opción 4: ").strip()
        
        correcta = input("Respuesta correcta: ").strip()
        puntos = input("Puntos: ").strip()
        puntos = int(puntos) if puntos.isdigit() else 10
        
        self.cursor.execute("""
            INSERT INTO core_juego (titulo, descripcion, pregunta, categoria_id, nivel_id,
                                     tipo, opcion1, opcion2, opcion3, opcion4,
                                     respuesta_correcta, puntos, activo)
            VALUES (%s, %s, %s, %s, %s, 'opcion', %s, %s, %s, %s, %s, %s, 1)
        """, (titulo, descripcion, pregunta, int(cat_id), int(niv_id),
              opcion1, opcion2, opcion3, opcion4, correcta, puntos))
        self.connection.commit()
        
        juego_id = self.cursor.lastrowid
        print(f"\n{Colors.GREEN}✅ Juego creado exitosamente! ID: {juego_id}{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_juego(self):
        """Editar juego"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR JUEGO")
        
        juego_id = input("ID del juego: ").strip()
        if not juego_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo, descripcion, pregunta, puntos, activo FROM core_juego WHERE id = %s", (int(juego_id),))
        juego = self.cursor.fetchone()
        if not juego:
            print(f"{Colors.RED}❌ Juego no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        
        titulo = input(f"Título [{juego[0]}]: ").strip() or juego[0]
        descripcion = input(f"Descripción [{juego[1]}]: ").strip() or juego[1]
        pregunta = input(f"Pregunta [{juego[2]}]: ").strip() or juego[2]
        puntos = input(f"Puntos [{juego[3]}]: ").strip()
        puntos = int(puntos) if puntos.isdigit() else juego[3]
        
        activo_input = input(f"Activo (s/N) [{'S' if juego[4] else 'N'}]: ").strip().lower()
        activo = juego[4] if activo_input == '' else activo_input == 's'
        
        self.cursor.execute("""
            UPDATE core_juego
            SET titulo = %s, descripcion = %s, pregunta = %s, puntos = %s, activo = %s
            WHERE id = %s
        """, (titulo, descripcion, pregunta, puntos, activo, int(juego_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Juego actualizado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_juego(self):
        """Eliminar juego"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR JUEGO")
        
        juego_id = input("ID del juego: ").strip()
        if not juego_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_juego WHERE id = %s", (int(juego_id),))
        juego = self.cursor.fetchone()
        if not juego:
            print(f"{Colors.RED}❌ Juego no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Eliminar el juego '{juego[0]}'? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_juego WHERE id = %s", (int(juego_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Juego eliminado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def estadisticas_juego(self):
        """Ver estadísticas de un juego"""
        self.limpiar_pantalla()
        self.mostrar_header("📊 ESTADÍSTICAS DEL JUEGO")
        
        juego_id = input("ID del juego: ").strip()
        if not juego_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT titulo, veces_jugado, tasa_aciertos,
                   (SELECT COUNT(*) FROM core_partida WHERE juego_id = %s AND correcto = 1) as correctas,
                   (SELECT COUNT(*) FROM core_partida WHERE juego_id = %s) as total
            FROM core_juego WHERE id = %s
        """, (int(juego_id), int(juego_id), int(juego_id)))
        
        juego = self.cursor.fetchone()
        if not juego:
            print(f"{Colors.RED}❌ Juego no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.BOLD}🎮 {juego[0]}{Colors.END}")
        print(f"  Veces jugado: {juego[1]}")
        print(f"  Tasa de aciertos: {juego[2]}%")
        print(f"  Total correctas: {juego[3]}")
        print(f"  Total partidas: {juego[4]}")
        
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 4. GESTIÓN DE EVALUACIONES
    # ============================================================
    
    def menu_evaluaciones(self):
        """Menú de gestión de evaluaciones"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("📝 GESTIÓN DE EVALUACIONES")
            
            print("1. Listar evaluaciones")
            print("2. Crear evaluación")
            print("3. Editar evaluación")
            print("4. Eliminar evaluación")
            print("5. Ver preguntas de evaluación")
            print("6. Agregar pregunta a evaluación")
            print("7. Editar pregunta")
            print("8. Eliminar pregunta")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.listar_evaluaciones()
            elif opcion == '2':
                self.crear_evaluacion()
            elif opcion == '3':
                self.editar_evaluacion()
            elif opcion == '4':
                self.eliminar_evaluacion()
            elif opcion == '5':
                self.ver_preguntas_evaluacion()
            elif opcion == '6':
                self.agregar_pregunta()
            elif opcion == '7':
                self.editar_pregunta()
            elif opcion == '8':
                self.eliminar_pregunta()
    
    def listar_evaluaciones(self):
        """Listar todas las evaluaciones"""
        self.limpiar_pantalla()
        self.mostrar_header("📋 LISTA DE EVALUACIONES")
        
        self.cursor.execute("""
            SELECT e.id, e.titulo, c.titulo as curso, e.tipo, e.puntaje_maximo,
                   e.intentos_permitidos, e.activo,
                   (SELECT COUNT(*) FROM core_preguntaevaluacion WHERE evaluacion_id = e.id) as preguntas
            FROM core_evaluacion e
            LEFT JOIN core_curso c ON e.curso_id = c.id
            ORDER BY e.id
        """)
        
        evaluaciones = self.cursor.fetchall()
        
        if not evaluaciones:
            print(f"{Colors.YELLOW}No hay evaluaciones disponibles.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Título':<25} {'Curso':<25} {'Tipo':<12} {'Puntaje':<8} {'Intentos':<10} {'Preguntas':<10} {'Activo':<8}")
        print("-" * 110)
        for e in evaluaciones:
            activo = f"{Colors.GREEN}✅{Colors.END}" if e[6] else f"{Colors.RED}❌{Colors.END}"
            print(f"{e[0]:<4} {e[1][:24]:<25} {e[2][:24]:<25} {e[3][:11]:<12} {e[4]:<8} {e[5]:<10} {e[7]:<10} {activo:<8}")
        
        print(f"\n{Colors.YELLOW}Total: {len(evaluaciones)} evaluaciones{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def crear_evaluacion(self):
        """Crear nueva evaluación"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ CREAR EVALUACIÓN")
        
        # Obtener cursos
        self.cursor.execute("SELECT id, titulo FROM core_curso WHERE activo = 1")
        cursos = self.cursor.fetchall()
        
        if not cursos:
            print(f"{Colors.RED}❌ No hay cursos disponibles. Crea un curso primero.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{Colors.YELLOW}Cursos disponibles:{Colors.END}")
        for c in cursos:
            print(f"  {c[0]}. {c[1]}")
        
        curso_id = input("ID del curso: ").strip()
        if not curso_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        titulo = input("Título de la evaluación: ").strip()
        descripcion = input("Descripción: ").strip()
        
        print("\nTipos: diagnostica, formativa, sumativa, final")
        tipo = input("Tipo [formativa]: ").strip() or "formativa"
        
        puntaje_max = input("Puntaje máximo [100]: ").strip()
        puntaje_max = int(puntaje_max) if puntaje_max.isdigit() else 100
        
        intentos = input("Intentos permitidos [1]: ").strip()
        intentos = int(intentos) if intentos.isdigit() else 1
        
        self.cursor.execute("""
            INSERT INTO core_evaluacion (curso_id, titulo, descripcion, tipo,
                                          puntaje_maximo, intentos_permitidos, activo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
        """, (int(curso_id), titulo, descripcion, tipo, puntaje_max, intentos))
        self.connection.commit()
        
        eval_id = self.cursor.lastrowid
        print(f"\n{Colors.GREEN}✅ Evaluación creada exitosamente! ID: {eval_id}{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_evaluacion(self):
        """Editar evaluación"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR EVALUACIÓN")
        
        eval_id = input("ID de la evaluación: ").strip()
        if not eval_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT titulo, descripcion, tipo, puntaje_maximo, intentos_permitidos, activo
            FROM core_evaluacion WHERE id = %s
        """, (int(eval_id),))
        
        eval_data = self.cursor.fetchone()
        if not eval_data:
            print(f"{Colors.RED}❌ Evaluación no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        
        titulo = input(f"Título [{eval_data[0]}]: ").strip() or eval_data[0]
        descripcion = input(f"Descripción [{eval_data[1]}]: ").strip() or eval_data[1]
        tipo = input(f"Tipo [{eval_data[2]}]: ").strip() or eval_data[2]
        puntaje_max = input(f"Puntaje máximo [{eval_data[3]}]: ").strip()
        puntaje_max = int(puntaje_max) if puntaje_max.isdigit() else eval_data[3]
        intentos = input(f"Intentos permitidos [{eval_data[4]}]: ").strip()
        intentos = int(intentos) if intentos.isdigit() else eval_data[4]
        
        activo_input = input(f"Activo (s/N) [{'S' if eval_data[5] else 'N'}]: ").strip().lower()
        activo = eval_data[5] if activo_input == '' else activo_input == 's'
        
        self.cursor.execute("""
            UPDATE core_evaluacion
            SET titulo = %s, descripcion = %s, tipo = %s,
                puntaje_maximo = %s, intentos_permitidos = %s, activo = %s
            WHERE id = %s
        """, (titulo, descripcion, tipo, puntaje_max, intentos, activo, int(eval_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Evaluación actualizada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_evaluacion(self):
        """Eliminar evaluación"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR EVALUACIÓN")
        
        eval_id = input("ID de la evaluación: ").strip()
        if not eval_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_evaluacion WHERE id = %s", (int(eval_id),))
        eval_data = self.cursor.fetchone()
        if not eval_data:
            print(f"{Colors.RED}❌ Evaluación no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Eliminar la evaluación '{eval_data[0]}'? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_evaluacion WHERE id = %s", (int(eval_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Evaluación eliminada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def ver_preguntas_evaluacion(self):
        """Ver preguntas de una evaluación"""
        self.limpiar_pantalla()
        self.mostrar_header("❓ PREGUNTAS DE LA EVALUACIÓN")
        
        eval_id = input("ID de la evaluación: ").strip()
        if not eval_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_evaluacion WHERE id = %s", (int(eval_id),))
        eval_data = self.cursor.fetchone()
        if not eval_data:
            print(f"{Colors.RED}❌ Evaluación no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Evaluación: {eval_data[0]}{Colors.END}\n")
        
        self.cursor.execute("""
            SELECT id, pregunta, tipo, puntaje, orden, activo
            FROM core_preguntaevaluacion
            WHERE evaluacion_id = %s
            ORDER BY orden
        """, (int(eval_id),))
        
        preguntas = self.cursor.fetchall()
        
        if not preguntas:
            print(f"{Colors.YELLOW}Esta evaluación no tiene preguntas.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Pregunta':<50} {'Tipo':<12} {'Puntaje':<8} {'Orden':<6} {'Activo':<8}")
        print("-" * 90)
        for p in preguntas:
            activo = f"{Colors.GREEN}✅{Colors.END}" if p[5] else f"{Colors.RED}❌{Colors.END}"
            print(f"{p[0]:<4} {p[1][:49]:<50} {p[2][:11]:<12} {p[3]:<8} {p[4]:<6} {activo:<8}")
        
        input("\nPresiona Enter para continuar...")
    
    def agregar_pregunta(self):
        """Agregar pregunta a evaluación"""
        self.limpiar_pantalla()
        self.mostrar_header("➕ AGREGAR PREGUNTA")
        
        eval_id = input("ID de la evaluación: ").strip()
        if not eval_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT titulo FROM core_evaluacion WHERE id = %s", (int(eval_id),))
        eval_data = self.cursor.fetchone()
        if not eval_data:
            print(f"{Colors.RED}❌ Evaluación no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Evaluación: {eval_data[0]}{Colors.END}\n")
        
        pregunta = input("Pregunta: ").strip()
        
        print("\nTipos: opcion, verdadero_falso, texto")
        tipo = input("Tipo [opcion]: ").strip() or "opcion"
        
        if tipo == 'opcion':
            print("\nOpciones:")
            opcion1 = input("Opción 1: ").strip()
            opcion2 = input("Opción 2: ").strip()
            opcion3 = input("Opción 3: ").strip()
            opcion4 = input("Opción 4: ").strip()
        else:
            opcion1 = opcion2 = opcion3 = opcion4 = ''
        
        respuesta = input("Respuesta correcta: ").strip()
        puntaje = input("Puntaje [10]: ").strip()
        puntaje = int(puntaje) if puntaje.isdigit() else 10
        orden = input("Orden: ").strip()
        orden = int(orden) if orden.isdigit() else 0
        
        self.cursor.execute("""
            INSERT INTO core_preguntaevaluacion
            (evaluacion_id, pregunta, tipo, opcion1, opcion2, opcion3, opcion4,
             respuesta_correcta, puntaje, orden, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """, (int(eval_id), pregunta, tipo, opcion1, opcion2, opcion3, opcion4,
              respuesta, puntaje, orden))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Pregunta agregada exitosamente!{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def editar_pregunta(self):
        """Editar pregunta"""
        self.limpiar_pantalla()
        self.mostrar_header("✏️ EDITAR PREGUNTA")
        
        pregunta_id = input("ID de la pregunta: ").strip()
        if not pregunta_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("""
            SELECT pregunta, tipo, puntaje, orden, activo
            FROM core_preguntaevaluacion WHERE id = %s
        """, (int(pregunta_id),))
        
        pregunta_data = self.cursor.fetchone()
        if not pregunta_data:
            print(f"{Colors.RED}❌ Pregunta no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Deja en blanco para mantener el valor actual{Colors.END}\n")
        
        pregunta = input(f"Pregunta [{pregunta_data[0]}]: ").strip() or pregunta_data[0]
        tipo = input(f"Tipo [{pregunta_data[1]}]: ").strip() or pregunta_data[1]
        puntaje = input(f"Puntaje [{pregunta_data[2]}]: ").strip()
        puntaje = int(puntaje) if puntaje.isdigit() else pregunta_data[2]
        orden = input(f"Orden [{pregunta_data[3]}]: ").strip()
        orden = int(orden) if orden.isdigit() else pregunta_data[3]
        
        activo_input = input(f"Activo (s/N) [{'S' if pregunta_data[4] else 'N'}]: ").strip().lower()
        activo = pregunta_data[4] if activo_input == '' else activo_input == 's'
        
        self.cursor.execute("""
            UPDATE core_preguntaevaluacion
            SET pregunta = %s, tipo = %s, puntaje = %s, orden = %s, activo = %s
            WHERE id = %s
        """, (pregunta, tipo, puntaje, orden, activo, int(pregunta_id)))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Pregunta actualizada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def eliminar_pregunta(self):
        """Eliminar pregunta"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR PREGUNTA")
        
        pregunta_id = input("ID de la pregunta: ").strip()
        if not pregunta_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT pregunta FROM core_preguntaevaluacion WHERE id = %s", (int(pregunta_id),))
        pregunta_data = self.cursor.fetchone()
        if not pregunta_data:
            print(f"{Colors.RED}❌ Pregunta no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Eliminar la pregunta? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_preguntaevaluacion WHERE id = %s", (int(pregunta_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Pregunta eliminada exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 5. GESTIÓN DE PARTIDAS Y PROGRESO
    # ============================================================
    
    def menu_partidas(self):
        """Menú de gestión de partidas"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("📊 GESTIÓN DE PARTIDAS Y PROGRESO")
            
            print("1. Ver últimas partidas")
            print("2. Ver progreso de un usuario")
            print("3. Ver estadísticas de partidas")
            print("4. Eliminar partidas de un usuario")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.ver_ultimas_partidas()
            elif opcion == '2':
                self.ver_progreso_usuario()
            elif opcion == '3':
                self.estadisticas_partidas()
            elif opcion == '4':
                self.eliminar_partidas_usuario()
    
    def ver_ultimas_partidas(self):
        """Ver últimas partidas"""
        self.limpiar_pantalla()
        self.mostrar_header("🕐 ÚLTIMAS PARTIDAS")
        
        limite = input("Número de partidas a mostrar [20]: ").strip()
        limite = int(limite) if limite.isdigit() else 20
        
        self.cursor.execute("""
            SELECT p.id, u.username, j.titulo, p.correcto, p.puntuacion_obtenida,
                   p.tiempo_segundos, p.fecha
            FROM core_partida p
            JOIN auth_user u ON p.usuario_id = u.id
            JOIN core_juego j ON p.juego_id = j.id
            ORDER BY p.fecha DESC
            LIMIT %s
        """, (limite,))
        
        partidas = self.cursor.fetchall()
        
        if not partidas:
            print(f"{Colors.YELLOW}No hay partidas registradas.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Usuario':<12} {'Juego':<30} {'Resultado':<10} {'Puntos':<8} {'Tiempo':<8} {'Fecha':<20}")
        print("-" * 100)
        for p in partidas:
            resultado = f"{Colors.GREEN}✅ Correcto{Colors.END}" if p[3] else f"{Colors.RED}❌ Incorrecto{Colors.END}"
            print(f"{p[0]:<4} {p[1][:11]:<12} {p[2][:29]:<30} {resultado:<10} {p[4]:<8} {p[5]:<8} {p[6]:<20}")
        
        input("\nPresiona Enter para continuar...")
    
    def ver_progreso_usuario(self):
        """Ver progreso de un usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("📊 PROGRESO DE USUARIO")
        
        usuario_id = input("ID del usuario: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT username FROM auth_user WHERE id = %s", (int(usuario_id),))
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Usuario: {usuario[0]}{Colors.END}\n")
        
        self.cursor.execute("""
            SELECT j.titulo, p.completado, p.intentos, p.puntuacion, p.fecha_completado
            FROM core_progreso p
            JOIN core_juego j ON p.juego_id = j.id
            WHERE p.usuario_id = %s
            ORDER BY p.ultimo_intento DESC
        """, (int(usuario_id),))
        
        progreso = self.cursor.fetchall()
        
        if not progreso:
            print(f"{Colors.YELLOW}Este usuario no tiene progreso registrado.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'Juego':<30} {'Completado':<12} {'Intentos':<10} {'Puntuación':<12} {'Fecha':<20}")
        print("-" * 85)
        for p in progreso:
            completado = f"{Colors.GREEN}✅ Sí{Colors.END}" if p[1] else f"{Colors.RED}❌ No{Colors.END}"
            fecha = p[4] if p[4] else "-"
            print(f"{p[0][:29]:<30} {completado:<12} {p[2]:<10} {p[3]:<12} {fecha:<20}")
        
        input("\nPresiona Enter para continuar...")
    
    def estadisticas_partidas(self):
        """Estadísticas de partidas"""
        self.limpiar_pantalla()
        self.mostrar_header("📈 ESTADÍSTICAS DE PARTIDAS")
        
        # Total partidas
        self.cursor.execute("SELECT COUNT(*) FROM core_partida")
        total = self.cursor.fetchone()[0]
        
        # Correctas/Incorrectas
        self.cursor.execute("SELECT COUNT(*) FROM core_partida WHERE correcto = 1")
        correctas = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_partida WHERE correcto = 0")
        incorrectas = self.cursor.fetchone()[0]
        
        # Usuarios activos
        self.cursor.execute("SELECT COUNT(DISTINCT usuario_id) FROM core_partida")
        usuarios_activos = self.cursor.fetchone()[0]
        
        # Juegos más jugados
        self.cursor.execute("""
            SELECT j.titulo, COUNT(*) as total
            FROM core_partida p
            JOIN core_juego j ON p.juego_id = j.id
            GROUP BY j.id
            ORDER BY total DESC
            LIMIT 5
        """)
        top_juegos = self.cursor.fetchall()
        
        print(f"{Colors.BOLD}📊 Resumen General{Colors.END}")
        print(f"  Total partidas: {total}")
        print(f"  ✅ Correctas: {correctas}")
        print(f"  ❌ Incorrectas: {incorrectas}")
        print(f"  🎯 Porcentaje aciertos: {(correctas/total*100):.1f}%" if total > 0 else "  🎯 Porcentaje aciertos: 0%")
        print(f"  👥 Usuarios activos: {usuarios_activos}")
        
        if top_juegos:
            print(f"\n{Colors.BOLD}🎮 Top 5 juegos más jugados{Colors.END}")
            for juego in top_juegos:
                print(f"  {juego[0]}: {juego[1]} partidas")
        
        input("\nPresiona Enter para continuar...")
    
    def eliminar_partidas_usuario(self):
        """Eliminar partidas de un usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("🗑️ ELIMINAR PARTIDAS")
        
        usuario_id = input("ID del usuario: ").strip()
        if not usuario_id.isdigit():
            print(f"{Colors.RED}❌ ID inválido{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT username FROM auth_user WHERE id = %s", (int(usuario_id),))
        usuario = self.cursor.fetchone()
        if not usuario:
            print(f"{Colors.RED}❌ Usuario no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("SELECT COUNT(*) FROM core_partida WHERE usuario_id = %s", (int(usuario_id),))
        total = self.cursor.fetchone()[0]
        
        if total == 0:
            print(f"{Colors.YELLOW}El usuario no tiene partidas.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n{Colors.YELLOW}Usuario: {usuario[0]}{Colors.END}")
        print(f"  Partidas a eliminar: {total}")
        
        confirmar = input(f"\n¿Eliminar todas las partidas de este usuario? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.cursor.execute("DELETE FROM core_partida WHERE usuario_id = %s", (int(usuario_id),))
        self.cursor.execute("DELETE FROM core_progreso WHERE usuario_id = %s", (int(usuario_id),))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}✅ Partidas eliminadas exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 6. REPORTES Y ESTADÍSTICAS
    # ============================================================
    
    def menu_reportes(self):
        """Menú de reportes"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("📈 REPORTES Y ESTADÍSTICAS")
            
            print("1. Reporte general del sistema")
            print("2. Reporte de usuarios")
            print("3. Reporte de juegos")
            print("4. Reporte de cursos")
            print("5. Exportar datos")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.reporte_general()
            elif opcion == '2':
                self.reporte_usuarios()
            elif opcion == '3':
                self.reporte_juegos()
            elif opcion == '4':
                self.reporte_cursos()
            elif opcion == '5':
                self.exportar_datos()
    
    def reporte_general(self):
        """Reporte general del sistema"""
        self.limpiar_pantalla()
        self.mostrar_header("📊 REPORTE GENERAL DEL SISTEMA")
        
        # Contar todo
        self.cursor.execute("SELECT COUNT(*) FROM auth_user")
        total_usuarios = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM auth_user WHERE is_active = 1")
        usuarios_activos = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_curso")
        total_cursos = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_juego")
        total_juegos = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_partida")
        total_partidas = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_evaluacion")
        total_evaluaciones = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM core_leccion")
        total_lecciones = self.cursor.fetchone()[0]
        
        print(f"{Colors.BOLD}📊 Resumen del Sistema{Colors.END}")
        print(f"  👤 Usuarios: {total_usuarios} ({usuarios_activos} activos)")
        print(f"  📚 Cursos: {total_cursos}")
        print(f"  📖 Lecciones: {total_lecciones}")
        print(f"  📝 Evaluaciones: {total_evaluaciones}")
        print(f"  🎮 Juegos: {total_juegos}")
        print(f"  🎯 Partidas: {total_partidas}")
        
        input("\nPresiona Enter para continuar...")
    
    def reporte_usuarios(self):
        """Reporte de usuarios"""
        self.limpiar_pantalla()
        self.mostrar_header("👤 REPORTE DE USUARIOS")
        
        # Top usuarios por puntuación
        self.cursor.execute("""
            SELECT u.username, e.puntuacion_total, e.juegos_completados
            FROM auth_user u
            JOIN core_estadisticasusuario e ON e.usuario_id = u.id
            WHERE u.is_active = 1
            ORDER BY e.puntuacion_total DESC
            LIMIT 10
        """)
        
        top_usuarios = self.cursor.fetchall()
        
        print(f"{Colors.BOLD}🏆 Top 10 usuarios por puntuación{Colors.END}")
        if top_usuarios:
            print(f"{'Usuario':<20} {'Puntuación':<12} {'Juegos':<10}")
            print("-" * 45)
            for u in top_usuarios:
                print(f"{u[0]:<20} {u[1]:<12} {u[2]:<10}")
        else:
            print(f"{Colors.YELLOW}No hay datos disponibles{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def reporte_juegos(self):
        """Reporte de juegos"""
        self.limpiar_pantalla()
        self.mostrar_header("🎮 REPORTE DE JUEGOS")
        
        # Top juegos
        self.cursor.execute("""
            SELECT j.titulo, j.veces_jugado, j.tasa_aciertos
            FROM core_juego j
            WHERE j.activo = 1
            ORDER BY j.veces_jugado DESC
            LIMIT 10
        """)
        
        top_juegos = self.cursor.fetchall()
        
        print(f"{Colors.BOLD}🎮 Top 10 juegos más jugados{Colors.END}")
        if top_juegos:
            print(f"{'Juego':<30} {'Veces jugado':<15} {'Aciertos':<10}")
            print("-" * 55)
            for j in top_juegos:
                print(f"{j[0][:29]:<30} {j[1]:<15} {j[2]:<10}%")
        else:
            print(f"{Colors.YELLOW}No hay datos disponibles{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def reporte_cursos(self):
        """Reporte de cursos"""
        self.limpiar_pantalla()
        self.mostrar_header("📚 REPORTE DE CURSOS")
        
        self.cursor.execute("""
            SELECT c.titulo,
                   (SELECT COUNT(*) FROM core_leccion WHERE curso_id = c.id) as lecciones,
                   (SELECT COUNT(*) FROM core_evaluacion WHERE curso_id = c.id) as evaluaciones,
                   (SELECT COUNT(*) FROM core_progresocurso WHERE curso_id = c.id) as inscritos
            FROM core_curso c
            WHERE c.activo = 1
            ORDER BY c.id
        """)
        
        cursos = self.cursor.fetchall()
        
        if cursos:
            print(f"{'Curso':<30} {'Lecciones':<12} {'Evaluaciones':<14} {'Inscritos':<10}")
            print("-" * 70)
            for c in cursos:
                print(f"{c[0][:29]:<30} {c[1]:<12} {c[2]:<14} {c[3]:<10}")
        else:
            print(f"{Colors.YELLOW}No hay cursos disponibles{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def exportar_datos(self):
        """Exportar datos a JSON"""
        self.limpiar_pantalla()
        self.mostrar_header("📤 EXPORTAR DATOS")
        
        print("1. Exportar usuarios")
        print("2. Exportar juegos")
        print("3. Exportar cursos")
        print("4. Exportar todo")
        print("0. Volver")
        print()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == '0':
            return
        
        tabla = None
        if opcion == '1':
            tabla = 'auth_user'
        elif opcion == '2':
            tabla = 'core_juego'
        elif opcion == '3':
            tabla = 'core_curso'
        elif opcion == '4':
            self.exportar_todo()
            return
        
        if tabla:
            self.exportar_tabla(tabla)
    
    def exportar_tabla(self, tabla):
        """Exportar una tabla a JSON"""
        self.cursor.execute(f"SELECT * FROM {tabla}")
        data = self.cursor.fetchall()
        
        # Obtener nombres de columnas
        self.cursor.execute(f"DESCRIBE {tabla}")
        columns = [col[0] for col in self.cursor.fetchall()]
        
        filename = f"export_{tabla}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        result = []
        for row in data:
            result.append(dict(zip(columns, row)))
        
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n{Colors.GREEN}✅ Datos exportados a {filename}{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def exportar_todo(self):
        """Exportar todas las tablas"""
        tablas = ['auth_user', 'core_categoria', 'core_nivel', 'core_curso', 
                 'core_leccion', 'core_evaluacion', 'core_preguntaevaluacion',
                 'core_juego', 'core_partida', 'core_progreso', 
                 'core_estadisticasusuario']
        
        for tabla in tablas:
            self.exportar_tabla(tabla)
        
        print(f"\n{Colors.GREEN}✅ Todos los datos exportados{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 7. RESPALDO DE BASE DE DATOS
    # ============================================================
    
    def menu_respaldo(self):
        """Menú de respaldo"""
        self.limpiar_pantalla()
        self.mostrar_header("🗄️ RESPALDO DE BASE DE DATOS")
        
        print("1. Crear respaldo completo")
        print("2. Restaurar respaldo")
        print("3. Ver respaldos disponibles")
        print("0. Volver")
        print()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == '1':
            self.crear_respaldo()
        elif opcion == '2':
            self.restaurar_respaldo()
        elif opcion == '3':
            self.ver_respaldos()
    
    def crear_respaldo(self):
        """Crear respaldo de la base de datos"""
        self.limpiar_pantalla()
        self.mostrar_header("💾 CREAR RESPALDO")
        
        filename = f"respaldo_morphoplay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        
        os.system(f"mysqldump -u morphoplay_user -pmorphoplay_pass morphoplay_db > {filename}")
        
        if os.path.exists(filename):
            print(f"\n{Colors.GREEN}✅ Respaldo creado: {filename}{Colors.END}")
            print(f"  Tamaño: {os.path.getsize(filename) / 1024:.2f} KB")
        else:
            print(f"\n{Colors.RED}❌ Error al crear el respaldo{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def restaurar_respaldo(self):
        """Restaurar respaldo"""
        self.limpiar_pantalla()
        self.mostrar_header("🔄 RESTAURAR RESPALDO")
        
        self.ver_respaldos()
        
        filename = input("\nNombre del archivo a restaurar: ").strip()
        
        if not os.path.exists(filename):
            print(f"{Colors.RED}❌ Archivo no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        confirmar = input(f"¿Restaurar {filename}? (s/N): ").lower()
        if confirmar != 's':
            print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        os.system(f"mysql -u morphoplay_user -pmorphoplay_pass morphoplay_db < {filename}")
        
        print(f"\n{Colors.GREEN}✅ Respaldo restaurado exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def ver_respaldos(self):
        """Ver respaldos disponibles"""
        self.limpiar_pantalla()
        self.mostrar_header("📋 RESPALDOS DISPONIBLES")
        
        import glob
        respaldos = glob.glob("respaldo_morphoplay_*.sql")
        
        if not respaldos:
            print(f"{Colors.YELLOW}No hay respaldos disponibles{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'Archivo':<50} {'Tamaño':<10} {'Fecha':<20}")
        print("-" * 80)
        for r in sorted(respaldos, reverse=True):
            size = os.path.getsize(r) / 1024
            fecha = datetime.fromtimestamp(os.path.getmtime(r)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{r:<50} {size:.1f} KB  {fecha:<20}")
        
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # 8. HERRAMIENTAS DEL SISTEMA
    # ============================================================
    
    def menu_herramientas(self):
        """Menú de herramientas del sistema"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("🔧 HERRAMIENTAS DEL SISTEMA")
            
            print("1. Ver información del sistema")
            print("2. Ver conexiones activas")
            print("3. Optimizar tablas")
            print("4. Ver tamaño de la base de datos")
            print("0. Volver")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '1':
                self.info_sistema()
            elif opcion == '2':
                self.conexiones_activas()
            elif opcion == '3':
                self.optimizar_tablas()
            elif opcion == '4':
                self.tamano_db()
    
    def info_sistema(self):
        """Información del sistema"""
        self.limpiar_pantalla()
        self.mostrar_header("ℹ️ INFORMACIÓN DEL SISTEMA")
        
        import platform
        print(f"{Colors.BOLD}Sistema Operativo:{Colors.END} {platform.system()} {platform.release()}")
        print(f"{Colors.BOLD}Python:{Colors.END} {platform.python_version()}")
        print(f"{Colors.BOLD}MySQL:{Colors.END}")
        
        self.cursor.execute("SELECT VERSION()")
        version = self.cursor.fetchone()[0]
        print(f"  Versión: {version}")
        
        self.cursor.execute("SHOW VARIABLES LIKE 'max_connections'")
        max_conn = self.cursor.fetchone()[1]
        print(f"  Max conexiones: {max_conn}")
        
        self.cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
        conn_actual = self.cursor.fetchone()[1]
        print(f"  Conexiones actuales: {conn_actual}")
        
        input("\nPresiona Enter para continuar...")
    
    def conexiones_activas(self):
        """Ver conexiones activas"""
        self.limpiar_pantalla()
        self.mostrar_header("🔗 CONEXIONES ACTIVAS")
        
        self.cursor.execute("SHOW PROCESSLIST")
        procesos = self.cursor.fetchall()
        
        if procesos:
            print(f"{'ID':<8} {'Usuario':<15} {'Host':<20} {'Base de datos':<15} {'Comando':<12} {'Tiempo':<8} {'Estado':<20}")
            print("-" * 100)
            for p in procesos:
                print(f"{p[0]:<8} {p[1]:<15} {p[2][:19]:<20} {p[3] or '-':<15} {p[4]:<12} {p[5]:<8} {p[6] or '-':<20}")
        else:
            print(f"{Colors.YELLOW}No hay conexiones activas{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def optimizar_tablas(self):
        """Optimizar tablas"""
        self.limpiar_pantalla()
        self.mostrar_header("⚡ OPTIMIZAR TABLAS")
        
        self.cursor.execute("SHOW TABLES")
        tablas = self.cursor.fetchall()
        
        print("Optimizando tablas...")
        for tabla in tablas:
            self.cursor.execute(f"OPTIMIZE TABLE {tabla[0]}")
            print(f"  ✅ {tabla[0]}")
        
        self.connection.commit()
        print(f"\n{Colors.GREEN}✅ Tablas optimizadas exitosamente{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
    def tamano_db(self):
        """Ver tamaño de la base de datos"""
        self.limpiar_pantalla()
        self.mostrar_header("📊 TAMAÑO DE LA BASE DE DATOS")
        
        self.cursor.execute("""
            SELECT table_schema AS 'Database',
                   ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)',
                   ROUND(SUM(data_length) / 1024 / 1024, 2) AS 'Data (MB)',
                   ROUND(SUM(index_length) / 1024 / 1024, 2) AS 'Index (MB)'
            FROM information_schema.tables
            WHERE table_schema = 'morphoplay_db'
            GROUP BY table_schema
        """)
        
        datos = self.cursor.fetchone()
        
        if datos:
            print(f"{Colors.BOLD}Base de datos: {datos[0]}{Colors.END}")
            print(f"  Tamaño total: {datos[1]} MB")
            print(f"  Datos: {datos[2]} MB")
            print(f"  Índices: {datos[3]} MB")
        
        # Tamaño por tabla
        self.cursor.execute("""
            SELECT table_name,
                   ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
            FROM information_schema.tables
            WHERE table_schema = 'morphoplay_db'
            ORDER BY (data_length + index_length) DESC
        """)
        
        tablas = self.cursor.fetchall()
        
        if tablas:
            print(f"\n{Colors.BOLD}Tablas por tamaño:{Colors.END}")
            for t in tablas[:10]:
                print(f"  {t[0]}: {t[1]} MB")
        
        input("\nPresiona Enter para continuar...")
    
    # ============================================================
    # EJECUCIÓN PRINCIPAL
    # ============================================================
    
    def run(self):
        """Ejecutar el programa principal"""
        if not self.conectar_db():
            print(f"{Colors.RED}❌ No se pudo conectar a la base de datos{Colors.END}")
            return
        
        print(f"{Colors.GREEN}✅ Conectado a la base de datos{Colors.END}")
        
        while True:
            try:
                opcion = self.mostrar_menu_principal()
                
                if opcion == '1':
                    self.menu_usuarios()
                elif opcion == '2':
                    self.menu_cursos()
                elif opcion == '3':
                    self.menu_juegos()
                elif opcion == '4':
                    self.menu_evaluaciones()
                elif opcion == '5':
                    self.menu_partidas()
                elif opcion == '6':
                    self.menu_reportes()
                elif opcion == '7':
                    self.menu_respaldo()
                elif opcion == '8':
                    self.menu_herramientas()
                elif opcion == '9':
                    print(f"\n{Colors.GREEN}👋 ¡Hasta luego!{Colors.END}")
                    break
                else:
                    print(f"{Colors.YELLOW}⚠️ Opción inválida{Colors.END}")
                    self.pausa(1)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 ¡Hasta luego!{Colors.END}")
                break
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
                self.pausa(2)
        
        self.cerrar_db()

if __name__ == "__main__":
    app = MorphoPlayAdmin()
    app.run()
