# migration_update.py - Script para actualizar IDs al nuevo formato
import csv
import os

def actualizar_ids_formato():
    """
    Actualiza los IDs existentes al nuevo formato con prefijos de letras
    """
    print("Iniciando actualización de IDs al nuevo formato...")
    
    # Mapeo de IDs antiguos a nuevos
    mapeo_estudiantes = {}
    mapeo_cursos = {}
    mapeo_inscripciones = {}
    mapeo_matriculas = {}
    
    # 1. Actualizar estudiantes
    try:
        estudiantes = []
        with open('datos/estudiantes.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                id_antiguo = row['id']
                id_nuevo = f"E{i}"
                mapeo_estudiantes[id_antiguo] = id_nuevo
                
                row['id'] = id_nuevo
                estudiantes.append(row)
        
        # Guardar estudiantes actualizados
        with open('datos/estudiantes.csv', 'w', newline='', encoding='utf-8') as f:
            if estudiantes:
                fieldnames = ['id', 'documento', 'nombres', 'apellidos', 'correo', 'fecha_nacimiento']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(estudiantes)
        
        print(f"✅ Actualizados {len(estudiantes)} estudiantes")
        
    except FileNotFoundError:
        print("⚠️  Archivo de estudiantes no encontrado")
    
    # 2. Actualizar cursos
    try:
        cursos = []
        with open('datos/cursos.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                codigo_antiguo = row['codigo']
                codigo_nuevo = f"C{i}"
                mapeo_cursos[codigo_antiguo] = codigo_nuevo
                
                row['codigo'] = codigo_nuevo
                cursos.append(row)
        
        # Guardar cursos actualizados
        with open('datos/cursos.csv', 'w', newline='', encoding='utf-8') as f:
            if cursos:
                fieldnames = ['codigo', 'nombre', 'creditos', 'docente']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cursos)
        
        print(f"✅ Actualizados {len(cursos)} cursos")
        
    except FileNotFoundError:
        print("⚠️  Archivo de cursos no encontrado")
    
    # 3. Actualizar inscripciones
    try:
        inscripciones = []
        with open('datos/inscripciones.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                id_antiguo = row['id']
                id_nuevo = f"I{i}"
                mapeo_inscripciones[id_antiguo] = id_nuevo
                
                row['id'] = id_nuevo
                
                # Actualizar referencias
                if row['estudiante_id'] in mapeo_estudiantes:
                    row['estudiante_id'] = mapeo_estudiantes[row['estudiante_id']]
                
                if row['curso_codigo'] in mapeo_cursos:
                    row['curso_codigo'] = mapeo_cursos[row['curso_codigo']]
                
                inscripciones.append(row)
        
        # Guardar inscripciones actualizadas
        with open('datos/inscripciones.csv', 'w', newline='', encoding='utf-8') as f:
            if inscripciones:
                fieldnames = ['id', 'estudiante_id', 'curso_codigo', 'fecha_inscripcion']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(inscripciones)
        
        print(f"✅ Actualizadas {len(inscripciones)} inscripciones")
        
    except FileNotFoundError:
        print("⚠️  Archivo de inscripciones no encontrado")
    
    # 4. Actualizar matrículas
    try:
        matriculas = []
        with open('datos/matriculas.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                id_antiguo = row['id']
                id_nuevo = f"M{i}"
                mapeo_matriculas[id_antiguo] = id_nuevo
                
                row['id'] = id_nuevo
                
                # Actualizar referencias
                if row['inscripcion_id'] in mapeo_inscripciones:
                    row['inscripcion_id'] = mapeo_inscripciones[row['inscripcion_id']]
                
                if row['estudiante_id'] in mapeo_estudiantes:
                    row['estudiante_id'] = mapeo_estudiantes[row['estudiante_id']]
                
                if row['curso_codigo'] in mapeo_cursos:
                    row['curso_codigo'] = mapeo_cursos[row['curso_codigo']]
                
                matriculas.append(row)
        
        # Guardar matrículas actualizadas
        with open('datos/matriculas.csv', 'w', newline='', encoding='utf-8') as f:
            if matriculas:
                fieldnames = ['id', 'inscripcion_id', 'estudiante_id', 'curso_codigo', 'fecha_matricula', 'nota']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(matriculas)
        
        print(f"✅ Actualizadas {len(matriculas)} matrículas")
        
    except FileNotFoundError:
        print("⚠️  Archivo de matrículas no encontrado")
    
    print("\n🎉 Actualización de IDs completada exitosamente!")
    print("\nNuevo formato de IDs:")
    print("  • Estudiantes: E1, E2, E3...")
    print("  • Cursos: C1, C2, C3...")
    print("  • Inscripciones: I1, I2, I3...")
    print("  • Matrículas: M1, M2, M3...")

if __name__ == "__main__":
    actualizar_ids_formato()