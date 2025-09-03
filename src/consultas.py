# src/consultas.py - Versión actualizada con inscripciones
from typing import List, Tuple, Optional
from src.modelos import Estudiante, Curso, Inscripcion, Matricula

class ConsultasAcademicas:
    """Clase para realizar consultas y reportes del sistema"""
    
    def __init__(self, estudiantes: List[Estudiante], cursos: List[Curso], 
                 inscripciones: List[Inscripcion], matriculas: List[Matricula]):
        self.estudiantes = estudiantes
        self.cursos = cursos
        self.inscripciones = inscripciones
        self.matriculas = matriculas
    
    def buscar_estudiante_por_documento(self, documento: str) -> Optional[Estudiante]:
        """Busca estudiante por número de documento"""
        for estudiante in self.estudiantes:
            if estudiante.documento == documento:
                return estudiante
        return None
    
    def buscar_estudiante_por_correo(self, correo: str) -> Optional[Estudiante]:
        """Busca estudiante por correo electrónico"""
        for estudiante in self.estudiantes:
            if estudiante.correo.lower() == correo.lower():
                return estudiante
        return None
    
    def listar_estudiantes_ordenados_por_apellido(self) -> List[Estudiante]:
        """Retorna lista de estudiantes ordenados por apellido"""
        return sorted(self.estudiantes, key=lambda e: e.apellidos.lower())
    
    def obtener_top_promedios_por_curso(self, codigo_curso: str, top: int = 3) -> List[Tuple[Estudiante, float]]:
        """Obtiene los mejores promedios de un curso específico"""
        matriculas_curso = [m for m in self.matriculas 
                           if m.curso_codigo == codigo_curso and m.nota is not None]
        
        # Crear lista de estudiante-nota
        estudiantes_notas = []
        for matricula in matriculas_curso:
            estudiante = self.buscar_estudiante_por_id(matricula.estudiante_id)
            if estudiante:
                estudiantes_notas.append((estudiante, matricula.nota))
        
        # Ordenar por nota descendente y tomar el top
        estudiantes_notas.sort(key=lambda x: x[1], reverse=True)
        return estudiantes_notas[:top]
    
    def obtener_reprobados(self, nota_minima: float = 3.0) -> List[Tuple[Estudiante, Curso, float]]:
        """Obtiene estudiantes reprobados (nota < nota_minima)"""
        reprobados = []
        
        for matricula in self.matriculas:
            if matricula.nota is not None and matricula.nota < nota_minima:
                estudiante = self.buscar_estudiante_por_id(matricula.estudiante_id)
                curso = self.buscar_curso_por_codigo(matricula.curso_codigo)
                
                if estudiante and curso:
                    reprobados.append((estudiante, curso, matricula.nota))
        
        return reprobados
    
    def obtener_creditos_inscritos_por_estudiante(self, estudiante_id: str) -> int:
        """Calcula total de créditos inscritos por un estudiante (basado en inscripciones)"""
        creditos_total = 0
        
        inscripciones_estudiante = [i for i in self.inscripciones if i.estudiante_id == estudiante_id]
        
        for inscripcion in inscripciones_estudiante:
            curso = self.buscar_curso_por_codigo(inscripcion.curso_codigo)
            if curso:
                creditos_total += curso.creditos
        
        return creditos_total
    
    def obtener_creditos_disponibles_estudiante(self, estudiante_id: str, limite_creditos: int = 20) -> int:
        """Calcula créditos disponibles para un estudiante"""
        creditos_inscritos = self.obtener_creditos_inscritos_por_estudiante(estudiante_id)
        return limite_creditos - creditos_inscritos
    
    def puede_inscribirse_curso(self, estudiante_id: str, curso_codigo: str, limite_creditos: int = 20) -> tuple[bool, str]:
        """Verifica si un estudiante puede inscribirse a un curso"""
        # Verificar si ya está inscrito
        for inscripcion in self.inscripciones:
            if inscripcion.estudiante_id == estudiante_id and inscripcion.curso_codigo == curso_codigo:
                return False, "El estudiante ya está inscrito en este curso"
        
        # Verificar límite de créditos
        curso = self.buscar_curso_por_codigo(curso_codigo)
        if not curso:
            return False, "Curso no encontrado"
        
        creditos_actuales = self.obtener_creditos_inscritos_por_estudiante(estudiante_id)
        if creditos_actuales + curso.creditos > limite_creditos:
            return False, f"Excede el límite de créditos. Disponibles: {limite_creditos - creditos_actuales}, Necesarios: {curso.creditos}"
        
        return True, "Puede inscribirse"
    
    def tiene_estudiantes_inscritos(self, curso_codigo: str) -> bool:
        """Verifica si un curso tiene estudiantes inscritos o matriculados"""
        # Verificar inscripciones
        for inscripcion in self.inscripciones:
            if inscripcion.curso_codigo == curso_codigo:
                return True
        
        # Verificar matrículas
        for matricula in self.matriculas:
            if matricula.curso_codigo == curso_codigo:
                return True
        
        return False
    
    def buscar_estudiante_por_id(self, estudiante_id: str) -> Optional[Estudiante]:
        """Busca estudiante por ID"""
        for estudiante in self.estudiantes:
            if estudiante.id == estudiante_id:
                return estudiante
        return None
    
    def buscar_curso_por_codigo(self, codigo: str) -> Optional[Curso]:
        """Busca curso por código"""
        for curso in self.cursos:
            if curso.codigo == codigo:
                return curso
        return None
    
    def buscar_inscripcion_por_id(self, inscripcion_id: str) -> Optional[Inscripcion]:
        """Busca inscripción por ID"""
        for inscripcion in self.inscripciones:
            if inscripcion.id == inscripcion_id:
                return inscripcion
        return None
    
    def obtener_dominios_correo_unicos(self) -> List[str]:
        """Obtiene lista de dominios de correo únicos"""
        dominios = set()
        for estudiante in self.estudiantes:
            if '@' in estudiante.correo:
                dominio = estudiante.correo.split('@')[1]
                dominios.add(dominio)
        
        return sorted(list(dominios))
    
    def buscar_binario_estudiante(self, apellido_buscar: str) -> Optional[Estudiante]:
        """Implementa búsqueda binaria por apellido (requiere lista ordenada)"""
        estudiantes_ordenados = self.listar_estudiantes_ordenados_por_apellido()
        
        izq, der = 0, len(estudiantes_ordenados) - 1
        
        while izq <= der:
            medio = (izq + der) // 2
            apellido_medio = estudiantes_ordenados[medio].apellidos.lower()
            apellido_buscar_lower = apellido_buscar.lower()
            
            if apellido_medio == apellido_buscar_lower:
                return estudiantes_ordenados[medio]
            elif apellido_medio < apellido_buscar_lower:
                izq = medio + 1
            else:
                der = medio - 1
        
        return None
    
    def obtener_inscripciones_sin_matricular(self) -> List[Tuple[Inscripcion, Estudiante, Curso]]:
        """Obtiene inscripciones que aún no se han convertido en matrículas"""
        inscripciones_ids = {m.inscripcion_id for m in self.matriculas}
        inscripciones_pendientes = []
        
        for inscripcion in self.inscripciones:
            if inscripcion.id not in inscripciones_ids:
                estudiante = self.buscar_estudiante_por_id(inscripcion.estudiante_id)
                curso = self.buscar_curso_por_codigo(inscripcion.curso_codigo)
                
                if estudiante and curso:
                    inscripciones_pendientes.append((inscripcion, estudiante, curso))
        
        return inscripciones_pendientes
    
    def obtener_matriculas_con_inscripcion(self) -> List[Tuple[Matricula, Inscripcion, Estudiante, Curso]]:
        """Obtiene matrículas con información completa de inscripción, estudiante y curso"""
        matriculas_completas = []
        
        for matricula in self.matriculas:
            inscripcion = self.buscar_inscripcion_por_id(matricula.inscripcion_id)
            estudiante = self.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.buscar_curso_por_codigo(matricula.curso_codigo)
            
            if inscripcion and estudiante and curso:
                matriculas_completas.append((matricula, inscripcion, estudiante, curso))
        
        return matriculas_completas