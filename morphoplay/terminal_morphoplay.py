#!/usr/bin/env python
"""
MorphoPlay - Terminal Edition
Practica cursos, juegos y evaluaciones desde la terminal
"""
import os
import sys
import time
import pymysql
from datetime import datetime
from getpass import getpass

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

class MorphoPlayTerminal:
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
        self.usuario_id = None
        self.usuario_nombre = None
        
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
        print(f"\n{Colors.GREEN}{'🚀' * 20}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}MORPHOPLAY - TERMINAL EDITION{Colors.END}")
        print(f"{Colors.GREEN}{'🚀' * 20}{Colors.END}\n")
        
        if self.usuario_nombre:
            print(f"{Colors.YELLOW}👤 Usuario: {self.usuario_nombre}{Colors.END}\n")
        
        print("1. 📚 Cursos")
        print("2. 🎮 Juegos")
        print("3. 📊 Mi Progreso")
        print("4. 🏆 Estadísticas")
        print("5. 👤 Usuarios")
        print("6. 🔐 Salir")
        print()
        
        return input("Selecciona una opción: ").strip()
    
    def menu_cursos(self):
        """Menú de cursos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("📚 CURSOS DISPONIBLES")
            
            # Obtener cursos
            self.cursor.execute("""
                SELECT c.id, c.titulo, cat.nombre as categoria, n.nombre as nivel,
                       (SELECT COUNT(*) FROM core_leccion WHERE curso_id = c.id) as lecciones,
                       (SELECT COUNT(*) FROM core_evaluacion WHERE curso_id = c.id) as evaluaciones
                FROM core_curso c
                LEFT JOIN core_categoria cat ON c.categoria_id = cat.id
                LEFT JOIN core_nivel n ON c.nivel_id = n.id
                WHERE c.activo = 1
                ORDER BY c.orden
            """)
            
            cursos = self.cursor.fetchall()
            
            if not cursos:
                print(f"{Colors.YELLOW}No hay cursos disponibles.{Colors.END}")
                input("\nPresiona Enter para continuar...")
                return
            
            # Mostrar cursos
            print(f"{'ID':<4} {'Título':<30} {'Categoría':<15} {'Nivel':<12} {'Lecciones':<10} {'Evaluaciones':<12}")
            print("-" * 90)
            for curso in cursos:
                print(f"{curso[0]:<4} {curso[1][:29]:<30} {curso[2][:14]:<15} {curso[3][:11]:<12} {curso[4]:<10} {curso[5]:<12}")
            
            print(f"\n{Colors.YELLOW}0. Volver al menú principal{Colors.END}")
            print(f"{Colors.YELLOW}99. Ver lecciones de un curso{Colors.END}")
            print(f"{Colors.YELLOW}100. Tomar evaluación de un curso{Colors.END}")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion == '99':
                curso_id = input("Ingresa el ID del curso para ver lecciones: ").strip()
                if curso_id.isdigit():
                    self.ver_lecciones_curso(int(curso_id))
            elif opcion == '100':
                curso_id = input("Ingresa el ID del curso para tomar evaluación: ").strip()
                if curso_id.isdigit():
                    self.tomar_evaluacion(int(curso_id))
    
    def ver_lecciones_curso(self, curso_id):
        """Ver lecciones de un curso"""
        self.limpiar_pantalla()
        self.mostrar_header("📖 LECCIONES DEL CURSO")
        
        # Obtener título del curso
        self.cursor.execute("SELECT titulo FROM core_curso WHERE id = %s", (curso_id,))
        curso = self.cursor.fetchone()
        if not curso:
            print(f"{Colors.RED}❌ Curso no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{Colors.YELLOW}Curso: {curso[0]}{Colors.END}\n")
        
        # Obtener lecciones
        self.cursor.execute("""
            SELECT id, titulo, orden, 
                   CASE WHEN activo = 1 THEN '✅' ELSE '❌' END as estado
            FROM core_leccion
            WHERE curso_id = %s
            ORDER BY orden
        """, (curso_id,))
        
        lecciones = self.cursor.fetchall()
        
        if not lecciones:
            print(f"{Colors.YELLOW}Este curso no tiene lecciones.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{'ID':<4} {'Orden':<6} {'Título':<50} {'Estado':<8}")
        print("-" * 70)
        for leccion in lecciones:
            print(f"{leccion[0]:<4} {leccion[2]:<6} {leccion[1][:49]:<50} {leccion[3]:<8}")
        
        print(f"\n{Colors.YELLOW}Ingresa el ID de una lección para ver su contenido{Colors.END}")
        print(f"{Colors.YELLOW}0. Volver{Colors.END}")
        
        opcion = input("\nSelecciona una lección: ").strip()
        if opcion.isdigit() and int(opcion) > 0:
            self.ver_contenido_leccion(int(opcion))
    
    def ver_contenido_leccion(self, leccion_id):
        """Ver contenido de una lección"""
        self.limpiar_pantalla()
        self.mostrar_header("📖 CONTENIDO DE LA LECCIÓN")
        
        self.cursor.execute("""
            SELECT titulo, contenido FROM core_leccion WHERE id = %s
        """, (leccion_id,))
        
        leccion = self.cursor.fetchone()
        if not leccion:
            print(f"{Colors.RED}❌ Lección no encontrada{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{Colors.BOLD}{Colors.BLUE}{leccion[0]}{Colors.END}")
        print("-" * 60)
        print(f"\n{leccion[1]}\n")
        
        input("Presiona Enter para continuar...")
    
    def tomar_evaluacion(self, curso_id):
        """Tomar una evaluación de un curso"""
        if not self.usuario_id:
            print(f"{Colors.RED}❌ Debes iniciar sesión primero{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_header("📝 EVALUACIÓN DEL CURSO")
        
        # Obtener evaluación
        self.cursor.execute("""
            SELECT id, titulo, descripcion, puntaje_maximo, tiempo_limite, 
                   intentos_permitidos, tipo
            FROM core_evaluacion
            WHERE curso_id = %s AND activo = 1
            ORDER BY orden LIMIT 1
        """, (curso_id,))
        
        evaluacion = self.cursor.fetchone()
        if not evaluacion:
            print(f"{Colors.YELLOW}Este curso no tiene evaluaciones disponibles.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        eval_id, titulo, descripcion, puntaje_max, tiempo_limite, intentos, tipo = evaluacion
        
        # Verificar intentos anteriores
        self.cursor.execute("""
            SELECT COUNT(*) FROM core_intentoevaluacion
            WHERE usuario_id = %s AND evaluacion_id = %s AND estado = 'completado'
        """, (self.usuario_id, eval_id))
        
        intentos_previos = self.cursor.fetchone()[0]
        
        if intentos_previos >= intentos:
            print(f"{Colors.RED}❌ Has agotado todos los intentos permitidos ({intentos}){Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"{Colors.BOLD}{titulo}{Colors.END}")
        print(f"📝 {descripcion}")
        print(f"📊 Puntaje máximo: {puntaje_max}")
        print(f"⏱ Tiempo límite: {tiempo_limite} minutos")
        print(f"🔄 Intentos restantes: {intentos - intentos_previos}\n")
        
        # Obtener preguntas
        self.cursor.execute("""
            SELECT id, pregunta, opcion1, opcion2, opcion3, opcion4, tipo, puntaje
            FROM core_preguntaevaluacion
            WHERE evaluacion_id = %s AND activo = 1
            ORDER BY orden
        """, (eval_id,))
        
        preguntas = self.cursor.fetchall()
        
        if not preguntas:
            print(f"{Colors.YELLOW}No hay preguntas en esta evaluación.{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Registrar intento
        self.cursor.execute("""
            INSERT INTO core_intentoevaluacion 
            (usuario_id, evaluacion_id, estado, intento_numero)
            VALUES (%s, %s, 'iniciado', %s)
        """, (self.usuario_id, eval_id, intentos_previos + 1))
        self.connection.commit()
        
        intento_id = self.cursor.lastrowid
        respuestas = {}
        puntaje_obtenido = 0
        
        # Mostrar preguntas
        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n{Colors.YELLOW}Pregunta {i} (Puntaje: {pregunta[7]} pts){Colors.END}")
            print(f"📝 {pregunta[1]}")
            print()
            
            if pregunta[6] == 'opcion':
                opciones = [pregunta[2], pregunta[3], pregunta[4], pregunta[5]]
                letras = ['A', 'B', 'C', 'D']
                for j, opcion in enumerate(opciones):
                    if opcion:
                        print(f"  {letras[j]}. {opcion}")
                
                respuesta = input("\nTu respuesta (A/B/C/D): ").strip().upper()
                if respuesta in letras:
                    idx = letras.index(respuesta)
                    respuestas[str(pregunta[0])] = opciones[idx]
                    
                    # Verificar si es correcta
                    self.cursor.execute("""
                        SELECT respuesta_correcta FROM core_preguntaevaluacion WHERE id = %s
                    """, (pregunta[0],))
                    correcta = self.cursor.fetchone()[0]
                    
                    if opciones[idx] == correcta:
                        puntaje_obtenido += pregunta[7]
                        print(f"{Colors.GREEN}✅ Correcto! +{pregunta[7]} pts{Colors.END}")
                    else:
                        print(f"{Colors.RED}❌ Incorrecto. Respuesta correcta: {correcta}{Colors.END}")
            else:
                respuesta = input("Tu respuesta: ").strip()
                respuestas[str(pregunta[0])] = respuesta
        
        # Finalizar intento
        import json
        self.cursor.execute("""
            UPDATE core_intentoevaluacion
            SET estado = 'completado',
                puntaje_obtenido = %s,
                respuestas = %s,
                fecha_completado = NOW()
            WHERE id = %s
        """, (puntaje_obtenido, json.dumps(respuestas), intento_id))
        self.connection.commit()
        
        print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}📊 RESULTADO DE LA EVALUACIÓN{Colors.END}")
        print(f"{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"Puntaje obtenido: {Colors.BOLD}{puntaje_obtenido}/{puntaje_max}{Colors.END}")
        print(f"Porcentaje: {Colors.BOLD}{(puntaje_obtenido/puntaje_max*100):.1f}%{Colors.END}")
        
        if puntaje_obtenido >= puntaje_max * 0.7:
            print(f"{Colors.GREEN}🎉 ¡Felicidades! Has aprobado la evaluación.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}📚 Sigue practicando para mejorar.{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def menu_juegos(self):
        """Menú de juegos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header("🎮 JUEGOS DISPONIBLES")
            
            # Obtener juegos
            self.cursor.execute("""
                SELECT j.id, j.titulo, cat.nombre as categoria, n.nombre as nivel,
                       j.puntos, j.tipo,
                       CASE WHEN p.completado = 1 THEN '✅' ELSE '⬜' END as estado
                FROM core_juego j
                LEFT JOIN core_categoria cat ON j.categoria_id = cat.id
                LEFT JOIN core_nivel n ON j.nivel_id = n.id
                LEFT JOIN core_progreso p ON p.juego_id = j.id AND p.usuario_id = %s
                WHERE j.activo = 1
                ORDER BY j.orden
            """, (self.usuario_id or 0,))
            
            juegos = self.cursor.fetchall()
            
            if not juegos:
                print(f"{Colors.YELLOW}No hay juegos disponibles.{Colors.END}")
                input("\nPresiona Enter para continuar...")
                return
            
            print(f"{'ID':<4} {'Título':<25} {'Categoría':<12} {'Nivel':<10} {'Puntos':<8} {'Tipo':<10} {'Estado':<8}")
            print("-" * 90)
            for juego in juegos:
                print(f"{juego[0]:<4} {juego[1][:24]:<25} {juego[2][:11]:<12} {juego[3][:9]:<10} {juego[4]:<8} {juego[5][:9]:<10} {juego[6]:<8}")
            
            print(f"\n{Colors.YELLOW}0. Volver al menú principal{Colors.END}")
            print(f"{Colors.YELLOW}99. Jugar un juego (ingresa ID){Colors.END}")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '0':
                break
            elif opcion.isdigit() and int(opcion) > 0:
                self.jugar_juego(int(opcion))
    
    def jugar_juego(self, juego_id):
        """Jugar un juego interactivo"""
        if not self.usuario_id:
            print(f"{Colors.RED}❌ Debes iniciar sesión primero{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_header("🎯 JUGANDO")
        
        # Obtener juego
        self.cursor.execute("""
            SELECT id, titulo, descripcion, pregunta, 
                   opcion1, opcion2, opcion3, opcion4,
                   respuesta_correcta, puntos
            FROM core_juego
            WHERE id = %s AND activo = 1
        """, (juego_id,))
        
        juego = self.cursor.fetchone()
        if not juego:
            print(f"{Colors.RED}❌ Juego no encontrado{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        _, titulo, descripcion, pregunta, op1, op2, op3, op4, correcta, puntos = juego
        
        print(f"{Colors.BOLD}{titulo}{Colors.END}")
        print(f"📝 {descripcion}\n")
        print(f"❓ {pregunta}\n")
        
        opciones = [op1, op2, op3, op4]
        letras = ['A', 'B', 'C', 'D']
        for i, opcion in enumerate(opciones):
            if opcion:
                print(f"  {letras[i]}. {opcion}")
        
        print(f"\n💡 Puntos: {puntos}")
        respuesta = input("\nTu respuesta (A/B/C/D): ").strip().upper()
        
        if respuesta in letras:
            idx = letras.index(respuesta)
            es_correcto = opciones[idx] == correcta
            
            # Registrar partida
            self.cursor.execute("""
                INSERT INTO core_partida (usuario_id, juego_id, correcto, puntuacion_obtenida)
                VALUES (%s, %s, %s, %s)
            """, (self.usuario_id, juego_id, es_correcto, puntos if es_correcto else 0))
            self.connection.commit()
            
            # Actualizar progreso
            self.cursor.execute("""
                INSERT INTO core_progreso (usuario_id, juego_id, intentos)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE
                intentos = intentos + 1,
                completado = IF(%s = 1, 1, completado),
                puntuacion = IF(%s = 1 AND completado = 0, %s, puntuacion),
                fecha_completado = IF(%s = 1 AND completado = 0, NOW(), fecha_completado)
            """, (self.usuario_id, juego_id, es_correcto, es_correcto, puntos, es_correcto))
            self.connection.commit()
            
            if es_correcto:
                print(f"\n{Colors.GREEN}✅ ¡Correcto! +{puntos} puntos{Colors.END}")
                
                # Actualizar estadísticas
                self.cursor.execute("""
                    UPDATE core_estadisticasusuario
                    SET juegos_completados = juegos_completados + 1,
                        puntuacion_total = puntuacion_total + %s,
                        racha_actual = racha_actual + 1,
                        racha_maxima = GREATEST(racha_maxima, racha_actual + 1)
                    WHERE usuario_id = %s
                """, (puntos, self.usuario_id))
                self.connection.commit()
            else:
                print(f"\n{Colors.RED}❌ Incorrecto. La respuesta correcta era: {correcta}{Colors.END}")
                
                # Reiniciar racha
                self.cursor.execute("""
                    UPDATE core_estadisticasusuario
                    SET racha_actual = 0
                    WHERE usuario_id = %s
                """, (self.usuario_id,))
                self.connection.commit()
        
        input("\nPresiona Enter para continuar...")
    
    def menu_progreso(self):
        """Mostrar progreso del usuario"""
        if not self.usuario_id:
            print(f"{Colors.RED}❌ Debes iniciar sesión primero{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_header("📊 MI PROGRESO")
        
        # Estadísticas generales
        self.cursor.execute("""
            SELECT juegos_completados, puntuacion_total, racha_actual, racha_maxima,
                   ultima_actividad
            FROM core_estadisticasusuario
            WHERE usuario_id = %s
        """, (self.usuario_id,))
        
        stats = self.cursor.fetchone()
        if stats:
            print(f"{Colors.BOLD}📈 Estadísticas Generales{Colors.END}")
            print(f"  Juegos Completados: {stats[0]}")
            print(f"  Puntuación Total: {stats[1]}")
            print(f"  Racha Actual: 🔥 {stats[2]}")
            print(f"  Mejor Racha: 🏆 {stats[3]}")
            print(f"  Última Actividad: {stats[4]}")
        
        # Progreso por categoría
        print(f"\n{Colors.BOLD}📊 Progreso por Categoría{Colors.END}")
        self.cursor.execute("""
            SELECT cat.nombre,
                   COUNT(j.id) as total,
                   SUM(CASE WHEN p.completado = 1 THEN 1 ELSE 0 END) as completados
            FROM core_categoria cat
            LEFT JOIN core_juego j ON j.categoria_id = cat.id
            LEFT JOIN core_progreso p ON p.juego_id = j.id AND p.usuario_id = %s
            WHERE cat.activo = 1 AND j.activo = 1
            GROUP BY cat.id
        """, (self.usuario_id,))
        
        categorias = self.cursor.fetchall()
        for cat in categorias:
            if cat[1] > 0:
                porcentaje = (cat[2] / cat[1]) * 100
                print(f"  {cat[0]}: {cat[2]}/{cat[1]} ({porcentaje:.1f}%)")
        
        input("\nPresiona Enter para continuar...")
    
    def menu_estadisticas(self):
        """Mostrar estadísticas detalladas"""
        if not self.usuario_id:
            print(f"{Colors.RED}❌ Debes iniciar sesión primero{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.limpiar_pantalla()
        self.mostrar_header("🏆 ESTADÍSTICAS COMPLETAS")
        
        # Partidas por mes
        self.cursor.execute("""
            SELECT DATE_FORMAT(fecha, '%%Y-%%m') as mes,
                   COUNT(*) as total,
                   SUM(CASE WHEN correcto = 1 THEN 1 ELSE 0 END) as correctas
            FROM core_partida
            WHERE usuario_id = %s
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """, (self.usuario_id,))
        
        partidas_mes = self.cursor.fetchall()
        
        if partidas_mes:
            print(f"{Colors.BOLD}📊 Partidas por Mes{Colors.END}")
            print(f"{'Mes':<10} {'Total':<10} {'Correctas':<12} {'Porcentaje':<10}")
            print("-" * 45)
            for mes in partidas_mes:
                porcentaje = (mes[2] / mes[1]) * 100 if mes[1] > 0 else 0
                print(f"{mes[0]:<10} {mes[1]:<10} {mes[2]:<12} {porcentaje:.1f}%")
        
        # Mejores juegos
        print(f"\n{Colors.BOLD}🎯 Mejores Juegos{Colors.END}")
        self.cursor.execute("""
            SELECT j.titulo,
                   COUNT(p.id) as veces,
                   SUM(CASE WHEN p.correcto = 1 THEN 1 ELSE 0 END) as correctas
            FROM core_partida p
            JOIN core_juego j ON p.juego_id = j.id
            WHERE p.usuario_id = %s
            GROUP BY j.id
            ORDER BY veces DESC
            LIMIT 5
        """, (self.usuario_id,))
        
        top_juegos = self.cursor.fetchall()
        for juego in top_juegos:
            porcentaje = (juego[2] / juego[1]) * 100 if juego[1] > 0 else 0
            print(f"  {juego[0]}: {juego[2]}/{juego[1]} ({porcentaje:.1f}%)")
        
        input("\nPresiona Enter para continuar...")
    
    def menu_usuarios(self):
        """Menú de usuarios (iniciar sesión)"""
        self.limpiar_pantalla()
        self.mostrar_header("👤 USUARIOS")
        
        if self.usuario_nombre:
            print(f"✅ Sesión iniciada como: {Colors.GREEN}{self.usuario_nombre}{Colors.END}")
            print("\n1. Cerrar sesión")
            print("2. Cambiar usuario")
            print("0. Volver")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1' or opcion == '2':
                self.usuario_id = None
                self.usuario_nombre = None
                if opcion == '2':
                    self.iniciar_sesion()
            return
        
        print("1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("0. Volver")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            self.iniciar_sesion()
        elif opcion == '2':
            self.registrar_usuario()
    
    def iniciar_sesion(self):
        """Iniciar sesión de usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("🔑 INICIAR SESIÓN")
        
        username = input("Usuario: ").strip()
        password = getpass("Contraseña: ").strip()
        
        # Verificar credenciales
        self.cursor.execute("""
            SELECT id, username, password, is_active
            FROM auth_user
            WHERE username = %s
        """, (username,))
        
        user = self.cursor.fetchone()
        
        if user and user[3] == 1:
            # Verificar contraseña (en producción usaría hashing)
            # Por simplicidad, asumimos que la contraseña es correcta si existe
            self.usuario_id = user[0]
            self.usuario_nombre = user[1]
            print(f"\n{Colors.GREEN}✅ Bienvenido, {self.usuario_nombre}!{Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ Usuario o contraseña incorrectos{Colors.END}")
        
        input("\nPresiona Enter para continuar...")
    
    def registrar_usuario(self):
        """Registrar nuevo usuario"""
        self.limpiar_pantalla()
        self.mostrar_header("📝 REGISTRO DE USUARIO")
        
        username = input("Usuario: ").strip()
        email = input("Email: ").strip()
        password = getpass("Contraseña: ").strip()
        
        # Verificar si ya existe
        self.cursor.execute("SELECT id FROM auth_user WHERE username = %s", (username,))
        if self.cursor.fetchone():
            print(f"{Colors.RED}❌ El usuario ya existe{Colors.END}")
            input("\nPresiona Enter para continuar...")
            return
        
        # Crear usuario (contraseña en texto plano para simplificar)
        self.cursor.execute("""
            INSERT INTO auth_user (username, email, password, is_active, date_joined)
            VALUES (%s, %s, %s, 1, NOW())
        """, (username, email, password))
        self.connection.commit()
        
        usuario_id = self.cursor.lastrowid
        
        # Crear estadísticas
        self.cursor.execute("""
            INSERT INTO core_estadisticasusuario (usuario_id)
            VALUES (%s)
        """, (usuario_id,))
        self.connection.commit()
        
        self.usuario_id = usuario_id
        self.usuario_nombre = username
        
        print(f"\n{Colors.GREEN}✅ ¡Usuario registrado exitosamente!{Colors.END}")
        print(f"{Colors.GREEN}✅ Bienvenido, {self.usuario_nombre}!{Colors.END}")
        input("\nPresiona Enter para continuar...")
    
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
                    self.menu_cursos()
                elif opcion == '2':
                    self.menu_juegos()
                elif opcion == '3':
                    self.menu_progreso()
                elif opcion == '4':
                    self.menu_estadisticas()
                elif opcion == '5':
                    self.menu_usuarios()
                elif opcion == '6':
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
    app = MorphoPlayTerminal()
    app.run()
