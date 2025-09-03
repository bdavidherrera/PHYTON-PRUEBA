# tests/pruebas_basicas.py - Versión actualizada
import unittest
import tempfile
import shutil
from datetime import datetime
import os
import sys

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelos import Estudiante, Curso, Inscripcion, Matricula
from src.validaciones import validar_correo, validar_documento, validar_fecha, validar_creditos, validar_nota
from src.persistencia import PersistenciaCSV
from src.consultas import ConsultasAcademicas

class TestModelos(unittest.TestCase):
    """Pruebas para los modelos de datos"""
    
    def test_crear_estudiante_valido(self):
        """Prueba creación de estudiante válido"""
        estudiante = Estudiante(
            id="E1",
            documento="12345678",
            nombres="Juan Carlos",
            apellidos="Pérez García",
            correo="juan.perez@email.com",
            fecha_nacimiento="1995-06-15"
        )
        
        self.assertEqual(estudiante.id, "E1")
        self.assertEqual(estudiante.documento, "12345678")
        self.assertEqual(estudiante.nombre_completo(), "Juan Carlos Pérez García")
    
    def test_crear_curso_valido(self):
        """Prueba creación de curso válido"""
        curso = Curso(
            codigo="C1",
            nombre="Matemáticas Básicas",
            creditos=3,
            docente="Dr. Ana López"
        )
        
        self.assertEqual(curso.codigo, "C1")
        self.assertEqual(curso.creditos, 3)
    
    def test_crear_inscripcion_valida(self):
        """Prueba creación de inscripción válida"""
        inscripcion = Inscripcion(
            id="I1",
            estudiante_id="E1",
            curso_codigo="C1",
            fecha_inscripcion="2024-02-15"
        )
        
        self.assertEqual(inscripcion.estudiante_id, "E1")
        self.assertEqual(inscripcion.curso_codigo, "C1")
    
    def test_crear_matricula_valida(self):
        """Prueba creación de matrícula válida"""
        matricula = Matricula(
            id="M1",
            inscripcion_id="I1",
            estudiante_id="E1",
            curso_codigo="C1",
            fecha_matricula="2024-02-15"
        )
        
        self.assertEqual(matricula.estudiante_id, "E1")
        self.assertEqual(matricula.curso_codigo, "C1")
        self.assertIsNone(matricula.nota)

class TestValidaciones(unittest.TestCase):
    """Pruebas para las funciones de validación"""
    
    # ... (las pruebas de validación se mantienen igual)
    
class TestPersistencia(unittest.TestCase):
    """Pruebas para la persistencia de datos"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.temp_dir = tempfile.mkdtemp()
        self.persistencia = PersistenciaCSV(self.temp_dir)
        
        # Datos de prueba
        self.estudiantes_prueba = [
            Estudiante("E1", "12345678", "Juan", "Pérez", "juan@test.com", "1995-01-01"),
            Estudiante("E2", "87654321", "María", "González", "maria@test.com", "1996-02-02")
        ]
        
        self.cursos_prueba = [
            Curso("C1", "Matemáticas", 3, "Dr. López"),
            Curso("C2", "Física", 4, "Dr. García")
        ]
        
        self.inscripciones_prueba = [
            Inscripcion("I1", "E1", "C1", "2024-02-01"),
            Inscripcion("I2", "E2", "C1", "2024-02-01")
        ]
        
        self.matriculas_prueba = [
            Matricula("M1", "I1", "E1", "C1", "2024-02-01", 4.5),
            Matricula("M2", "I2", "E2", "C1", "2024-02-01", 3.8)
        ]
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        shutil.rmtree(self.temp_dir)
    
    def test_guardar_y_cargar_estudiantes(self):
        """Prueba guardar y cargar estudiantes"""
        # Guardar
        self.persistencia.guardar_estudiantes(self.estudiantes_prueba)
        
        # Cargar
        estudiantes_cargados = self.persistencia.cargar_estudiantes()
        
        # Verificar
        self.assertEqual(len(estudiantes_cargados), 2)
        self.assertEqual(estudiantes_cargados[0].documento, "12345678")
        self.assertEqual(estudiantes_cargados[1].correo, "maria@test.com")
    
    def test_guardar_y_cargar_cursos(self):
        """Prueba guardar y cargar cursos"""
        # Guardar
        self.persistencia.guardar_cursos(self.cursos_prueba)
        
        # Cargar
        cursos_cargados = self.persistencia.cargar_cursos()
        
        # Verificar
        self.assertEqual(len(cursos_cargados), 2)
        self.assertEqual(cursos_cargados[0].codigo, "C1")
        self.assertEqual(cursos_cargados[1].creditos, 4)
    
    def test_guardar_y_cargar_inscripciones(self):
        """Prueba guardar y cargar inscripciones"""
        # Guardar
        self.persistencia.guardar_inscripciones(self.inscripciones_prueba)
        
        # Cargar
        inscripciones_cargadas = self.persistencia.cargar_inscripciones()
        
        # Verificar
        self.assertEqual(len(inscripciones_cargadas), 2)
        self.assertEqual(inscripciones_cargadas[0].estudiante_id, "E1")
        self.assertEqual(inscripciones_cargadas[1].curso_codigo, "C1")
    
    def test_guardar_y_cargar_matriculas(self):
        """Prueba guardar y cargar matrículas"""
        # Guardar
        self.persistencia.guardar_matriculas(self.matriculas_prueba)
        
        # Cargar
        matriculas_cargadas = self.persistencia.cargar_matriculas()
        
        # Verificar
        self.assertEqual(len(matriculas_cargadas), 2)
        self.assertEqual(matriculas_cargadas[0].estudiante_id, "E1")
        self.assertEqual(matriculas_cargadas[1].nota, 3.8)

class TestConsultas(unittest.TestCase):
    """Pruebas para las consultas académicas"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.estudiantes = [
            Estudiante("E1", "12345678", "Juan", "Pérez", "juan@test.com", "1995-01-01"),
            Estudiante("E2", "87654321", "María", "González", "maria@test.com", "1996-02-02"),
            Estudiante("E3", "11111111", "Ana", "López", "ana@test.com", "1997-03-03")
        ]
        
        self.cursos = [
            Curso("C1", "Matemáticas", 3, "Dr. López"),
            Curso("C2", "Física", 4, "Dr. García")
        ]
        
        self.inscripciones = [
            Inscripcion("I1", "E1", "C1", "2024-02-01"),
            Inscripcion("I2", "E2", "C1", "2024-02-01"),
            Inscripcion("I3", "E3", "C1", "2024-02-01"),
            Inscripcion("I4", "E1", "C2", "2024-02-01")
        ]
        
        self.matriculas = [
            Matricula("M1", "I1", "E1", "C1", "2024-02-01", 4.5),
            Matricula("M2", "I2", "E2", "C1", "2024-02-01", 3.8),
            Matricula("M3", "I3", "E3", "C1", "2024-02-01", 2.1),
            Matricula("M4", "I4", "E1", "C2", "2024-02-01", None)
        ]
        
        self.consultas = ConsultasAcademicas(
            self.estudiantes, 
            self.cursos, 
            self.inscripciones, 
            self.matriculas
        )
    
    def test_buscar_estudiante_por_documento(self):
        """Prueba búsqueda de estudiante por documento"""
        estudiante = self.consultas.buscar_estudiante_por_documento("12345678")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.nombres, "Juan")
        
        estudiante_inexistente = self.consultas.buscar_estudiante_por_documento("99999999")
        self.assertIsNone(estudiante_inexistente)
    
    def test_buscar_estudiante_por_correo(self):
        """Prueba búsqueda de estudiante por correo"""
        estudiante = self.consultas.buscar_estudiante_por_correo("maria@test.com")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.apellidos, "González")
        
        # Prueba case insensitive
        estudiante = self.consultas.buscar_estudiante_por_correo("MARIA@TEST.COM")
        self.assertIsNotNone(estudiante)
    
    def test_listar_estudiantes_ordenados_por_apellido(self):
        """Prueba listado ordenado por apellido"""
        ordenados = self.consultas.listar_estudiantes_ordenados_por_apellido()
        
        self.assertEqual(len(ordenados), 3)
        self.assertEqual(ordenados[0].apellidos, "González")  # Primero alfabéticamente
        self.assertEqual(ordenados[1].apellidos, "López")
        self.assertEqual(ordenados[2].apellidos, "Pérez")
    
    def test_obtener_top_promedios_por_curso(self):
        """Prueba obtención de top promedios"""
        top = self.consultas.obtener_top_promedios_por_curso("C1", 3)
        
        self.assertEqual(len(top), 3)
        # Verificar que está ordenado descendente por nota
        self.assertEqual(top[0][1], 4.5)  # Juan - nota más alta
        self.assertEqual(top[1][1], 3.8)  # María
        self.assertEqual(top[2][1], 2.1)  # Ana - nota más baja
    
    def test_obtener_reprobados(self):
        """Prueba obtención de reprobados"""
        reprobados = self.consultas.obtener_reprobados(3.0)
        
        self.assertEqual(len(reprobados), 1)
        self.assertEqual(reprobados[0][2], 2.1)  # Ana con nota 2.1
    
    def test_obtener_creditos_inscritos_por_estudiante(self):
        """Prueba cálculo de créditos inscritos"""
        creditos = self.consultas.obtener_creditos_inscritos_por_estudiante("E1")
        self.assertEqual(creditos, 7)  # C1 (3) + C2 (4)
        
        creditos = self.consultas.obtener_creditos_inscritos_por_estudiante("E2")
        self.assertEqual(creditos, 3)  # Solo C1 (3)
    
    def test_obtener_dominios_correo_unicos(self):
        """Prueba obtención de dominios únicos"""
        dominios = self.consultas.obtener_dominios_correo_unicos()
        
        self.assertEqual(len(dominios), 1)
        self.assertEqual(dominios[0], "test.com")
    
    def test_buscar_binario_estudiante(self):
        """Prueba búsqueda binaria por apellido"""
        estudiante = self.consultas.buscar_binario_estudiante("López")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.nombres, "Ana")
        
        estudiante_inexistente = self.consultas.buscar_binario_estudiante("Inexistente")
        self.assertIsNone(estudiante_inexistente)
    
    def test_puede_inscribirse_curso(self):
        """Prueba verificación de inscripción a curso"""
        # Estudiante E1 ya está inscrito en C1 y C2
        puede, mensaje = self.consultas.puede_inscribirse_curso("E1", "C1", 20)
        self.assertFalse(puede)
        self.assertEqual(mensaje, "El estudiante ya está inscrito en este curso")
        
        # Estudiante E2 solo está inscrito en C1, puede inscribirse en C2
        puede, mensaje = self.consultas.puede_inscribirse_curso("E2", "C2", 20)
        self.assertTrue(puede)
        self.assertEqual(mensaje, "Puede inscribirse")

if __name__ == '__main__':
    print("Ejecutando pruebas básicas de MiniSIGA...")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)