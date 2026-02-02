#!/usr/bin/env python3
"""
AZ-104 Microsoft Azure Administrator - Simulador de Examen
Aplicación Web Interactiva
"""

import http.server
import socketserver
import json
import webbrowser
import threading
import os
from urllib.parse import parse_qs, urlparse

PORT = 8080

# Banco de preguntas - Estilo Examen Real AZ-104
QUESTIONS_DB = {
    "governance": {
        "name": "Administrar Identidades y Gobernanza de Azure",
        "percentage": "20-25%",
        "icon": "👥",
        "color": "#4A90D9",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """CASO DE ESTUDIO: Contoso, Ltd.

Contoso tiene una suscripción de Azure llamada Sub1 que contiene los siguientes recursos:

| Nombre | Tipo | Grupo de Recursos |
|--------|------|-------------------|
| VM1 | Virtual Machine | RG-Prod |
| VM2 | Virtual Machine | RG-Prod |
| Storage1 | Storage Account | RG-Data |
| VNET1 | Virtual Network | RG-Network |

Contoso tiene un usuario llamado Admin1 que necesita poder asignar roles de Azure RBAC a otros usuarios para recursos en Sub1. Admin1 NO debe poder realizar ninguna otra tarea administrativa.

¿Qué rol debe asignar a Admin1?""",
                "options": [
                    "Owner",
                    "User Access Administrator",
                    "Contributor",
                    "Security Administrator"
                ],
                "answer": 1,
                "explanation": "User Access Administrator es el rol con privilegios mínimos que permite gestionar el acceso de usuarios a los recursos de Azure. Este rol puede crear asignaciones de roles pero no puede realizar otras tareas administrativas como crear o modificar recursos. Owner también puede asignar roles pero incluye permisos completos de administración. Contributor puede administrar recursos pero no puede asignar roles."
            },
            {
                "id": 2,
                "type": "single",
                "question": """Tiene un tenant de Microsoft Entra ID (Azure AD) llamado contoso.com que contiene los siguientes usuarios:

| Nombre | Departamento | Rol Asignado |
|--------|--------------|--------------|
| User1 | IT | Ninguno |
| User2 | HR | Ninguno |
| User3 | Finance | Groups Administrator |

User1 necesita crear grupos de seguridad en Microsoft Entra ID.

¿Cuál es el rol de Microsoft Entra ID con privilegios mínimos que debe asignar a User1?""",
                "options": [
                    "Global Administrator",
                    "Groups Administrator",
                    "User Administrator",
                    "Directory Writers"
                ],
                "answer": 1,
                "explanation": "Groups Administrator es el rol con privilegios mínimos que permite crear y gestionar todos los aspectos de los grupos en Microsoft Entra ID. User Administrator puede crear grupos pero tiene permisos adicionales innecesarios para gestionar usuarios. Global Administrator tiene todos los permisos. Directory Writers tiene permisos muy limitados y no puede crear grupos de seguridad."
            },
            {
                "id": 3,
                "type": "single",
                "question": """Fabrikam, Inc. tiene la siguiente configuración de Azure:

- Suscripción: Fabrikam-Sub1
- Tenant de Microsoft Entra: fabrikam.com
- Regiones permitidas: Solo East US y West US

Los desarrolladores de Fabrikam reportan que pueden crear máquinas virtuales en la región North Europe, lo cual viola la política de la empresa.

Necesita implementar una solución que PREVENGA la creación de recursos en regiones no autorizadas.

¿Qué efecto de Azure Policy debe usar?""",
                "options": [
                    "Audit - para registrar recursos no conformes",
                    "Deny - para prevenir la creación de recursos no conformes",
                    "Append - para agregar configuraciones a los recursos",
                    "DeployIfNotExists - para remediar recursos no conformes"
                ],
                "answer": 1,
                "explanation": "El efecto 'Deny' previene activamente la creación de recursos que no cumplan con la política. 'Audit' solo registra el incumplimiento pero permite la creación. 'Append' agrega propiedades a recursos existentes. 'DeployIfNotExists' despliega recursos de remediación después de la creación. Solo 'Deny' puede PREVENIR la creación."
            },
            {
                "id": 4,
                "type": "single",
                "question": """Tiene una aplicación web de Azure App Service llamada WebApp1 que necesita acceder a un Azure Key Vault llamado KV1 para obtener secretos.

Los requisitos son:
- La solución NO debe requerir almacenar credenciales en el código
- La solución NO debe requerir rotación manual de credenciales
- La solución debe usar el principio de privilegio mínimo

¿Qué debe configurar?""",
                "options": [
                    "Crear un usuario de Microsoft Entra y almacenar las credenciales en App Settings",
                    "Crear un Service Principal con un secreto de cliente y almacenarlo en Key Vault",
                    "Habilitar System-Assigned Managed Identity para WebApp1",
                    "Crear un grupo de Microsoft Entra y agregar WebApp1 como miembro"
                ],
                "answer": 2,
                "explanation": "System-Assigned Managed Identity es la solución correcta porque: 1) Azure gestiona automáticamente las credenciales, 2) No requiere almacenar secretos en el código ni en configuración, 3) Las credenciales rotan automáticamente, 4) La identidad se elimina automáticamente cuando se elimina el recurso. Service Principal requiere gestión manual de secretos. Las credenciales de usuario no son apropiadas para aplicaciones."
            },
            {
                "id": 5,
                "type": "single",
                "question": """Tiene la siguiente jerarquía de Azure:

Grupo de Administración Raíz (Tenant Root Group)
└── MG-Production
    ├── Sub-Prod1 (Suscripción)
    │   └── RG-Web (Grupo de Recursos)
    └── Sub-Prod2 (Suscripción)
        └── RG-Database (Grupo de Recursos)

Asigna una Azure Policy en MG-Production que requiere la etiqueta "Environment".

¿Qué recursos se verán afectados por esta política?""",
                "options": [
                    "Solo los recursos en Sub-Prod1",
                    "Solo los grupos de recursos RG-Web y RG-Database",
                    "Todos los recursos en Sub-Prod1 y Sub-Prod2",
                    "Solo los recursos creados después de asignar la política"
                ],
                "answer": 2,
                "explanation": "Las políticas asignadas a un grupo de administración se heredan a TODAS las suscripciones y recursos dentro de ese grupo de administración. La herencia va: Grupo de Administración → Suscripciones → Grupos de Recursos → Recursos. Por lo tanto, todos los recursos en Sub-Prod1 y Sub-Prod2 serán evaluados contra esta política, tanto existentes como nuevos."
            },
            {
                "id": 6,
                "type": "single",
                "question": """Un administrador con el rol de Contributor en una suscripción de Azure reporta que no puede crear una máquina virtual.

El error que recibe es: "RequestDisallowedByPolicy"

La suscripción tiene la siguiente configuración:
- Azure Policy: "Allowed virtual machine SKUs" (Solo permite Standard_D2s_v3)
- Resource Lock: No hay bloqueos configurados
- RBAC: El administrador tiene rol Contributor

El administrador intentó crear una VM con SKU Standard_B2ms.

¿Cuál es la causa del error?""",
                "options": [
                    "El rol Contributor no tiene permisos para crear VMs",
                    "Azure Policy está bloqueando la creación porque el SKU no está permitido",
                    "Existe un Resource Lock de tipo ReadOnly",
                    "El administrador necesita el rol Owner"
                ],
                "answer": 1,
                "explanation": "El error 'RequestDisallowedByPolicy' indica claramente que una Azure Policy está bloqueando la operación. La política 'Allowed virtual machine SKUs' solo permite Standard_D2s_v3, pero el administrador intentó crear una VM con Standard_B2ms. El rol Contributor tiene permisos completos para crear VMs, pero Azure Policy tiene precedencia sobre los permisos de RBAC para operaciones de escritura."
            },
            {
                "id": 7,
                "type": "single",
                "question": """Litware, Inc. tiene el siguiente requisito de cumplimiento:

"Todos los recursos de Azure DEBEN tener una etiqueta llamada 'CostCenter' con un valor válido. Los recursos que no tengan esta etiqueta NO deben poder crearse."

Necesita implementar este requisito usando Azure Policy.

¿Qué definición de política integrada debe usar?""",
                "options": [
                    "Require a tag on resources",
                    "Require a tag on resource groups",
                    "Inherit a tag from the resource group if missing",
                    "Add a tag to resources"
                ],
                "answer": 0,
                "explanation": "'Require a tag on resources' usa el efecto Deny para prevenir la creación de recursos que no tengan la etiqueta especificada. 'Require a tag on resource groups' solo aplica a grupos de recursos, no a recursos individuales. 'Inherit a tag from the resource group' copia etiquetas pero no previene la creación. 'Add a tag to resources' usa Modify para agregar etiquetas después de la creación, no previene la creación."
            },
            {
                "id": 8,
                "type": "single",
                "question": """Tiene una suscripción de Azure con Microsoft Entra ID Premium P2.

Necesita configurar lo siguiente:
- Revisiones periódicas trimestrales de los miembros del grupo "Azure-Admins"
- Los revisores deben ser los managers de cada miembro
- Los miembros que no sean aprobados deben ser removidos automáticamente

¿Dónde debe configurar esto?""",
                "options": [
                    "Microsoft Entra ID > Privileged Identity Management",
                    "Microsoft Entra ID > Identity Protection",
                    "Microsoft Entra ID > Identity Governance > Access Reviews",
                    "Microsoft Entra ID > Conditional Access"
                ],
                "answer": 2,
                "explanation": "Access Reviews en Identity Governance es la característica específica para configurar revisiones periódicas de membresía de grupos. Permite configurar: frecuencia de revisión, quiénes son los revisores, y acciones automáticas para miembros no aprobados (como remoción). PIM es para acceso privilegiado just-in-time. Identity Protection es para detección de riesgos. Conditional Access es para políticas de acceso basadas en condiciones."
            },
            {
                "id": 9,
                "type": "single",
                "question": """Tiene la siguiente configuración:

- Suscripción: Contoso-Sub1
  - Grupo de Recursos: RG-Production
    - VM: VM-Web01
    - VM: VM-Web02
  - Grupo de Recursos: RG-Development
    - VM: VM-Dev01

Un desarrollador llamado Dev1 necesita:
- Iniciar y detener VM-Dev01
- NO debe poder acceder a ningún recurso en RG-Production

¿En qué ámbito debe asignar el rol "Virtual Machine Contributor" a Dev1?""",
                "options": [
                    "A nivel de suscripción Contoso-Sub1",
                    "A nivel de grupo de administración",
                    "A nivel del grupo de recursos RG-Development",
                    "A nivel de la VM VM-Dev01"
                ],
                "answer": 2,
                "explanation": "Para cumplir con el principio de privilegio mínimo, el rol debe asignarse en el ámbito más restrictivo posible. Asignar a nivel de RG-Development permite a Dev1 administrar VMs en ese grupo de recursos (actualmente solo VM-Dev01) pero no en RG-Production. Asignar a nivel de VM individual sería más restrictivo pero limitaría la capacidad de crear nuevas VMs de desarrollo si fuera necesario."
            },
            {
                "id": 10,
                "type": "single",
                "question": """Su empresa tiene los siguientes requisitos para administradores de Azure:

1. Los administradores deben solicitar acceso a roles privilegiados cuando los necesiten
2. Las solicitudes deben requerir aprobación de un administrador senior
3. El acceso privilegiado debe ser temporal (máximo 8 horas)
4. Todas las activaciones deben requerir justificación

¿Qué característica de Microsoft Entra debe implementar?""",
                "options": [
                    "Conditional Access con control de sesión",
                    "Privileged Identity Management (PIM)",
                    "Identity Protection con políticas de riesgo",
                    "Roles personalizados de Azure RBAC"
                ],
                "answer": 1,
                "explanation": "Privileged Identity Management (PIM) proporciona exactamente estas capacidades: 1) Activación just-in-time de roles, 2) Flujos de trabajo de aprobación, 3) Acceso con límite de tiempo, 4) Requisito de justificación. También proporciona alertas y auditoría de activaciones. Conditional Access no proporciona activación de roles. Identity Protection es para detección de riesgos. RBAC personalizado no proporciona acceso temporal."
            },
            {
                "id": 11,
                "type": "multiple",
                "question": """Tiene un entorno híbrido con Active Directory Domain Services (AD DS) on-premises y Microsoft Entra ID.

Necesita implementar sincronización de identidades usando Microsoft Entra Connect.

¿Cuáles DOS métodos de autenticación puede configurar con Microsoft Entra Connect? (Seleccione dos)""",
                "options": [
                    "Password Hash Synchronization (PHS)",
                    "Certificate-based authentication",
                    "Pass-through Authentication (PTA)",
                    "RADIUS authentication"
                ],
                "answer": [0, 2],
                "explanation": "Microsoft Entra Connect soporta tres métodos de autenticación: 1) Password Hash Synchronization (PHS) - sincroniza hashes de contraseñas a la nube, 2) Pass-through Authentication (PTA) - valida contraseñas directamente contra AD DS on-premises, 3) Federation con AD FS (no listada). Certificate-based y RADIUS authentication no son métodos de autenticación de Microsoft Entra Connect."
            },
            {
                "id": 12,
                "type": "single",
                "question": """Tiene una suscripción de Azure con múltiples grupos de recursos que contienen cientos de recursos.

El CFO necesita:
- Ver los costos de TODOS los recursos en la suscripción
- Crear reportes de costos y exportarlos
- Configurar presupuestos y alertas de costos
- NO debe poder crear, modificar o eliminar ningún recurso

¿Qué rol de Azure RBAC debe asignar al CFO?""",
                "options": [
                    "Reader",
                    "Cost Management Reader",
                    "Billing Reader",
                    "Cost Management Contributor"
                ],
                "answer": 3,
                "explanation": "Cost Management Contributor permite: ver costos, crear/gestionar exportaciones de costos, crear/gestionar presupuestos y alertas, pero NO permite modificar recursos. Cost Management Reader solo puede VER datos de costos, no puede crear presupuestos ni exportaciones. Reader puede ver recursos pero no datos detallados de costos. Billing Reader es para facturación a nivel de cuenta/suscripción, no para análisis de costos de recursos."
            },
            {
                "id": 13,
                "type": "single",
                "question": """Tailwind Traders tiene la siguiente estructura de Azure:

Suscripciones:
- TT-Production
- TT-Development
- TT-Testing
- TT-Sandbox

Necesita aplicar las siguientes políticas de manera consistente en TODAS las suscripciones:
- Allowed locations: East US, West US
- Require tag: Environment
- Allowed VM SKUs: Standard_D series only

¿Cuál es la forma MÁS eficiente de implementar esto?""",
                "options": [
                    "Asignar las políticas individualmente en cada suscripción",
                    "Crear un Management Group, mover las suscripciones, y asignar las políticas al Management Group",
                    "Usar Azure Automation para aplicar las políticas",
                    "Crear una Azure Blueprint y desplegarla en cada suscripción"
                ],
                "answer": 1,
                "explanation": "Usar un Management Group es la forma más eficiente porque: 1) Las políticas se heredan automáticamente a todas las suscripciones hijas, 2) Cualquier nueva suscripción agregada al grupo heredará las políticas automáticamente, 3) Gestión centralizada desde un solo lugar. Asignar individualmente no escala y requiere gestión manual. Azure Automation no es para políticas. Blueprints son para despliegues completos, no solo políticas."
            },
            {
                "id": 14,
                "type": "multiple",
                "question": """Tiene los siguientes requisitos de seguridad para Microsoft Entra ID:

1. Los usuarios deben poder registrar sus dispositivos personales para acceder a recursos corporativos
2. Los administradores deben usar MFA cuando accedan al portal de Azure

¿Cuáles DOS características debe configurar? (Seleccione dos)""",
                "options": [
                    "Microsoft Entra Join para dispositivos corporativos",
                    "Self-Service Password Reset (SSPR)",
                    "Conditional Access con política para administradores",
                    "Microsoft Entra Device Registration para dispositivos personales"
                ],
                "answer": [2, 3],
                "explanation": "Para cumplir los requisitos: 1) Microsoft Entra Device Registration permite a usuarios registrar dispositivos personales (BYOD) sin unirlos completamente al directorio. 2) Conditional Access permite crear políticas que requieran MFA basado en condiciones como rol del usuario (administradores) y aplicación de destino (portal de Azure). Microsoft Entra Join es para dispositivos corporativos propiedad de la organización. SSPR es para restablecimiento de contraseñas."
            },
            {
                "id": 15,
                "type": "single",
                "question": """Tiene un grupo de recursos llamado RG-Applications que contiene varios recursos.

Crea una Azure Policy con las siguientes características:
- Definición: "Inherit a tag from the resource group"
- Tag name: Environment
- Efecto: Modify

El grupo de recursos RG-Applications tiene la etiqueta: Environment = Production

¿Qué sucederá con los recursos en RG-Applications?""",
                "options": [
                    "Los recursos existentes y nuevos recibirán automáticamente la etiqueta Environment = Production",
                    "Solo los recursos nuevos recibirán la etiqueta automáticamente",
                    "Los recursos existentes recibirán la etiqueta, los nuevos deben etiquetarse manualmente",
                    "Los recursos existentes recibirán la etiqueta solo después de ejecutar una tarea de remediación"
                ],
                "answer": 3,
                "explanation": "Las políticas con efecto 'Modify' funcionan así: 1) Para recursos NUEVOS: la etiqueta se aplica automáticamente durante la creación, 2) Para recursos EXISTENTES: se requiere ejecutar una tarea de remediación para aplicar la etiqueta. Esto es porque las políticas no modifican recursos existentes automáticamente para evitar cambios no deseados. Debe crear una tarea de remediación desde la vista de cumplimiento de la política."
            }
        ]
    },
    "storage": {
        "name": "Implementar y Administrar Almacenamiento",
        "percentage": "15-20%",
        "icon": "💾",
        "color": "#50C878",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso almacena registros de transacciones en Azure Blob Storage.

Patrón de acceso de los datos:
- Días 1-30: Acceso frecuente para análisis en tiempo real
- Días 31-90: Acceso ocasional para reportes mensuales
- Días 91-365: Acceso muy raro, solo para auditoría
- Después de 365 días: Retención legal, acceso extremadamente raro

Contoso necesita optimizar costos manteniendo los datos accesibles cuando se necesiten.

¿Qué debe configurar?""",
                "options": [
                    "Hot tier para todos los blobs con eliminación después de 365 días",
                    "Cool tier para todos los blobs con lifecycle management",
                    "Hot tier con lifecycle management policy que mueva a Cool, luego a Archive",
                    "Archive tier para todos los blobs desde el inicio"
                ],
                "answer": 2,
                "explanation": "La solución correcta es: Hot tier inicial (acceso frecuente días 1-30) con lifecycle management que automáticamente mueva blobs a Cool tier (días 31-90), luego a Archive tier (después de 90 días). Esto optimiza costos: Hot es más caro pero óptimo para acceso frecuente, Cool es más económico para acceso ocasional, Archive es el más económico para retención a largo plazo."
            },
            {
                "id": 2,
                "type": "single",
                "question": """Fabrikam tiene una aplicación crítica que almacena datos en Azure Storage.

Requisitos:
- Los datos deben sobrevivir a la pérdida completa de un datacenter
- Los datos deben sobrevivir a la pérdida completa de una región de Azure
- Se requiere acceso de lectura a los datos en la región secundaria durante una interrupción regional
- Minimizar costos dentro de estos requisitos

¿Qué opción de redundancia debe elegir?""",
                "options": [
                    "Locally Redundant Storage (LRS)",
                    "Zone-Redundant Storage (ZRS)",
                    "Geo-Redundant Storage (GRS)",
                    "Read-Access Geo-Redundant Storage (RA-GRS)"
                ],
                "answer": 3,
                "explanation": "RA-GRS es la respuesta correcta porque: 1) Replica datos a una región secundaria (resistencia regional), 2) Mantiene 3 copias en la región primaria, 3) Proporciona acceso de LECTURA a la región secundaria SIN esperar failover. GRS también replica geográficamente pero NO proporciona acceso de lectura a la secundaria durante operación normal. ZRS protege contra falla de datacenter pero no contra falla regional. LRS solo protege contra falla de hardware."
            },
            {
                "id": 3,
                "type": "single",
                "question": """Tiene la siguiente configuración:

- 10 VMs Windows Server en Azure (diferentes regiones)
- Aplicación que requiere compartir archivos de configuración entre todas las VMs
- Los archivos deben ser accesibles mediante rutas UNC estándar de Windows (\\\\server\\share)
- Tamaño total estimado: 500 GB

¿Qué servicio de Azure Storage debe usar?""",
                "options": [
                    "Azure Blob Storage con contenedor público",
                    "Azure Files con SMB file share",
                    "Azure Queue Storage",
                    "Azure Table Storage"
                ],
                "answer": 1,
                "explanation": "Azure Files es el servicio correcto porque: 1) Proporciona file shares accesibles via protocolo SMB 3.0, 2) Compatible con rutas UNC de Windows (\\\\storageaccount.file.core.windows.net\\sharename), 3) Puede montarse en múltiples VMs simultáneamente, 4) Soporta los 500 GB requeridos (hasta 100 TiB por share). Blob Storage no soporta SMB ni rutas UNC directamente."
            },
            {
                "id": 4,
                "type": "single",
                "question": """Su empresa tiene requisitos de seguridad estrictos para datos almacenados en Azure:

Requisito: "Todos los datos en reposo deben estar cifrados con claves controladas y rotadas por nuestra organización. Las claves deben almacenarse en un HSM validado FIPS 140-2 Level 2."

¿Qué configuración de cifrado debe implementar?""",
                "options": [
                    "Storage Service Encryption (SSE) con Microsoft-managed keys",
                    "Storage Service Encryption (SSE) con Customer-managed keys en Azure Key Vault",
                    "Client-side encryption antes de subir los datos",
                    "Azure Disk Encryption para las VMs que acceden al storage"
                ],
                "answer": 1,
                "explanation": "SSE con Customer-managed keys (CMK) en Azure Key Vault cumple todos los requisitos: 1) Cifrado de datos en reposo automático, 2) La organización controla las claves en su propio Key Vault, 3) La organización puede rotar las claves según su política, 4) Azure Key Vault usa HSMs validados FIPS 140-2 Level 2 (o Level 3 con Key Vault Premium/HSM). Microsoft-managed keys no da control a la organización."
            },
            {
                "id": 5,
                "type": "single",
                "question": """Un partner externo necesita acceso temporal a un blob específico en su cuenta de almacenamiento.

Requisitos:
- Acceso solo de lectura
- Válido solo por 24 horas
- No debe requerir cuenta de Azure del partner
- No debe exponer las claves de la cuenta de almacenamiento
- Debe poder revocar el acceso si es necesario antes de que expire

¿Qué debe proporcionar al partner?""",
                "options": [
                    "Las Access Keys de la cuenta de almacenamiento",
                    "Una Shared Access Signature (SAS) con User Delegation key",
                    "Habilitar acceso anónimo público al contenedor",
                    "Crear una cuenta de usuario de Microsoft Entra para el partner"
                ],
                "answer": 1,
                "explanation": "User Delegation SAS es la mejor opción porque: 1) Proporciona acceso granular al blob específico, 2) Puede configurarse solo para lectura, 3) Tiene tiempo de expiración (24 horas), 4) No expone las claves de la cuenta, 5) Puede revocarse revocando las credenciales del usuario que creó el SAS o rotando las claves de delegación. Las Access Keys dan acceso completo. El acceso público no tiene control de tiempo. Una cuenta de usuario requiere licencia y es excesivo para acceso temporal."
            },
            {
                "id": 6,
                "type": "single",
                "question": """Su empresa está sujeta a regulaciones financieras que requieren:

"Los registros de transacciones deben retenerse por exactamente 7 años. Durante este período, los registros NO pueden ser eliminados ni modificados bajo ninguna circunstancia, incluyendo por administradores."

La cuenta de almacenamiento se llama contosotransactions.

¿Qué debe configurar en el contenedor de blobs?""",
                "options": [
                    "Soft delete con período de retención de 7 años",
                    "Immutable storage con time-based retention policy de 7 años en estado Locked",
                    "Lifecycle management policy para eliminar después de 7 años",
                    "Legal hold sin fecha de expiración"
                ],
                "answer": 1,
                "explanation": "Immutable storage con time-based retention policy en estado LOCKED garantiza: 1) Los blobs no pueden eliminarse ni modificarse durante el período de retención (WORM - Write Once Read Many), 2) El período de 7 años se aplica desde la creación/modificación del blob, 3) Una vez LOCKED, la política no puede reducirse ni eliminarse. Soft delete permite recuperación pero no previene eliminación. Legal hold no tiene fecha de expiración definida. El estado LOCKED es crítico - sin él, la política puede modificarse."
            },
            {
                "id": 7,
                "type": "single",
                "question": """Necesita migrar 80 TB de datos desde un datacenter on-premises a Azure Blob Storage.

Restricciones:
- Ancho de banda de Internet: 100 Mbps (compartido con otras aplicaciones)
- Ventana de migración: máximo 2 semanas
- Los datos contienen información sensible (PII)

Cálculo aproximado: 80 TB a 100 Mbps = ~74 días de transferencia continua

¿Qué solución de migración debe usar?""",
                "options": [
                    "AzCopy sobre Internet con múltiples hilos",
                    "Azure Data Box (dispositivo de 100 TB)",
                    "Azure File Sync",
                    "Azure Storage Explorer con conexión ExpressRoute"
                ],
                "answer": 1,
                "explanation": "Azure Data Box es la solución correcta porque: 1) Dispositivo físico de 100 TB (suficiente para 80 TB), 2) Microsoft envía el dispositivo, se copian los datos localmente, se envía de vuelta, y Microsoft carga los datos a Azure, 3) Tiempo total típico: 7-10 días incluyendo envío, 4) Los datos están cifrados con AES-256 durante el transporte, 5) Cumple con la ventana de 2 semanas. AzCopy a 100 Mbps tomaría más de 2 meses. ExpressRoute requeriría provisioning adicional."
            },
            {
                "id": 8,
                "type": "single",
                "question": """Tiene un servidor de archivos Windows on-premises con 2 TB de datos.

Requisitos:
- Sincronizar archivos con Azure Files para backup y DR
- Mantener archivos accedidos frecuentemente en caché local
- Archivos raramente accedidos deben moverse a la nube automáticamente
- Los usuarios deben poder acceder a todos los archivos como si estuvieran locales

¿Qué debe implementar?""",
                "options": [
                    "Azure Backup con Recovery Services vault",
                    "Azure File Sync con cloud tiering habilitado",
                    "Robocopy programado para copiar a Azure Files",
                    "Azure Data Box Gateway"
                ],
                "answer": 1,
                "explanation": "Azure File Sync con cloud tiering es la solución correcta: 1) Sincroniza archivos bidireccionales entre servidor on-premises y Azure Files, 2) Cloud tiering mantiene archivos frecuentes localmente y mueve los menos usados a Azure (solo metadata y punteros locales), 3) Los archivos tiered aparecen normalmente en el servidor pero se descargan on-demand cuando se acceden, 4) Proporciona DR porque los datos están en Azure. Azure Backup es solo para backup, no sincronización activa. Robocopy no proporciona cloud tiering."
            },
            {
                "id": 9,
                "type": "single",
                "question": """Tiene la siguiente configuración:

Storage Account: stcontoso (firewall habilitado)
- Allowed networks: VNet-Prod (10.1.0.0/16)

VNet-Dev (10.2.0.0/16) contiene una VM llamada VM-Dev que necesita acceder a stcontoso.
VNet-Dev NO está conectada a VNet-Prod.

Error actual: "This request is not authorized to perform this operation"

¿Qué debe configurar para permitir el acceso desde VM-Dev?""",
                "options": [
                    "Crear VNet peering entre VNet-Dev y VNet-Prod",
                    "Agregar la subnet de VM-Dev a las reglas de firewall de la cuenta de almacenamiento",
                    "Habilitar Service Endpoint para Microsoft.Storage en la subnet de VNet-Dev",
                    "Combinar B y C: Habilitar Service Endpoint Y agregar la subnet a las reglas de firewall"
                ],
                "answer": 3,
                "explanation": "Se requieren AMBOS pasos: 1) Habilitar Service Endpoint para Microsoft.Storage en la subnet de VNet-Dev - esto permite que el tráfico use la red backbone de Azure en lugar de Internet público, 2) Agregar esa subnet a las reglas de firewall de la cuenta de almacenamiento - esto autoriza el tráfico desde esa subnet. Solo crear VNet peering no funcionaría porque el firewall bloquea todo excepto las redes explícitamente permitidas. Solo agregar la subnet no funciona sin el Service Endpoint habilitado."
            },
            {
                "id": 10,
                "type": "single",
                "question": """Tiene blobs almacenados en Archive tier en una cuenta de Azure Storage.

Un auditor necesita acceso urgente a un blob específico (audit-2023-q1.zip, 50 GB) que está en Archive tier. El auditor necesita el archivo lo antes posible.

¿Cuál es la opción MÁS RÁPIDA para obtener acceso al blob?""",
                "options": [
                    "Acceder directamente al blob - Archive tier permite acceso inmediato",
                    "Rehidratar el blob con prioridad Standard (hasta 15 horas)",
                    "Rehidratar el blob con prioridad High (típicamente menos de 1 hora)",
                    "Copiar el blob a otra cuenta de almacenamiento"
                ],
                "answer": 2,
                "explanation": "Los blobs en Archive tier NO pueden accederse directamente - deben rehidratarse primero a Hot o Cool tier. La opción más rápida es rehidratación con prioridad High, que típicamente completa en menos de 1 hora para blobs de menos de 10 GB y puede tomar más para blobs más grandes pero sigue siendo mucho más rápido que Standard. Standard priority puede tomar hasta 15 horas. Copiar el blob no es posible directamente desde Archive sin rehidratación."
            },
            {
                "id": 11,
                "type": "single",
                "question": """Está creando una cuenta de almacenamiento para un proyecto de big data analytics.

Requisitos:
- Almacenar petabytes de datos estructurados y no estructurados
- Soporte para procesamiento con Apache Spark, Databricks y HDInsight
- Organización jerárquica de datos (directorios y subdirectorios)
- Permisos granulares a nivel de directorio usando ACLs
- Compatible con HDFS (Hadoop Distributed File System)

¿Qué debe habilitar al crear la cuenta de almacenamiento?""",
                "options": [
                    "Large file shares",
                    "Hierarchical namespace",
                    "NFS 3.0 protocol support",
                    "SFTP support"
                ],
                "answer": 1,
                "explanation": "Hierarchical namespace habilita Azure Data Lake Storage Gen2, que proporciona: 1) Sistema de archivos jerárquico real con directorios (no pseudo-directorios como Blob Storage estándar), 2) ACLs POSIX para permisos granulares, 3) Compatibilidad con HDFS para herramientas de big data (Spark, Databricks, HDInsight), 4) Rendimiento optimizado para analytics. Large file shares es para Azure Files. NFS 3.0 y SFTP son protocolos de acceso pero no proporcionan las capacidades de Data Lake."
            },
            {
                "id": 12,
                "type": "single",
                "question": """La cuenta de almacenamiento stcontoso tiene la siguiente configuración:

- Blob soft delete: Habilitado (14 días de retención)
- Container soft delete: Habilitado (7 días de retención)
- Versioning: Deshabilitado

Un administrador ejecutó el siguiente comando por error hace 2 días:

Remove-AzStorageBlob -Container "reports" -Blob "financial-report-2023.xlsx"

¿Cómo puede recuperar el archivo?""",
                "options": [
                    "No es posible recuperar el archivo",
                    "Restaurar desde Azure Backup",
                    "Usar la opción 'Undelete' en el blob soft-deleted desde el portal o PowerShell",
                    "Contactar Microsoft Support para recuperación de emergencia"
                ],
                "answer": 2,
                "explanation": "Con soft delete habilitado, los blobs eliminados no se borran permanentemente de inmediato. Se mantienen en estado 'soft-deleted' durante el período de retención (14 días en este caso). Como solo han pasado 2 días, el blob puede recuperarse usando: 1) Azure Portal: navegar al contenedor, mostrar blobs eliminados, seleccionar y hacer 'Undelete', 2) PowerShell: Get-AzStorageBlob -Container reports -Blob financial-report-2023.xlsx -IncludeDeleted | Undelete-AzStorageBlob. No se requiere Azure Backup si soft delete está configurado."
            },
            {
                "id": 13,
                "type": "multiple",
                "question": """Tiene una aplicación web (WebApp1) que necesita:
1. Escribir archivos de log a Azure Blob Storage
2. Los logs deben ser accesibles públicamente para un sistema de monitoreo externo que no tiene credenciales de Azure

La cuenta de almacenamiento stlogs tiene un contenedor llamado "applogs".

¿Cuáles DOS configuraciones debe realizar? (Seleccione dos)""",
                "options": [
                    "Configurar el nivel de acceso público del contenedor a 'Blob (anonymous read access for blobs only)'",
                    "Habilitar Static Website hosting en la cuenta de almacenamiento",
                    "Asignar el rol 'Storage Blob Data Contributor' a la Managed Identity de WebApp1",
                    "Deshabilitar 'Require secure transfer' en la cuenta de almacenamiento"
                ],
                "answer": [0, 2],
                "explanation": "Se necesitan dos configuraciones: 1) Asignar 'Storage Blob Data Contributor' a la Managed Identity de WebApp1 - esto permite que la aplicación escriba logs usando autenticación de identidad administrada (más seguro que access keys), 2) Configurar acceso público a nivel de blob en el contenedor - esto permite que el sistema de monitoreo externo lea los logs sin autenticación. Static Website no es necesario para este escenario. Deshabilitar secure transfer reduciría la seguridad innecesariamente."
            },
            {
                "id": 14,
                "type": "single",
                "question": """Necesita copiar blobs desde una cuenta de almacenamiento (stsource) a otra cuenta (stdestination).

Requisitos:
- Ambas cuentas están en la misma región
- Los datos deben copiarse de forma asíncrona
- El proceso de copia debe manejarse completamente por Azure (server-side)
- No debe consumir ancho de banda del cliente
- Necesita poder monitorear el progreso de la copia

¿Qué operación debe usar?""",
                "options": [
                    "AzCopy sync desde línea de comandos local",
                    "Copy Blob operation (Start-AzStorageBlobCopy en PowerShell)",
                    "Azure Data Factory Copy Activity",
                    "Storage Explorer drag and drop"
                ],
                "answer": 1,
                "explanation": "Copy Blob operation (Start-AzStorageBlobCopy) es una operación asíncrona server-side que: 1) Copia datos directamente entre cuentas de almacenamiento en la infraestructura de Azure, 2) No requiere descargar/subir datos a través del cliente, 3) Devuelve inmediatamente y la copia continúa en background, 4) El estado puede monitorearse con Get-AzStorageBlobCopyState. AzCopy descarga/sube a través del cliente. Data Factory es más complejo de lo necesario para copia simple. Storage Explorer también usa ancho de banda del cliente."
            },
            {
                "id": 15,
                "type": "single",
                "question": """Su aplicación necesita procesar mensajes de manera confiable con las siguientes características:

- Millones de mensajes por día
- Procesamiento estrictamente en orden FIFO (First-In-First-Out)
- Garantía de entrega exactamente una vez (exactly-once delivery)
- Los mensajes pueden agruparse en sesiones (todos los mensajes de una transacción juntos)
- Tamaño máximo de mensaje: 1 MB

¿Qué servicio de Azure debe usar?""",
                "options": [
                    "Azure Blob Storage con lease",
                    "Azure Queue Storage",
                    "Azure Service Bus Queue con Sessions habilitadas",
                    "Azure Table Storage"
                ],
                "answer": 2,
                "explanation": "Azure Service Bus Queue con Sessions proporciona: 1) FIFO garantizado cuando se usan sesiones (los mensajes con el mismo SessionId se procesan en orden), 2) Entrega exactly-once con transacciones, 3) Soporte para mensajes hasta 256 KB (Standard) o 100 MB (Premium), 4) Sesiones para agrupar mensajes relacionados. Azure Queue Storage es más simple pero solo garantiza FIFO aproximado y at-least-once delivery. Blob Storage y Table Storage no son servicios de mensajería."
            }
        ]
    },
    "compute": {
        "name": "Desplegar y Administrar Recursos de Cómputo",
        "percentage": "20-25%",
        "icon": "🖥️",
        "color": "#FF6B6B",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso está desplegando una aplicación de producción crítica.

Requisitos de la aplicación:
- SLA de 99.99% de disponibilidad
- La aplicación debe continuar funcionando si un datacenter completo de Azure falla
- La aplicación corre en VMs Windows Server
- Se requieren al menos 2 instancias para alta disponibilidad

La región seleccionada es East US, que tiene 3 Availability Zones.

¿Qué configuración de disponibilidad cumple con los requisitos?""",
                "options": [
                    "Una VM con Premium SSD",
                    "Múltiples VMs en un Availability Set (diferentes Fault Domains)",
                    "Múltiples VMs distribuidas en diferentes Availability Zones",
                    "Una VM en cada región de Azure (East US y West US)"
                ],
                "answer": 2,
                "explanation": "Para lograr 99.99% SLA se requieren múltiples VMs en diferentes Availability Zones. Availability Zones son datacenters físicamente separados dentro de una región, con energía, refrigeración y red independientes. Un Availability Set solo proporciona 99.95% SLA (protege contra fallas de rack/hardware, no de datacenter). Una sola VM con Premium SSD tiene 99.9% SLA. La distribución multi-región agrega complejidad innecesaria cuando las Availability Zones cumplen el requisito."
            },
            {
                "id": 2,
                "type": "single",
                "question": """Tiene una VM de Azure llamada VM1 con la siguiente configuración:

| Propiedad | Valor |
|-----------|-------|
| Tamaño actual | Standard_D2s_v3 (2 vCPU, 8 GB RAM) |
| Estado | Running |
| Discos | OS: Premium SSD, Data: Standard SSD |

Necesita cambiar el tamaño a Standard_D4s_v3 (4 vCPU, 16 GB RAM) para manejar mayor carga.

¿Qué sucederá cuando cambie el tamaño de la VM?""",
                "options": [
                    "El cambio se aplicará sin interrupción (hot resize)",
                    "La VM se reiniciará para aplicar el nuevo tamaño",
                    "La VM se detendrá permanentemente y deberá iniciarla manualmente",
                    "Se creará una nueva VM con el nuevo tamaño y la original se eliminará"
                ],
                "answer": 1,
                "explanation": "Cuando redimensiona una VM en ejecución, Azure la reiniciará automáticamente. El proceso es: 1) Azure apaga la VM (graceful shutdown), 2) Realoca recursos para el nuevo tamaño, 3) Reinicia la VM automáticamente. La IP privada se mantiene. La IP pública dinámica podría cambiar (use IP estática para evitarlo). El reinicio típicamente toma unos minutos. Los datos en los discos no se afectan."
            },
            {
                "id": 3,
                "type": "single",
                "question": """Está desplegando múltiples VMs Windows Server usando una plantilla ARM.

Requisitos de configuración post-despliegue:
- Instalar IIS en todas las VMs
- Configurar el firewall de Windows
- Copiar archivos de configuración desde un Storage Account
- Unir las VMs al dominio de Active Directory

La configuración debe ejecutarse automáticamente sin intervención manual después del despliegue.

¿Qué debe usar?""",
                "options": [
                    "Boot diagnostics para verificar el proceso de arranque",
                    "Custom Script Extension para ejecutar un script de PowerShell",
                    "Run Command para ejecutar comandos después del despliegue",
                    "Serial Console para acceder a la consola de la VM"
                ],
                "answer": 1,
                "explanation": "Custom Script Extension es la solución correcta porque: 1) Se ejecuta automáticamente durante o inmediatamente después del despliegue de la VM, 2) Puede descargar scripts desde Azure Storage o URLs públicas, 3) Ejecuta scripts de PowerShell (Windows) o Bash (Linux), 4) Se puede incluir en plantillas ARM para despliegue repetible. Run Command es para ejecución manual/ad-hoc. Boot diagnostics es solo para troubleshooting. Serial Console es para acceso interactivo de emergencia."
            },
            {
                "id": 4,
                "type": "single",
                "question": """Necesita ejecutar un job de procesamiento por lotes que:

- Ejecuta en un contenedor Docker
- Se ejecuta una vez al día durante aproximadamente 30 minutos
- Procesa archivos de Azure Blob Storage
- No requiere orquestación compleja
- Debe minimizar costos (pago solo por tiempo de ejecución)

¿Qué servicio de Azure debe usar?""",
                "options": [
                    "Azure Virtual Machine con Docker instalado",
                    "Azure Kubernetes Service (AKS)",
                    "Azure Container Instances (ACI)",
                    "Azure App Service for Containers"
                ],
                "answer": 2,
                "explanation": "Azure Container Instances (ACI) es la mejor opción porque: 1) Es serverless - no hay servidores que administrar, 2) Facturación por segundo de ejecución (solo paga los ~30 minutos de ejecución diaria), 3) Inicio rápido de contenedores (segundos), 4) Ideal para jobs batch y tareas de corta duración, 5) Integración fácil con Azure Storage. VMs tienen costo continuo y requieren gestión. AKS es excesivo para un job simple y tiene costo del cluster. App Service tiene costo del plan incluso sin uso."
            },
            {
                "id": 5,
                "type": "single",
                "question": """Una VM Windows llamada VM-Prod01 no responde después de instalar un nuevo driver de red.

Síntomas:
- RDP no conecta (timeout)
- El ping a la IP privada no responde
- El portal de Azure muestra la VM como "Running"
- Boot diagnostics muestra que Windows arrancó pero la pantalla de login no aparece

Necesita acceder a la VM para desinstalar el driver problemático.

¿Qué herramienta debe usar?""",
                "options": [
                    "Azure Bastion para conectar via RDP en el navegador",
                    "Serial Console para acceder a la consola de comandos",
                    "Run Command para ejecutar scripts remotamente",
                    "Reiniciar la VM desde el portal de Azure"
                ],
                "answer": 1,
                "explanation": "Serial Console es la herramienta correcta porque: 1) Proporciona acceso a la consola de la VM a través de una conexión serial, independiente de la red, 2) Funciona incluso cuando RDP/SSH no funcionan debido a problemas de red o configuración, 3) Permite acceder a CMD o PowerShell para troubleshooting, 4) Puede usarse para deshabilitar drivers, modificar configuración de red, etc. Azure Bastion también usa la red de la VM (no funcionaría). Run Command requiere que el VM Agent esté respondiendo. Reiniciar probablemente no resolvería el problema del driver."
            },
            {
                "id": 6,
                "type": "single",
                "question": """Está desplegando una aplicación web en Azure App Service.

Requisitos:
- Configurar auto-scaling basado en uso de CPU
- Desplegar a 5 deployment slots para CI/CD
- Usar dominio personalizado con SSL
- Ejecutar WebJobs continuos

¿Cuál es el tier MÍNIMO de App Service Plan que cumple con TODOS los requisitos?""",
                "options": [
                    "Free (F1)",
                    "Basic (B1)",
                    "Standard (S1)",
                    "Premium (P1v2)"
                ],
                "answer": 2,
                "explanation": "Standard (S1) es el tier mínimo que cumple TODOS los requisitos: 1) Auto-scaling: Standard y superiores, 2) Deployment slots: Standard permite 5 slots, Basic no tiene slots, 3) Custom domains con SSL: Todos los tiers pagados (Basic y superiores), 4) WebJobs continuos: Basic y superiores. Free no soporta custom domains ni WebJobs continuos. Basic no tiene auto-scaling ni deployment slots. Standard (S1) cumple todos los requisitos con el costo mínimo."
            },
            {
                "id": 7,
                "type": "single",
                "question": """Tiene una VM con un disco OS de 128 GB (Premium SSD P10).

La partición de Windows está quedando sin espacio y necesita expandir el disco OS a 256 GB.

¿Cuáles son los pasos correctos para expandir el disco OS?""",
                "options": [
                    "Desde el portal, expandir el disco mientras la VM está Running",
                    "1) Deallocate la VM, 2) Expandir el disco desde el portal, 3) Start la VM, 4) Extender la partición dentro de Windows",
                    "Crear un nuevo disco de 256 GB, copiar datos, y reemplazar el disco OS",
                    "Expandir directamente desde Disk Management dentro de Windows sin cambios en Azure"
                ],
                "answer": 1,
                "explanation": "El proceso correcto es: 1) DEALLOCATE la VM (Stop-AzVM -ResourceGroupName RG -Name VM -Force), 2) Expandir el disco en Azure Portal o PowerShell (Update-AzDisk), 3) START la VM, 4) Dentro de Windows, usar Disk Management o diskpart para extender la partición al nuevo tamaño. No puede expandir un disco OS mientras la VM está running. La expansión en Azure solo aumenta el tamaño del disco virtual; el sistema operativo debe reconocer y usar el espacio adicional."
            },
            {
                "id": 8,
                "type": "single",
                "question": """Está evaluando Azure Kubernetes Service (AKS) para su organización.

Su equipo pregunta: "¿Qué componentes de Kubernetes administra Microsoft y cuáles administramos nosotros?"

¿Cuál es la responsabilidad de administración correcta en AKS?""",
                "options": [
                    "Microsoft administra todo: control plane, worker nodes, y aplicaciones",
                    "Microsoft administra el control plane; usted administra worker nodes y aplicaciones",
                    "Usted administra todo, Microsoft solo proporciona la infraestructura de red",
                    "Microsoft administra worker nodes; usted administra el control plane y aplicaciones"
                ],
                "answer": 1,
                "explanation": "En AKS, Microsoft administra el Control Plane (API server, etcd, scheduler, controller manager) SIN COSTO ADICIONAL - usted no tiene acceso directo a estos componentes. Usted es responsable de: 1) Worker nodes (aunque Azure ayuda con actualizaciones), 2) Pods y aplicaciones, 3) Configuración de red y seguridad de aplicaciones, 4) Persistent volumes y almacenamiento. Solo paga por los worker nodes (VMs) que usa."
            },
            {
                "id": 9,
                "type": "single",
                "question": """Tiene una aplicación web en Azure App Service que necesita acceder a secretos almacenados en Azure Key Vault.

Requisitos de seguridad:
- NO almacenar credenciales en código ni configuración
- Las credenciales NO deben requerir rotación manual
- Usar el principio de privilegio mínimo
- La aplicación debe poder leer secretos pero NO modificarlos

¿Qué configuración debe implementar?""",
                "options": [
                    "Almacenar la connection string de Key Vault en App Settings",
                    "Crear un Service Principal, guardar el secreto en App Settings, y asignar 'Key Vault Administrator' role",
                    "Habilitar System-Assigned Managed Identity y asignar 'Key Vault Secrets User' role",
                    "Usar las Access Keys de Key Vault en el código de la aplicación"
                ],
                "answer": 2,
                "explanation": "System-Assigned Managed Identity con 'Key Vault Secrets User' role es la configuración correcta: 1) Managed Identity no requiere credenciales en código - Azure gestiona automáticamente, 2) Las credenciales rotan automáticamente, 3) 'Key Vault Secrets User' permite solo LEER secretos (Get, List) - privilegio mínimo, 4) 'Key Vault Administrator' tendría permisos excesivos (puede modificar/eliminar). Service Principal requiere gestión de secretos. Access Keys dan demasiados permisos."
            },
            {
                "id": 10,
                "type": "single",
                "question": """Necesita crear VMs desde una imagen personalizada que incluya:

- Windows Server 2022
- IIS preinstalado y configurado
- Software corporativo preinstalado
- Configuraciones de seguridad aplicadas

Esta imagen será usada para crear múltiples VMs idénticas en diferentes regiones.

¿Cuál es el proceso correcto para crear esta imagen?""",
                "options": [
                    "Crear un snapshot del disco OS de una VM configurada",
                    "Ejecutar Sysprep en la VM, generalizarla, deallocate, y capturar como imagen",
                    "Exportar el VHD de la VM a una cuenta de almacenamiento",
                    "Clonar la VM usando Azure Site Recovery"
                ],
                "answer": 1,
                "explanation": "El proceso correcto para Windows es: 1) Configurar la VM con todo el software y configuraciones necesarias, 2) Ejecutar Sysprep con /generalize para eliminar información específica de la máquina (SID, nombre de computadora, etc.), 3) Deallocate la VM en Azure, 4) Capturar como imagen (Capture en portal o New-AzImage). La imagen resultante puede usarse para crear múltiples VMs con configuraciones únicas. Un snapshot solo copia el disco, no crea una imagen generalizada. El VHD exportado requiere procesamiento adicional."
            },
            {
                "id": 11,
                "type": "multiple",
                "question": """Tiene un Virtual Machine Scale Set (VMSS) que hospeda una aplicación web.

Requisitos de auto-scaling:
- Aumentar instancias cuando CPU promedio > 70% por 5 minutos
- Reducir instancias cuando CPU promedio < 30% por 10 minutos
- Mínimo 2 instancias, máximo 10 instancias

¿Cuáles DOS configuraciones de scaling debe crear? (Seleccione dos)""",
                "options": [
                    "Regla de Scale OUT: Si CPU > 70% durante 5 min, aumentar en 1 instancia",
                    "Configurar Azure Load Balancer con health probes",
                    "Regla de Scale IN: Si CPU < 30% durante 10 min, reducir en 1 instancia",
                    "Habilitar Accelerated Networking en las instancias"
                ],
                "answer": [0, 2],
                "explanation": "Para auto-scaling efectivo necesita DOS tipos de reglas: 1) Scale OUT (aumentar capacidad): Se activa cuando la carga aumenta - en este caso cuando CPU > 70% por 5 minutos, 2) Scale IN (reducir capacidad): Se activa cuando la carga disminuye - en este caso cuando CPU < 30% por 10 minutos, evitando pagar por capacidad no utilizada. Load Balancer distribuye tráfico pero no controla scaling. Accelerated Networking mejora rendimiento de red pero no es parte del auto-scaling."
            },
            {
                "id": 12,
                "type": "single",
                "question": """Una VM de base de datos SQL Server tiene problemas de rendimiento de disco.

Configuración actual:
- VM Size: Standard_D4s_v3
- Disco OS: Standard HDD S10 (500 IOPS)
- Disco de datos (DB): Standard HDD S30 (500 IOPS)

Métricas observadas:
- Disk Queue Length: consistentemente > 10
- Disk IOPS consumed: 100% del límite
- Disk latency: 50-100ms

Requisitos: Reducir latencia a < 5ms y soportar 5,000+ IOPS para cargas de base de datos.

¿Qué tipo de disco debe usar para el disco de datos?""",
                "options": [
                    "Standard SSD E30",
                    "Premium SSD P30",
                    "Ultra Disk",
                    "Premium SSD P30 es suficiente para la mayoría de cargas DB; Ultra Disk para cargas extremas"
                ],
                "answer": 3,
                "explanation": "La respuesta depende de los requisitos específicos: 1) Premium SSD P30 proporciona 5,000 IOPS y ~5ms de latencia - suficiente para la mayoría de cargas de SQL Server, 2) Ultra Disk proporciona latencia sub-milisegundo y IOPS configurables hasta 160,000 - necesario para cargas extremas como SAP HANA, data warehousing intensivo, o bases de datos de misión crítica. Standard SSD mejoraría pero no alcanzaría los requisitos de IOPS. Evalúe el costo: Ultra Disk es significativamente más caro."
            },
            {
                "id": 13,
                "type": "single",
                "question": """Tiene una aplicación web en Azure App Service con deployment slots:

- Production (slot principal)
- Staging

La aplicación se desplegó a Staging y pasó todas las pruebas. Necesita promover Staging a Production sin downtime para los usuarios.

¿Qué acción debe realizar?""",
                "options": [
                    "Copiar los archivos de Staging a Production usando FTP",
                    "Ejecutar Swap operation entre Staging y Production slots",
                    "Eliminar Production y renombrar Staging a Production",
                    "Configurar Traffic Manager para redirigir tráfico a Staging"
                ],
                "answer": 1,
                "explanation": "Swap operation es el método correcto porque: 1) Es instantáneo - sin downtime para usuarios, 2) Azure primero 'calienta' (warm up) el slot de staging enviándole requests, 3) Luego intercambia las configuraciones de routing entre slots, 4) Si hay problemas, puede hacer swap de vuelta inmediatamente (rollback). El swap intercambia todo: código, configuración, etc. Las settings marcadas como 'slot settings' permanecen en su slot original (útil para connection strings de DB diferentes por ambiente)."
            },
            {
                "id": 14,
                "type": "single",
                "question": """Su empresa tiene VMs de desarrollo que solo se usan de lunes a viernes, 8:00 AM a 6:00 PM.

Configuración actual:
- 10 VMs Standard_D4s_v3 en RG-Development
- Costo mensual actual: ~$3,000 (VMs running 24/7)

Requisito: Reducir costos lo máximo posible manteniendo las VMs disponibles durante horario laboral.

¿Qué solución debe implementar?""",
                "options": [
                    "Cambiar todas las VMs a tamaño más pequeño (Standard_B2s)",
                    "Comprar Reserved Instances de 1 año para las 10 VMs",
                    "Configurar Azure Automation con runbooks para iniciar/detener VMs según horario",
                    "Migrar las VMs a Azure Virtual Desktop"
                ],
                "answer": 2,
                "explanation": "Azure Automation con runbooks programados es la mejor solución porque: 1) VMs deallocated (detenidas) no incurren costos de cómputo - solo almacenamiento, 2) Las VMs se usarían ~50 horas/semana vs 168 horas/semana = ~70% de ahorro en cómputo, 3) El costo de Azure Automation es mínimo. Cálculo: 10 horas/día × 5 días = 50 horas vs 168 horas = 30% del tiempo original. Reserved Instances requieren compromiso de 1-3 años y no eliminan costo de horas no usadas. Cambiar tamaño reduce rendimiento."
            },
            {
                "id": 15,
                "type": "single",
                "question": """Tiene un Azure App Service Plan en tier Standard (S1).

Necesita planificar la capacidad para manejar picos de tráfico.

¿Qué tipos de scaling puede configurar en este tier?""",
                "options": [
                    "Solo Scale Up (vertical) - cambiar a un tier más alto",
                    "Solo Scale Out (horizontal) - agregar más instancias",
                    "Scale Up (vertical) y Scale Out (horizontal)",
                    "Ninguno - Standard tier no soporta scaling"
                ],
                "answer": 2,
                "explanation": "El tier Standard (S1) soporta AMBOS tipos de scaling: 1) Scale Up (vertical): Cambiar a un tier más alto (S2, S3, P1v2, etc.) para obtener más CPU/memoria por instancia - requiere un breve reinicio, 2) Scale Out (horizontal): Agregar más instancias del mismo tier (hasta 10 instancias en Standard) - puede ser manual o automático basado en métricas/horario. El tier Basic solo soporta scaling manual (hasta 3 instancias). Free/Shared no soportan scaling. Para auto-scale necesita Standard o superior."
            }
        ]
    },
    "networking": {
        "name": "Implementar y Administrar Redes Virtuales",
        "percentage": "15-20%",
        "icon": "🌐",
        "color": "#9B59B6",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso tiene la siguiente infraestructura en Azure:

VNet-Production (East US)
- Address space: 10.1.0.0/16
- Contiene VMs de aplicación

VNet-Database (East US)
- Address space: 10.2.0.0/16
- Contiene Azure SQL VMs

Requisitos:
- Las VMs en VNet-Production deben comunicarse con las VMs en VNet-Database
- El tráfico NO debe salir a Internet público
- Latencia mínima
- Sin costo de dispositivos de gateway

¿Qué debe configurar?""",
                "options": [
                    "VPN Gateway en cada VNet con conexión VNet-to-VNet",
                    "VNet Peering entre VNet-Production y VNet-Database",
                    "ExpressRoute para conectar ambas VNets",
                    "NAT Gateway en cada VNet"
                ],
                "answer": 1,
                "explanation": "VNet Peering es la solución correcta porque: 1) Conecta VNets directamente a través del backbone de Azure (baja latencia), 2) El tráfico nunca sale a Internet público, 3) No requiere gateways - solo configuración de peering, 4) Es el método más económico para conectar VNets en la misma región. VPN Gateway tiene costo por hora. ExpressRoute es para conexión on-premises. NAT Gateway es para tráfico saliente a Internet."
            },
            {
                "id": 2,
                "type": "single",
                "question": """Tiene una subnet llamada Subnet-Web que contiene servidores web.

Requisitos de seguridad:
- Permitir tráfico HTTPS (TCP 443) desde Internet
- Permitir tráfico HTTP (TCP 80) desde Internet (redirige a HTTPS)
- Bloquear todo otro tráfico entrante desde Internet
- Permitir que los servidores respondan a las conexiones establecidas

¿Qué debe configurar?""",
                "options": [
                    "Azure Firewall con reglas de aplicación",
                    "Network Security Group (NSG) con reglas de entrada para puertos 80 y 443",
                    "Application Gateway con WAF",
                    "Route Table con rutas personalizadas"
                ],
                "answer": 1,
                "explanation": "Network Security Group (NSG) es la solución correcta para este escenario: 1) Permite filtrar tráfico basado en puerto, protocolo, origen y destino, 2) Regla 1: Allow Inbound TCP 443 from Internet, 3) Regla 2: Allow Inbound TCP 80 from Internet, 4) Las reglas de salida por defecto permiten tráfico de respuesta (NSG es stateful). Azure Firewall es más complejo y costoso para este caso simple. Application Gateway es un balanceador L7, no solo filtrado. Route Tables son para routing, no filtrado."
            },
            {
                "id": 3,
                "type": "single",
                "question": """Tiene VMs en una subnet privada que necesitan acceder a Internet para:
- Descargar actualizaciones de Windows Update
- Acceder a APIs externas
- Descargar paquetes de repositorios públicos

Requisitos:
- Las VMs NO deben tener IPs públicas
- Las VMs NO deben ser accesibles directamente desde Internet
- Todas las VMs deben usar la misma IP para conexiones salientes

¿Qué debe configurar?""",
                "options": [
                    "Asignar IP pública a cada VM",
                    "Configurar NAT Gateway en la subnet",
                    "Crear un VPN Gateway",
                    "Configurar Azure Firewall como default route"
                ],
                "answer": 1,
                "explanation": "NAT Gateway es la solución correcta porque: 1) Proporciona conectividad de salida a Internet para VMs sin IP pública, 2) Las VMs no son accesibles directamente desde Internet (solo saliente), 3) Todas las VMs de la subnet comparten las IPs públicas del NAT Gateway para conexiones salientes (SNAT), 4) Es un servicio administrado, altamente disponible. Azure Firewall también funcionaría pero es más costoso y complejo para solo SNAT. VPN Gateway es para conectividad híbrida."
            },
            {
                "id": 4,
                "type": "single",
                "question": """Necesita implementar un balanceador de carga para su aplicación web con los siguientes requisitos:

- Terminación SSL/TLS en el balanceador
- Enrutamiento basado en URL (/api/* → backend-api, /images/* → backend-static)
- Web Application Firewall para protección OWASP
- Afinidad de sesión (sticky sessions) basada en cookies

¿Qué servicio de Azure debe usar?""",
                "options": [
                    "Azure Load Balancer Standard",
                    "Azure Application Gateway con WAF",
                    "Azure Traffic Manager",
                    "Azure Front Door"
                ],
                "answer": 1,
                "explanation": "Azure Application Gateway es la respuesta correcta porque: 1) Es un balanceador de carga de capa 7 (HTTP/HTTPS), 2) Soporta terminación SSL/TLS, 3) Permite enrutamiento basado en URL path, 4) Tiene SKU con WAF integrado para protección OWASP, 5) Soporta cookie-based session affinity. Azure Load Balancer es capa 4 (no entiende HTTP/URLs). Traffic Manager es DNS-based, no puede hacer routing por URL. Front Door también cumpliría pero es global/CDN."
            },
            {
                "id": 5,
                "type": "single",
                "question": """Tiene la siguiente configuración:

- VNet-Hub con un Network Virtual Appliance (NVA) de firewall: 10.0.0.4
- VNet-Spoke con VMs que necesitan que TODO su tráfico pase por el NVA

Actualmente las VMs en VNet-Spoke pueden acceder a Internet directamente sin pasar por el NVA.

¿Qué debe configurar para forzar el tráfico a través del NVA?""",
                "options": [
                    "NSG en VNet-Spoke bloqueando tráfico a Internet",
                    "User Defined Route (UDR) con next hop 'Virtual Appliance' apuntando al NVA",
                    "VNet Peering con 'Allow forwarded traffic' habilitado",
                    "Service Endpoint hacia el NVA"
                ],
                "answer": 1,
                "explanation": "User Defined Route (UDR) es necesario para anular el routing por defecto: 1) Crear Route Table con ruta: 0.0.0.0/0 → Next hop type: Virtual Appliance → Next hop IP: 10.0.0.4, 2) Asociar la Route Table a las subnets de VNet-Spoke. Esto fuerza TODO el tráfico (incluyendo Internet) a pasar por el NVA. También necesita: VNet peering entre Hub y Spoke, IP forwarding habilitado en la NIC del NVA. NSG solo bloquea/permite, no redirecciona. Service Endpoints son para acceso a servicios PaaS."
            },
            {
                "id": 6,
                "type": "single",
                "question": """Una aplicación en una VM necesita acceder a Azure SQL Database.

Requisitos de seguridad:
- El tráfico NO debe pasar por Internet público
- La base de datos debe tener una IP privada en la VNet
- La conexión debe funcionar desde VNets peered y desde on-premises vía VPN

¿Qué debe configurar?""",
                "options": [
                    "Service Endpoint para Microsoft.Sql en la subnet",
                    "Private Endpoint para Azure SQL Database",
                    "VNet Integration en Azure SQL",
                    "Azure Firewall con reglas para Azure SQL"
                ],
                "answer": 1,
                "explanation": "Private Endpoint es la solución correcta porque: 1) Crea una interfaz de red con IP privada en su VNet para Azure SQL, 2) El tráfico va por la red privada de Azure, nunca por Internet, 3) Funciona con VNet peering y conexiones VPN/ExpressRoute (el DNS resuelve a la IP privada), 4) Deshabilita el acceso público a la base de datos. Service Endpoint también usa red privada pero la base de datos mantiene su IP pública y requiere configuración de firewall - no funciona tan bien con conexiones híbridas."
            },
            {
                "id": 7,
                "type": "single",
                "question": """Tiene tres VNets que necesitan resolver nombres DNS entre sí:

- VNet-App (10.1.0.0/16) - contiene app.contoso.local
- VNet-DB (10.2.0.0/16) - contiene db.contoso.local
- VNet-Web (10.3.0.0/16) - contiene web.contoso.local

Las VNets están conectadas mediante peering. Las VMs necesitan resolver nombres como "app.contoso.local" desde cualquier VNet.

¿Qué debe configurar?""",
                "options": [
                    "Azure DNS public zone para contoso.local",
                    "Azure Private DNS zone con Virtual Network links a las tres VNets",
                    "Servidor DNS personalizado en una de las VNets",
                    "Archivos hosts en cada VM"
                ],
                "answer": 1,
                "explanation": "Azure Private DNS zone es la solución correcta: 1) Crear Private DNS zone 'contoso.local', 2) Crear Virtual Network links a VNet-App, VNet-DB, y VNet-Web, 3) Registrar los records A (app, db, web) con sus IPs privadas, 4) Las VMs usan Azure DNS (168.63.129.16) automáticamente y resuelven los nombres. No requiere gestionar servidores DNS. Public DNS no funcionaría con IPs privadas. Los archivos hosts no escalan y son difíciles de mantener."
            },
            {
                "id": 8,
                "type": "single",
                "question": """Su empresa tiene un datacenter on-premises y necesita conectividad a Azure.

Requisitos:
- Conexión privada (no sobre Internet público)
- Latencia predecible y baja (< 10ms)
- Ancho de banda garantizado de 1 Gbps
- SLA de disponibilidad de 99.95%

¿Qué tipo de conexión debe implementar?""",
                "options": [
                    "Site-to-Site VPN sobre Internet",
                    "Point-to-Site VPN",
                    "ExpressRoute",
                    "VPN Gateway con BGP"
                ],
                "answer": 2,
                "explanation": "ExpressRoute es la única opción que cumple TODOS los requisitos: 1) Conexión privada dedicada a través de un proveedor de conectividad - no usa Internet público, 2) Latencia baja y predecible debido a la conexión dedicada, 3) Ancho de banda garantizado (desde 50 Mbps hasta 10 Gbps), 4) SLA de disponibilidad de 99.95% (o 99.99% con ExpressRoute Premium y dos circuitos). VPN sobre Internet no garantiza latencia ni ancho de banda. Point-to-Site es para usuarios individuales, no para datacenter."
            },
            {
                "id": 9,
                "type": "multiple",
                "question": """Necesita configurar una conexión Site-to-Site VPN entre Azure y su oficina on-premises.

El dispositivo VPN on-premises es un Cisco ASA con IP pública 203.0.113.10.
La VNet de Azure es 10.1.0.0/16.
La red on-premises es 192.168.0.0/24.

¿Cuáles DOS recursos de Azure debe crear? (Seleccione dos)""",
                "options": [
                    "Virtual Network Gateway (VPN type) en una GatewaySubnet",
                    "Local Network Gateway con IP 203.0.113.10 y address space 192.168.0.0/24",
                    "ExpressRoute Circuit",
                    "Application Gateway"
                ],
                "answer": [0, 1],
                "explanation": "Para Site-to-Site VPN necesita: 1) Virtual Network Gateway (VPN type): Es el endpoint de VPN en Azure. Debe desplegarse en una subnet especial llamada 'GatewaySubnet' en su VNet. 2) Local Network Gateway: Representa el dispositivo VPN on-premises. Configura: IP pública del dispositivo (203.0.113.10) y los address spaces de la red on-premises (192.168.0.0/24). Luego crea una Connection entre ambos con la Pre-Shared Key. ExpressRoute es diferente a VPN. Application Gateway es un load balancer."
            },
            {
                "id": 10,
                "type": "single",
                "question": """Tiene un NSG asociado a una subnet con las siguientes reglas INBOUND:

| Priority | Name | Source | Destination | Port | Action |
|----------|------|--------|-------------|------|--------|
| 100 | Allow-HTTPS | Any | Any | 443 | Allow |
| 200 | Deny-All | Any | Any | Any | Deny |
| 65000 | AllowVnetInBound | VirtualNetwork | VirtualNetwork | Any | Allow |
| 65500 | DenyAllInBound | Any | Any | Any | Deny |

Una VM en OTRA subnet de la MISMA VNet intenta conectar al puerto 22 (SSH) a una VM en esta subnet.

¿Se permitirá la conexión?""",
                "options": [
                    "Sí, porque la regla AllowVnetInBound permite tráfico VNet-to-VNet",
                    "No, porque la regla Deny-All (priority 200) bloquea antes que AllowVnetInBound",
                    "Sí, porque SSH desde VNets internas siempre se permite",
                    "Depende de si la VM origen tiene IP pública"
                ],
                "answer": 1,
                "explanation": "NO se permitirá. Las reglas de NSG se evalúan por prioridad (número más bajo = mayor prioridad): 1) Priority 100 (Allow-HTTPS): No coincide - el puerto es 22, no 443, 2) Priority 200 (Deny-All): COINCIDE - origen Any, destino Any, puerto Any → DENY. La evaluación termina aquí. La regla AllowVnetInBound (priority 65000) NUNCA se evalúa porque Deny-All tiene mayor prioridad. Las reglas default (65000, 65500) solo aplican si ninguna regla personalizada coincide antes."
            },
            {
                "id": 11,
                "type": "single",
                "question": """Necesita implementar balanceo de carga para servidores de base de datos SQL Server (puerto 1433) dentro de una VNet.

Requisitos:
- Los clientes están en la misma VNet
- El balanceador debe tener una IP privada
- Balanceo TCP puro (capa 4)
- Health probes para detectar servidores caídos

¿Qué servicio de Azure debe usar?""",
                "options": [
                    "Azure Load Balancer Internal (Standard SKU)",
                    "Azure Load Balancer Public (Standard SKU)",
                    "Azure Application Gateway",
                    "Azure Traffic Manager"
                ],
                "answer": 0,
                "explanation": "Azure Load Balancer Internal (Standard SKU) es correcto porque: 1) 'Internal' significa IP privada (frontend) para uso dentro de VNet, 2) Es capa 4 (TCP/UDP) - perfecto para SQL Server, 3) Soporta health probes TCP para detectar disponibilidad, 4) Standard SKU proporciona mejor SLA y más features que Basic. Application Gateway es capa 7 (HTTP/HTTPS). Traffic Manager es DNS-based para distribución global. Public Load Balancer expondría el servicio a Internet."
            },
            {
                "id": 12,
                "type": "single",
                "question": """Tiene la siguiente configuración:

VNet1 (10.1.0.0/16):
- Contiene VM-App
- Tiene VNet peering con VNet2

VNet2 (10.2.0.0/16):
- Tiene un VPN Gateway conectado a red on-premises (192.168.0.0/24)

Requisito: VM-App en VNet1 necesita comunicarse con servidores on-premises a través del VPN Gateway en VNet2.

¿Qué configuración debe realizar en el peering?""",
                "options": [
                    "Crear un VPN Gateway adicional en VNet1",
                    "En VNet1: habilitar 'Use remote gateways', En VNet2: habilitar 'Allow gateway transit'",
                    "Configurar ExpressRoute en VNet1",
                    "El peering ya permite esta comunicación por defecto"
                ],
                "answer": 1,
                "explanation": "Gateway Transit es la funcionalidad correcta: 1) En VNet2 (la que tiene el gateway): Habilitar 'Allow gateway transit' - permite que VNets peered usen su gateway, 2) En VNet1 (la que NO tiene gateway): Habilitar 'Use remote gateways' - configura la VNet para usar el gateway de la VNet peered. También necesita agregar la ruta a 192.168.0.0/24 en VNet1 o usar BGP. No necesita gateway adicional en VNet1. Por defecto, el peering no comparte gateways."
            },
            {
                "id": 13,
                "type": "single",
                "question": """Tiene empleados que trabajan remotamente desde sus hogares y necesitan acceder a recursos en una VNet de Azure.

Requisitos:
- Los empleados usan laptops Windows 10/11 corporativos
- Cada empleado debe poder conectarse individualmente desde cualquier ubicación
- No se requiere hardware VPN en las ubicaciones de los empleados
- La conexión debe ser segura (cifrada)

¿Qué tipo de conexión VPN debe configurar?""",
                "options": [
                    "Site-to-Site VPN",
                    "Point-to-Site VPN",
                    "ExpressRoute",
                    "VNet Peering"
                ],
                "answer": 1,
                "explanation": "Point-to-Site (P2S) VPN es la solución correcta porque: 1) Permite conexiones individuales desde cualquier ubicación con acceso a Internet, 2) No requiere hardware VPN - solo software cliente en el laptop, 3) Soporta protocolos seguros: IKEv2, OpenVPN, SSTP, 4) Ideal para empleados remotos, teletrabajo. Site-to-Site requiere un dispositivo VPN en cada ubicación. ExpressRoute es para conexiones dedicadas de datacenter. VNet Peering es entre VNets de Azure, no para usuarios externos."
            },
            {
                "id": 14,
                "type": "single",
                "question": """Está diseñando la arquitectura de red para una aplicación de tres capas:

- Web tier: Servidores web públicos
- Application tier: Lógica de negocio
- Database tier: SQL Server

Requisitos de seguridad:
- Web tier debe ser accesible desde Internet (HTTPS)
- Application tier solo debe ser accesible desde Web tier
- Database tier solo debe ser accesible desde Application tier
- Aislar cada tier para contener brechas de seguridad

¿Cuál es la mejor práctica de diseño?""",
                "options": [
                    "Una VNet con una subnet y NSG a nivel de NIC",
                    "Una subnet por tier con NSG en cada subnet",
                    "Una VNet separada por tier con VNet peering",
                    "Todas las VMs en la misma subnet con Application Security Groups"
                ],
                "answer": 1,
                "explanation": "Una subnet por tier con NSG es la mejor práctica: 1) Subnet-Web con NSG: Allow HTTPS from Internet, 2) Subnet-App con NSG: Allow from Subnet-Web only, 3) Subnet-DB con NSG: Allow SQL (1433) from Subnet-App only. Beneficios: Segmentación clara, políticas de seguridad por tier, contención de brechas (si comprometen Web tier, no pueden acceder directamente a DB). VNets separadas agregan complejidad innecesaria. Una sola subnet no proporciona aislamiento. ASGs son complementarios pero no reemplazan subnets."
            },
            {
                "id": 15,
                "type": "single",
                "question": """Su aplicación web en Azure App Service está expuesta a ataques.

Los logs muestran intentos de:
- SQL injection en parámetros de URL
- Cross-Site Scripting (XSS) en formularios
- Path traversal attacks
- Escaneos automatizados de vulnerabilidades

Requisitos:
- Proteger contra OWASP Top 10 vulnerabilidades
- Bloquear solicitudes maliciosas automáticamente
- Registrar todos los ataques bloqueados

¿Qué debe implementar?""",
                "options": [
                    "Network Security Group con reglas personalizadas",
                    "Azure Firewall con threat intelligence",
                    "Web Application Firewall (WAF) con Application Gateway o Front Door",
                    "DDoS Protection Standard"
                ],
                "answer": 2,
                "explanation": "Web Application Firewall (WAF) es la solución correcta porque: 1) Diseñado específicamente para proteger aplicaciones web, 2) Incluye reglas predefinidas para OWASP Top 10 (SQL injection, XSS, etc.), 3) Puede configurarse en modo 'Prevention' para bloquear ataques automáticamente, 4) Logging detallado de todas las solicitudes bloqueadas. NSG opera en capa 4, no entiende HTTP. Azure Firewall es para tráfico de red general. DDoS Protection es para ataques de denegación de servicio, no ataques de capa de aplicación."
            }
        ]
    },
    "monitoring": {
        "name": "Monitorear y Mantener Recursos de Azure",
        "percentage": "10-15%",
        "icon": "📊",
        "color": "#F39C12",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso tiene VMs de producción críticas que hospedan una aplicación de e-commerce.

Requisitos de monitoreo:
- Recibir notificación por EMAIL cuando el uso de CPU supere 80% por más de 5 minutos
- La notificación debe incluir el nombre de la VM afectada
- También se debe crear un ticket automático en ServiceNow

¿Qué componentes de Azure Monitor debe configurar?""",
                "options": [
                    "Activity Log alert para monitorear métricas de CPU",
                    "Metric alert con condition CPU > 80% y Action Group con acciones de email y webhook",
                    "Log Analytics query que se ejecute cada 5 minutos",
                    "Azure Advisor recommendation para alertas de rendimiento"
                ],
                "answer": 1,
                "explanation": "Metric Alert + Action Group es la solución correcta: 1) Metric Alert permite configurar condiciones basadas en métricas (CPU > 80% durante 5 minutos), 2) Action Group define las acciones a tomar: email a destinatarios y webhook para integración con ServiceNow, 3) El alert incluye el contexto del recurso (nombre de VM, etc.). Activity Log es para eventos de administración, no métricas de rendimiento. Log Analytics queries son para análisis de logs, no métricas en tiempo real."
            },
            {
                "id": 2,
                "type": "single",
                "question": """Tiene 50 VMs distribuidas en 5 suscripciones de Azure.

Necesita:
- Recopilar logs de eventos de Windows (Application, System, Security)
- Recopilar logs de syslog de VMs Linux
- Consultar los logs usando KQL (Kusto Query Language)
- Crear alertas basadas en patrones en los logs
- Retener los logs por 2 años

¿Qué servicio debe usar como destino central de los logs?""",
                "options": [
                    "Azure Monitor Metrics",
                    "Log Analytics workspace",
                    "Azure Storage Account con blob containers",
                    "Azure Event Hubs"
                ],
                "answer": 1,
                "explanation": "Log Analytics workspace es la solución correcta porque: 1) Puede recopilar logs de múltiples suscripciones en un workspace central, 2) Soporta Windows Event Logs y Syslog, 3) Permite consultas con KQL para análisis y troubleshooting, 4) Se integra con Azure Monitor Alerts para alertas basadas en consultas de logs, 5) Soporta retención hasta 2 años (o más con archive). Azure Metrics es para métricas numéricas. Storage Account permite almacenar pero no consultar fácilmente. Event Hubs es para streaming a sistemas externos."
            },
            {
                "id": 3,
                "type": "single",
                "question": """Tiene VMs de producción que necesitan protección de datos.

Requisitos:
- Backup diario a las 2:00 AM
- Retención de backups diarios por 30 días
- Retención de backup semanal por 12 semanas
- Capacidad de restaurar archivos individuales sin restaurar toda la VM
- Los backups deben almacenarse en una región diferente

¿Qué debe configurar?""",
                "options": [
                    "Azure Site Recovery para replicación continua",
                    "Azure Backup con Recovery Services vault y backup policy personalizada",
                    "Snapshots manuales de discos programados con Azure Automation",
                    "Copiar VHDs a un Storage Account en otra región"
                ],
                "answer": 1,
                "explanation": "Azure Backup con Recovery Services vault cumple todos los requisitos: 1) Backup policies permiten configurar schedule (diario 2 AM) y retención (30 días, 12 semanas), 2) File Recovery permite restaurar archivos individuales montando el backup como disco, 3) Geo-redundant storage (GRS) replica backups a otra región. Site Recovery es para DR (replicación continua), no backup tradicional. Snapshots manuales no ofrecen retención automática ni file recovery fácil."
            },
            {
                "id": 4,
                "type": "single",
                "question": """El CFO solicita un reporte de optimización de costos de Azure.

Necesita identificar:
- VMs que están sobredimensionadas (over-provisioned)
- Discos huérfanos que no están attached a ninguna VM
- Reserved Instance recommendations para ahorrar costos
- VMs con uso de CPU consistentemente bajo

¿Qué herramienta de Azure proporciona estas recomendaciones automáticamente?""",
                "options": [
                    "Azure Monitor con Workbooks personalizados",
                    "Azure Advisor",
                    "Microsoft Defender for Cloud",
                    "Azure Cost Management"
                ],
                "answer": 1,
                "explanation": "Azure Advisor proporciona recomendaciones automáticas en 5 categorías: 1) Cost (lo que solicita el CFO): VMs sobredimensionadas, Reserved Instance recommendations, recursos no utilizados, 2) Security, 3) Reliability, 4) Operational Excellence, 5) Performance. Las recomendaciones de costo incluyen savings estimados en $. Cost Management es para análisis de costos actuales, no recomendaciones de optimización. Defender for Cloud es principalmente para seguridad."
            },
            {
                "id": 5,
                "type": "single",
                "question": """El equipo de auditoría necesita saber:

- Quién creó un Resource Group llamado RG-Test hace 60 días
- Quién eliminó 3 VMs del grupo RG-Production la semana pasada
- Qué cambios de configuración se hicieron a un NSG específico
- Todas las operaciones de creación/eliminación en las últimas 12 semanas

¿Dónde debe buscar esta información?""",
                "options": [
                    "Azure Monitor Metrics",
                    "Activity Log (Azure Monitor Activity Log)",
                    "Resource Health",
                    "Azure Advisor History"
                ],
                "answer": 1,
                "explanation": "Activity Log registra todas las operaciones de administración (control plane): 1) Quién realizó la acción (caller), 2) Qué acción se realizó (operation), 3) Cuándo (timestamp), 4) Estado (succeeded, failed). Incluye: creación/eliminación de recursos, cambios de configuración, asignaciones de roles. Retención: 90 días (puede exportar a Log Analytics o Storage para más tiempo). Metrics son para datos numéricos de rendimiento. Resource Health es estado actual, no histórico de acciones."
            },
            {
                "id": 6,
                "type": "single",
                "question": """Una aplicación web .NET en Azure App Service está experimentando errores intermitentes.

Los usuarios reportan:
- Errores HTTP 500 esporádicos
- Tiempos de respuesta lentos en ciertas páginas
- La aplicación a veces no responde

Necesita:
- Ver cada request y su tiempo de respuesta
- Identificar qué excepciones están ocurriendo
- Correlacionar requests con las excepciones que generan
- Ver el stack trace de las excepciones
- Identificar dependencias lentas (SQL, APIs externas)

¿Qué debe habilitar?""",
                "options": [
                    "Diagnostic Settings para enviar logs a Log Analytics",
                    "Application Insights para la aplicación web",
                    "Azure Monitor Metrics con alertas",
                    "Activity Log monitoring"
                ],
                "answer": 1,
                "explanation": "Application Insights es la solución correcta porque: 1) Instrumentación automática de aplicaciones .NET - captura requests, excepciones, dependencias, 2) Request tracking: tiempo de respuesta, código de estado, URL, 3) Exception tracking: tipo de excepción, mensaje, stack trace completo, 4) Correlation: conecta requests con las excepciones que generan usando Operation ID, 5) Dependency tracking: tiempo de llamadas a SQL, HTTP, etc. 6) Application Map visualiza la arquitectura y rendimiento. Diagnostic Settings no proporciona esta telemetría de aplicación."
            },
            {
                "id": 7,
                "type": "single",
                "question": """Necesita implementar una estrategia de Disaster Recovery para VMs de producción.

Requisitos:
- RPO (Recovery Point Objective): máximo 15 minutos de pérdida de datos
- RTO (Recovery Time Objective): máximo 1 hora para estar operacional
- Failover a una región secundaria en caso de desastre regional
- Pruebas de failover sin afectar producción

¿Qué servicio debe usar?""",
                "options": [
                    "Azure Backup con GRS (Geo-Redundant Storage)",
                    "Azure Site Recovery (ASR)",
                    "Availability Zones en la misma región",
                    "Virtual Machine Scale Sets multi-región"
                ],
                "answer": 1,
                "explanation": "Azure Site Recovery (ASR) es la solución correcta porque: 1) Replicación continua: RPO de segundos a minutos (cumple < 15 min), 2) Failover automatizado o manual con RTO típico de minutos a 1 hora, 3) Soporta failover a región secundaria (DR regional), 4) Test Failover permite probar el plan de DR sin afectar producción ni replicación, 5) Failback cuando la región primaria se recupera. Azure Backup tiene RPO de horas (frecuencia de backup). Availability Zones protegen contra falla de datacenter, no de región."
            },
            {
                "id": 8,
                "type": "single",
                "question": """Su organización tiene 5 suscripciones de Azure y el CFO necesita:

- Ver costos consolidados de TODAS las suscripciones
- Crear presupuestos con alertas al 80% y 100% del límite
- Analizar costos por departamento usando tags
- Exportar reportes de costos mensualmente a un Storage Account

¿Qué herramienta debe usar?""",
                "options": [
                    "Azure Pricing Calculator",
                    "Azure Cost Management + Billing",
                    "Azure Advisor Cost recommendations",
                    "Azure Monitor con Workbooks"
                ],
                "answer": 1,
                "explanation": "Azure Cost Management + Billing proporciona: 1) Cost Analysis: vista consolidada de costos de múltiples suscripciones, filtros y agrupación por tags (departamento), 2) Budgets: crear presupuestos con alertas configurables (80%, 100%), 3) Exports: programar exportación de datos de costos a Storage Account, 4) Recommendations: integración con Azure Advisor para optimización. Pricing Calculator es para estimación pre-deployment. Advisor es solo para recomendaciones, no análisis de costos. Monitor es para métricas y logs operacionales."
            },
            {
                "id": 9,
                "type": "single",
                "question": """Tiene VMs Windows Server que necesitan enviar los siguientes datos a Log Analytics:

- Windows Event Logs (Application, System, Security)
- Performance counters (CPU, Memory, Disk, Network)
- IIS Logs
- Custom logs de una aplicación

¿Qué debe instalar en las VMs?""",
                "options": [
                    "Azure Diagnostics extension solamente",
                    "Azure Monitor Agent (AMA) con Data Collection Rules",
                    "Application Insights SDK",
                    "Custom Script Extension con script de recolección"
                ],
                "answer": 1,
                "explanation": "Azure Monitor Agent (AMA) con Data Collection Rules es la solución actual recomendada: 1) Reemplaza al agente legacy (MMA/OMS), 2) Data Collection Rules (DCR) definen qué datos recopilar y a dónde enviarlos, 3) Soporta Windows Events, Performance Counters, IIS Logs, Custom logs, 4) Configuración centralizada y escalable. La extensión Diagnostics es para métricas a Azure Monitor y logs a Storage, no óptima para Log Analytics. Application Insights es para aplicaciones, no infraestructura de VM."
            },
            {
                "id": 10,
                "type": "single",
                "question": """Una VM de producción muestra el estado 'Unavailable' en Azure Resource Health.

Los usuarios reportan que no pueden conectar a la aplicación en esta VM.
El portal de Azure muestra la VM como 'Running'.

¿Qué indica el estado 'Unavailable' en Resource Health?""",
                "options": [
                    "El usuario apagó la VM intencionalmente",
                    "Azure ha detectado un problema de plataforma que afecta la VM",
                    "La VM necesita actualizaciones del sistema operativo",
                    "El agente de Azure VM no está respondiendo"
                ],
                "answer": 1,
                "explanation": "Resource Health 'Unavailable' indica que Azure ha detectado un problema de PLATAFORMA afectando el recurso: 1) Puede ser falla de hardware del host, 2) Problemas de red en la infraestructura de Azure, 3) Otros problemas del servicio de Azure. Es diferente de problemas causados por el usuario o el sistema operativo guest. Cuando el problema es de plataforma, Azure típicamente inicia auto-recovery (migración de la VM a otro host). El estado 'Running' en el portal indica el estado deseado, no necesariamente el estado actual de salud."
            },
            {
                "id": 11,
                "type": "multiple",
                "question": """Está configurando Azure Backup para proteger VMs en la región East US.

El Recovery Services vault se llama vault-backup-eastus.

¿Cuáles DOS afirmaciones son correctas sobre Azure Backup para VMs? (Seleccione dos)""",
                "options": [
                    "El Recovery Services vault debe estar en la misma región que las VMs que protege",
                    "Un Recovery Services vault puede proteger VMs en cualquier región de Azure",
                    "Azure Backup soporta tanto discos Managed como Unmanaged",
                    "Azure Backup solo funciona con VMs Windows, no Linux"
                ],
                "answer": [0, 2],
                "explanation": "Las afirmaciones correctas son: 1) El vault DEBE estar en la misma región que las VMs - esto es un requisito de Azure Backup. Para proteger VMs en diferentes regiones, necesita vaults en cada región. 2) Azure Backup soporta discos Managed y Unmanaged, aunque Microsoft recomienda Managed disks. Azure Backup funciona tanto con Windows como Linux VMs - no es exclusivo de Windows."
            },
            {
                "id": 12,
                "type": "single",
                "question": """Necesita crear un dashboard ejecutivo que muestre:

- Estado de salud de todas las VMs de producción
- Métricas de rendimiento (CPU, memoria) en tiempo real
- Alertas activas
- Tendencias de costos del último mes
- Todo en una sola vista accesible desde el portal de Azure

¿Cuál es la MEJOR opción para crear este dashboard?""",
                "options": [
                    "Azure Monitor Workbooks con visualizaciones personalizadas",
                    "Log Analytics queries guardadas",
                    "Azure Portal Dashboard con tiles de métricas",
                    "Cualquiera de las opciones anteriores funcionaría, pero Workbooks ofrece más flexibilidad"
                ],
                "answer": 3,
                "explanation": "Todas las opciones pueden crear dashboards, pero tienen diferentes fortalezas: 1) Azure Portal Dashboard: Fácil de crear, permite pinear métricas y charts, bueno para dashboards simples, 2) Log Analytics queries: Potente para análisis de logs, puede crear visualizaciones, 3) Workbooks: Más flexible, combina métricas, logs, texto, parámetros interactivos, ideal para reportes ejecutivos complejos. Para el escenario descrito (múltiples tipos de datos), Workbooks ofrece la mayor flexibilidad para combinar diferentes fuentes de datos en una vista cohesiva."
            },
            {
                "id": 13,
                "type": "single",
                "question": """Su empresa requiere retener los Activity Logs por 3 años para cumplimiento regulatorio.

El Activity Log en Azure tiene una retención predeterminada de 90 días.

¿Qué debe configurar para cumplir con el requisito de 3 años?""",
                "options": [
                    "Cambiar la configuración de retención del Activity Log a 3 años",
                    "Crear un Diagnostic Setting para exportar Activity Logs a Log Analytics o Storage Account",
                    "No es posible retener Activity Logs por más de 90 días",
                    "Crear alertas que guarden los eventos importantes"
                ],
                "answer": 1,
                "explanation": "Diagnostic Settings es la solución correcta: 1) Activity Log tiene retención FIJA de 90 días - no se puede cambiar, 2) Debe crear un Diagnostic Setting para exportar a: - Log Analytics workspace (retención hasta 2 años built-in, o más con archive) - Storage Account (retención ilimitada, más económico para largo plazo), 3) Para 3 años, Storage Account es típicamente más económico. El Diagnostic Setting envía continuamente los nuevos eventos al destino configurado. Puede configurar ambos destinos para tener análisis en Log Analytics y archivo a largo plazo en Storage."
            },
            {
                "id": 14,
                "type": "single",
                "question": """Tiene VMs de producción críticas y necesita ser notificado proactivamente cuando:

- Azure planea mantenimiento que podría afectar sus VMs
- Hay un incidente de servicio en la región donde están sus recursos
- Hay avisos de seguridad que afectan servicios que usa

¿Qué debe configurar?""",
                "options": [
                    "Activity Log alerts para todas las categorías",
                    "Service Health alerts",
                    "Metric alerts para disponibilidad de VM",
                    "Azure Advisor notifications"
                ],
                "answer": 1,
                "explanation": "Service Health alerts es la solución correcta para notificaciones proactivas de Azure: 1) Planned Maintenance: notifica sobre mantenimiento programado que podría afectar sus recursos específicos, 2) Service Issues: alerta sobre incidentes de servicio/outages en regiones donde tiene recursos, 3) Security Advisories: avisos de seguridad que afectan servicios de Azure, 4) Health Advisories: otra información relevante. Service Health filtra eventos relevantes a SUS recursos, no eventos globales que no le afectan. Activity Log alerts son para eventos de administración, no eventos de plataforma."
            },
            {
                "id": 15,
                "type": "single",
                "question": """Tiene Application Insights configurado para su aplicación web.

Necesita detectar automáticamente:
- Anomalías en tiempos de respuesta
- Aumento inusual en tasa de errores
- Degradación de rendimiento
- Problemas de dependencias (SQL lento, APIs fallando)

SIN tener que configurar umbrales específicos para cada métrica.

¿Qué feature de Application Insights proporciona esto?""",
                "options": [
                    "Smart Detection (Detección Inteligente)",
                    "Live Metrics Stream",
                    "Alert Rules configuradas manualmente",
                    "Availability Tests"
                ],
                "answer": 0,
                "explanation": "Smart Detection es la característica correcta porque: 1) Usa machine learning para detectar anomalías automáticamente SIN configurar umbrales, 2) Detecta: tiempos de respuesta anormalmente lentos, tasas de error inusuales, degradación de rendimiento, problemas de memoria, 3) Envía notificaciones por email cuando detecta problemas, 4) Aprende el comportamiento 'normal' de su aplicación y alerta sobre desviaciones. Alert Rules requieren umbrales manuales. Live Metrics es para monitoreo en tiempo real pero no alertas automáticas. Availability Tests verifican disponibilidad desde ubicaciones externas."
            }
        ]
    }
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AZ-104 - Simulador de Examen</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            text-align: center;
            padding: 40px 0;
        }

        .header h1 {
            font-size: 3.5em;
            color: #00d4ff;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            margin-bottom: 10px;
        }

        .header h2 {
            font-size: 1.5em;
            color: #fff;
            font-weight: 300;
        }

        .header p {
            color: #888;
            margin-top: 10px;
        }

        /* Buttons */
        .btn {
            display: inline-block;
            padding: 15px 40px;
            font-size: 1.1em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: white;
            font-weight: 600;
            margin: 10px;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .btn-primary { background: linear-gradient(135deg, #4A90D9, #357ABD); }
        .btn-success { background: linear-gradient(135deg, #50C878, #3DA55D); }
        .btn-danger { background: linear-gradient(135deg, #FF6B6B, #ee5a5a); }
        .btn-secondary { background: linear-gradient(135deg, #666, #555); }
        .btn-purple { background: linear-gradient(135deg, #9B59B6, #8E44AD); }

        /* Menu */
        .menu {
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-width: 500px;
            margin: 40px auto;
        }

        .menu-btn {
            padding: 20px 30px;
            font-size: 1.2em;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .menu-btn span {
            font-size: 1.5em;
        }

        /* Topics Grid */
        .topics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .topic-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .topic-card:hover {
            transform: translateY(-5px);
            border-color: var(--topic-color);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .topic-card .icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }

        .topic-card h3 {
            color: var(--topic-color);
            margin-bottom: 10px;
        }

        .topic-card p {
            color: #888;
        }

        .topic-card p.topic-percentage {
            color: var(--topic-color);
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 5px;
        }

        /* Question Section */
        .question-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
        }

        .progress-bar {
            background: #333;
            height: 8px;
            border-radius: 4px;
            margin-bottom: 20px;
            overflow: hidden;
        }

        .progress-fill {
            background: linear-gradient(90deg, #00d4ff, #4A90D9);
            height: 100%;
            transition: width 0.3s ease;
        }

        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .question-number {
            color: #00d4ff;
            font-size: 1.2em;
        }

        .timer {
            background: rgba(255, 215, 0, 0.2);
            color: #FFD700;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }

        .topic-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 20px;
        }

        .question-text {
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 30px;
            white-space: pre-line;
        }

        .options {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .option {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 15px 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .option:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: #4A90D9;
        }

        .option.selected {
            background: rgba(74, 144, 217, 0.2);
            border-color: #4A90D9;
        }

        .option.correct {
            background: rgba(80, 200, 120, 0.2);
            border-color: #50C878;
        }

        .option.incorrect {
            background: rgba(255, 107, 107, 0.2);
            border-color: #FF6B6B;
        }

        .option-letter {
            width: 35px;
            height: 35px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .option.selected .option-letter {
            background: #4A90D9;
        }

        .option.correct .option-letter {
            background: #50C878;
        }

        .option.incorrect .option-letter {
            background: #FF6B6B;
        }

        .multi-hint {
            color: #FFD700;
            font-style: italic;
            margin-bottom: 20px;
        }

        /* Explanation */
        .explanation {
            background: rgba(0, 212, 255, 0.1);
            border-left: 4px solid #00d4ff;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            margin-top: 20px;
        }

        .explanation h4 {
            color: #00d4ff;
            margin-bottom: 10px;
        }

        /* Results */
        .results-container {
            text-align: center;
            padding: 40px;
        }

        .result-status {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 20px 40px;
            border-radius: 15px;
            display: inline-block;
        }

        .result-status.passed {
            background: rgba(80, 200, 120, 0.2);
            color: #50C878;
        }

        .result-status.failed {
            background: rgba(255, 107, 107, 0.2);
            color: #FF6B6B;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
        }

        .stat-card h4 {
            color: #888;
            font-size: 0.9em;
            margin-bottom: 10px;
        }

        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
        }

        /* Topic breakdown */
        .topic-breakdown {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            text-align: left;
        }

        .topic-breakdown h4 {
            margin-bottom: 15px;
            color: #00d4ff;
        }

        .topic-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .topic-row:last-child {
            border-bottom: none;
        }

        .topic-score {
            font-weight: bold;
        }

        .topic-score.good { color: #50C878; }
        .topic-score.bad { color: #FF6B6B; }

        /* Navigation buttons */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
            flex-wrap: wrap;
            gap: 10px;
        }

        /* Info text */
        .info-text {
            color: #888;
            margin-top: 40px;
            text-align: center;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }

        /* Responsive */
        @media (max-width: 600px) {
            .header h1 { font-size: 2.5em; }
            .menu-btn { font-size: 1em; }
            .question-text { font-size: 1em; }
        }
    </style>
</head>
<body>
    <div class="container" id="app">
        <!-- Content will be loaded here -->
    </div>

    <script>
        // Questions data from Python
        const questionsDB = QUESTIONS_DATA_PLACEHOLDER;

        // Timer - Cuenta regresiva de 120 minutos (7200 segundos)
        const EXAM_TIME_LIMIT = 120 * 60; // 120 minutos en segundos
        let timerInterval = null;

        // App state
        let state = {
            screen: 'menu',
            currentQuestions: [],
            currentIndex: 0,
            score: 0,
            answers: [],
            selectedOptions: [],
            startTime: null,
            timeRemaining: EXAM_TIME_LIMIT,
            isExamMode: false,
            currentTopic: null,
            showingResult: false
        };

        function formatTime(seconds) {
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = seconds % 60;
            return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        }

        function startTimer() {
            state.startTime = Date.now();
            state.timeRemaining = EXAM_TIME_LIMIT;
            timerInterval = setInterval(updateTimer, 1000);
        }

        function stopTimer() {
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        }

        function updateTimer() {
            const timerEl = document.getElementById('timer');
            if (timerEl && state.startTime) {
                const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
                const remaining = Math.max(0, EXAM_TIME_LIMIT - elapsed);
                state.timeRemaining = remaining;

                // Cambiar color si queda poco tiempo
                if (remaining <= 300) { // 5 minutos o menos
                    timerEl.style.background = 'rgba(255, 107, 107, 0.3)';
                    timerEl.style.color = '#FF6B6B';
                } else if (remaining <= 600) { // 10 minutos o menos
                    timerEl.style.background = 'rgba(255, 193, 7, 0.3)';
                    timerEl.style.color = '#FFC107';
                }

                timerEl.textContent = formatTime(remaining);

                // Tiempo agotado
                if (remaining <= 0) {
                    stopTimer();
                    alert('⏰ ¡Tiempo agotado! El examen ha finalizado.');
                    finishExamDueToTimeout();
                }
            }
        }

        function finishExamDueToTimeout() {
            // Marcar preguntas sin responder como incorrectas
            while (state.answers.length < state.currentQuestions.length) {
                state.answers.push({
                    selected: null,
                    isCorrect: false
                });
            }
            state.screen = 'results';
            render();
        }

        function getElapsedTime() {
            if (state.startTime) {
                return Math.floor((Date.now() - state.startTime) / 1000);
            }
            return 0;
        }

        function getRemainingTime() {
            return state.timeRemaining || EXAM_TIME_LIMIT;
        }

        // Shuffle array
        function shuffle(array) {
            const arr = [...array];
            for (let i = arr.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
        }

        // Render functions
        function render() {
            const app = document.getElementById('app');

            switch(state.screen) {
                case 'menu':
                    app.innerHTML = renderMenu();
                    break;
                case 'topics':
                    app.innerHTML = renderTopics();
                    break;
                case 'question':
                    app.innerHTML = renderQuestion();
                    break;
                case 'result':
                    app.innerHTML = renderQuestionResult();
                    break;
                case 'results':
                    app.innerHTML = renderResults();
                    break;
                case 'review':
                    app.innerHTML = renderReview();
                    break;
            }
        }

        function renderMenu() {
            const totalQuestions = Object.values(questionsDB).reduce((sum, t) => sum + t.questions.length, 0);

            return `
                <div class="header fade-in">
                    <h1>AZ-104</h1>
                    <h2>Microsoft Azure Administrator</h2>
                    <p>Simulador de Examen de Certificación</p>
                </div>

                <div class="menu fade-in">
                    <button class="btn menu-btn btn-primary" onclick="showTopics()">
                        <span>📚</span> Practicar por Tema
                    </button>
                    <button class="btn menu-btn btn-success" onclick="startExam(40)">
                        <span>📝</span> Examen Simulado (40 preguntas)
                    </button>
                    <button class="btn menu-btn btn-danger" onclick="startExam(60)">
                        <span>🎯</span> Examen Completo (60 preguntas)
                    </button>
                </div>

                <p class="info-text">
                    📊 ${totalQuestions} preguntas disponibles • 5 temas • ⏱️ 120 minutos • Puntaje para aprobar: 70%
                </p>
            `;
        }

        function renderTopics() {
            let topicsHTML = '';

            for (const [key, topic] of Object.entries(questionsDB)) {
                const percentage = topic.percentage || '';
                topicsHTML += `
                    <div class="topic-card" style="--topic-color: ${topic.color}" onclick="startPractice('${key}')">
                        <div class="icon">${topic.icon}</div>
                        <h3>${topic.name}</h3>
                        <p class="topic-percentage">${percentage}</p>
                        <p>${topic.questions.length} preguntas</p>
                    </div>
                `;
            }

            return `
                <div class="header fade-in">
                    <h2>Selecciona un Tema</h2>
                </div>

                <div class="topics-grid fade-in">
                    ${topicsHTML}
                </div>

                <div class="nav-buttons fade-in">
                    <button class="btn btn-secondary" onclick="goToMenu()">← Volver al Menú</button>
                </div>
            `;
        }

        function renderQuestion() {
            const q = state.currentQuestions[state.currentIndex];
            const progress = ((state.currentIndex + 1) / state.currentQuestions.length) * 100;
            const topicColor = q.topicColor || '#4A90D9';

            let optionsHTML = '';
            const letters = ['A', 'B', 'C', 'D'];

            q.options.forEach((opt, i) => {
                const isSelected = state.selectedOptions.includes(i);
                const selectedClass = isSelected ? 'selected' : '';

                optionsHTML += `
                    <div class="option ${selectedClass}" onclick="selectOption(${i})">
                        <div class="option-letter">${letters[i]}</div>
                        <div>${opt}</div>
                    </div>
                `;
            });

            const multiHint = q.type === 'multiple' ?
                '<p class="multi-hint">⚠️ Seleccione todas las respuestas correctas</p>' : '';

            const timerHTML = state.isExamMode ?
                `<div class="timer" id="timer">02:00:00</div>` : '';

            return `
                <div class="question-container fade-in">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${progress}%"></div>
                    </div>

                    <div class="question-header">
                        <span class="question-number">Pregunta ${state.currentIndex + 1} de ${state.currentQuestions.length}</span>
                        ${timerHTML}
                    </div>

                    <div class="topic-badge" style="background: ${topicColor}20; color: ${topicColor}">
                        ${q.topicName || state.currentTopic}
                    </div>

                    <div class="question-text">${q.question}</div>

                    ${multiHint}

                    <div class="options">
                        ${optionsHTML}
                    </div>

                    <div class="nav-buttons">
                        <button class="btn btn-secondary" onclick="confirmExit()">Salir</button>
                        <button class="btn btn-success" onclick="submitAnswer()">
                            ${state.isExamMode ? (state.currentIndex < state.currentQuestions.length - 1 ? 'Siguiente →' : 'Finalizar') : 'Verificar Respuesta'}
                        </button>
                    </div>
                </div>
            `;
        }

        function renderQuestionResult() {
            const q = state.currentQuestions[state.currentIndex];
            const userAnswer = state.answers[state.currentIndex];
            const isCorrect = userAnswer.isCorrect;
            const letters = ['A', 'B', 'C', 'D'];

            let optionsHTML = '';
            q.options.forEach((opt, i) => {
                let optClass = '';
                const isCorrectAnswer = Array.isArray(q.answer) ? q.answer.includes(i) : q.answer === i;
                const isUserAnswer = Array.isArray(userAnswer.selected) ?
                    userAnswer.selected.includes(i) : userAnswer.selected === i;

                if (isCorrectAnswer) {
                    optClass = 'correct';
                } else if (isUserAnswer && !isCorrectAnswer) {
                    optClass = 'incorrect';
                }

                optionsHTML += `
                    <div class="option ${optClass}">
                        <div class="option-letter">${letters[i]}</div>
                        <div>${opt}</div>
                    </div>
                `;
            });

            const resultIcon = isCorrect ? '✓' : '✗';
            const resultText = isCorrect ? '¡CORRECTO!' : 'INCORRECTO';
            const resultColor = isCorrect ? '#50C878' : '#FF6B6B';

            const correctAnswerText = Array.isArray(q.answer) ?
                q.answer.map(i => letters[i]).join(', ') : letters[q.answer];

            return `
                <div class="question-container fade-in">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <div style="font-size: 3em; color: ${resultColor}; margin-bottom: 10px;">${resultIcon}</div>
                        <div style="font-size: 1.5em; color: ${resultColor}; font-weight: bold;">${resultText}</div>
                        <div style="color: #888; margin-top: 10px;">
                            Puntaje actual: ${state.score}/${state.currentIndex + 1}
                        </div>
                    </div>

                    ${!isCorrect ? `
                        <div style="text-align: center; margin-bottom: 20px;">
                            <span style="color: #FFD700; font-weight: bold;">
                                Respuesta correcta: ${correctAnswerText}
                            </span>
                        </div>
                    ` : ''}

                    <div class="question-text" style="font-size: 1em; color: #aaa;">${q.question}</div>

                    <div class="options" style="margin-bottom: 20px;">
                        ${optionsHTML}
                    </div>

                    <div class="explanation">
                        <h4>📖 Explicación</h4>
                        <p>${q.explanation}</p>
                    </div>

                    <div class="nav-buttons">
                        <button class="btn btn-secondary" onclick="goToMenu()">Menú Principal</button>
                        <button class="btn btn-primary" onclick="nextQuestion()">
                            ${state.currentIndex < state.currentQuestions.length - 1 ? 'Siguiente Pregunta →' : 'Ver Resultados'}
                        </button>
                    </div>
                </div>
            `;
        }

        function renderResults() {
            stopTimer();

            const total = state.currentQuestions.length;
            const percentage = Math.round((state.score / total) * 100);
            const passed = percentage >= 70;
            const elapsed = getElapsedTime();

            // Calculate topic breakdown
            const topicStats = {};
            state.answers.forEach((answer, i) => {
                const q = state.currentQuestions[i];
                const topic = q.topicName || state.currentTopic;
                if (!topicStats[topic]) {
                    topicStats[topic] = { correct: 0, total: 0 };
                }
                topicStats[topic].total++;
                if (answer.isCorrect) {
                    topicStats[topic].correct++;
                }
            });

            let topicBreakdownHTML = '';
            for (const [topic, stats] of Object.entries(topicStats)) {
                const topicPct = Math.round((stats.correct / stats.total) * 100);
                const scoreClass = topicPct >= 70 ? 'good' : 'bad';
                topicBreakdownHTML += `
                    <div class="topic-row">
                        <span>${topic}</span>
                        <span class="topic-score ${scoreClass}">${stats.correct}/${stats.total} (${topicPct}%)</span>
                    </div>
                `;
            }

            return `
                <div class="results-container fade-in">
                    <h2>RESULTADOS</h2>

                    <div class="result-status ${passed ? 'passed' : 'failed'}">
                        ${passed ? '¡APROBADO!' : 'NO APROBADO'}
                    </div>

                    <div class="stats-grid">
                        <div class="stat-card">
                            <h4>Respuestas Correctas</h4>
                            <div class="value">${state.score}/${total}</div>
                        </div>
                        <div class="stat-card">
                            <h4>Porcentaje</h4>
                            <div class="value">${percentage}%</div>
                        </div>
                        <div class="stat-card">
                            <h4>Tiempo Usado</h4>
                            <div class="value">${formatTime(elapsed)} / 02:00:00</div>
                        </div>
                        <div class="stat-card">
                            <h4>Puntaje Requerido</h4>
                            <div class="value">70%</div>
                        </div>
                    </div>

                    ${state.isExamMode ? `
                        <div class="topic-breakdown">
                            <h4>📊 Desglose por Tema</h4>
                            ${topicBreakdownHTML}
                        </div>
                    ` : ''}

                    <div class="nav-buttons" style="justify-content: center; margin-top: 30px;">
                        <button class="btn btn-purple" onclick="startReview()">📝 Revisar Respuestas</button>
                        <button class="btn btn-primary" onclick="goToMenu()">🏠 Menú Principal</button>
                    </div>
                </div>
            `;
        }

        function renderReview() {
            const q = state.currentQuestions[state.currentIndex];
            const answer = state.answers[state.currentIndex];
            const letters = ['A', 'B', 'C', 'D'];

            let optionsHTML = '';
            q.options.forEach((opt, i) => {
                let optClass = '';
                const isCorrectAnswer = Array.isArray(q.answer) ? q.answer.includes(i) : q.answer === i;
                const isUserAnswer = Array.isArray(answer.selected) ?
                    answer.selected.includes(i) : answer.selected === i;

                if (isCorrectAnswer) {
                    optClass = 'correct';
                } else if (isUserAnswer && !isCorrectAnswer) {
                    optClass = 'incorrect';
                }

                optionsHTML += `
                    <div class="option ${optClass}">
                        <div class="option-letter">${letters[i]}</div>
                        <div>${opt}</div>
                    </div>
                `;
            });

            return `
                <div class="question-container fade-in">
                    <div class="question-header">
                        <span class="question-number">Revisión ${state.currentIndex + 1} de ${state.currentQuestions.length}</span>
                        <span style="color: ${answer.isCorrect ? '#50C878' : '#FF6B6B'}; font-weight: bold;">
                            ${answer.isCorrect ? '✓ Correcta' : '✗ Incorrecta'}
                        </span>
                    </div>

                    <div class="question-text">${q.question}</div>

                    <div class="options">
                        ${optionsHTML}
                    </div>

                    <div class="explanation">
                        <h4>📖 Explicación</h4>
                        <p>${q.explanation}</p>
                    </div>

                    <div class="nav-buttons">
                        ${state.currentIndex > 0 ?
                            '<button class="btn btn-secondary" onclick="prevReview()">← Anterior</button>' :
                            '<div></div>'}
                        <button class="btn btn-primary" onclick="showResults()">Ver Resultados</button>
                        ${state.currentIndex < state.currentQuestions.length - 1 ?
                            '<button class="btn btn-secondary" onclick="nextReview()">Siguiente →</button>' :
                            '<div></div>'}
                    </div>
                </div>
            `;
        }

        // Actions
        function goToMenu() {
            stopTimer();
            state = {
                screen: 'menu',
                currentQuestions: [],
                currentIndex: 0,
                score: 0,
                answers: [],
                selectedOptions: [],
                startTime: null,
                timeRemaining: EXAM_TIME_LIMIT,
                isExamMode: false,
                currentTopic: null,
                showingResult: false
            };
            render();
        }

        function showTopics() {
            state.screen = 'topics';
            render();
        }

        function startPractice(topicKey) {
            const topic = questionsDB[topicKey];
            state.currentQuestions = shuffle(topic.questions).map(q => ({
                ...q,
                topicName: topic.name,
                topicColor: topic.color
            }));
            state.currentTopic = topic.name;
            state.currentIndex = 0;
            state.score = 0;
            state.answers = [];
            state.selectedOptions = [];
            state.isExamMode = false;
            state.screen = 'question';
            startTimer();
            render();
        }

        function startExam(numQuestions) {
            let allQuestions = [];
            for (const [key, topic] of Object.entries(questionsDB)) {
                topic.questions.forEach(q => {
                    allQuestions.push({
                        ...q,
                        topicName: topic.name,
                        topicColor: topic.color
                    });
                });
            }

            state.currentQuestions = shuffle(allQuestions).slice(0, numQuestions);
            state.currentTopic = 'Examen Simulado';
            state.currentIndex = 0;
            state.score = 0;
            state.answers = [];
            state.selectedOptions = [];
            state.isExamMode = true;
            state.screen = 'question';
            startTimer();
            render();
        }

        function selectOption(index) {
            const q = state.currentQuestions[state.currentIndex];

            if (q.type === 'multiple') {
                const idx = state.selectedOptions.indexOf(index);
                if (idx > -1) {
                    state.selectedOptions.splice(idx, 1);
                } else {
                    state.selectedOptions.push(index);
                }
            } else {
                state.selectedOptions = [index];
            }

            render();

            // Restart timer display if in exam mode
            if (state.isExamMode) {
                updateTimer();
            }
        }

        function submitAnswer() {
            if (state.selectedOptions.length === 0) {
                alert('Por favor selecciona una respuesta');
                return;
            }

            const q = state.currentQuestions[state.currentIndex];
            let isCorrect;

            if (q.type === 'multiple') {
                const sorted1 = [...state.selectedOptions].sort();
                const sorted2 = [...q.answer].sort();
                isCorrect = sorted1.length === sorted2.length &&
                           sorted1.every((v, i) => v === sorted2[i]);
            } else {
                isCorrect = state.selectedOptions[0] === q.answer;
            }

            if (isCorrect) state.score++;

            state.answers.push({
                selected: q.type === 'multiple' ? [...state.selectedOptions] : state.selectedOptions[0],
                isCorrect
            });

            if (state.isExamMode) {
                // In exam mode, go directly to next question
                if (state.currentIndex < state.currentQuestions.length - 1) {
                    state.currentIndex++;
                    state.selectedOptions = [];
                    render();
                    updateTimer();
                } else {
                    state.screen = 'results';
                    render();
                }
            } else {
                // In practice mode, show result
                state.screen = 'result';
                render();
            }
        }

        function nextQuestion() {
            if (state.currentIndex < state.currentQuestions.length - 1) {
                state.currentIndex++;
                state.selectedOptions = [];
                state.screen = 'question';
                render();
            } else {
                state.screen = 'results';
                render();
            }
        }

        function showResults() {
            state.screen = 'results';
            render();
        }

        function startReview() {
            state.currentIndex = 0;
            state.screen = 'review';
            render();
        }

        function prevReview() {
            if (state.currentIndex > 0) {
                state.currentIndex--;
                render();
            }
        }

        function nextReview() {
            if (state.currentIndex < state.currentQuestions.length - 1) {
                state.currentIndex++;
                render();
            }
        }

        function confirmExit() {
            if (confirm('¿Estás seguro de que quieres salir? Se perderá tu progreso.')) {
                goToMenu();
            }
        }

        // Initialize
        render();
    </script>
</body>
</html>
'''

class ExamHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # Inject questions data
            html = HTML_TEMPLATE.replace(
                'QUESTIONS_DATA_PLACEHOLDER',
                json.dumps(QUESTIONS_DB, ensure_ascii=False)
            )
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/api/questions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(QUESTIONS_DB).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logging

def open_browser():
    """Opens the browser after a short delay"""
    import time
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    print("=" * 60)
    print("  AZ-104 - Simulador de Examen de Certificación")
    print("=" * 60)
    print(f"\n🚀 Iniciando servidor en http://localhost:{PORT}")
    print("\n📌 La aplicación se abrirá automáticamente en tu navegador.")
    print("   Si no se abre, visita: http://localhost:8080")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor.\n")

    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ExamHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego! Servidor detenido.")

if __name__ == "__main__":
    main()
