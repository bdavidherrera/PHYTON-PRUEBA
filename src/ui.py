# src/ui.py - Versión completa con editar y eliminar
from typing import List 
from datetime import datetime
from src.modelos import Estudiante, Curso, Inscripcion, Matricula
from src.validaciones import validar_estudiante_completo, validar_fecha, validar_creditos, validar_nota, validar_correo
from src.consultas import ConsultasAcademicas

class InterfazUsuario:
    """Interfaz de usuario para el sistema MiniSIGA"""
    
    def __init__(self, estudiantes: List[Estudiante], cursos: List[Curso], 
                 inscripciones: List[Inscripcion], matriculas: List[Matricula]):
        self.estudiantes = estudiantes
        self.cursos = cursos
        self.inscripciones = inscripciones
        self.matriculas = matriculas
        self.consultas = ConsultasAcademicas(estudiantes, cursos, inscripciones, matriculas)
        self.limite_creditos = 20
    
    def generar_siguiente_id(self, tipo: str) -> str:
        """Genera el siguiente ID autoincremental para cada tipo de entidad"""
        if tipo == "estudiante":
            max_num = 0
            for est in self.estudiantes:
                if est.id.startswith("E") and est.id[1:].isdigit():
                    num = int(est.id[1:])
                    max_num = max(max_num, num)
            return f"E{max_num + 1}"
        
        elif tipo == "curso":
            max_num = 0
            for curso in self.cursos:
                if curso.codigo.startswith("C") and curso.codigo[1:].isdigit():
                    num = int(curso.codigo[1:])
                    max_num = max(max_num, num)
            return f"C{max_num + 1}"
        
        elif tipo == "inscripcion":
            max_num = 0
            for insc in self.inscripciones:
                if insc.id.startswith("I") and insc.id[1:].isdigit():
                    num = int(insc.id[1:])
                    max_num = max(max_num, num)
            return f"I{max_num + 1}"
        
        elif tipo == "matricula":
            max_num = 0
            for mat in self.matriculas:
                if mat.id.startswith("M") and mat.id[1:].isdigit():
                    num = int(mat.id[1:])
                    max_num = max(max_num, num)
            return f"M{max_num + 1}"
        
        return "ID1"
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema"""
        print("\n" + "="*50)
        print("           MINISIGA - SISTEMA ACADÉMICO")
        print("="*50)
        print("1. Estudiantes")
        print("2. Cursos") 
        print("3. Inscripciones")
        print("4. Matrículas")
        print("5. Consultas/Reportes")
        print("6. Exportar JSON")
        print("0. Salir")
        print("="*50)
    
    def mostrar_menu_estudiantes(self):
        """Muestra el menú de gestión de estudiantes"""
        print("\n--- GESTIÓN DE ESTUDIANTES ---")
        print("1. Crear estudiante")
        print("2. Editar estudiante")
        print("3. Eliminar estudiante")
        print("4. Listar estudiantes")
        print("0. Volver al menú principal")
    
    def mostrar_menu_cursos(self):
        """Muestra el menú de gestión de cursos"""
        print("\n--- GESTIÓN DE CURSOS ---")
        print("1. Crear curso")
        print("2. Editar curso")
        print("3. Eliminar curso")
        print("4. Listar cursos")
        print("0. Volver al menú principal")
    
    def mostrar_menu_inscripciones(self):
        """Muestra el menú de gestión de inscripciones"""
        print("\n--- GESTIÓN DE INSCRIPCIONES ---")
        print("1. Crear inscripción")
        print("2. Editar inscripción")
        print("3. Eliminar inscripción")
        print("4. Listar inscripciones")
        print("5. Ver inscripciones pendientes de matrícula")
        print("0. Volver al menú principal")
    
    def mostrar_menu_matriculas(self):
        """Muestra el menú de gestión de matrículas"""
        print("\n--- GESTIÓN DE MATRÍCULAS ---")
        print("1. Crear matrícula (desde inscripción)")
        print("2. Asignar nota")
        print("3. Eliminar matrícula")
        print("4. Listar matrículas")
        print("0. Volver al menú principal")
    
    def mostrar_menu_consultas(self):
        """Muestra el menú de consultas y reportes"""
        print("\n--- CONSULTAS Y REPORTES ---")
        print("1. Buscar estudiante por documento")
        print("2. Buscar estudiante por correo")
        print("3. Listar estudiantes ordenados por apellido")
        print("4. Top 3 promedios por curso")
        print("5. Estudiantes reprobados")
        print("6. Créditos inscritos por estudiante")
        print("7. Dominios de correo únicos")
        print("8. Búsqueda binaria por apellido")
        print("0. Volver al menú principal")
    
    def crear_estudiante(self):
        """Interfaz para crear un nuevo estudiante"""
        print("\n--- CREAR NUEVO ESTUDIANTE ---")
        
        datos = {}
        
        # Validar documento inmediatamente
        while True:
            documento = input("Documento: ").strip()
            if not documento:
                print("❌ Error: El documento es obligatorio")
                continue
            if not documento.isdigit() or not (6 <= len(documento) <= 15):
                print("❌ Error: El documento debe contener solo números y tener entre 6-15 dígitos")
                continue
            
            # Verificar duplicado
            documento_existe = any(est.documento == documento for est in self.estudiantes)
            if documento_existe:
                print(f"❌ Error: Ya existe un estudiante con documento {documento}")
                continue
            
            datos['documento'] = documento
            break
        
        # Validar nombres inmediatamente
        while True:
            nombres = input("Nombres: ").strip()
            if not nombres:
                print("❌ Error: Los nombres son obligatorios")
                continue
            datos['nombres'] = nombres
            break
        
        # Validar apellidos inmediatamente
        while True:
            apellidos = input("Apellidos: ").strip()
            if not apellidos:
                print("❌ Error: Los apellidos son obligatorios")
                continue
            datos['apellidos'] = apellidos
            break
        
        # Validar correo inmediatamente
        while True:
            correo = input("Correo electrónico: ").strip()
            if not correo:
                print("❌ Error: El correo es obligatorio")
                continue
            if not validar_correo(correo):
                print("❌ Error: El formato del correo no es válido")
                continue
            
            # Verificar duplicado
            correo_existe = any(est.correo.lower() == correo.lower() for est in self.estudiantes)
            if correo_existe:
                print(f"❌ Error: Ya existe un estudiante con correo {correo}")
                continue
            
            datos['correo'] = correo
            break
        
        # Validar fecha de nacimiento inmediatamente
        while True:
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            if not fecha_nacimiento:
                print("❌ Error: La fecha de nacimiento es obligatoria")
                continue
            if not validar_fecha(fecha_nacimiento):
                print("❌ Error: La fecha debe estar en formato YYYY-MM-DD")
                continue
            
            # Validar edad mínima
            from src.validaciones import validar_edad_minima
            if not validar_edad_minima(fecha_nacimiento, 10):
                print("❌ Error: El estudiante debe tener al menos 10 años de edad")
                continue
            
            datos['fecha_nacimiento'] = fecha_nacimiento
            break
        
        # Crear estudiante
        nuevo_id = self.generar_siguiente_id("estudiante")
        nuevo_estudiante = Estudiante(
            id=nuevo_id,
            documento=datos['documento'],
            nombres=datos['nombres'],
            apellidos=datos['apellidos'],
            correo=datos['correo'],
            fecha_nacimiento=datos['fecha_nacimiento']
        )
        
        self.estudiantes.append(nuevo_estudiante)
        print(f"✅ Estudiante creado exitosamente con ID: {nuevo_id}")
        return True
    
    def editar_estudiante(self):
        """Interfaz para editar un estudiante existente"""
        print("\n--- EDITAR ESTUDIANTE ---")
        
        if not self.estudiantes:
            print("❌ No hay estudiantes registrados.")
            return False
        
        # Mostrar estudiantes disponibles
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return False
            
            estudiante_a_editar = self.estudiantes[indice]
            
            print(f"\n--- EDITANDO: {estudiante_a_editar.nombre_completo()} ---")
            print("⚠️  NOTA: El ID del estudiante no se puede modificar")
            print("Ingrese los nuevos datos (presione Enter para mantener el valor actual):")
            
            # Validar documento con verificación inmediata
            while True:
                print(f"Documento actual: {estudiante_a_editar.documento}")
                nuevo_documento = input("Nuevo documento (Enter para mantener): ").strip()
                if not nuevo_documento:
                    nuevo_documento = estudiante_a_editar.documento
                    break
                
                if not nuevo_documento.isdigit() or not (6 <= len(nuevo_documento) <= 15):
                    print("❌ Error: El documento debe contener solo números y tener entre 6-15 dígitos")
                    continue
                
                # Verificar duplicado (excluyendo el estudiante actual)
                documento_existe = any(est.documento == nuevo_documento and est.id != estudiante_a_editar.id 
                                     for est in self.estudiantes)
                if documento_existe:
                    print(f"❌ Error: Ya existe otro estudiante con documento {nuevo_documento}")
                    continue
                
                break
            
            # Validar nombres con verificación inmediata
            while True:
                print(f"Nombres actuales: {estudiante_a_editar.nombres}")
                nuevos_nombres = input("Nuevos nombres (Enter para mantener): ").strip()
                if not nuevos_nombres:
                    nuevos_nombres = estudiante_a_editar.nombres
                    break
                if nuevos_nombres:
                    break
                print("❌ Error: Los nombres no pueden estar vacíos")
            
            # Validar apellidos con verificación inmediata
            while True:
                print(f"Apellidos actuales: {estudiante_a_editar.apellidos}")
                nuevos_apellidos = input("Nuevos apellidos (Enter para mantener): ").strip()
                if not nuevos_apellidos:
                    nuevos_apellidos = estudiante_a_editar.apellidos
                    break
                if nuevos_apellidos:
                    break
                print("❌ Error: Los apellidos no pueden estar vacíos")
            
            # Validar correo con verificación inmediata
            while True:
                print(f"Correo actual: {estudiante_a_editar.correo}")
                nuevo_correo = input("Nuevo correo (Enter para mantener): ").strip()
                if not nuevo_correo:
                    nuevo_correo = estudiante_a_editar.correo
                    break
                
                if not validar_correo(nuevo_correo):
                    print("❌ Error: El formato del correo no es válido")
                    continue
                
                # Verificar duplicado (excluyendo el estudiante actual)
                correo_existe = any(est.correo.lower() == nuevo_correo.lower() and est.id != estudiante_a_editar.id 
                                  for est in self.estudiantes)
                if correo_existe:
                    print(f"❌ Error: Ya existe otro estudiante con correo {nuevo_correo}")
                    continue
                
                break
            
            # Validar fecha de nacimiento con verificación inmediata
            while True:
                print(f"Fecha de nacimiento actual: {estudiante_a_editar.fecha_nacimiento}")
                nueva_fecha = input("Nueva fecha de nacimiento (YYYY-MM-DD, Enter para mantener): ").strip()
                if not nueva_fecha:
                    nueva_fecha = estudiante_a_editar.fecha_nacimiento
                    break
                
                if not validar_fecha(nueva_fecha):
                    print("❌ Error: La fecha debe estar en formato YYYY-MM-DD")
                    continue
                
                # Validar edad mínima
                from src.validaciones import validar_edad_minima
                if not validar_edad_minima(nueva_fecha, 10):
                    print("❌ Error: El estudiante debe tener al menos 10 años de edad")
                    continue
                
                break
            
            # Actualizar estudiante
            estudiante_a_editar.documento = nuevo_documento
            estudiante_a_editar.nombres = nuevos_nombres
            estudiante_a_editar.apellidos = nuevos_apellidos
            estudiante_a_editar.correo = nuevo_correo
            estudiante_a_editar.fecha_nacimiento = nueva_fecha
            
            print("✅ Estudiante actualizado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_estudiante(self):
        """Interfaz para eliminar un estudiante"""
        print("\n--- ELIMINAR ESTUDIANTE ---")
        
        if not self.estudiantes:
            print("❌ No hay estudiantes registrados.")
            return False
        
        # Mostrar estudiantes disponibles
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return False
            
            estudiante_a_eliminar = self.estudiantes[indice]
            
            # Verificar si tiene inscripciones o matrículas
            tiene_inscripciones = any(i.estudiante_id == estudiante_a_eliminar.id for i in self.inscripciones)
            tiene_matriculas = any(m.estudiante_id == estudiante_a_eliminar.id for m in self.matriculas)
            
            if tiene_inscripciones or tiene_matriculas:
                print(f"⚠️  ADVERTENCIA: El estudiante {estudiante_a_eliminar.nombre_completo()} tiene registros asociados:")
                if tiene_inscripciones:
                    inscripciones_count = len([i for i in self.inscripciones if i.estudiante_id == estudiante_a_eliminar.id])
                    print(f"  • {inscripciones_count} inscripciones activas")
                if tiene_matriculas:
                    matriculas_count = len([m for m in self.matriculas if m.estudiante_id == estudiante_a_eliminar.id])
                    print(f"  • {matriculas_count} matrículas registradas")
                
                confirmar = input("Se eliminarán automáticamente todos sus registros. ¿Continuar? (s/N): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada")
                    return False
            
            # Eliminar inscripciones asociadas
            inscripciones_eliminadas = len([i for i in self.inscripciones if i.estudiante_id == estudiante_a_eliminar.id])
            self.inscripciones = [i for i in self.inscripciones if i.estudiante_id != estudiante_a_eliminar.id]
            
            # Eliminar matrículas asociadas
            matriculas_eliminadas = len([m for m in self.matriculas if m.estudiante_id == estudiante_a_eliminar.id])
            self.matriculas = [m for m in self.matriculas if m.estudiante_id != estudiante_a_eliminar.id]
            
            # Eliminar estudiante
            self.estudiantes.remove(estudiante_a_eliminar)
            print(f"✅ Estudiante {estudiante_a_eliminar.nombre_completo()} eliminado exitosamente")
            if inscripciones_eliminadas > 0:
                print(f"  • {inscripciones_eliminadas} inscripciones eliminadas")
            if matriculas_eliminadas > 0:
                print(f"  • {matriculas_eliminadas} matrículas eliminadas")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_estudiantes(self):
            """Lista todos los estudiantes con sus créditos matriculados"""
            if not self.estudiantes:
                print("No hay estudiantes registrados.")
                return
    
            print(f"\n--- LISTA DE ESTUDIANTES ({len(self.estudiantes)}) ---")
            print(f"{'ID':<10} {'Documento':<12} {'Nombres':<20} {'Apellidos':<20} {'Correo':<25} {'Créditos':<10}")
            print("-" * 107)
    
            for estudiante in self.estudiantes:
                creditos = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante.id)
                print(f"{estudiante.id:<10} {estudiante.documento:<12} {estudiante.nombres:<20} {estudiante.apellidos:<20} {estudiante.correo:<25} {creditos:<10}")
    
    def crear_curso(self):
        """Interfaz para crear un nuevo curso"""
        print("\n--- CREAR NUEVO CURSO ---")
        
        # Validar nombre inmediatamente
        while True:
            nombre = input("Nombre del curso: ").strip()
            if not nombre:
                print("❌ Error: El nombre del curso es obligatorio")
                continue
            break
        
        # Validar créditos inmediatamente
        while True:
            creditos_str = input("Número de créditos (1-10): ").strip()
            if not creditos_str:
                print("❌ Error: Los créditos son obligatorios")
                continue
            
            try:
                creditos = int(creditos_str)
            except ValueError:
                print("❌ Error: Los créditos deben ser un número entero")
                continue
            
            if not validar_creditos(creditos):
                print("❌ Error: Los créditos deben estar entre 1 y 10")
                continue
            
            break
        
        # Validar docente inmediatamente
        while True:
            docente = input("Nombre del docente: ").strip()
            if not docente:
                print("❌ Error: El nombre del docente es obligatorio")
                continue
            break
        
        # Crear curso
        codigo = self.generar_siguiente_id("curso")
        nuevo_curso = Curso(
            codigo=codigo,
            nombre=nombre,
            creditos=creditos,
            docente=docente
        )
        
        self.cursos.append(nuevo_curso)
        print(f"✅ Curso creado exitosamente con código: {codigo}")
        return True
    
    def editar_curso(self):
        """Interfaz para editar un curso existente"""
        print("\n--- EDITAR CURSO ---")
        
        if not self.cursos:
            print("❌ No hay cursos registrados.")
            return False
        
        # Mostrar cursos disponibles
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return False
            
            curso_a_editar = self.cursos[indice]
            
            print(f"\n--- EDITANDO: {curso_a_editar.nombre} ---")
            print("⚠️  NOTA: El código del curso no se puede modificar")
            print("Ingrese los nuevos datos (presione Enter para mantener el valor actual):")
            
            print(f"Nombre actual: {curso_a_editar.nombre}")
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if not nuevo_nombre:
                nuevo_nombre = curso_a_editar.nombre
            
            # Validar créditos con verificación inmediata
            while True:
                print(f"Créditos actuales: {curso_a_editar.creditos}")
                nuevos_creditos_str = input("Nuevos créditos (Enter para mantener): ").strip()
                if not nuevos_creditos_str:
                    nuevos_creditos = curso_a_editar.creditos
                    break
                
                try:
                    nuevos_creditos = int(nuevos_creditos_str)
                except ValueError:
                    print("❌ Error: Los créditos deben ser un número entero")
                    continue
                
                if not validar_creditos(nuevos_creditos):
                    print("❌ Error: Los créditos deben estar entre 1 y 10")
                    continue
                
                break
            
            print(f"Docente actual: {curso_a_editar.docente}")
            nuevo_docente = input("Nuevo docente: ").strip()
            if not nuevo_docente:
                nuevo_docente = curso_a_editar.docente
            
            # Actualizar curso
            curso_a_editar.nombre = nuevo_nombre
            curso_a_editar.creditos = nuevos_creditos
            curso_a_editar.docente = nuevo_docente
            
            print("✅ Curso actualizado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_curso(self):
        """Interfaz para eliminar un curso"""
        print("\n--- ELIMINAR CURSO ---")
        
        if not self.cursos:
            print("❌ No hay cursos registrados.")
            return False
        
        # Mostrar cursos disponibles
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return False
            
            curso_a_eliminar = self.cursos[indice]
            
            # Verificar si tiene estudiantes inscritos o matriculados
            if self.consultas.tiene_estudiantes_inscritos(curso_a_eliminar.codigo):
                print(f"❌ Error: No se puede eliminar el curso {curso_a_eliminar.nombre}")
                print("   Motivo: Hay estudiantes inscritos o matriculados en este curso")
                print("   Debe esperar a que todos los estudiantes terminen el curso antes de eliminarlo")
                return False
            
            # Eliminar curso
            self.cursos.remove(curso_a_eliminar)
            print(f"✅ Curso {curso_a_eliminar.nombre} eliminado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_cursos(self):
        """Lista todos los cursos"""
        if not self.cursos:
            print("No hay cursos registrados.")
            return
        
        print(f"\n--- LISTA DE CURSOS ({len(self.cursos)}) ---")
        print(f"{'Código':<10} {'Nombre':<30} {'Créditos':<10} {'Docente':<25}")
        print("-" * 75)
        
        for curso in self.cursos:
            print(f"{curso.codigo:<10} {curso.nombre:<30} {curso.creditos:<10} {curso.docente:<25}")
    
    def crear_inscripcion(self):
            """Interfaz para crear una nueva inscripción"""
            print("\n--- CREAR NUEVA INSCRIPCIÓN ---")
            
            if not self.estudiantes:
                print("❌ Error: No hay estudiantes registrados")
                return False
            
            if not self.cursos:
                print("❌ Error: No hay cursos registrados")
                return False
            
            # Mostrar estudiantes disponibles
            print("\nEstudiantes disponibles:")
            for i, estudiante in enumerate(self.estudiantes, 1):
                creditos_inscritos = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante.id)
                creditos_disponibles = self.limite_creditos - creditos_inscritos
                print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()} (Créditos: {creditos_inscritos}/{self.limite_creditos}, Disponibles: {creditos_disponibles})")
            
            try:
                indice_estudiante = int(input("\nSeleccione estudiante (número): ")) - 1
                if indice_estudiante < 0 or indice_estudiante >= len(self.estudiantes):
                    print("❌ Error: Selección inválida")
                    return False
                estudiante_seleccionado = self.estudiantes[indice_estudiante]
            except ValueError:
                print("❌ Error: Debe ingresar un número válido")
                return False
            
            # Obtener cursos en los que ya está inscrito el estudiante
            cursos_inscritos = set()
            for inscripcion in self.inscripciones:
                if inscripcion.estudiante_id == estudiante_seleccionado.id:
                    cursos_inscritos.add(inscripcion.curso_codigo)
            
            # Filtrar cursos disponibles (excluir los ya inscritos)
            cursos_disponibles = [curso for curso in self.cursos if curso.codigo not in cursos_inscritos]
            
            if not cursos_disponibles:
                print("❌ El estudiante ya está inscrito en todos los cursos disponibles.")
                return False
            
            print("\nCursos disponibles:")
            for i, curso in enumerate(cursos_disponibles, 1):
                print(f"{i}. {curso.codigo} - {curso.nombre} ({curso.creditos} créditos)")
            
            try:
                indice_curso = int(input("\nSeleccione curso (número): ")) - 1
                if indice_curso < 0 or indice_curso >= len(cursos_disponibles):
                    print("❌ Error: Selección inválida")
                    return False
                curso_seleccionado = cursos_disponibles[indice_curso]
            except ValueError:
                print("❌ Error: Debe ingresar un número válido")
                return False
            
            # Verificar límite de créditos
            puede_inscribirse, mensaje = self.consultas.puede_inscribirse_curso(
                estudiante_seleccionado.id, 
                curso_seleccionado.codigo, 
                self.limite_creditos
            )
            
            if not puede_inscribirse:
                print(f"❌ Error: {mensaje}")
                return False
            
            # Crear inscripción
            nuevo_id = self.generar_siguiente_id("inscripcion")
            nueva_inscripcion = Inscripcion(
                id=nuevo_id,
                estudiante_id=estudiante_seleccionado.id,
                curso_codigo=curso_seleccionado.codigo,
                fecha_inscripcion=datetime.now().strftime('%Y-%m-%d')
            )
            
            self.inscripciones.append(nueva_inscripcion)
            
            # Mostrar información de créditos actualizada
            creditos_actualizados = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante_seleccionado.id)
            creditos_disponibles = self.limite_creditos - creditos_actualizados
            
            print(f"✅ Inscripción creada exitosamente. ID: {nuevo_id}")
            print(f"   Estudiante: {estudiante_seleccionado.nombre_completo()}")
            print(f"   Curso: {curso_seleccionado.nombre}")
            print(f"   Créditos utilizados: {creditos_actualizados}/{self.limite_creditos}")
            print(f"   Créditos disponibles: {creditos_disponibles}")
            return True

    def editar_inscripcion(self):
        """Interfaz para editar una inscripción existente"""
        print("\n--- EDITAR INSCRIPCIÓN ---")
        
        if not self.inscripciones:
            print("❌ No hay inscripciones registradas.")
            return False
        
        # Mostrar inscripciones disponibles
        print("\nInscripciones disponibles:")
        for i, inscripcion in enumerate(self.inscripciones, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            print(f"{i}. {inscripcion.id} - {nombre_estudiante} en {nombre_curso}")
        
        try:
            indice = int(input("\nSeleccione inscripción a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.inscripciones):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_a_editar = self.inscripciones[indice]
            
            # Verificar si ya tiene matrícula asociada
            tiene_matricula = any(m.inscripcion_id == inscripcion_a_editar.id for m in self.matriculas)
            if tiene_matricula:
                print("⚠️  Esta inscripción ya tiene una matrícula asociada.")
                print("⚠️  NOTA: El ID de la inscripción no se puede modificar")
                print("Solo se puede modificar la fecha de inscripción.")
                
                # Validar fecha con verificación inmediata
                while True:
                    print(f"Fecha actual: {inscripcion_a_editar.fecha_inscripcion}")
                    nueva_fecha = input("Nueva fecha (YYYY-MM-DD) o Enter para mantener: ").strip()
                    
                    if not nueva_fecha:
                        print("No se realizaron cambios")
                        return True
                    
                    if not validar_fecha(nueva_fecha):
                        print("❌ Error: Formato de fecha inválido")
                        continue
                    
                    break
                
                inscripcion_a_editar.fecha_inscripcion = nueva_fecha
                print("✅ Fecha de inscripción actualizada")
                return True
            
            print(f"\n--- EDITANDO INSCRIPCIÓN: {inscripcion_a_editar.id} ---")
            print("⚠️  NOTA: El ID de la inscripción no se puede modificar")
            
            # Cambiar estudiante
            print("\n1. Cambiar estudiante:")
            print(f"   Estudiante actual: {self.consultas.buscar_estudiante_por_id(inscripcion_a_editar.estudiante_id).nombre_completo()}")
            cambiar_estudiante = input("¿Cambiar estudiante? (s/N): ").strip().lower()
            
            nuevo_estudiante_id = inscripcion_a_editar.estudiante_id
            if cambiar_estudiante == 's':
                print("\nEstudiantes disponibles:")
                for i, estudiante in enumerate(self.estudiantes, 1):
                    creditos_inscritos = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante.id)
                    creditos_disponibles = self.limite_creditos - creditos_inscritos
                    print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()} (Disponibles: {creditos_disponibles})")
                
                try:
                    indice_est = int(input("Seleccione nuevo estudiante (número): ")) - 1
                    if 0 <= indice_est < len(self.estudiantes):
                        nuevo_estudiante_id = self.estudiantes[indice_est].id
                    else:
                        print("❌ Selección inválida, manteniendo estudiante actual")
                except ValueError:
                    print("❌ Entrada inválida, manteniendo estudiante actual")
            
            # Cambiar curso
            print("\n2. Cambiar curso:")
            print(f"   Curso actual: {self.consultas.buscar_curso_por_codigo(inscripcion_a_editar.curso_codigo).nombre}")
            cambiar_curso = input("¿Cambiar curso? (s/N): ").strip().lower()
            
            nuevo_curso_codigo = inscripcion_a_editar.curso_codigo
            if cambiar_curso == 's':
                print("\nCursos disponibles:")
                for i, curso in enumerate(self.cursos, 1):
                    print(f"{i}. {curso.codigo} - {curso.nombre}")
                
                try:
                    indice_curso = int(input("Seleccione nuevo curso (número): ")) - 1
                    if 0 <= indice_curso < len(self.cursos):
                        nuevo_curso_codigo = self.cursos[indice_curso].codigo
                    else:
                        print("❌ Selección inválida, manteniendo curso actual")
                except ValueError:
                    print("❌ Entrada inválida, manteniendo curso actual")
            
            # Verificar que no exista duplicado
            if (nuevo_estudiante_id != inscripcion_a_editar.estudiante_id or 
                nuevo_curso_codigo != inscripcion_a_editar.curso_codigo):
                
                for inscripcion in self.inscripciones:
                    if (inscripcion.id != inscripcion_a_editar.id and
                        inscripcion.estudiante_id == nuevo_estudiante_id and 
                        inscripcion.curso_codigo == nuevo_curso_codigo):
                        print("❌ Error: Ya existe una inscripción con esta combinación")
                        return False
                
                # Verificar límite de créditos si cambia el estudiante
                if nuevo_estudiante_id != inscripcion_a_editar.estudiante_id:
                    puede_inscribirse, mensaje = self.consultas.puede_inscribirse_curso(
                        nuevo_estudiante_id, nuevo_curso_codigo, self.limite_creditos
                    )
                    if not puede_inscribirse:
                        print(f"❌ Error: {mensaje}")
                        return False
            
            # Cambiar fecha
            while True:
                print(f"\n3. Fecha actual: {inscripcion_a_editar.fecha_inscripcion}")
                nueva_fecha = input("Nueva fecha (YYYY-MM-DD) o Enter para mantener: ").strip()
                if not nueva_fecha:
                    nueva_fecha = inscripcion_a_editar.fecha_inscripcion
                    break
                
                if not validar_fecha(nueva_fecha):
                    print("❌ Error: Formato de fecha inválido")
                    continue
                
                break
            
            # Aplicar cambios
            inscripcion_a_editar.estudiante_id = nuevo_estudiante_id
            inscripcion_a_editar.curso_codigo = nuevo_curso_codigo
            inscripcion_a_editar.fecha_inscripcion = nueva_fecha
            
            print("✅ Inscripción actualizada exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_inscripcion(self):
        """Interfaz para eliminar una inscripción"""
        print("\n--- ELIMINAR INSCRIPCIÓN ---")
        
        if not self.inscripciones:
            print("❌ No hay inscripciones registradas.")
            return False
        
        # Mostrar inscripciones disponibles
        print("\nInscripciones disponibles:")
        for i, inscripcion in enumerate(self.inscripciones, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            # Verificar si tiene matrícula
            tiene_matricula = any(m.inscripcion_id == inscripcion.id for m in self.matriculas)
            estado = " [CON MATRÍCULA]" if tiene_matricula else ""
            
            print(f"{i}. {inscripcion.id} - {nombre_estudiante} en {nombre_curso}{estado}")
        
        try:
            indice = int(input("\nSeleccione inscripción a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.inscripciones):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_a_eliminar = self.inscripciones[indice]
            
            # Verificar si tiene matrícula asociada
            matriculas_asociadas = [m for m in self.matriculas if m.inscripcion_id == inscripcion_a_eliminar.id]
            
            if matriculas_asociadas:
                print(f"⚠️  ADVERTENCIA: Esta inscripción tiene {len(matriculas_asociadas)} matrícula(s) asociada(s)")
                confirmar = input("¿Desea eliminarla junto con sus matrículas? (s/N): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada")
                    return False
                
                # Eliminar matrículas asociadas
                self.matriculas = [m for m in self.matriculas if m.inscripcion_id != inscripcion_a_eliminar.id]
                print(f"  • {len(matriculas_asociadas)} matrícula(s) eliminada(s)")
            
            # Eliminar inscripción
            self.inscripciones.remove(inscripcion_a_eliminar)
            
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion_a_eliminar.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion_a_eliminar.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            print(f"✅ Inscripción eliminada exitosamente")
            print(f"   {nombre_estudiante} - {nombre_curso}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_inscripciones(self):
        """Lista todas las inscripciones"""
        if not self.inscripciones:
            print("No hay inscripciones registradas.")
            return
        
        print(f"\n--- LISTA DE INSCRIPCIONES ({len(self.inscripciones)}) ---")
        print(f"{'ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12} {'Estado':<12}")
        print("-" * 74)
        
        for inscripcion in self.inscripciones:
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            codigo_curso = curso.codigo if curso else "N/A"
            
            # Verificar si ya tiene matrícula
            tiene_matricula = any(m.inscripcion_id == inscripcion.id for m in self.matriculas)
            estado = "Matriculado" if tiene_matricula else "Pendiente"
            
            print(f"{inscripcion.id:<10} {nombre_estudiante:<25} {codigo_curso:<15} {inscripcion.fecha_inscripcion:<12} {estado:<12}")
    
    def ver_inscripciones_pendientes(self):
        """Muestra inscripciones pendientes de convertir en matrícula"""
        pendientes = self.consultas.obtener_inscripciones_sin_matricular()
        
        if not pendientes:
            print("✅ No hay inscripciones pendientes de matrícula.")
            return
        
        print(f"\n--- INSCRIPCIONES PENDIENTES DE MATRÍCULA ({len(pendientes)}) ---")
        print(f"{'ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12}")
        print("-" * 62)
        
        for inscripcion, estudiante, curso in pendientes:
            print(f"{inscripcion.id:<10} {estudiante.nombre_completo():<25} {curso.codigo:<15} {inscripcion.fecha_inscripcion:<12}")
    
    def crear_matricula(self):
        """Interfaz para crear matrícula desde inscripción"""
        print("\n--- CREAR MATRÍCULA DESDE INSCRIPCIÓN ---")
        
        # Obtener inscripciones pendientes
        pendientes = self.consultas.obtener_inscripciones_sin_matricular()
        
        if not pendientes:
            print("❌ No hay inscripciones pendientes de matrícula.")
            return False
        
        print("\nInscripciones disponibles para matrícula:")
        for i, (inscripcion, estudiante, curso) in enumerate(pendientes, 1):
            print(f"{i}. {inscripcion.id} - {estudiante.nombre_completo()} en {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione inscripción (número): ")) - 1
            if indice < 0 or indice >= len(pendientes):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_seleccionada, estudiante, curso = pendientes[indice]
            
            # Crear matrícula desde inscripción
            nuevo_id = self.generar_siguiente_id("matricula")
            nueva_matricula = Matricula.from_inscripcion(
                inscripcion_seleccionada, 
                nuevo_id
            )
            
            self.matriculas.append(nueva_matricula)
            print(f"✅ Matrícula creada exitosamente. ID: {nuevo_id}")
            print(f"   Estudiante: {estudiante.nombre_completo()}")
            print(f"   Curso: {curso.nombre}")
            print(f"   Basada en inscripción: {inscripcion_seleccionada.id}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def asignar_nota(self):
        """Interfaz para asignar nota a una matrícula"""
        print("\n--- ASIGNAR NOTA ---")
        
        # Mostrar matrículas sin nota
        matriculas_sin_nota = [m for m in self.matriculas if m.nota is None]
        
        if not matriculas_sin_nota:
            print("No hay matrículas pendientes de calificación.")
            return False
        
        print("\nMatrículas pendientes de calificación:")
        for i, matricula in enumerate(matriculas_sin_nota, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            if estudiante and curso:
                print(f"{i}. {estudiante.nombre_completo()} - {curso.nombre} (ID: {matricula.id})")
        
        try:
            indice = int(input("\nSeleccione matrícula (número): ")) - 1
            if indice < 0 or indice >= len(matriculas_sin_nota):
                print("❌ Error: Selección inválida")
                return False
            
            matricula_seleccionada = matriculas_sin_nota[indice]
            
            # Validar nota con verificación inmediata
            while True:
                nota_str = input("Ingrese la nota (0.0 - 5.0): ").strip()
                if not nota_str:
                    print("❌ Error: La nota es obligatoria")
                    continue
                
                try:
                    nota = float(nota_str)
                except ValueError:
                    print("❌ Error: La nota debe ser un número válido")
                    continue
                
                if not validar_nota(nota):
                    print("❌ Error: La nota debe estar entre 0.0 y 5.0")
                    continue
                
                break
            
            matricula_seleccionada.nota = nota
            print(f"✅ Nota asignada exitosamente: {nota}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_matricula(self):
        """Interfaz para eliminar una matrícula"""
        print("\n--- ELIMINAR MATRÍCULA ---")
        
        if not self.matriculas:
            print("❌ No hay matrículas registradas.")
            return False
        
        # Mostrar matrículas disponibles
        print("\nMatrículas disponibles:")
        for i, matricula in enumerate(self.matriculas, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            nota_str = f"{matricula.nota:.1f}" if matricula.nota is not None else "Sin nota"
            
            print(f"{i}. {matricula.id} - {nombre_estudiante} en {nombre_curso} ({nota_str})")
        
        try:
            indice = int(input("\nSeleccione matrícula a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.matriculas):
                print("❌ Error: Selección inválida")
                return False
            
            matricula_a_eliminar = self.matriculas[indice]
            
            # Mostrar información de la matrícula
            estudiante = self.consultas.buscar_estudiante_por_id(matricula_a_eliminar.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula_a_eliminar.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            nota_str = f"{matricula_a_eliminar.nota:.1f}" if matricula_a_eliminar.nota is not None else "Sin nota"
            
            print(f"\n⚠️  Matrícula a eliminar:")
            print(f"   ID: {matricula_a_eliminar.id}")
            print(f"   Estudiante: {nombre_estudiante}")
            print(f"   Curso: {nombre_curso}")
            print(f"   Nota: {nota_str}")
            print(f"   Fecha: {matricula_a_eliminar.fecha_matricula}")
            
            confirmar = input("\n¿Está seguro de eliminar esta matrícula? (s/N): ").strip().lower()
            if confirmar != 's':
                print("Eliminación cancelada")
                return False
            
            # Eliminar matrícula
            self.matriculas.remove(matricula_a_eliminar)
            print(f"✅ Matrícula {matricula_a_eliminar.id} eliminada exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_matriculas(self):
        """Lista todas las matrículas con información completa"""
        if not self.matriculas:
            print("No hay matrículas registradas.")
            return
        
        print(f"\n--- LISTA DE MATRÍCULAS ({len(self.matriculas)}) ---")
        print(f"{'ID':<10} {'Inscr.ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12} {'Nota':<6}")
        print("-" * 88)
        
        for matricula in self.matriculas:
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            codigo_curso = curso.codigo if curso else "N/A"
            nota_str = f"{matricula.nota:.1f}" if matricula.nota is not None else "---"
            
            print(f"{matricula.id:<10} {matricula.inscripcion_id:<10} {nombre_estudiante:<25} {codigo_curso:<15} {matricula.fecha_matricula:<12} {nota_str:<6}")
    
    # Métodos de consultas (mantienen la misma funcionalidad)
    def ejecutar_consulta_buscar_documento(self):
        """Ejecuta consulta de búsqueda por documento"""
        documento = input("Ingrese documento a buscar: ").strip()
        estudiante = self.consultas.buscar_estudiante_por_documento(documento)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado:")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con documento {documento}")
    
    def ejecutar_consulta_buscar_correo(self):
        """Ejecuta consulta de búsqueda por correo"""
        correo = input("Ingrese correo a buscar: ").strip()
        estudiante = self.consultas.buscar_estudiante_por_correo(correo)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado:")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con correo {correo}")
    
    def ejecutar_consulta_ordenados_apellido(self):
        """Ejecuta consulta de estudiantes ordenados por apellido"""
        estudiantes_ordenados = self.consultas.listar_estudiantes_ordenados_por_apellido()
        
        if not estudiantes_ordenados:
            print("No hay estudiantes registrados.")
            return
        
        print(f"\n--- ESTUDIANTES ORDENADOS POR APELLIDO ({len(estudiantes_ordenados)}) ---")
        print(f"{'Apellidos':<20} {'Nombres':<20} {'Documento':<12} {'Correo':<25}")
        print("-" * 77)
        
        for estudiante in estudiantes_ordenados:
            print(f"{estudiante.apellidos:<20} {estudiante.nombres:<20} {estudiante.documento:<12} {estudiante.correo:<25}")
    
    def ejecutar_consulta_top_promedios(self):
        """Ejecuta consulta de top 3 promedios por curso"""
        if not self.cursos:
            print("No hay cursos registrados.")
            return
        
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return
            
            curso_seleccionado = self.cursos[indice]
            top_estudiantes = self.consultas.obtener_top_promedios_por_curso(curso_seleccionado.codigo)
            
            if not top_estudiantes:
                print(f"No hay notas registradas para el curso {curso_seleccionado.codigo}")
                return
            
            print(f"\n--- TOP 3 PROMEDIOS - {curso_seleccionado.nombre} ---")
            print(f"{'Posición':<10} {'Estudiante':<25} {'Nota':<6}")
            print("-" * 41)
            
            for i, (estudiante, nota) in enumerate(top_estudiantes, 1):
                print(f"{i}°{'':<8} {estudiante.nombre_completo():<25} {nota:.1f}")
                
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
    
    def ejecutar_consulta_reprobados(self):
        """Ejecuta consulta de estudiantes reprobados"""
        reprobados = self.consultas.obtener_reprobados()
        
        if not reprobados:
            print("No hay estudiantes reprobados (nota < 3.0)")
            return
        
        print(f"\n--- ESTUDIANTES REPROBADOS ({len(reprobados)}) ---")
        print(f"{'Estudiante':<25} {'Curso':<15} {'Nota':<6}")
        print("-" * 46)
        
        for estudiante, curso, nota in reprobados:
            print(f"{estudiante.nombre_completo():<25} {curso.codigo:<15} {nota:.1f}")
    
    def ejecutar_consulta_creditos_estudiante(self):
        """Ejecuta consulta de créditos inscritos por estudiante"""
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return
            
            estudiante_seleccionado = self.estudiantes[indice]
            creditos = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante_seleccionado.id)
            creditos_disponibles = self.consultas.obtener_creditos_disponibles_estudiante(estudiante_seleccionado.id, self.limite_creditos)
            
            print(f"\n--- CRÉDITOS INSCRITOS ---")
            print(f"Estudiante: {estudiante_seleccionado.nombre_completo()}")
            print(f"Créditos utilizados: {creditos}")
            print(f"Límite total de créditos: {self.limite_creditos}")
            print(f"Créditos disponibles: {creditos_disponibles}")
            
            # Mostrar detalle de inscripciones
            inscripciones_estudiante = [i for i in self.inscripciones if i.estudiante_id == estudiante_seleccionado.id]
            if inscripciones_estudiante:
                print(f"\nDetalle de inscripciones:")
                for inscripcion in inscripciones_estudiante:
                    curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
                    if curso:
                        print(f"  • {curso.codigo} - {curso.nombre} ({curso.creditos} créditos)")
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
    
    def ejecutar_consulta_dominios_correo(self):
        """Ejecuta consulta de dominios de correo únicos"""
        dominios = self.consultas.obtener_dominios_correo_unicos()
        
        if not dominios:
            print("No hay dominios de correo registrados.")
            return
        
        print(f"\n--- DOMINIOS DE CORREO ÚNICOS ({len(dominios)}) ---")
        for i, dominio in enumerate(dominios, 1):
            print(f"{i}. {dominio}")
    
    def ejecutar_busqueda_binaria_apellido(self):
        """Ejecuta búsqueda binaria por apellido"""
        apellido = input("Ingrese apellido a buscar: ").strip()
        estudiante = self.consultas.buscar_binario_estudiante(apellido)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado (búsqueda binaria):")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con apellido {apellido}")