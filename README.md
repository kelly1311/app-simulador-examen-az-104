# AZ-104 Microsoft Azure Administrator - Simulador de Examen

Aplicacion para practicar y prepararse para la certificacion **AZ-104 Microsoft Azure Administrator**.

## Descripcion

Este simulador de examen proporciona una experiencia de practica realista para la certificacion AZ-104. Incluye un banco de preguntas que cubren los cinco dominios principales del examen oficial, con explicaciones detalladas para cada respuesta.

## Versiones Disponibles

La aplicacion viene en tres versiones diferentes para adaptarse a tus preferencias:

| Archivo | Descripcion | Como Ejecutar |
|---------|-------------|---------------|
| `az104_exam.py` | Version de linea de comandos (CLI) | `python3 az104_exam.py` |
| `az104_exam_gui.py` | Version con interfaz grafica (Tkinter) | `python3 az104_exam_gui.py` |
| `az104_web_app.py` | Version web (navegador) | `python3 az104_web_app.py` |

## Temas Cubiertos

El simulador incluye preguntas de los cinco dominios del examen AZ-104:

1. **Administrar Identidades y Gobernanza de Azure**
   - Azure AD / Microsoft Entra ID
   - RBAC (Control de Acceso Basado en Roles)
   - Azure Policy
   - Grupos de Administracion
   - Managed Identities

2. **Implementacion y Administracion de Almacenamiento**
   - Cuentas de Almacenamiento
   - Blob Storage (Hot, Cool, Archive)
   - Azure Files
   - Replicacion (LRS, ZRS, GRS, GZRS)
   - Lifecycle Management

3. **Despliegue y Administracion de Recursos de Computo**
   - Maquinas Virtuales
   - Availability Sets y Zones
   - Virtual Machine Scale Sets
   - Azure App Service
   - Azure Container Instances
   - Azure Kubernetes Service (AKS)

4. **Implementacion y Administracion de Redes Virtuales**
   - Virtual Networks y Subnets
   - Network Security Groups (NSG)
   - VNet Peering
   - VPN Gateway y ExpressRoute
   - Azure Load Balancer
   - Application Gateway

5. **Monitoreo y Administracion de Recursos**
   - Azure Monitor
   - Log Analytics
   - Azure Backup
   - Azure Site Recovery
   - Alertas y Action Groups

## Caracteristicas

- **Modo Practica por Tema**: Practica preguntas de un tema especifico
- **Examen Simulado**: 40 preguntas aleatorias con temporizador de 120 minutos
- **Examen Completo**: 60 preguntas aleatorias con temporizador
- **Explicaciones Detalladas**: Cada pregunta incluye explicacion de la respuesta correcta
- **Tipos de Preguntas**: Seleccion unica y seleccion multiple
- **Revision de Respuestas**: Revisa tus respuestas al finalizar el examen
- **Desglose por Tema**: Ve tu rendimiento en cada dominio

## Requisitos

- Python 3.6 o superior
- Para la version GUI: Tkinter (incluido en la mayoria de instalaciones de Python)
- Para la version Web: Solo Python estandar (usa `http.server`)

## Uso

### Version CLI (Linea de Comandos)

```bash
python3 az104_exam.py
```

Navega usando los numeros del menu:
- `1` - Practicar por tema
- `2` - Examen simulado (40 preguntas)
- `3` - Examen completo (60 preguntas)
- `4` - Ver estadisticas
- `5` - Salir

### Version GUI (Interfaz Grafica)

```bash
python3 az104_exam_gui.py
```

Utiliza los botones de la interfaz para navegar entre las opciones.

### Version Web

```bash
python3 az104_web_app.py
```

Se abrira automaticamente tu navegador en `http://localhost:8080`. Si no se abre automaticamente, navega manualmente a esa direccion.

## Formato del Examen Real AZ-104

| Aspecto | Valor |
|---------|-------|
| Numero de preguntas | 40-60 preguntas |
| Tiempo limite | 120 minutos |
| Puntaje para aprobar | 700/1000 (~70%) |
| Idiomas disponibles | Ingles, Japones, Chino, Coreano, Aleman, Frances, Espanol, Portugues |

## Estructura del Proyecto

```
az104/
├── az104_exam.py        # Version CLI
├── az104_exam_gui.py    # Version GUI con Tkinter
├── az104_web_app.py     # Version Web
└── README.md            # Este archivo
```

## Tips para el Examen

1. **Practica con escenarios reales**: Las preguntas del examen real presentan casos de estudio
2. **Entiende la jerarquia de Azure**: Tenant > Management Groups > Subscriptions > Resource Groups > Resources
3. **Conoce los privilegios minimos**: Muchas preguntas piden el rol con "privilegios minimos"
4. **Familiarizate con Azure Policy**: Efectos como Deny, Audit, Append, DeployIfNotExists
5. **Estudia las diferencias entre servicios similares**: Load Balancer vs Application Gateway, Service Endpoints vs Private Endpoints

## Recursos Adicionales

- [Microsoft Learn - AZ-104](https://learn.microsoft.com/es-es/certifications/exams/az-104)
- [Documentacion de Azure](https://docs.microsoft.com/es-es/azure/)
- [Azure Portal](https://portal.azure.com)

## Licencia

Este proyecto es para fines educativos y de practica personal.

---

**Buena suerte en tu examen de certificacion AZ-104!**
