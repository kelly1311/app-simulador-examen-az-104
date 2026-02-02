#!/usr/bin/env python3
"""
AZ-104 Microsoft Azure Administrator - Simulador de Examen
Versión con Interfaz Gráfica (GUI)
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Tiempo límite del examen: 120 minutos (7200 segundos)
EXAM_TIME_LIMIT = 120 * 60

# ============================================================================
# BANCO DE PREGUNTAS - Estilo Examen Real AZ-104
# ============================================================================


# Banco de preguntas estilo examen real AZ-104
# Basado en Microsoft Learn Study Guide (Abril 2025)

QUESTIONS_DB = {
    "governance": {
        "name": "Administrar Identidades y Gobernanza de Azure",
        "percentage": "20-25%",
        "color": "#4A90D9",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """CASO DE ESTUDIO: Contoso, Ltd.

Contoso, Ltd. es una empresa de consultoría con oficinas principales en Montreal y sucursales en Seattle y Nueva York.

La empresa tiene los siguientes usuarios en Microsoft Entra ID:

| Usuario | Departamento | Rol actual |
|---------|--------------|------------|
| User1 | IT | Global Reader |
| User2 | HR | None |
| User3 | Finance | User Administrator |

User2 necesita crear y administrar grupos de seguridad en Microsoft Entra ID, pero NO debe poder crear ni administrar usuarios.

¿Cuál es el rol de Microsoft Entra ID con PRIVILEGIOS MÍNIMOS que debe asignar a User2?""",
                "options": ['Global Administrator', 'User Administrator', 'Groups Administrator', 'Directory Writers'],
                "answer": 2,
                "explanation": "Groups Administrator es el rol con privilegios mínimos que permite crear y administrar todos los aspectos de los grupos sin tener permisos para administrar usuarios. User Administrator puede crear grupos pero también tiene permisos para administrar usuarios, lo cual viola el principio de privilegio mínimo. Global Administrator tiene todos los permisos. Directory Writers no puede crear grupos de seguridad."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una suscripción de Azure llamada Sub1 que contiene los siguientes recursos:

| Nombre | Tipo | Grupo de Recursos |
|--------|------|-------------------|
| VM1 | Virtual Machine | RG-Prod |
| VM2 | Virtual Machine | RG-Prod |
| SA1 | Storage Account | RG-Data |
| VNET1 | Virtual Network | RG-Network |

Un administrador llamado Admin1 necesita poder asignar roles de Azure RBAC a otros usuarios para los recursos en Sub1.

Admin1 NO debe poder:
- Crear ni eliminar recursos
- Modificar configuraciones de recursos

¿Qué rol debe asignar a Admin1?""",
                "options": ['Owner', 'Contributor', 'User Access Administrator', 'Security Administrator'],
                "answer": 2,
                "explanation": "User Access Administrator permite gestionar el acceso de usuarios a los recursos de Azure (asignar roles RBAC) sin poder crear, modificar o eliminar recursos. Owner tiene todos los permisos incluyendo RBAC y administración de recursos. Contributor puede administrar recursos pero NO puede asignar roles. Security Administrator es para configuraciones de seguridad en Microsoft Defender for Cloud."
            },
            {
                "id": 3,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene la siguiente configuración de Azure:

- Tenant de Microsoft Entra: fabrikam.com
- Suscripción: Fabrikam-Prod
- Política de la empresa: Los recursos solo pueden crearse en East US y West US

Los desarrolladores reportan que pudieron crear máquinas virtuales en North Europe, violando la política de la empresa.

Necesita implementar una solución que PREVENGA la creación de recursos en regiones no autorizadas.

¿Qué efecto de Azure Policy debe usar?""",
                "options": ['Audit', 'Deny', 'Append', 'DeployIfNotExists'],
                "answer": 1,
                "explanation": "El efecto 'Deny' previene activamente la creación o actualización de recursos que no cumplan con la política. 'Audit' solo registra el incumplimiento en el Activity Log pero permite la creación. 'Append' agrega propiedades a recursos. 'DeployIfNotExists' despliega recursos de remediación después de la creación del recurso no conforme."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum tiene la siguiente jerarquía de Azure:

Tenant Root Group
└── MG-Enterprise
    ├── MG-Production
    │   ├── Sub-Prod1
    │   └── Sub-Prod2
    └── MG-Development
        └── Sub-Dev1

Aplica una Azure Policy en MG-Production que requiere la etiqueta "CostCenter" en todos los recursos.

¿Qué recursos serán evaluados por esta política?""",
                "options": ['Solo los recursos en Sub-Prod1', 'Los recursos en Sub-Prod1 y Sub-Prod2', 'Los recursos en todas las suscripciones (Sub-Prod1, Sub-Prod2, Sub-Dev1)', 'Solo los recursos creados después de asignar la política'],
                "answer": 1,
                "explanation": "Las políticas de Azure se heredan hacia abajo en la jerarquía. Una política asignada a MG-Production afectará a todas las suscripciones dentro de ese grupo de administración (Sub-Prod1 y Sub-Prod2), pero NO a Sub-Dev1 que está en MG-Development. La política evalúa tanto recursos existentes como nuevos."
            },
            {
                "id": 5,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Un usuario de Contoso con el rol Contributor en la suscripción intenta crear una máquina virtual y recibe el siguiente error:

"RequestDisallowedByPolicy: Resource 'VM3' was disallowed by policy."

La suscripción tiene la siguiente configuración:
- Azure Policy: "Allowed virtual machine size SKUs" configurada para permitir solo Standard_D2s_v3
- Resource Locks: Ninguno configurado

El usuario intentó crear una VM con el tamaño Standard_B2ms.

¿Cuál es la causa del error?""",
                "options": ['El rol Contributor no tiene permisos para crear VMs', 'Azure Policy está bloqueando la creación porque el SKU no está permitido', 'Existe un Resource Lock de tipo ReadOnly en la suscripción', 'El usuario necesita el rol Owner para crear VMs'],
                "answer": 1,
                "explanation": "El mensaje 'RequestDisallowedByPolicy' indica que una Azure Policy está bloqueando la operación. La política 'Allowed virtual machine size SKUs' solo permite Standard_D2s_v3, pero se intentó crear con Standard_B2ms. El rol Contributor tiene permisos completos para crear VMs. Azure Policy se evalúa DESPUÉS de RBAC y puede bloquear operaciones incluso con permisos suficientes."
            },
            {
                "id": 6,
                "type": "multiple",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank necesita configurar Microsoft Entra ID para cumplir con los siguientes requisitos:

- Los usuarios deben poder restablecer sus propias contraseñas sin contactar al helpdesk
- Se requiere autenticación multifactor para usuarios con roles administrativos
- Los dispositivos móviles de los empleados deben poder acceder a recursos corporativos

¿Qué DOS características de Microsoft Entra debe configurar? (Seleccione dos)""",
                "options": ['Self-Service Password Reset (SSPR)', 'Microsoft Entra Connect', 'Conditional Access', 'Microsoft Entra Domain Services'],
                "answer": [0, 2],
                "explanation": "Self-Service Password Reset (SSPR) permite a los usuarios restablecer sus propias contraseñas. Conditional Access permite crear políticas que requieran MFA para roles específicos y controlar el acceso desde dispositivos. Microsoft Entra Connect es para sincronización con AD on-premises. Microsoft Entra Domain Services proporciona servicios de dominio administrados."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders tiene una aplicación web en Azure App Service que necesita acceder a secretos almacenados en Azure Key Vault.

Los requisitos son:
- NO almacenar credenciales en el código o configuración de la aplicación
- NO requerir rotación manual de credenciales
- La identidad debe eliminarse automáticamente si se elimina la aplicación

¿Qué debe configurar?""",
                "options": ['Crear un Service Principal con secreto de cliente', 'Habilitar System-Assigned Managed Identity', 'Habilitar User-Assigned Managed Identity', 'Usar las Access Keys del Key Vault'],
                "answer": 1,
                "explanation": "System-Assigned Managed Identity cumple todos los requisitos: Azure gestiona las credenciales automáticamente, no requiere almacenar secretos, las credenciales rotan automáticamente, y la identidad se elimina cuando se elimina el recurso. User-Assigned Managed Identity persiste independientemente del recurso. Service Principal requiere gestión manual de secretos."
            },
            {
                "id": 8,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene los siguientes grupos de recursos:

| Grupo de Recursos | Bloqueo | Tipo de Bloqueo |
|-------------------|---------|-----------------|
| RG-Production | Lock1 | Delete |
| RG-Staging | Ninguno | N/A |
| RG-Development | Lock2 | ReadOnly |

Un administrador con rol Owner intenta eliminar una VM en RG-Development.

¿Cuál será el resultado?""",
                "options": ['La VM se eliminará correctamente', 'La operación fallará porque el bloqueo ReadOnly previene eliminaciones', 'La operación fallará porque se requiere el rol Contributor', 'La VM se eliminará pero el disco persistirá'],
                "answer": 1,
                "explanation": "Un bloqueo ReadOnly previene cualquier modificación a los recursos, incluyendo eliminaciones. Incluso un Owner no puede eliminar recursos bajo un bloqueo ReadOnly sin primero eliminar el bloqueo. El bloqueo Delete solo previene eliminaciones pero permite modificaciones."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware necesita implementar la siguiente política de etiquetado:

"Todos los recursos DEBEN tener una etiqueta llamada 'Environment' con un valor. Los recursos sin esta etiqueta NO deben poder crearse."

¿Qué definición de Azure Policy integrada debe usar?""",
                "options": ['Require a tag and its value on resources', 'Require a tag on resource groups', 'Inherit a tag from the resource group if missing', 'Add a tag to resources'],
                "answer": 0,
                "explanation": "'Require a tag and its value on resources' usa el efecto Deny para prevenir la creación de recursos que no tengan la etiqueta especificada con un valor. 'Require a tag on resource groups' aplica solo a grupos de recursos. 'Inherit a tag' copia etiquetas pero no previene la creación. 'Add a tag' usa Modify para agregar etiquetas después de la creación."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene usuarios externos que necesitan colaborar en proyectos de Azure. Los usuarios externos son de una organización asociada con el dominio partner.com.

Los requisitos son:
- Los usuarios externos deben autenticarse usando sus credenciales de partner.com
- Los usuarios externos deben poder acceder a recursos específicos en la suscripción de Fabrikam
- Debe minimizarse la sobrecarga administrativa

¿Qué debe configurar?""",
                "options": ['Crear usuarios miembro en Microsoft Entra ID para cada usuario externo', 'Configurar Microsoft Entra B2B collaboration e invitar usuarios guest', 'Configurar Microsoft Entra B2C', 'Crear un nuevo tenant de Microsoft Entra para los usuarios externos'],
                "answer": 1,
                "explanation": "Microsoft Entra B2B (Business-to-Business) collaboration permite invitar usuarios externos como guests. Los usuarios se autentican con sus propias credenciales (partner.com) y pueden acceder a recursos según los permisos asignados. B2C es para aplicaciones consumer-facing. Crear usuarios miembro o un nuevo tenant aumentaría la sobrecarga administrativa."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene configurado Microsoft Entra Connect para sincronizar su Active Directory on-premises con Microsoft Entra ID.

Un usuario on-premises llamado User1 tiene los siguientes atributos:
- userPrincipalName: user1@contoso.local
- mail: user1@contoso.com

Después de la sincronización, User1 no puede iniciar sesión en Azure Portal.

¿Qué debe hacer para resolver el problema?""",
                "options": ['Cambiar el userPrincipalName on-premises a user1@contoso.com', 'Agregar y verificar el dominio contoso.local en Microsoft Entra ID', 'Deshabilitar la sincronización de hash de contraseñas', 'Asignar una licencia de Microsoft Entra ID Premium a User1'],
                "answer": 0,
                "explanation": "El dominio .local no es un dominio enrutable en Internet y no puede verificarse en Microsoft Entra ID. El userPrincipalName debe usar un dominio verificado (como contoso.com) para que el usuario pueda autenticarse. La solución es cambiar el UPN on-premises a un dominio verificado o agregar un sufijo UPN alternativo en Active Directory."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum necesita delegar la administración de Azure de la siguiente manera:

- El equipo de Network debe poder administrar solo redes virtuales y NSGs
- El equipo de Database debe poder administrar solo servidores SQL y bases de datos
- Ningún equipo debe poder administrar recursos fuera de su área

¿Cuál es la mejor estrategia para implementar esto?""",
                "options": ['Asignar el rol Owner a cada equipo en la suscripción con Azure Policy para restringir', 'Crear grupos de recursos separados y asignar roles específicos a cada equipo en su grupo de recursos', 'Asignar el rol Contributor a todos los usuarios en la suscripción', 'Crear suscripciones separadas para cada equipo'],
                "answer": 1,
                "explanation": "La mejor práctica es usar grupos de recursos para agrupar recursos relacionados y asignar roles RBAC específicos (como Network Contributor, SQL DB Contributor) a cada equipo en su grupo de recursos correspondiente. Esto implementa el principio de mínimo privilegio y segmentación. Crear suscripciones separadas sería excesivo para este escenario."
            },
            {
                "id": 13,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene los siguientes requisitos de cumplimiento:

- Los usuarios con roles administrativos deben solicitar activación de sus privilegios
- La activación debe requerir aprobación de un manager
- Se debe registrar quién aprobó cada activación
- Los privilegios deben expirar automáticamente después de 8 horas

¿Qué característica de Microsoft Entra debe implementar?""",
                "options": ['Conditional Access', 'Privileged Identity Management (PIM)', 'Identity Protection', 'Access Reviews'],
                "answer": 1,
                "explanation": "Privileged Identity Management (PIM) proporciona activación just-in-time de roles privilegiados, flujos de aprobación, registro de auditoría completo y duración configurable de la activación. Conditional Access controla el acceso basado en condiciones pero no gestiona activación de roles. Access Reviews es para revisiones periódicas de acceso. Identity Protection detecta riesgos de identidad."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita optimizar los costos de Azure. El equipo de finanzas requiere:

- Recibir alertas cuando el gasto supere el 80% del presupuesto mensual
- Ver recomendaciones para reducir costos
- Analizar el gasto por departamento usando etiquetas

¿Qué herramientas debe usar?""",
                "options": ['Azure Monitor y Log Analytics', 'Azure Cost Management + Billing y Azure Advisor', 'Azure Policy y Resource Graph', 'Microsoft Defender for Cloud'],
                "answer": 1,
                "explanation": "Azure Cost Management + Billing proporciona análisis de costos, presupuestos con alertas, y puede agrupar costos por etiquetas. Azure Advisor proporciona recomendaciones de optimización de costos (como VMs infrautilizadas, reservas). Azure Monitor es para métricas y logs operacionales. Azure Policy es para gobernanza, no análisis de costos."
            },
            {
                "id": 15,
                "type": "multiple",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso está configurando Microsoft Entra Connect para sincronizar usuarios desde Active Directory on-premises.

Los requisitos son:
- Los usuarios deben poder usar las mismas credenciales on-premises y en la nube
- La autenticación debe validarse contra el AD on-premises
- Si la conexión a on-premises falla, los usuarios deben poder seguir autenticándose

¿Qué DOS opciones de autenticación debe configurar? (Seleccione dos)""",
                "options": ['Password Hash Synchronization (PHS)', 'Pass-through Authentication (PTA)', 'Federation with AD FS', 'Certificate-based authentication'],
                "answer": [0, 1],
                "explanation": "Pass-through Authentication (PTA) valida contraseñas contra AD on-premises en tiempo real. Password Hash Synchronization (PHS) debe habilitarse como respaldo - si PTA falla, los usuarios pueden autenticarse usando los hashes sincronizados. Federation con AD FS también validaría on-premises pero no se solicitó y PTA es más simple. Certificate-based auth no es un método de Microsoft Entra Connect."
            }
        ]
    },
    "storage": {
        "name": "Implementar y Administrar Almacenamiento",
        "percentage": "15-20%",
        "color": "#50C878",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene una cuenta de almacenamiento llamada contosostorage con la siguiente configuración:

| Propiedad | Valor |
|-----------|-------|
| Rendimiento | Standard |
| Redundancia | LRS |
| Nivel de acceso | Hot |

Contoso almacena archivos de log que:
- Se acceden frecuentemente durante los primeros 30 días
- Raramente se acceden después de 30 días
- Deben retenerse por 1 año
- Deben optimizarse para costo

¿Qué debe configurar?""",
                "options": ['Cambiar la redundancia a GRS', 'Configurar Lifecycle Management para mover blobs a Cool después de 30 días y a Archive después de 90 días', 'Cambiar el nivel de acceso de la cuenta a Cool', 'Habilitar soft delete con retención de 365 días'],
                "answer": 1,
                "explanation": "Lifecycle Management permite automatizar el movimiento de blobs entre tiers basado en la antigüedad. Hot tier para los primeros 30 días (acceso frecuente), Cool tier para 30-90 días (acceso infrecuente, menor costo de almacenamiento), y Archive para el resto del año (costo mínimo de almacenamiento). Esto optimiza los costos automáticamente."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene requisitos de recuperación de desastres para sus datos en Azure Storage:

- Los datos deben estar disponibles si toda la región primaria falla
- La aplicación debe poder leer datos de la región secundaria inmediatamente durante una interrupción
- Los costos deben minimizarse

¿Qué tipo de redundancia debe configurar?""",
                "options": ['Locally Redundant Storage (LRS)', 'Zone-Redundant Storage (ZRS)', 'Geo-Redundant Storage (GRS)', 'Read-Access Geo-Redundant Storage (RA-GRS)'],
                "answer": 3,
                "explanation": "RA-GRS replica datos a una región secundaria (como GRS) Y permite acceso de lectura a la región secundaria sin necesidad de failover. GRS también replica geográficamente pero la región secundaria solo es accesible después de un failover iniciado por Microsoft o el cliente. LRS y ZRS no proporcionan redundancia geográfica."
            },
            {
                "id": 3,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene múltiples máquinas virtuales Windows que necesitan compartir archivos. Los requisitos son:

- Los archivos deben ser accesibles via protocolo SMB
- Múltiples VMs deben poder acceder simultáneamente
- Se requiere capacidad de 500 GB
- Los archivos deben poder montarse como una unidad de red (Z:)

¿Qué servicio de Azure Storage debe usar?""",
                "options": ['Azure Blob Storage', 'Azure Files', 'Azure Queue Storage', 'Azure Table Storage'],
                "answer": 1,
                "explanation": "Azure Files proporciona file shares completamente administrados accesibles via protocolo SMB 3.0. Puede montarse como una unidad de red en Windows (y Linux/macOS) y permite acceso simultáneo desde múltiples VMs. Blob Storage es para objetos/archivos no estructurados pero no soporta SMB. Queue es para mensajería, Table para datos NoSQL."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank necesita proporcionar acceso temporal a un contractor externo para descargar un archivo específico de Blob Storage.

Los requisitos son:
- El acceso debe expirar en 24 horas
- El contractor solo debe poder descargar, no modificar ni eliminar
- NO debe compartirse las access keys de la cuenta de almacenamiento
- El acceso debe ser solo para ese archivo específico

¿Qué debe crear?""",
                "options": ['Una Stored Access Policy', 'Un Service SAS token con permisos de lectura', 'Un User Delegation SAS token', 'Configurar acceso anónimo público en el contenedor'],
                "answer": 1,
                "explanation": "Un Service SAS (Shared Access Signature) permite delegar acceso granular a un recurso específico (blob individual) con permisos específicos (solo lectura) y tiempo de expiración (24 horas). User Delegation SAS usaría credenciales de Microsoft Entra pero tiene los mismos beneficios. Stored Access Policy define políticas reusables pero necesita SAS para generar tokens. Acceso anónimo expondría el archivo a todos."
            },
            {
                "id": 5,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum tiene datos en Azure Blob Storage que deben cumplir con regulaciones de retención legal:

- Los datos NO deben poder modificarse durante 7 años
- Los datos NO deben poder eliminarse durante 7 años
- Debe cumplir con SEC Rule 17a-4

¿Qué debe configurar?""",
                "options": ['Soft delete con retención de 7 años', 'Blob versioning', 'Immutable storage con time-based retention policy', 'Legal hold sin retention policy'],
                "answer": 2,
                "explanation": "Immutable storage con time-based retention policy proporciona almacenamiento WORM (Write Once, Read Many) que cumple con regulaciones como SEC 17a-4, FINRA, CFTC. Los blobs no pueden modificarse ni eliminarse durante el período de retención. Soft delete permite recuperación pero no previene eliminación. Legal hold no tiene período definido. Versioning mantiene versiones pero permite eliminación."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita migrar 60 TB de datos desde un datacenter on-premises a Azure Blob Storage.

Las restricciones son:
- La conexión de red es de solo 100 Mbps
- La migración debe completarse en menos de 2 semanas
- Los datos contienen información sensible

¿Cuál es la mejor solución?""",
                "options": ['Usar AzCopy para transferir los datos por Internet', 'Usar Azure Data Box', 'Configurar Azure File Sync', 'Usar Azure Storage Explorer'],
                "answer": 1,
                "explanation": "Con 100 Mbps, transferir 60 TB tomaría aproximadamente 55 días (60TB × 8 / 0.1Gbps / 86400). Azure Data Box es un dispositivo físico que Microsoft envía, se cargan los datos localmente (encriptados), y se envía de vuelta a Microsoft para cargar a Azure. Puede transferir hasta 80 TB por dispositivo en días. Es la única opción viable para cumplir el deadline de 2 semanas."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene una cuenta de almacenamiento con un blob en el tier Archive. Se necesita acceso urgente al blob para una auditoría.

¿Qué debe hacer y cuál es el tiempo estimado?""",
                "options": ['Acceder directamente al blob; disponible inmediatamente', 'Cambiar el tier a Hot; disponible en minutos', 'Rehidratar el blob con prioridad Standard; disponible en hasta 15 horas', 'Rehidratar el blob con prioridad High; disponible en menos de 1 hora para blobs < 10 GB'],
                "answer": 3,
                "explanation": "Los blobs en Archive tier no pueden accederse directamente; deben rehidratarse a Hot o Cool tier primero. Con prioridad High (disponible para blobs < 10 GB), la rehidratación puede completarse en menos de 1 hora. Con prioridad Standard, puede tomar hasta 15 horas. El costo de rehidratación con High priority es mayor."
            },
            {
                "id": 8,
                "type": "multiple",
                "question": """ESCENARIO: Litware, Inc.

Litware necesita configurar seguridad para una cuenta de almacenamiento que contiene datos sensibles.

Los requisitos son:
- Solo VMs en la VNet corporativa pueden acceder a la cuenta de almacenamiento
- Los datos deben estar encriptados con claves controladas por Litware
- El acceso desde Internet público debe estar bloqueado

¿Qué DOS configuraciones debe implementar? (Seleccione dos)""",
                "options": ['Configurar Storage Firewall y agregar la VNet', 'Habilitar Customer-Managed Keys (CMK) con Azure Key Vault', 'Configurar acceso anónimo a nivel de cuenta', 'Cambiar la redundancia a GRS'],
                "answer": [0, 1],
                "explanation": "Storage Firewall permite restringir el acceso a VNets específicas y bloquear acceso público. Customer-Managed Keys (CMK) permite usar sus propias claves de Azure Key Vault para el cifrado, dando control total sobre las claves. El acceso anónimo haría lo contrario de lo requerido. GRS es para redundancia, no seguridad."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene un servidor de archivos Windows on-premises con 2 TB de datos. Necesitan:

- Mantener los archivos accesibles localmente para acceso rápido
- Sincronizar los archivos con Azure Files
- Liberar espacio en el servidor local moviendo archivos poco usados a la nube
- Los usuarios deben ver todos los archivos aunque estén en la nube

¿Qué debe implementar?""",
                "options": ['Azure Backup', 'Azure File Sync con Cloud Tiering habilitado', 'AzCopy con sincronización programada', 'Robocopy a Azure Blob Storage'],
                "answer": 1,
                "explanation": "Azure File Sync sincroniza servidores Windows con Azure Files. Cloud Tiering es una característica opcional que convierte archivos poco accedidos en stubs (punteros) que se descargan on-demand, liberando espacio local mientras los usuarios ven todos los archivos. Azure Backup es para respaldos, no sincronización. AzCopy y Robocopy no proporcionan tiering."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank eliminó accidentalmente un blob importante hace 3 días. La cuenta de almacenamiento tiene soft delete habilitado con retención de 14 días.

¿Cómo puede recuperar el blob?""",
                "options": ['Restaurar desde Azure Backup', 'Usar la operación Undelete desde el portal de Azure o código', 'Contactar a Microsoft Support para recuperar el blob', 'El blob no puede recuperarse después de 24 horas'],
                "answer": 1,
                "explanation": "Con soft delete habilitado, los blobs eliminados se mantienen en estado 'soft deleted' durante el período de retención configurado (14 días en este caso). Pueden recuperarse usando la operación Undelete desde Azure Portal, PowerShell, Azure CLI, o código. No se necesita backup separado ni contactar a soporte."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum necesita configurar una cuenta de almacenamiento para Azure Data Lake Storage Gen2 para análisis de big data.

¿Qué debe habilitar durante la creación de la cuenta de almacenamiento?""",
                "options": ['Large file shares', 'Hierarchical namespace', 'NFS 3.0 protocol', 'SFTP'],
                "answer": 1,
                "explanation": "Hierarchical namespace es el requisito para habilitar Azure Data Lake Storage Gen2. Proporciona un sistema de archivos jerárquico real (directorios, permisos a nivel de archivo) sobre Blob Storage, necesario para operaciones eficientes de big data como rename atómico de directorios. Las otras opciones son características separadas que no habilitan ADLS Gen2."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene dos cuentas de almacenamiento en regiones diferentes:

| Cuenta | Región | Propósito |
|--------|--------|-----------|
| contosoprod | East US | Producción |
| contosodr | West US | DR |

Necesita copiar blobs de contosoprod a contosodr de forma asíncrona, sin descargar los datos al cliente.

¿Qué método debe usar?""",
                "options": ['AzCopy sync desde una VM', 'Copy Blob API (Start-AzStorageBlobCopy)', 'Azure Storage Explorer drag and drop', 'Object Replication'],
                "answer": 3,
                "explanation": "Object Replication copia blobs asincrónicamente entre cuentas de almacenamiento sin intervención del cliente. Los datos se copian directamente entre cuentas en el backend de Azure. Copy Blob API también es asíncrono y server-side, pero Object Replication es para replicación continua automática. AzCopy y Storage Explorer requieren un cliente intermediario."
            },
            {
                "id": 13,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders tiene una aplicación que necesita almacenar millones de mensajes pequeños para procesamiento asíncrono.

Los requisitos son:
- Procesamiento FIFO garantizado
- Detección de mensajes duplicados
- Soporte para transacciones

¿Qué servicio debe usar?""",
                "options": ['Azure Queue Storage', 'Azure Service Bus Queue', 'Azure Event Hub', 'Azure Event Grid'],
                "answer": 1,
                "explanation": "Azure Service Bus Queue proporciona FIFO garantizado (con sesiones), detección de duplicados, y soporte para transacciones. Azure Queue Storage es más simple y económico pero NO garantiza FIFO estricto ni tiene detección de duplicados. Event Hub es para streaming de eventos de alto volumen. Event Grid es para eventos reactivos, no colas de mensajes."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una cuenta de almacenamiento con el firewall habilitado, permitiendo solo la VNet VNet-Prod.

Una aplicación en otra VNet (VNet-Dev) necesita acceder a la cuenta de almacenamiento sin deshabilitar el firewall.

¿Qué puede configurar? (Seleccione la opción más apropiada)""",
                "options": ['Agregar VNet-Dev al firewall de la cuenta de almacenamiento', 'Crear un Private Endpoint en VNet-Dev', 'Configurar VNet Peering entre VNet-Prod y VNet-Dev', 'A o B son opciones válidas'],
                "answer": 3,
                "explanation": "Ambas opciones son válidas: 1) Agregar VNet-Dev al firewall usando Service Endpoints permite tráfico desde esa VNet. 2) Private Endpoint crea una interfaz de red privada en VNet-Dev con IP privada para la cuenta de almacenamiento. VNet Peering solo no es suficiente; también necesitaría Service Endpoint o Private Endpoint."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita configurar acceso a Azure Files para aplicaciones que usan identidades de Microsoft Entra.

Los requisitos son:
- Las aplicaciones deben autenticarse usando Microsoft Entra ID
- Los permisos deben configurarse a nivel de share y archivo/directorio
- NO usar access keys

¿Qué debe configurar?""",
                "options": ['Shared Access Signatures (SAS)', 'Identity-based authentication con Microsoft Entra ID', 'Storage account access keys', 'Anonymous public access'],
                "answer": 1,
                "explanation": "Azure Files soporta identity-based authentication con Microsoft Entra ID (anteriormente Azure AD DS o Microsoft Entra Domain Services, y ahora también Microsoft Entra Kerberos para usuarios híbridos). Permite asignar permisos RBAC a nivel de share y permisos NTFS a nivel de archivo/directorio. SAS usa tokens, no identidades. Access keys dan acceso completo."
            }
        ]
    },
    "compute": {
        "name": "Desplegar y Administrar Recursos de Cómputo de Azure",
        "percentage": "20-25%",
        "color": "#FF6B6B",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso está desplegando una aplicación crítica que requiere un SLA de 99.99% de disponibilidad.

La aplicación se ejecutará en máquinas virtuales en Azure.

¿Qué configuración cumple con el requisito de SLA?""",
                "options": ['Una VM con Premium SSD', 'Dos VMs en un Availability Set', 'Dos o más VMs en diferentes Availability Zones', 'Una VM con un disco Ultra'],
                "answer": 2,
                "explanation": "Para lograr 99.99% de SLA, se requieren dos o más VMs desplegadas en diferentes Availability Zones. Una sola VM tiene máximo 99.9% de SLA (con Premium SSD). Availability Sets proporcionan 99.95% de SLA. Availability Zones son ubicaciones físicamente separadas dentro de una región con energía, red y refrigeración independientes."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una VM llamada VM1 con el tamaño Standard_D4s_v3. Necesitan cambiar el tamaño a Standard_D8s_v3.

VM1 está actualmente en ejecución.

¿Qué sucederá cuando cambie el tamaño?""",
                "options": ['La VM se redimensionará sin interrupción', 'La VM se reiniciará durante el proceso', 'La VM se eliminará y se creará una nueva', 'El cambio fallará; debe detener la VM primero'],
                "answer": 1,
                "explanation": "Cuando se redimensiona una VM en ejecución, Azure la reiniciará para aplicar el nuevo tamaño. Si el nuevo tamaño no está disponible en el cluster actual, la VM debe ser desasignada (deallocated) primero. En este caso, Standard_D8s_v3 está en la misma familia que D4s_v3, así que probablemente solo reiniciará."
            },
            {
                "id": 3,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita ejecutar un script de configuración automáticamente cada vez que se despliega una nueva VM desde una imagen.

El script debe:
- Instalar software adicional
- Configurar el sistema operativo
- Ejecutarse sin intervención manual

¿Qué debe usar?""",
                "options": ['Run Command', 'Custom Script Extension', 'Boot diagnostics', 'Serial Console'],
                "answer": 1,
                "explanation": "Custom Script Extension permite ejecutar scripts automáticamente durante o después del despliegue de VMs. Los scripts pueden descargarse desde Azure Storage, GitHub, o cualquier URL. Se integra con plantillas ARM/Bicep para automatización completa. Run Command es para ejecución ad-hoc. Boot diagnostics es para diagnóstico. Serial Console es para acceso de consola."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum tiene una VM que no puede arrancar después de una actualización del sistema operativo.

El equipo de IT no puede conectarse via RDP porque la VM no completa el arranque.

¿Qué herramienta debe usar para diagnosticar y solucionar el problema?""",
                "options": ['Azure Bastion', 'Network Watcher', 'Serial Console', 'Run Command'],
                "answer": 2,
                "explanation": "Serial Console proporciona acceso de consola de texto a una VM, útil cuando RDP/SSH no funcionan debido a problemas de arranque, configuración de red o sistema operativo corrupto. Permite interactuar con el bootloader y el sistema operativo en modo texto. Bastion requiere que la VM responda. Run Command requiere que el agente de VM funcione."
            },
            {
                "id": 5,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita ejecutar contenedores Docker para procesar trabajos batch de corta duración.

Los requisitos son:
- No gestionar infraestructura de servidores
- Pagar solo por el tiempo de ejecución
- Iniciar contenedores rápidamente bajo demanda

¿Qué servicio debe usar?""",
                "options": ['Azure Kubernetes Service (AKS)', 'Azure Container Instances (ACI)', 'Azure App Service for Containers', 'Virtual Machines con Docker'],
                "answer": 1,
                "explanation": "Azure Container Instances (ACI) es un servicio serverless para ejecutar contenedores sin gestionar VMs ni orquestadores. Factura por segundo de ejecución, inicia en segundos, e ideal para cargas batch, tareas programadas o procesamiento de eventos. AKS requiere gestión del cluster. App Service tiene instancias siempre activas. VMs requieren gestión de infraestructura."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene un App Service Plan en el tier Standard S1. La aplicación web experimenta picos de tráfico predecibles cada lunes de 9am a 12pm.

Necesita configurar auto-scaling para manejar los picos de forma económica.

¿Qué tipo de scaling debe configurar?""",
                "options": ['Scale up manual a un tier más alto', 'Scale out basado en métrica de CPU', 'Scale out programado para lunes 9am-12pm', 'Scale out basado en métricas Y programado'],
                "answer": 2,
                "explanation": "Para picos de tráfico predecibles con horario conocido, scale out programado es la mejor opción. Configura reglas que aumentan las instancias automáticamente en el horario especificado (lunes 9am) y las reducen después (12pm). El scaling basado en métricas es mejor para tráfico impredecible. Combinar ambos es válido pero más complejo para este escenario simple."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso necesita desplegar una aplicación web .NET 6 en Azure App Service.

La aplicación requiere:
- Auto-scaling basado en demanda
- Slots de deployment para staging
- Backups diarios automatizados

¿Cuál es el tier MÍNIMO de App Service Plan requerido?""",
                "options": ['Free (F1)', 'Basic (B1)', 'Standard (S1)', 'Premium (P1v2)'],
                "answer": 2,
                "explanation": "Standard (S1) es el tier mínimo que soporta auto-scaling, deployment slots (hasta 5), y backups diarios (hasta 10 por día). Basic soporta hasta 3 instancias pero manual scaling, sin slots ni backups automatizados. Free es muy limitado. Premium agrega más slots, más backups, y otras características enterprise."
            },
            {
                "id": 8,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una VM con un disco OS de 128 GB que necesita expandirse a 256 GB.

¿Cuáles son los pasos correctos?""",
                "options": ['Expandir el disco desde el portal mientras la VM está en ejecución', 'Detener (deallocate) la VM, expandir el disco, iniciar la VM, extender la partición en el OS', 'Crear un snapshot, crear un nuevo disco de 256 GB desde el snapshot', 'Agregar un nuevo disco de datos de 128 GB'],
                "answer": 1,
                "explanation": "Para expandir un disco OS managed: 1) Deallocate la VM (no solo detener), 2) Expandir el disco en el portal/CLI/PowerShell, 3) Iniciar la VM, 4) Dentro del sistema operativo, extender la partición/volumen para usar el espacio adicional. Los discos de datos pueden expandirse sin deallocate en muchos casos, pero discos OS requieren deallocate."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam quiere crear una imagen personalizada de una VM para usarla como plantilla para múltiples VMs.

La imagen debe incluir el sistema operativo Windows Server 2022 con aplicaciones preinstaladas.

¿Cuál es el proceso correcto?""",
                "options": ['Crear un snapshot del disco OS y usarlo como imagen', 'Ejecutar Sysprep en la VM, deallocate, marcar como generalizada, capturar imagen', 'Copiar el disco VHD a otra cuenta de almacenamiento', 'Exportar la VM a un archivo OVF'],
                "answer": 1,
                "explanation": "Para crear una imagen generalizada reutilizable: 1) Ejecutar Sysprep /generalize /oobe /shutdown en Windows (o waagent -deprovision en Linux), 2) Deallocate la VM, 3) Marcarla como generalizada (Set-AzVm -Generalized), 4) Capturar como imagen (New-AzImage o desde portal). Las imágenes generalizadas permiten crear VMs con identidades únicas."
            },
            {
                "id": 10,
                "type": "multiple",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum está configurando un Virtual Machine Scale Set (VMSS) para una aplicación web.

Necesitan:
- Aumentar instancias automáticamente cuando CPU > 75%
- Reducir instancias cuando CPU < 25%
- Mínimo 2 instancias, máximo 10 instancias

¿Qué DOS configuraciones son REQUERIDAS para auto-scaling? (Seleccione dos)""",
                "options": ['Regla de scale out (aumentar instancias)', 'Regla de scale in (reducir instancias)', 'Load Balancer', 'Application Gateway'],
                "answer": [0, 1],
                "explanation": "Para auto-scaling efectivo basado en métricas se requieren: 1) Regla de scale out para aumentar capacidad bajo carga alta, 2) Regla de scale in para reducir capacidad y costos cuando la demanda baja. Load Balancer es recomendado para distribuir tráfico pero no es técnicamente requerido para que auto-scaling funcione."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders tiene una aplicación en App Service que necesita acceder a secretos en Azure Key Vault.

Actualmente, la aplicación usa un connection string almacenado en App Settings.

¿Cuál es la forma más segura de acceder a Key Vault?""",
                "options": ['Almacenar el secreto de Key Vault en App Settings', 'Usar Key Vault references en App Settings', 'Habilitar System-Assigned Managed Identity y dar acceso a Key Vault', 'B y C combinados'],
                "answer": 3,
                "explanation": "La solución más segura combina: 1) Managed Identity para autenticación sin secretos, 2) Key Vault references (@Microsoft.KeyVault(SecretUri=...)) en App Settings que resuelven automáticamente los secretos. Esto elimina secretos del código y configuración, y usa la identidad administrada para autenticarse con Key Vault."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene un App Service con dos deployment slots: Production y Staging.

Han desplegado una nueva versión en Staging y necesitan moverla a Production sin tiempo de inactividad.

¿Qué operación debe realizar?""",
                "options": ['Copiar los archivos de Staging a Production', 'Realizar un Swap de slots', 'Eliminar Production y renombrar Staging a Production', 'Redirigir manualmente el tráfico'],
                "answer": 1,
                "explanation": "Swap de slots intercambia las configuraciones y contenido entre slots instantáneamente. Azure realiza un 'warm up' del slot de destino antes del swap para evitar cold starts. Si hay problemas, puede hacer swap de nuevo para revertir. Es la forma estándar de implementar deployments blue-green sin downtime en App Service."
            },
            {
                "id": 13,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso necesita desplegar un cluster de Kubernetes administrado.

Los requisitos son:
- Azure debe gestionar el control plane
- Contoso debe gestionar los worker nodes
- Integración con Microsoft Entra ID para autenticación

¿Qué servicio debe usar?""",
                "options": ['Azure Container Instances', 'Azure Kubernetes Service (AKS)', 'Azure Container Apps', 'Azure Red Hat OpenShift'],
                "answer": 1,
                "explanation": "Azure Kubernetes Service (AKS) es el servicio de Kubernetes administrado donde Azure gestiona el control plane (API server, etcd, scheduler) sin costo adicional, y el usuario gestiona los worker nodes (node pools). Soporta integración nativa con Microsoft Entra ID. ACI es serverless sin Kubernetes. Container Apps abstrae más la infraestructura."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una VM con alta latencia de disco. Actualmente usa Standard HDD.

La VM ejecuta una base de datos que requiere:
- Alto IOPS (> 50,000)
- Baja latencia (< 1ms)
- Throughput consistente

¿Qué tipo de disco debe usar?""",
                "options": ['Standard SSD', 'Premium SSD', 'Premium SSD v2', 'Ultra Disk'],
                "answer": 3,
                "explanation": "Ultra Disk proporciona el mejor rendimiento con IOPS (hasta 160,000), throughput (hasta 4,000 MB/s), y latencia sub-millisegundo. Permite configurar IOPS y throughput independientemente. Premium SSD v2 también ofrece alto rendimiento pero Ultra Disk es superior para requisitos extremos como bases de datos de alto rendimiento. Premium SSD tiene límites más bajos."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene VMs que solo se usan durante horario laboral (8am-6pm, lunes a viernes).

Necesitan reducir costos de estas VMs.

¿Qué solución debe implementar?""",
                "options": ['Comprar Azure Reserved Instances', 'Configurar auto-shutdown en las VMs', 'Usar Azure Automation para start/stop programado', 'Cambiar a VMs más pequeñas'],
                "answer": 2,
                "explanation": "Azure Automation con runbooks permite programar el inicio Y detención de VMs. Auto-shutdown solo detiene las VMs pero no las inicia automáticamente. Las VMs detenidas (deallocated) no incurren costos de cómputo. Reserved Instances son para VMs que corren 24/7. Cambiar el tamaño no reduce costos si no se necesitan las VMs."
            }
        ]
    },
    "networking": {
        "name": "Implementar y Administrar Redes Virtuales",
        "percentage": "15-20%",
        "color": "#9B59B6",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene dos VNets en la misma región:

| VNet | Espacio de direcciones | Recursos |
|------|------------------------|----------|
| VNet-Hub | 10.0.0.0/16 | Firewall, VPN Gateway |
| VNet-Spoke | 10.1.0.0/16 | VMs de aplicación |

Las VMs en VNet-Spoke necesitan comunicarse con recursos en VNet-Hub.

El tráfico NO debe pasar por Internet.

¿Qué debe configurar?""",
                "options": ['VPN Gateway', 'VNet Peering', 'ExpressRoute', 'NAT Gateway'],
                "answer": 1,
                "explanation": "VNet Peering conecta dos VNets directamente a través del backbone de Microsoft Azure. El tráfico es privado, de baja latencia, y nunca pasa por Internet. Es la solución más simple y económica para conectar VNets en la misma región o diferentes regiones (Global VNet Peering). VPN Gateway es para conexiones cifradas sobre Internet."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una subnet con servidores web que deben ser accesibles SOLO por HTTPS (puerto 443) desde Internet.

Todo otro tráfico entrante debe ser bloqueado.

¿Qué debe configurar?""",
                "options": ['Azure Firewall', 'Network Security Group (NSG)', 'Application Gateway con WAF', 'Azure Front Door'],
                "answer": 1,
                "explanation": "Network Security Group (NSG) es un firewall de capa 3/4 que filtra tráfico hacia y desde recursos de Azure. Puede asociarse a subnets o NICs. Para este requisito simple (permitir solo 443 entrante), un NSG es la solución más directa y económica. Azure Firewall es para escenarios más complejos. WAF es para protección de aplicaciones web."
            },
            {
                "id": 3,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene VMs en una subnet privada (sin IP pública) que necesitan:

- Acceder a Internet para descargar actualizaciones
- NO ser accesibles desde Internet

¿Qué debe configurar?""",
                "options": ['Asignar IPs públicas a las VMs', 'Configurar NAT Gateway', 'Configurar VNet Peering con una VNet pública', 'Crear una VPN Point-to-Site'],
                "answer": 1,
                "explanation": "NAT Gateway permite que recursos en subnets privadas accedan a Internet para tráfico saliente sin exponer IPs públicas. Todo el tráfico saliente usa la IP del NAT Gateway. Las conexiones entrantes desde Internet no son posibles con NAT Gateway, cumpliendo el requisito de seguridad."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum está desplegando una aplicación web que requiere:

- Balanceo de carga en capa 7 (HTTP/HTTPS)
- Terminación SSL/TLS
- Enrutamiento basado en URL path (/api/* va a backend-api, /* va a backend-web)
- Web Application Firewall (WAF)

¿Qué servicio debe usar?""",
                "options": ['Azure Load Balancer', 'Azure Application Gateway', 'Azure Traffic Manager', 'Azure Load Balancer Standard'],
                "answer": 1,
                "explanation": "Application Gateway es un load balancer de capa 7 (aplicación) que soporta terminación SSL, enrutamiento basado en URL/host/headers, y WAF integrado. Azure Load Balancer es capa 4 (TCP/UDP) sin estas características. Traffic Manager es DNS-based para enrutamiento global, no para balanceo de aplicaciones."
            },
            {
                "id": 5,
                "type": "multiple",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita establecer una conexión VPN Site-to-Site entre su datacenter on-premises y Azure.

El datacenter tiene un dispositivo VPN con IP pública 203.0.113.10.
El rango de red on-premises es 192.168.0.0/16.

¿Qué DOS recursos debe crear en Azure? (Seleccione dos)""",
                "options": ['Virtual Network Gateway (VPN Gateway)', 'Local Network Gateway', 'ExpressRoute Circuit', 'Azure Bastion'],
                "answer": [0, 1],
                "explanation": "Para Site-to-Site VPN se requieren: 1) Virtual Network Gateway (VPN Gateway) - el endpoint de VPN en Azure, 2) Local Network Gateway - representa el dispositivo VPN on-premises (IP pública 203.0.113.10) y los rangos de red on-premises (192.168.0.0/16). Luego se crea una Connection entre ambos. ExpressRoute es una tecnología diferente."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene una VM que actúa como Network Virtual Appliance (firewall).

Todo el tráfico desde la subnet App-Subnet debe pasar por el NVA antes de ir a Internet.

¿Qué debe configurar?""",
                "options": ['NSG con regla de denegación', 'User Defined Route (UDR) con next hop al NVA', 'VNet Peering', 'Service Endpoint'],
                "answer": 1,
                "explanation": "User Defined Routes (UDR) permiten personalizar el enrutamiento de tráfico en Azure. Cree una Route Table con una ruta para 0.0.0.0/0 (todo el tráfico a Internet) con next hop type 'Virtual Appliance' y la IP del NVA. Asocie la Route Table a App-Subnet. El tráfico se redirigirá al NVA antes de salir a Internet."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene una aplicación que necesita conectarse a Azure SQL Database de forma completamente privada.

Los requisitos son:
- El tráfico nunca debe salir de la red de Microsoft
- La base de datos no debe tener endpoint público
- Debe resolverse usando una IP privada

¿Qué debe configurar?""",
                "options": ['Service Endpoint para Microsoft.Sql', 'Private Endpoint', 'VNet Peering con la VNet de SQL', 'Firewall de Azure SQL para permitir la VNet'],
                "answer": 1,
                "explanation": "Private Endpoint crea una interfaz de red privada en su VNet para Azure SQL Database con una IP privada. El tráfico va completamente por la red privada de Microsoft. Puede deshabilitar el endpoint público. Service Endpoint también mantiene el tráfico en la red de Microsoft pero la base de datos mantiene su IP pública."
            },
            {
                "id": 8,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene múltiples VNets y necesita resolución DNS privada entre todas ellas.

Los requisitos son:
- Registrar automáticamente los nombres de las VMs
- Resolver nombres entre VNets
- No usar servidores DNS personalizados

¿Qué debe configurar?""",
                "options": ['Azure DNS public zone', 'Azure Private DNS zone con VNet links', 'DNS servers en las VNets', 'Archivo hosts en cada VM'],
                "answer": 1,
                "explanation": "Azure Private DNS zones proporcionan resolución DNS dentro y entre VNets. Vincule la zona privada a las VNets que necesitan resolver nombres. Habilite auto-registration para que las VMs se registren automáticamente. Es una solución completamente administrada sin necesidad de servidores DNS. Las zonas públicas son para resolución desde Internet."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita conectar su datacenter on-premises a Azure con los siguientes requisitos:

- Conexión privada dedicada (no Internet)
- Latencia predecible y baja
- Ancho de banda garantizado de 1 Gbps
- SLA de conectividad

¿Qué debe implementar?""",
                "options": ['Site-to-Site VPN', 'Point-to-Site VPN', 'ExpressRoute', 'VNet Peering'],
                "answer": 2,
                "explanation": "ExpressRoute proporciona conexión privada dedicada entre on-premises y Azure a través de un proveedor de conectividad. Ofrece latencia predecible, ancho de banda garantizado (desde 50 Mbps hasta 100 Gbps), y SLA de disponibilidad. El tráfico no pasa por Internet público. VPN Site-to-Site usa Internet y no garantiza ancho de banda."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum tiene un NSG con las siguientes reglas entrantes:

| Prioridad | Nombre | Puerto | Acción |
|-----------|--------|--------|--------|
| 100 | Allow-HTTPS | 443 | Allow |
| 200 | Deny-All | * | Deny |
| 65000 | AllowVnetInBound | * | Allow |

¿Qué tráfico entrante será permitido?""",
                "options": ['Solo HTTPS (443) desde cualquier origen', 'HTTPS (443) y tráfico VNet-to-VNet', 'Todo el tráfico', 'Ningún tráfico'],
                "answer": 0,
                "explanation": "Las reglas NSG se evalúan por prioridad (menor número = mayor prioridad). HTTPS (443) es permitido por la regla 100. La regla 200 (Deny-All) bloquea todo otro tráfico ANTES de que se evalúe la regla default AllowVnetInBound (65000). Por lo tanto, incluso el tráfico VNet-to-VNet será bloqueado excepto 443."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita balancear tráfico TCP entre múltiples VMs en una subnet privada.

Los requisitos son:
- Balanceador con IP privada
- Alta disponibilidad
- Health probes

¿Qué tipo de recurso debe crear?""",
                "options": ['Azure Load Balancer - Public', 'Azure Load Balancer - Internal', 'Application Gateway', 'Traffic Manager'],
                "answer": 1,
                "explanation": "Internal (Private) Load Balancer distribuye tráfico dentro de una VNet usando una IP privada. Es ideal para balancear tráfico entre tiers de aplicación (por ejemplo, tier web a tier de aplicación). Public Load Balancer usa IP pública. Application Gateway es capa 7 (HTTP). Traffic Manager es DNS-based para tráfico global."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene la siguiente configuración:

- VNet1 tiene VMs
- VNet2 tiene un VPN Gateway conectado a on-premises
- VNet1 y VNet2 tienen VNet Peering configurado

Las VMs en VNet1 necesitan acceder a recursos on-premises a través del gateway en VNet2.

¿Qué configuración adicional necesita en el peering?""",
                "options": ['Crear un VPN Gateway en VNet1', "Habilitar 'Allow Gateway Transit' en VNet2 y 'Use Remote Gateway' en VNet1", 'Crear otro peering bidireccional', 'No se necesita configuración adicional'],
                "answer": 1,
                "explanation": "Gateway Transit permite compartir un VPN/ExpressRoute gateway entre VNets peered. En VNet2 (que tiene el gateway), habilite 'Allow Gateway Transit'. En VNet1 (que quiere usar el gateway remoto), habilite 'Use Remote Gateway'. Esto evita desplegar gateways redundantes y reduce costos."
            },
            {
                "id": 13,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene usuarios remotos que trabajan desde casa y necesitan acceder a recursos en una VNet de Azure.

Los requisitos son:
- Conexión VPN desde laptops individuales
- Autenticación con certificados o Microsoft Entra ID
- No requiere dispositivo VPN dedicado

¿Qué tipo de conexión debe configurar?""",
                "options": ['Site-to-Site VPN', 'Point-to-Site VPN', 'ExpressRoute', 'Azure Bastion'],
                "answer": 1,
                "explanation": "Point-to-Site (P2S) VPN permite que clientes individuales (laptops, desktops) se conecten a una VNet de Azure desde cualquier ubicación. Soporta autenticación con certificados, RADIUS, o Microsoft Entra ID (nativo). Site-to-Site es para conexiones entre redes completas. Bastion es para acceso RDP/SSH a VMs específicas."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware está diseñando la red para una aplicación de 3 tiers:

- Web tier (frontend)
- Application tier (lógica de negocio)
- Database tier (SQL Server)

¿Cuál es la mejor práctica para segmentación de red?""",
                "options": ['Una subnet para todos los tiers', 'Una subnet por tier con NSGs entre ellos', 'Una VNet por tier con peering', 'VMs en diferentes regiones'],
                "answer": 1,
                "explanation": "La mejor práctica es usar subnets separadas para cada tier (Web, App, Database) dentro de la misma VNet, con NSGs para controlar el tráfico entre ellos. Por ejemplo: Web permite 443 desde Internet, App permite tráfico solo desde Web, Database permite SQL solo desde App. Una VNet por tier añadiría complejidad innecesaria."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita proteger sus aplicaciones web contra ataques como SQL injection, cross-site scripting (XSS), y otros del OWASP Top 10.

¿Qué debe implementar?""",
                "options": ['Network Security Group (NSG)', 'Azure Firewall', 'Web Application Firewall (WAF)', 'DDoS Protection Standard'],
                "answer": 2,
                "explanation": "Web Application Firewall (WAF) protege aplicaciones web contra vulnerabilidades comunes como SQL injection, XSS, y otras amenazas OWASP Top 10. Puede implementarse con Application Gateway o Azure Front Door. NSG es capa 3/4, no inspecciona contenido HTTP. Azure Firewall es capa 3-7 pero no específico para OWASP. DDoS es para ataques volumétricos."
            }
        ]
    },
    "monitoring": {
        "name": "Monitorear y Mantener Recursos de Azure",
        "percentage": "10-15%",
        "color": "#F39C12",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso necesita ser notificado cuando el uso de CPU de una VM supere el 85% durante 5 minutos consecutivos.

La notificación debe enviarse por email al equipo de operaciones.

¿Qué debe configurar?""",
                "options": ['Activity Log alert', 'Metric alert con Action Group', 'Log Analytics query', 'Azure Advisor alert'],
                "answer": 1,
                "explanation": "Metric alerts monitorean métricas de recursos (CPU, memoria, etc.) y pueden disparar cuando se cumplen condiciones específicas (CPU > 85% por 5 minutos). Action Groups definen las acciones a tomar (email, SMS, webhook, Azure Function, etc.). Activity Log alerts son para eventos de administración, no métricas de rendimiento."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware necesita analizar logs de múltiples VMs para:

- Buscar patrones de errores
- Crear queries personalizadas
- Visualizar tendencias
- Configurar alertas basadas en logs

¿Qué servicio debe usar?""",
                "options": ['Azure Monitor Metrics', 'Log Analytics workspace', 'Storage Account logs', 'Azure Diagnostics extension'],
                "answer": 1,
                "explanation": "Log Analytics workspace (parte de Azure Monitor) almacena y permite consultar logs usando Kusto Query Language (KQL). Puede centralizar logs de múltiples recursos, crear dashboards, configurar alertas basadas en queries, y analizar patrones. Azure Monitor Metrics es para datos numéricos de series de tiempo. Storage Account almacena pero no permite queries avanzadas."
            },
            {
                "id": 3,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene VMs críticas que requieren:

- Backups diarios automáticos
- Retención de 30 días
- Capacidad de restaurar archivos individuales sin restaurar toda la VM
- Almacenamiento de backups en otra región

¿Qué debe configurar?""",
                "options": ['Azure Site Recovery', 'Azure Backup con Recovery Services vault (GRS)', 'Snapshots manuales del disco', 'AzCopy programado a otra región'],
                "answer": 1,
                "explanation": "Azure Backup con Recovery Services vault proporciona backups automáticos programados, políticas de retención configurables, y File Recovery para restaurar archivos individuales. Con redundancia GRS, los backups se replican a otra región. Site Recovery es para DR (replicación continua), no backups tradicionales. Snapshots son manuales y no incluyen File Recovery."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum quiere identificar oportunidades para:

- Optimizar costos
- Mejorar la seguridad
- Aumentar la confiabilidad
- Mejorar el rendimiento

Todo desde un solo servicio con recomendaciones personalizadas.

¿Qué herramienta debe usar?""",
                "options": ['Azure Monitor', 'Azure Advisor', 'Microsoft Defender for Cloud', 'Azure Cost Management'],
                "answer": 1,
                "explanation": "Azure Advisor analiza la configuración y uso de recursos y proporciona recomendaciones personalizadas en cinco categorías: Reliability (confiabilidad), Security (seguridad), Performance (rendimiento), Cost (costo), y Operational Excellence. Es un servicio gratuito que consolida todas estas áreas. Defender for Cloud es específico para seguridad."
            },
            {
                "id": 5,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita ver quién creó, modificó o eliminó recursos en una suscripción durante los últimos 90 días para una auditoría.

¿Dónde debe buscar esta información?""",
                "options": ['Azure Monitor Metrics', 'Activity Log', 'Resource health', 'Microsoft Defender for Cloud'],
                "answer": 1,
                "explanation": "Activity Log (registro de actividad) registra operaciones del plano de control realizadas en recursos: quién hizo qué operación, cuándo, desde dónde (IP), y el resultado. Incluye creación, modificación y eliminación de recursos. Se retiene 90 días por defecto. Para retención más larga, exportar a Log Analytics o Storage Account."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Una aplicación web en App Service tiene errores HTTP 500 intermitentes. El equipo necesita:

- Ver el stack trace de las excepciones
- Correlacionar errores con requests específicos
- Identificar dependencias lentas
- Analizar el rendimiento de la aplicación

¿Qué debe habilitar?""",
                "options": ['Diagnostic settings', 'Application Insights', 'Log Analytics', 'Azure Monitor Metrics'],
                "answer": 1,
                "explanation": "Application Insights es una herramienta de Application Performance Management (APM) que proporciona telemetría completa de aplicaciones: requests, excepciones con stack traces, dependencias, métricas personalizadas, y correlación end-to-end. Se integra con App Service y proporciona dashboards de rendimiento y diagnóstico de errores."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso necesita implementar disaster recovery para VMs críticas con:

- RPO (Recovery Point Objective) de 15 minutos
- RTO (Recovery Time Objective) de 1 hora
- Failover automático a región secundaria

¿Qué servicio debe usar?""",
                "options": ['Azure Backup', 'Azure Site Recovery', 'Availability Zones', 'Geo-redundant storage'],
                "answer": 1,
                "explanation": "Azure Site Recovery (ASR) proporciona replicación continua de VMs a una región secundaria con RPO de segundos a minutos. Permite failover rápido (minutos) cumpliendo RTO de 1 hora. Incluye planes de recuperación y pruebas de DR sin impacto. Azure Backup tiene RPO de horas (frecuencia de backup). Availability Zones son para HA regional, no DR."
            },
            {
                "id": 8,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene múltiples suscripciones y necesita:

- Vista consolidada de costos de todas las suscripciones
- Crear presupuestos mensuales con alertas
- Analizar costos por departamento (usando tags)
- Ver recomendaciones de ahorro

¿Qué herramienta debe usar?""",
                "options": ['Azure Pricing Calculator', 'Azure Cost Management + Billing', 'Azure Advisor (solo)', 'Azure Monitor'],
                "answer": 1,
                "explanation": "Azure Cost Management + Billing proporciona análisis de costos multi-suscripción, presupuestos con alertas configurables, agrupación por tags/resource groups/suscripciones, y recomendaciones de optimización de costos. Pricing Calculator es para estimar costos futuros, no analizar gastos actuales. Advisor proporciona algunas recomendaciones de costo pero no análisis completo."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita enviar logs de Windows Event Viewer de múltiples VMs a un Log Analytics workspace.

¿Qué debe instalar en las VMs?""",
                "options": ['Azure Diagnostics extension', 'Azure Monitor Agent', 'Application Insights SDK', 'Custom Script Extension'],
                "answer": 1,
                "explanation": "Azure Monitor Agent (AMA) es el agente recomendado para recopilar logs y métricas de VMs y enviarlos a Log Analytics workspace. Reemplaza al Legacy Log Analytics Agent (MMA) y Azure Diagnostics extension. Usa Data Collection Rules para configurar qué datos recopilar. Application Insights SDK es para aplicaciones, no logs del sistema operativo."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

Una VM de Azure muestra estado 'Unavailable' en Resource Health.

¿Qué indica esto?""",
                "options": ['La VM está apagada por el usuario', 'Azure detectó un problema de plataforma que afecta la VM', 'La VM necesita actualizaciones de sistema operativo', 'El disco de la VM está lleno'],
                "answer": 1,
                "explanation": "Resource Health muestra el estado actual e histórico de recursos. 'Unavailable' indica que Azure detectó un evento de plataforma (no causado por el usuario) que está afectando la disponibilidad del recurso. Proporciona información sobre la causa raíz y acciones recomendadas. VMs apagadas por usuario muestran 'Unknown' o estado diferente."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita ser notificado proactivamente cuando Azure planea realizar mantenimiento que afectará sus VMs.

¿Qué debe configurar?""",
                "options": ['Activity Log alert para eventos de VM', 'Service Health alerts', 'Metric alert para disponibilidad', 'Azure Advisor notifications'],
                "answer": 1,
                "explanation": "Service Health proporciona información personalizada sobre eventos de Azure que afectan sus recursos específicos: service issues (interrupciones), planned maintenance (mantenimiento planificado), y health advisories. Configure alertas de Service Health para recibir notificaciones proactivas sobre mantenimiento que afectará sus recursos."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank necesita retener Activity Logs por 2 años para cumplimiento regulatorio.

El Activity Log por defecto solo retiene 90 días.

¿Qué debe configurar?""",
                "options": ['Cambiar la configuración de retención del Activity Log', 'Exportar Activity Log a Log Analytics workspace o Storage Account', 'No es posible retener más de 90 días', 'Crear copias manuales cada 90 días'],
                "answer": 1,
                "explanation": "Activity Log tiene retención fija de 90 días que no puede cambiarse. Para retención más larga, configure Diagnostic Settings para exportar a: 1) Log Analytics workspace (hasta 12 años con archive), 2) Storage Account (retención ilimitada, más económico para largo plazo). También puede exportar a Event Hub para streaming a sistemas externos."
            },
            {
                "id": 13,
                "type": "multiple",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso está configurando Azure Backup para proteger VMs.

¿Cuáles DOS afirmaciones son correctas sobre Recovery Services vault? (Seleccione dos)""",
                "options": ['El vault debe estar en la misma región que las VMs a proteger', 'Un vault puede proteger VMs en cualquier región', 'Se puede configurar soft delete para proteger contra eliminación accidental de backups', 'Los backups solo funcionan con VMs Windows'],
                "answer": [0, 2],
                "explanation": "Recovery Services vault debe estar en la misma región que las VMs que protege (o en la región emparejada para Cross-Region Restore). Soft delete mantiene los datos de backup por 14 días adicionales después de eliminar un backup, protegiendo contra eliminación accidental o ransomware. Azure Backup soporta tanto VMs Windows como Linux."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware necesita crear un dashboard que muestre:

- Métricas de CPU y memoria de múltiples VMs
- Logs de errores de aplicaciones
- Estado de alertas activas
- Visualizaciones interactivas

¿Qué debe usar?""",
                "options": ['Azure Portal Dashboard solamente', 'Azure Monitor Workbooks', 'Log Analytics queries solamente', 'Power BI'],
                "answer": 1,
                "explanation": "Azure Monitor Workbooks proporciona reportes interactivos que combinan métricas, logs, y visualizaciones en un solo canvas. Permite crear visualizaciones personalizadas, filtros interactivos, y combinar datos de múltiples fuentes. Los dashboards del portal son más limitados. Log Analytics queries son la base pero Workbooks agrega interactividad."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam configuró Site Recovery para VMs críticas. Necesita probar el plan de recuperación sin afectar la producción.

¿Qué tipo de failover debe ejecutar?""",
                "options": ['Planned failover', 'Unplanned failover', 'Test failover', 'Forced failover'],
                "answer": 2,
                "explanation": "Test failover crea una réplica de las VMs en la región secundaria en una red aislada, sin afectar la replicación ni las VMs de producción. Permite validar que el plan de recuperación funciona correctamente. Después de la prueba, se limpian los recursos de test. Planned/Unplanned failover son para eventos reales que afectan producción."
            }
        ]
    }
}


class AZ104ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AZ-104 - Simulador de Examen")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a2e")

        # Variables
        self.current_questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_answers = []
        self.user_answers = []
        self.start_time = None
        self.timer_running = False

        # Configurar estilos
        self.setup_styles()

        # Mostrar pantalla principal
        self.show_main_menu()

    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')

        # Estilo para botones
        style.configure('Topic.TButton',
                       font=('Segoe UI', 11),
                       padding=15)

        style.configure('Action.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       padding=10)

        style.configure('Option.TRadiobutton',
                       font=('Segoe UI', 11),
                       padding=10)

        style.configure('Option.TCheckbutton',
                       font=('Segoe UI', 11),
                       padding=10)

    def clear_window(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Muestra el menú principal"""
        self.clear_window()

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        # Título
        title_label = tk.Label(
            main_frame,
            text="AZ-104",
            font=('Segoe UI', 48, 'bold'),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(
            main_frame,
            text="Microsoft Azure Administrator",
            font=('Segoe UI', 18),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        subtitle_label.pack(pady=(0, 10))

        desc_label = tk.Label(
            main_frame,
            text="Simulador de Examen de Certificación",
            font=('Segoe UI', 14),
            fg="#888888",
            bg="#1a1a2e"
        )
        desc_label.pack(pady=(0, 40))

        # Frame para botones
        buttons_frame = tk.Frame(main_frame, bg="#1a1a2e")
        buttons_frame.pack(expand=True)

        # Botón de práctica por tema
        practice_btn = tk.Button(
            buttons_frame,
            text="📚  Practicar por Tema",
            font=('Segoe UI', 14),
            fg="white",
            bg="#4A90D9",
            activebackground="#3a7bc8",
            activeforeground="white",
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            command=self.show_topic_selection
        )
        practice_btn.pack(pady=10)

        # Botón de examen simulado
        exam_btn = tk.Button(
            buttons_frame,
            text="📝  Examen Simulado (40 preguntas)",
            font=('Segoe UI', 14),
            fg="white",
            bg="#50C878",
            activebackground="#40b868",
            activeforeground="white",
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            command=lambda: self.start_exam(40)
        )
        exam_btn.pack(pady=10)

        # Botón de examen completo
        full_exam_btn = tk.Button(
            buttons_frame,
            text="🎯  Examen Completo (60 preguntas)",
            font=('Segoe UI', 14),
            fg="white",
            bg="#FF6B6B",
            activebackground="#e55b5b",
            activeforeground="white",
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            command=lambda: self.start_exam(60)
        )
        full_exam_btn.pack(pady=10)

        # Información
        info_frame = tk.Frame(main_frame, bg="#1a1a2e")
        info_frame.pack(side='bottom', pady=20)

        total_questions = sum(len(t['questions']) for t in QUESTIONS_DB.values())
        info_label = tk.Label(
            info_frame,
            text=f"📊 {total_questions} preguntas disponibles  •  5 temas  •  ⏱️ 120 minutos  •  Puntaje para aprobar: 70%",
            font=('Segoe UI', 11),
            fg="#888888",
            bg="#1a1a2e"
        )
        info_label.pack()

    def show_topic_selection(self):
        """Muestra la selección de temas"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Selecciona un Tema",
            font=('Segoe UI', 28, 'bold'),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 30))

        # Frame para temas
        topics_frame = tk.Frame(main_frame, bg="#1a1a2e")
        topics_frame.pack(expand=True)

        for topic_key, topic_data in QUESTIONS_DB.items():
            num_questions = len(topic_data['questions'])
            percentage = topic_data.get('percentage', '')

            topic_btn = tk.Button(
                topics_frame,
                text=f"{topic_data['name']} ({percentage})\n({num_questions} preguntas)",
                font=('Segoe UI', 12),
                fg="white",
                bg=topic_data['color'],
                activebackground=topic_data['color'],
                activeforeground="white",
                width=50,
                height=3,
                cursor="hand2",
                relief="flat",
                command=lambda k=topic_key: self.start_practice(k)
            )
            topic_btn.pack(pady=8)

        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="← Volver al Menú",
            font=('Segoe UI', 12),
            fg="white",
            bg="#555555",
            activebackground="#444444",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            command=self.show_main_menu
        )
        back_btn.pack(side='bottom', pady=20)

    def start_practice(self, topic_key):
        """Inicia la práctica de un tema específico"""
        self.current_questions = QUESTIONS_DB[topic_key]['questions'].copy()
        random.shuffle(self.current_questions)
        self.current_topic = QUESTIONS_DB[topic_key]['name']
        self.current_topic_color = QUESTIONS_DB[topic_key]['color']
        self.current_question_index = 0
        self.score = 0
        self.user_answers = []
        self.start_time = datetime.now()
        self.is_exam_mode = False

        self.show_question()

    def start_exam(self, num_questions):
        """Inicia un examen simulado"""
        all_questions = []
        for topic_key, topic_data in QUESTIONS_DB.items():
            for q in topic_data['questions']:
                q_copy = q.copy()
                q_copy['topic'] = topic_data['name']
                q_copy['topic_color'] = topic_data['color']
                all_questions.append(q_copy)

        random.shuffle(all_questions)
        self.current_questions = all_questions[:num_questions]
        self.current_topic = "Examen Simulado"
        self.current_topic_color = "#00d4ff"
        self.current_question_index = 0
        self.score = 0
        self.user_answers = []
        self.start_time = datetime.now()
        self.is_exam_mode = True
        self.timer_running = True

        self.show_question()

    def show_question(self):
        """Muestra la pregunta actual"""
        self.clear_window()

        question = self.current_questions[self.current_question_index]

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill='x', pady=(0, 20))

        # Progreso
        progress_text = f"Pregunta {self.current_question_index + 1} de {len(self.current_questions)}"
        progress_label = tk.Label(
            header_frame,
            text=progress_text,
            font=('Segoe UI', 14, 'bold'),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        progress_label.pack(side='left')

        # Timer (solo en modo examen)
        if self.is_exam_mode:
            self.timer_label = tk.Label(
                header_frame,
                text="00:00:00",
                font=('Segoe UI', 14),
                fg="#FFD700",
                bg="#1a1a2e"
            )
            self.timer_label.pack(side='right')
            self.update_timer()

        # Tema
        topic_name = question.get('topic', self.current_topic)
        topic_color = question.get('topic_color', self.current_topic_color)

        topic_label = tk.Label(
            main_frame,
            text=topic_name,
            font=('Segoe UI', 11),
            fg=topic_color,
            bg="#1a1a2e"
        )
        topic_label.pack(anchor='w')

        # Barra de progreso
        progress_frame = tk.Frame(main_frame, bg="#333333", height=6)
        progress_frame.pack(fill='x', pady=(10, 20))

        progress_pct = (self.current_question_index + 1) / len(self.current_questions)
        progress_bar = tk.Frame(progress_frame, bg="#00d4ff", height=6)
        progress_bar.place(relwidth=progress_pct, relheight=1)

        # Pregunta
        question_frame = tk.Frame(main_frame, bg="#252540", padx=20, pady=20)
        question_frame.pack(fill='x', pady=(0, 20))

        question_label = tk.Label(
            question_frame,
            text=question['question'],
            font=('Segoe UI', 13),
            fg="#ffffff",
            bg="#252540",
            wraplength=900,
            justify='left'
        )
        question_label.pack(anchor='w')

        # Tipo de pregunta
        if question['type'] == 'multiple':
            type_label = tk.Label(
                question_frame,
                text="(Seleccione todas las respuestas correctas)",
                font=('Segoe UI', 11, 'italic'),
                fg="#FFD700",
                bg="#252540"
            )
            type_label.pack(anchor='w', pady=(10, 0))

        # Opciones
        options_frame = tk.Frame(main_frame, bg="#1a1a2e")
        options_frame.pack(fill='x', expand=True)

        self.selected_answers = []

        if question['type'] == 'single':
            self.answer_var = tk.IntVar(value=-1)

            for i, option in enumerate(question['options']):
                opt_frame = tk.Frame(options_frame, bg="#2a2a4a", padx=15, pady=12)
                opt_frame.pack(fill='x', pady=5)

                rb = tk.Radiobutton(
                    opt_frame,
                    text=f"{chr(65+i)}. {option}",
                    variable=self.answer_var,
                    value=i,
                    font=('Segoe UI', 12),
                    fg="#ffffff",
                    bg="#2a2a4a",
                    activebackground="#3a3a5a",
                    activeforeground="#ffffff",
                    selectcolor="#3a3a5a",
                    cursor="hand2"
                )
                rb.pack(anchor='w')
        else:
            self.check_vars = []

            for i, option in enumerate(question['options']):
                opt_frame = tk.Frame(options_frame, bg="#2a2a4a", padx=15, pady=12)
                opt_frame.pack(fill='x', pady=5)

                var = tk.BooleanVar()
                self.check_vars.append(var)

                cb = tk.Checkbutton(
                    opt_frame,
                    text=f"{chr(65+i)}. {option}",
                    variable=var,
                    font=('Segoe UI', 12),
                    fg="#ffffff",
                    bg="#2a2a4a",
                    activebackground="#3a3a5a",
                    activeforeground="#ffffff",
                    selectcolor="#3a3a5a",
                    cursor="hand2"
                )
                cb.pack(anchor='w')

        # Botones
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(fill='x', pady=(20, 0))

        if not self.is_exam_mode:
            submit_btn = tk.Button(
                btn_frame,
                text="Verificar Respuesta",
                font=('Segoe UI', 12, 'bold'),
                fg="white",
                bg="#50C878",
                activebackground="#40b868",
                activeforeground="white",
                width=20,
                height=2,
                cursor="hand2",
                relief="flat",
                command=self.check_answer
            )
            submit_btn.pack(side='right')
        else:
            if self.current_question_index < len(self.current_questions) - 1:
                next_btn = tk.Button(
                    btn_frame,
                    text="Siguiente →",
                    font=('Segoe UI', 12, 'bold'),
                    fg="white",
                    bg="#4A90D9",
                    activebackground="#3a7bc8",
                    activeforeground="white",
                    width=15,
                    height=2,
                    cursor="hand2",
                    relief="flat",
                    command=self.next_question_exam
                )
                next_btn.pack(side='right')
            else:
                finish_btn = tk.Button(
                    btn_frame,
                    text="Finalizar Examen",
                    font=('Segoe UI', 12, 'bold'),
                    fg="white",
                    bg="#FF6B6B",
                    activebackground="#e55b5b",
                    activeforeground="white",
                    width=15,
                    height=2,
                    cursor="hand2",
                    relief="flat",
                    command=self.finish_exam
                )
                finish_btn.pack(side='right')

        # Botón salir
        quit_btn = tk.Button(
            btn_frame,
            text="Salir",
            font=('Segoe UI', 11),
            fg="white",
            bg="#555555",
            activebackground="#444444",
            activeforeground="white",
            width=10,
            cursor="hand2",
            relief="flat",
            command=self.confirm_exit
        )
        quit_btn.pack(side='left')

    def update_timer(self):
        """Actualiza el timer - cuenta regresiva de 120 minutos"""
        if self.timer_running and hasattr(self, 'timer_label'):
            elapsed = datetime.now() - self.start_time
            elapsed_seconds = int(elapsed.total_seconds())
            remaining = max(0, EXAM_TIME_LIMIT - elapsed_seconds)

            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Cambiar color si queda poco tiempo
            if remaining <= 300:  # 5 minutos o menos
                self.timer_label.config(fg="#FF6B6B")
            elif remaining <= 600:  # 10 minutos o menos
                self.timer_label.config(fg="#FFC107")

            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Tiempo agotado
            if remaining <= 0:
                self.timer_running = False
                messagebox.showwarning("⏰ Tiempo Agotado", "El tiempo del examen ha terminado.")
                self.finish_exam_timeout()
                return

            self.root.after(1000, self.update_timer)

    def finish_exam_timeout(self):
        """Finaliza el examen cuando se agota el tiempo"""
        # Marcar preguntas sin responder como incorrectas
        while len(self.user_answers) < len(self.current_questions):
            question = self.current_questions[len(self.user_answers)]
            self.user_answers.append({
                'question': question,
                'user_answer': None,
                'is_correct': False
            })
        self.show_results()

    def get_selected_answers(self, question):
        """Obtiene las respuestas seleccionadas"""
        if question['type'] == 'single':
            return self.answer_var.get()
        else:
            return [i for i, var in enumerate(self.check_vars) if var.get()]

    def check_answer(self):
        """Verifica la respuesta en modo práctica"""
        question = self.current_questions[self.current_question_index]
        user_answer = self.get_selected_answers(question)

        if question['type'] == 'single':
            if user_answer == -1:
                messagebox.showwarning("Aviso", "Por favor selecciona una respuesta")
                return
            is_correct = user_answer == question['answer']
        else:
            if not user_answer:
                messagebox.showwarning("Aviso", "Por favor selecciona al menos una respuesta")
                return
            is_correct = sorted(user_answer) == sorted(question['answer'])

        self.user_answers.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

        if is_correct:
            self.score += 1

        self.show_answer_result(question, user_answer, is_correct)

    def show_answer_result(self, question, user_answer, is_correct):
        """Muestra el resultado de la respuesta"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)

        # Resultado
        if is_correct:
            result_text = "✓ ¡CORRECTO!"
            result_color = "#50C878"
        else:
            result_text = "✗ INCORRECTO"
            result_color = "#FF6B6B"

        result_label = tk.Label(
            main_frame,
            text=result_text,
            font=('Segoe UI', 28, 'bold'),
            fg=result_color,
            bg="#1a1a2e"
        )
        result_label.pack(pady=(0, 20))

        # Puntaje actual
        score_label = tk.Label(
            main_frame,
            text=f"Puntaje: {self.score}/{self.current_question_index + 1}",
            font=('Segoe UI', 14),
            fg="#888888",
            bg="#1a1a2e"
        )
        score_label.pack(pady=(0, 20))

        # Respuesta correcta (si fue incorrecta)
        if not is_correct:
            if question['type'] == 'single':
                correct_text = f"Respuesta correcta: {chr(65 + question['answer'])}"
            else:
                correct_letters = [chr(65 + i) for i in question['answer']]
                correct_text = f"Respuestas correctas: {', '.join(correct_letters)}"

            correct_label = tk.Label(
                main_frame,
                text=correct_text,
                font=('Segoe UI', 13, 'bold'),
                fg="#FFD700",
                bg="#1a1a2e"
            )
            correct_label.pack(pady=(0, 20))

        # Explicación
        exp_frame = tk.Frame(main_frame, bg="#252540", padx=20, pady=20)
        exp_frame.pack(fill='both', expand=True, pady=(0, 20))

        exp_title = tk.Label(
            exp_frame,
            text="Explicación:",
            font=('Segoe UI', 13, 'bold'),
            fg="#00d4ff",
            bg="#252540"
        )
        exp_title.pack(anchor='w', pady=(0, 10))

        exp_text = tk.Label(
            exp_frame,
            text=question['explanation'],
            font=('Segoe UI', 12),
            fg="#ffffff",
            bg="#252540",
            wraplength=900,
            justify='left'
        )
        exp_text.pack(anchor='w')

        # Botones
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(fill='x')

        if self.current_question_index < len(self.current_questions) - 1:
            next_btn = tk.Button(
                btn_frame,
                text="Siguiente Pregunta →",
                font=('Segoe UI', 12, 'bold'),
                fg="white",
                bg="#4A90D9",
                activebackground="#3a7bc8",
                activeforeground="white",
                width=20,
                height=2,
                cursor="hand2",
                relief="flat",
                command=self.next_question
            )
            next_btn.pack(side='right')
        else:
            finish_btn = tk.Button(
                btn_frame,
                text="Ver Resultados",
                font=('Segoe UI', 12, 'bold'),
                fg="white",
                bg="#50C878",
                activebackground="#40b868",
                activeforeground="white",
                width=20,
                height=2,
                cursor="hand2",
                relief="flat",
                command=self.show_results
            )
            finish_btn.pack(side='right')

        menu_btn = tk.Button(
            btn_frame,
            text="Menú Principal",
            font=('Segoe UI', 11),
            fg="white",
            bg="#555555",
            activebackground="#444444",
            activeforeground="white",
            width=15,
            cursor="hand2",
            relief="flat",
            command=self.show_main_menu
        )
        menu_btn.pack(side='left')

    def next_question(self):
        """Avanza a la siguiente pregunta"""
        self.current_question_index += 1
        self.show_question()

    def next_question_exam(self):
        """Avanza a la siguiente pregunta en modo examen"""
        question = self.current_questions[self.current_question_index]
        user_answer = self.get_selected_answers(question)

        if question['type'] == 'single':
            if user_answer == -1:
                messagebox.showwarning("Aviso", "Por favor selecciona una respuesta")
                return
            is_correct = user_answer == question['answer']
        else:
            if not user_answer:
                messagebox.showwarning("Aviso", "Por favor selecciona al menos una respuesta")
                return
            is_correct = sorted(user_answer) == sorted(question['answer'])

        self.user_answers.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

        if is_correct:
            self.score += 1

        self.current_question_index += 1
        self.show_question()

    def finish_exam(self):
        """Finaliza el examen"""
        question = self.current_questions[self.current_question_index]
        user_answer = self.get_selected_answers(question)

        if question['type'] == 'single':
            if user_answer == -1:
                messagebox.showwarning("Aviso", "Por favor selecciona una respuesta")
                return
            is_correct = user_answer == question['answer']
        else:
            if not user_answer:
                messagebox.showwarning("Aviso", "Por favor selecciona al menos una respuesta")
                return
            is_correct = sorted(user_answer) == sorted(question['answer'])

        self.user_answers.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

        if is_correct:
            self.score += 1

        self.timer_running = False
        self.show_results()

    def show_results(self):
        """Muestra los resultados finales"""
        self.clear_window()
        self.timer_running = False

        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        # Calcular resultados
        total = len(self.current_questions)
        percentage = (self.score / total) * 100
        passed = percentage >= 70
        elapsed = datetime.now() - self.start_time

        # Título
        title_label = tk.Label(
            main_frame,
            text="RESULTADOS",
            font=('Segoe UI', 32, 'bold'),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))

        # Estado
        if passed:
            status_text = "¡APROBADO!"
            status_color = "#50C878"
        else:
            status_text = "NO APROBADO"
            status_color = "#FF6B6B"

        status_frame = tk.Frame(main_frame, bg=status_color, padx=40, pady=15)
        status_frame.pack(pady=(0, 30))

        status_label = tk.Label(
            status_frame,
            text=status_text,
            font=('Segoe UI', 24, 'bold'),
            fg="white",
            bg=status_color
        )
        status_label.pack()

        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg="#252540", padx=30, pady=20)
        stats_frame.pack(fill='x', pady=(0, 20))

        stats = [
            ("Respuestas Correctas", f"{self.score} de {total}"),
            ("Porcentaje", f"{percentage:.1f}%"),
            ("Tiempo Total", str(elapsed).split('.')[0]),
            ("Puntaje Requerido", "70%")
        ]

        for label, value in stats:
            row_frame = tk.Frame(stats_frame, bg="#252540")
            row_frame.pack(fill='x', pady=5)

            label_widget = tk.Label(
                row_frame,
                text=label + ":",
                font=('Segoe UI', 13),
                fg="#888888",
                bg="#252540"
            )
            label_widget.pack(side='left')

            value_widget = tk.Label(
                row_frame,
                text=value,
                font=('Segoe UI', 13, 'bold'),
                fg="#ffffff",
                bg="#252540"
            )
            value_widget.pack(side='right')

        # Desglose por tema (solo en modo examen)
        if self.is_exam_mode and self.user_answers:
            topic_stats = {}
            for answer in self.user_answers:
                topic = answer['question'].get('topic', 'General')
                if topic not in topic_stats:
                    topic_stats[topic] = {'correct': 0, 'total': 0}
                topic_stats[topic]['total'] += 1
                if answer['is_correct']:
                    topic_stats[topic]['correct'] += 1

            topics_frame = tk.Frame(main_frame, bg="#252540", padx=20, pady=15)
            topics_frame.pack(fill='x', pady=(0, 20))

            topics_title = tk.Label(
                topics_frame,
                text="Desglose por Tema:",
                font=('Segoe UI', 13, 'bold'),
                fg="#00d4ff",
                bg="#252540"
            )
            topics_title.pack(anchor='w', pady=(0, 10))

            for topic, data in topic_stats.items():
                topic_pct = (data['correct'] / data['total']) * 100
                color = "#50C878" if topic_pct >= 70 else "#FF6B6B"

                topic_row = tk.Frame(topics_frame, bg="#252540")
                topic_row.pack(fill='x', pady=2)

                topic_name = tk.Label(
                    topic_row,
                    text=topic[:45] + "..." if len(topic) > 45 else topic,
                    font=('Segoe UI', 11),
                    fg="#ffffff",
                    bg="#252540"
                )
                topic_name.pack(side='left')

                topic_score = tk.Label(
                    topic_row,
                    text=f"{data['correct']}/{data['total']} ({topic_pct:.0f}%)",
                    font=('Segoe UI', 11, 'bold'),
                    fg=color,
                    bg="#252540"
                )
                topic_score.pack(side='right')

        # Botones
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(fill='x', pady=(10, 0))

        review_btn = tk.Button(
            btn_frame,
            text="📝 Revisar Respuestas",
            font=('Segoe UI', 12),
            fg="white",
            bg="#9B59B6",
            activebackground="#8B49A6",
            activeforeground="white",
            width=20,
            height=2,
            cursor="hand2",
            relief="flat",
            command=self.review_answers
        )
        review_btn.pack(side='left', padx=5)

        menu_btn = tk.Button(
            btn_frame,
            text="🏠 Menú Principal",
            font=('Segoe UI', 12),
            fg="white",
            bg="#4A90D9",
            activebackground="#3a7bc8",
            activeforeground="white",
            width=20,
            height=2,
            cursor="hand2",
            relief="flat",
            command=self.show_main_menu
        )
        menu_btn.pack(side='right', padx=5)

    def review_answers(self):
        """Permite revisar las respuestas"""
        self.review_index = 0
        self.show_review_question()

    def show_review_question(self):
        """Muestra una pregunta en modo revisión"""
        self.clear_window()

        answer_data = self.user_answers[self.review_index]
        question = answer_data['question']
        user_answer = answer_data['user_answer']
        is_correct = answer_data['is_correct']

        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill='x', pady=(0, 15))

        progress_label = tk.Label(
            header_frame,
            text=f"Revisión {self.review_index + 1} de {len(self.user_answers)}",
            font=('Segoe UI', 14, 'bold'),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        progress_label.pack(side='left')

        status_text = "✓ Correcta" if is_correct else "✗ Incorrecta"
        status_color = "#50C878" if is_correct else "#FF6B6B"

        status_label = tk.Label(
            header_frame,
            text=status_text,
            font=('Segoe UI', 14, 'bold'),
            fg=status_color,
            bg="#1a1a2e"
        )
        status_label.pack(side='right')

        # Pregunta
        question_frame = tk.Frame(main_frame, bg="#252540", padx=20, pady=15)
        question_frame.pack(fill='x', pady=(0, 15))

        question_label = tk.Label(
            question_frame,
            text=question['question'],
            font=('Segoe UI', 12),
            fg="#ffffff",
            bg="#252540",
            wraplength=900,
            justify='left'
        )
        question_label.pack(anchor='w')

        # Opciones
        options_frame = tk.Frame(main_frame, bg="#1a1a2e")
        options_frame.pack(fill='x', pady=(0, 15))

        for i, option in enumerate(question['options']):
            if question['type'] == 'single':
                is_user_answer = (i == user_answer)
                is_correct_answer = (i == question['answer'])
            else:
                is_user_answer = (i in user_answer)
                is_correct_answer = (i in question['answer'])

            if is_correct_answer:
                bg_color = "#2d5a3d"
                prefix = "✓ "
            elif is_user_answer and not is_correct_answer:
                bg_color = "#5a2d2d"
                prefix = "✗ "
            else:
                bg_color = "#2a2a4a"
                prefix = "  "

            opt_frame = tk.Frame(options_frame, bg=bg_color, padx=15, pady=10)
            opt_frame.pack(fill='x', pady=3)

            opt_label = tk.Label(
                opt_frame,
                text=f"{prefix}{chr(65+i)}. {option}",
                font=('Segoe UI', 11),
                fg="#ffffff",
                bg=bg_color
            )
            opt_label.pack(anchor='w')

        # Explicación
        exp_frame = tk.Frame(main_frame, bg="#252540", padx=20, pady=15)
        exp_frame.pack(fill='both', expand=True, pady=(0, 15))

        exp_title = tk.Label(
            exp_frame,
            text="Explicación:",
            font=('Segoe UI', 12, 'bold'),
            fg="#00d4ff",
            bg="#252540"
        )
        exp_title.pack(anchor='w', pady=(0, 8))

        exp_text = tk.Label(
            exp_frame,
            text=question['explanation'],
            font=('Segoe UI', 11),
            fg="#ffffff",
            bg="#252540",
            wraplength=900,
            justify='left'
        )
        exp_text.pack(anchor='w')

        # Botones de navegación
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(fill='x')

        if self.review_index > 0:
            prev_btn = tk.Button(
                btn_frame,
                text="← Anterior",
                font=('Segoe UI', 11),
                fg="white",
                bg="#555555",
                activebackground="#444444",
                activeforeground="white",
                width=12,
                cursor="hand2",
                relief="flat",
                command=self.prev_review
            )
            prev_btn.pack(side='left')

        results_btn = tk.Button(
            btn_frame,
            text="Ver Resultados",
            font=('Segoe UI', 11),
            fg="white",
            bg="#4A90D9",
            activebackground="#3a7bc8",
            activeforeground="white",
            width=15,
            cursor="hand2",
            relief="flat",
            command=self.show_results
        )
        results_btn.pack(side='left', padx=20)

        if self.review_index < len(self.user_answers) - 1:
            next_btn = tk.Button(
                btn_frame,
                text="Siguiente →",
                font=('Segoe UI', 11),
                fg="white",
                bg="#555555",
                activebackground="#444444",
                activeforeground="white",
                width=12,
                cursor="hand2",
                relief="flat",
                command=self.next_review
            )
            next_btn.pack(side='right')

    def prev_review(self):
        """Muestra la pregunta anterior en revisión"""
        self.review_index -= 1
        self.show_review_question()

    def next_review(self):
        """Muestra la siguiente pregunta en revisión"""
        self.review_index += 1
        self.show_review_question()

    def confirm_exit(self):
        """Confirma la salida"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres salir?"):
            self.timer_running = False
            self.show_main_menu()


def main():
    root = tk.Tk()
    app = AZ104ExamApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
