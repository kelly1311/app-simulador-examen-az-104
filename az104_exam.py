#!/usr/bin/env python3
"""
AZ-104 Microsoft Azure Administrator - Simulador de Examen
Aplicación para practicar la certificación AZ-104
Preguntas estilo examen real - Basado en Microsoft Learn Study Guide (Abril 2025)
"""

import random
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Tiempo límite del examen: 120 minutos (7200 segundos)
EXAM_TIME_LIMIT = 120 * 60

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

QUESTIONS_DB = {
    "governance": {
        "name": "Administrar Identidades y Gobernanza de Azure",
        "percentage": "20-25%",
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
                "options": [
                    "A. Global Administrator",
                    "B. User Administrator",
                    "C. Groups Administrator",
                    "D. Directory Writers"
                ],
                "answer": "C",
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
                "options": [
                    "A. Owner",
                    "B. Contributor",
                    "C. User Access Administrator",
                    "D. Security Administrator"
                ],
                "answer": "C",
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
                "options": [
                    "A. Audit",
                    "B. Deny",
                    "C. Append",
                    "D. DeployIfNotExists"
                ],
                "answer": "B",
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
                "options": [
                    "A. Solo los recursos en Sub-Prod1",
                    "B. Los recursos en Sub-Prod1 y Sub-Prod2",
                    "C. Los recursos en todas las suscripciones (Sub-Prod1, Sub-Prod2, Sub-Dev1)",
                    "D. Solo los recursos creados después de asignar la política"
                ],
                "answer": "B",
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
                "options": [
                    "A. El rol Contributor no tiene permisos para crear VMs",
                    "B. Azure Policy está bloqueando la creación porque el SKU no está permitido",
                    "C. Existe un Resource Lock de tipo ReadOnly en la suscripción",
                    "D. El usuario necesita el rol Owner para crear VMs"
                ],
                "answer": "B",
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
                "options": [
                    "A. Self-Service Password Reset (SSPR)",
                    "B. Microsoft Entra Connect",
                    "C. Conditional Access",
                    "D. Microsoft Entra Domain Services"
                ],
                "answer": ["A", "C"],
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
                "options": [
                    "A. Crear un Service Principal con secreto de cliente",
                    "B. Habilitar System-Assigned Managed Identity",
                    "C. Habilitar User-Assigned Managed Identity",
                    "D. Usar las Access Keys del Key Vault"
                ],
                "answer": "B",
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
                "options": [
                    "A. La VM se eliminará correctamente",
                    "B. La operación fallará porque el bloqueo ReadOnly previene eliminaciones",
                    "C. La operación fallará porque se requiere el rol Contributor",
                    "D. La VM se eliminará pero el disco persistirá"
                ],
                "answer": "B",
                "explanation": "Un bloqueo ReadOnly previene cualquier modificación a los recursos, incluyendo eliminaciones. Incluso un Owner no puede eliminar recursos bajo un bloqueo ReadOnly sin primero eliminar el bloqueo. El bloqueo Delete solo previene eliminaciones pero permite modificaciones."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware necesita implementar la siguiente política de etiquetado:

"Todos los recursos DEBEN tener una etiqueta llamada 'Environment' con un valor. Los recursos sin esta etiqueta NO deben poder crearse."

¿Qué definición de Azure Policy integrada debe usar?""",
                "options": [
                    "A. Require a tag and its value on resources",
                    "B. Require a tag on resource groups",
                    "C. Inherit a tag from the resource group if missing",
                    "D. Add a tag to resources"
                ],
                "answer": "A",
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
                "options": [
                    "A. Crear usuarios miembro en Microsoft Entra ID para cada usuario externo",
                    "B. Configurar Microsoft Entra B2B collaboration e invitar usuarios guest",
                    "C. Configurar Microsoft Entra B2C",
                    "D. Crear un nuevo tenant de Microsoft Entra para los usuarios externos"
                ],
                "answer": "B",
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
                "options": [
                    "A. Cambiar el userPrincipalName on-premises a user1@contoso.com",
                    "B. Agregar y verificar el dominio contoso.local en Microsoft Entra ID",
                    "C. Deshabilitar la sincronización de hash de contraseñas",
                    "D. Asignar una licencia de Microsoft Entra ID Premium a User1"
                ],
                "answer": "A",
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
                "options": [
                    "A. Asignar el rol Owner a cada equipo en la suscripción con Azure Policy para restringir",
                    "B. Crear grupos de recursos separados y asignar roles específicos a cada equipo en su grupo de recursos",
                    "C. Asignar el rol Contributor a todos los usuarios en la suscripción",
                    "D. Crear suscripciones separadas para cada equipo"
                ],
                "answer": "B",
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
                "options": [
                    "A. Conditional Access",
                    "B. Privileged Identity Management (PIM)",
                    "C. Identity Protection",
                    "D. Access Reviews"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Monitor y Log Analytics",
                    "B. Azure Cost Management + Billing y Azure Advisor",
                    "C. Azure Policy y Resource Graph",
                    "D. Microsoft Defender for Cloud"
                ],
                "answer": "B",
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
                "options": [
                    "A. Password Hash Synchronization (PHS)",
                    "B. Pass-through Authentication (PTA)",
                    "C. Federation with AD FS",
                    "D. Certificate-based authentication"
                ],
                "answer": ["A", "B"],
                "explanation": "Pass-through Authentication (PTA) valida contraseñas contra AD on-premises en tiempo real. Password Hash Synchronization (PHS) debe habilitarse como respaldo - si PTA falla, los usuarios pueden autenticarse usando los hashes sincronizados. Federation con AD FS también validaría on-premises pero no se solicitó y PTA es más simple. Certificate-based auth no es un método de Microsoft Entra Connect."
            }
        ]
    },
    "storage": {
        "name": "Implementar y Administrar Almacenamiento",
        "percentage": "15-20%",
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
                "options": [
                    "A. Cambiar la redundancia a GRS",
                    "B. Configurar Lifecycle Management para mover blobs a Cool después de 30 días y a Archive después de 90 días",
                    "C. Cambiar el nivel de acceso de la cuenta a Cool",
                    "D. Habilitar soft delete con retención de 365 días"
                ],
                "answer": "B",
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
                "options": [
                    "A. Locally Redundant Storage (LRS)",
                    "B. Zone-Redundant Storage (ZRS)",
                    "C. Geo-Redundant Storage (GRS)",
                    "D. Read-Access Geo-Redundant Storage (RA-GRS)"
                ],
                "answer": "D",
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
                "options": [
                    "A. Azure Blob Storage",
                    "B. Azure Files",
                    "C. Azure Queue Storage",
                    "D. Azure Table Storage"
                ],
                "answer": "B",
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
                "options": [
                    "A. Una Stored Access Policy",
                    "B. Un Service SAS token con permisos de lectura",
                    "C. Un User Delegation SAS token",
                    "D. Configurar acceso anónimo público en el contenedor"
                ],
                "answer": "B",
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
                "options": [
                    "A. Soft delete con retención de 7 años",
                    "B. Blob versioning",
                    "C. Immutable storage con time-based retention policy",
                    "D. Legal hold sin retention policy"
                ],
                "answer": "C",
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
                "options": [
                    "A. Usar AzCopy para transferir los datos por Internet",
                    "B. Usar Azure Data Box",
                    "C. Configurar Azure File Sync",
                    "D. Usar Azure Storage Explorer"
                ],
                "answer": "B",
                "explanation": "Con 100 Mbps, transferir 60 TB tomaría aproximadamente 55 días (60TB × 8 / 0.1Gbps / 86400). Azure Data Box es un dispositivo físico que Microsoft envía, se cargan los datos localmente (encriptados), y se envía de vuelta a Microsoft para cargar a Azure. Puede transferir hasta 80 TB por dispositivo en días. Es la única opción viable para cumplir el deadline de 2 semanas."
            },
            {
                "id": 7,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso tiene una cuenta de almacenamiento con un blob en el tier Archive. Se necesita acceso urgente al blob para una auditoría.

¿Qué debe hacer y cuál es el tiempo estimado?""",
                "options": [
                    "A. Acceder directamente al blob; disponible inmediatamente",
                    "B. Cambiar el tier a Hot; disponible en minutos",
                    "C. Rehidratar el blob con prioridad Standard; disponible en hasta 15 horas",
                    "D. Rehidratar el blob con prioridad High; disponible en menos de 1 hora para blobs < 10 GB"
                ],
                "answer": "D",
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
                "options": [
                    "A. Configurar Storage Firewall y agregar la VNet",
                    "B. Habilitar Customer-Managed Keys (CMK) con Azure Key Vault",
                    "C. Configurar acceso anónimo a nivel de cuenta",
                    "D. Cambiar la redundancia a GRS"
                ],
                "answer": ["A", "B"],
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
                "options": [
                    "A. Azure Backup",
                    "B. Azure File Sync con Cloud Tiering habilitado",
                    "C. AzCopy con sincronización programada",
                    "D. Robocopy a Azure Blob Storage"
                ],
                "answer": "B",
                "explanation": "Azure File Sync sincroniza servidores Windows con Azure Files. Cloud Tiering es una característica opcional que convierte archivos poco accedidos en stubs (punteros) que se descargan on-demand, liberando espacio local mientras los usuarios ven todos los archivos. Azure Backup es para respaldos, no sincronización. AzCopy y Robocopy no proporcionan tiering."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank eliminó accidentalmente un blob importante hace 3 días. La cuenta de almacenamiento tiene soft delete habilitado con retención de 14 días.

¿Cómo puede recuperar el blob?""",
                "options": [
                    "A. Restaurar desde Azure Backup",
                    "B. Usar la operación Undelete desde el portal de Azure o código",
                    "C. Contactar a Microsoft Support para recuperar el blob",
                    "D. El blob no puede recuperarse después de 24 horas"
                ],
                "answer": "B",
                "explanation": "Con soft delete habilitado, los blobs eliminados se mantienen en estado 'soft deleted' durante el período de retención configurado (14 días en este caso). Pueden recuperarse usando la operación Undelete desde Azure Portal, PowerShell, Azure CLI, o código. No se necesita backup separado ni contactar a soporte."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum necesita configurar una cuenta de almacenamiento para Azure Data Lake Storage Gen2 para análisis de big data.

¿Qué debe habilitar durante la creación de la cuenta de almacenamiento?""",
                "options": [
                    "A. Large file shares",
                    "B. Hierarchical namespace",
                    "C. NFS 3.0 protocol",
                    "D. SFTP"
                ],
                "answer": "B",
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
                "options": [
                    "A. AzCopy sync desde una VM",
                    "B. Copy Blob API (Start-AzStorageBlobCopy)",
                    "C. Azure Storage Explorer drag and drop",
                    "D. Object Replication"
                ],
                "answer": "D",
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
                "options": [
                    "A. Azure Queue Storage",
                    "B. Azure Service Bus Queue",
                    "C. Azure Event Hub",
                    "D. Azure Event Grid"
                ],
                "answer": "B",
                "explanation": "Azure Service Bus Queue proporciona FIFO garantizado (con sesiones), detección de duplicados, y soporte para transacciones. Azure Queue Storage es más simple y económico pero NO garantiza FIFO estricto ni tiene detección de duplicados. Event Hub es para streaming de eventos de alto volumen. Event Grid es para eventos reactivos, no colas de mensajes."
            },
            {
                "id": 14,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una cuenta de almacenamiento con el firewall habilitado, permitiendo solo la VNet VNet-Prod.

Una aplicación en otra VNet (VNet-Dev) necesita acceder a la cuenta de almacenamiento sin deshabilitar el firewall.

¿Qué puede configurar? (Seleccione la opción más apropiada)""",
                "options": [
                    "A. Agregar VNet-Dev al firewall de la cuenta de almacenamiento",
                    "B. Crear un Private Endpoint en VNet-Dev",
                    "C. Configurar VNet Peering entre VNet-Prod y VNet-Dev",
                    "D. A o B son opciones válidas"
                ],
                "answer": "D",
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
                "options": [
                    "A. Shared Access Signatures (SAS)",
                    "B. Identity-based authentication con Microsoft Entra ID",
                    "C. Storage account access keys",
                    "D. Anonymous public access"
                ],
                "answer": "B",
                "explanation": "Azure Files soporta identity-based authentication con Microsoft Entra ID (anteriormente Azure AD DS o Microsoft Entra Domain Services, y ahora también Microsoft Entra Kerberos para usuarios híbridos). Permite asignar permisos RBAC a nivel de share y permisos NTFS a nivel de archivo/directorio. SAS usa tokens, no identidades. Access keys dan acceso completo."
            }
        ]
    },
    "compute": {
        "name": "Desplegar y Administrar Recursos de Cómputo de Azure",
        "percentage": "20-25%",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso está desplegando una aplicación crítica que requiere un SLA de 99.99% de disponibilidad.

La aplicación se ejecutará en máquinas virtuales en Azure.

¿Qué configuración cumple con el requisito de SLA?""",
                "options": [
                    "A. Una VM con Premium SSD",
                    "B. Dos VMs en un Availability Set",
                    "C. Dos o más VMs en diferentes Availability Zones",
                    "D. Una VM con un disco Ultra"
                ],
                "answer": "C",
                "explanation": "Para lograr 99.99% de SLA, se requieren dos o más VMs desplegadas en diferentes Availability Zones. Una sola VM tiene máximo 99.9% de SLA (con Premium SSD). Availability Sets proporcionan 99.95% de SLA. Availability Zones son ubicaciones físicamente separadas dentro de una región con energía, red y refrigeración independientes."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una VM llamada VM1 con el tamaño Standard_D4s_v3. Necesitan cambiar el tamaño a Standard_D8s_v3.

VM1 está actualmente en ejecución.

¿Qué sucederá cuando cambie el tamaño?""",
                "options": [
                    "A. La VM se redimensionará sin interrupción",
                    "B. La VM se reiniciará durante el proceso",
                    "C. La VM se eliminará y se creará una nueva",
                    "D. El cambio fallará; debe detener la VM primero"
                ],
                "answer": "B",
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
                "options": [
                    "A. Run Command",
                    "B. Custom Script Extension",
                    "C. Boot diagnostics",
                    "D. Serial Console"
                ],
                "answer": "B",
                "explanation": "Custom Script Extension permite ejecutar scripts automáticamente durante o después del despliegue de VMs. Los scripts pueden descargarse desde Azure Storage, GitHub, o cualquier URL. Se integra con plantillas ARM/Bicep para automatización completa. Run Command es para ejecución ad-hoc. Boot diagnostics es para diagnóstico. Serial Console es para acceso de consola."
            },
            {
                "id": 4,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

A. Datum tiene una VM que no puede arrancar después de una actualización del sistema operativo.

El equipo de IT no puede conectarse via RDP porque la VM no completa el arranque.

¿Qué herramienta debe usar para diagnosticar y solucionar el problema?""",
                "options": [
                    "A. Azure Bastion",
                    "B. Network Watcher",
                    "C. Serial Console",
                    "D. Run Command"
                ],
                "answer": "C",
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
                "options": [
                    "A. Azure Kubernetes Service (AKS)",
                    "B. Azure Container Instances (ACI)",
                    "C. Azure App Service for Containers",
                    "D. Virtual Machines con Docker"
                ],
                "answer": "B",
                "explanation": "Azure Container Instances (ACI) es un servicio serverless para ejecutar contenedores sin gestionar VMs ni orquestadores. Factura por segundo de ejecución, inicia en segundos, e ideal para cargas batch, tareas programadas o procesamiento de eventos. AKS requiere gestión del cluster. App Service tiene instancias siempre activas. VMs requieren gestión de infraestructura."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene un App Service Plan en el tier Standard S1. La aplicación web experimenta picos de tráfico predecibles cada lunes de 9am a 12pm.

Necesita configurar auto-scaling para manejar los picos de forma económica.

¿Qué tipo de scaling debe configurar?""",
                "options": [
                    "A. Scale up manual a un tier más alto",
                    "B. Scale out basado en métrica de CPU",
                    "C. Scale out programado para lunes 9am-12pm",
                    "D. Scale out basado en métricas Y programado"
                ],
                "answer": "C",
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
                "options": [
                    "A. Free (F1)",
                    "B. Basic (B1)",
                    "C. Standard (S1)",
                    "D. Premium (P1v2)"
                ],
                "answer": "C",
                "explanation": "Standard (S1) es el tier mínimo que soporta auto-scaling, deployment slots (hasta 5), y backups diarios (hasta 10 por día). Basic soporta hasta 3 instancias pero manual scaling, sin slots ni backups automatizados. Free es muy limitado. Premium agrega más slots, más backups, y otras características enterprise."
            },
            {
                "id": 8,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una VM con un disco OS de 128 GB que necesita expandirse a 256 GB.

¿Cuáles son los pasos correctos?""",
                "options": [
                    "A. Expandir el disco desde el portal mientras la VM está en ejecución",
                    "B. Detener (deallocate) la VM, expandir el disco, iniciar la VM, extender la partición en el OS",
                    "C. Crear un snapshot, crear un nuevo disco de 256 GB desde el snapshot",
                    "D. Agregar un nuevo disco de datos de 128 GB"
                ],
                "answer": "B",
                "explanation": "Para expandir un disco OS managed: 1) Deallocate la VM (no solo detener), 2) Expandir el disco en el portal/CLI/PowerShell, 3) Iniciar la VM, 4) Dentro del sistema operativo, extender la partición/volumen para usar el espacio adicional. Los discos de datos pueden expandirse sin deallocate en muchos casos, pero discos OS requieren deallocate."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam quiere crear una imagen personalizada de una VM para usarla como plantilla para múltiples VMs.

La imagen debe incluir el sistema operativo Windows Server 2022 con aplicaciones preinstaladas.

¿Cuál es el proceso correcto?""",
                "options": [
                    "A. Crear un snapshot del disco OS y usarlo como imagen",
                    "B. Ejecutar Sysprep en la VM, deallocate, marcar como generalizada, capturar imagen",
                    "C. Copiar el disco VHD a otra cuenta de almacenamiento",
                    "D. Exportar la VM a un archivo OVF"
                ],
                "answer": "B",
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
                "options": [
                    "A. Regla de scale out (aumentar instancias)",
                    "B. Regla de scale in (reducir instancias)",
                    "C. Load Balancer",
                    "D. Application Gateway"
                ],
                "answer": ["A", "B"],
                "explanation": "Para auto-scaling efectivo basado en métricas se requieren: 1) Regla de scale out para aumentar capacidad bajo carga alta, 2) Regla de scale in para reducir capacidad y costos cuando la demanda baja. Load Balancer es recomendado para distribuir tráfico pero no es técnicamente requerido para que auto-scaling funcione."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders tiene una aplicación en App Service que necesita acceder a secretos en Azure Key Vault.

Actualmente, la aplicación usa un connection string almacenado en App Settings.

¿Cuál es la forma más segura de acceder a Key Vault?""",
                "options": [
                    "A. Almacenar el secreto de Key Vault en App Settings",
                    "B. Usar Key Vault references en App Settings",
                    "C. Habilitar System-Assigned Managed Identity y dar acceso a Key Vault",
                    "D. B y C combinados"
                ],
                "answer": "D",
                "explanation": "La solución más segura combina: 1) Managed Identity para autenticación sin secretos, 2) Key Vault references (@Microsoft.KeyVault(SecretUri=...)) en App Settings que resuelven automáticamente los secretos. Esto elimina secretos del código y configuración, y usa la identidad administrada para autenticarse con Key Vault."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene un App Service con dos deployment slots: Production y Staging.

Han desplegado una nueva versión en Staging y necesitan moverla a Production sin tiempo de inactividad.

¿Qué operación debe realizar?""",
                "options": [
                    "A. Copiar los archivos de Staging a Production",
                    "B. Realizar un Swap de slots",
                    "C. Eliminar Production y renombrar Staging a Production",
                    "D. Redirigir manualmente el tráfico"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Container Instances",
                    "B. Azure Kubernetes Service (AKS)",
                    "C. Azure Container Apps",
                    "D. Azure Red Hat OpenShift"
                ],
                "answer": "B",
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
                "options": [
                    "A. Standard SSD",
                    "B. Premium SSD",
                    "C. Premium SSD v2",
                    "D. Ultra Disk"
                ],
                "answer": "D",
                "explanation": "Ultra Disk proporciona el mejor rendimiento con IOPS (hasta 160,000), throughput (hasta 4,000 MB/s), y latencia sub-millisegundo. Permite configurar IOPS y throughput independientemente. Premium SSD v2 también ofrece alto rendimiento pero Ultra Disk es superior para requisitos extremos como bases de datos de alto rendimiento. Premium SSD tiene límites más bajos."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam tiene VMs que solo se usan durante horario laboral (8am-6pm, lunes a viernes).

Necesitan reducir costos de estas VMs.

¿Qué solución debe implementar?""",
                "options": [
                    "A. Comprar Azure Reserved Instances",
                    "B. Configurar auto-shutdown en las VMs",
                    "C. Usar Azure Automation para start/stop programado",
                    "D. Cambiar a VMs más pequeñas"
                ],
                "answer": "C",
                "explanation": "Azure Automation con runbooks permite programar el inicio Y detención de VMs. Auto-shutdown solo detiene las VMs pero no las inicia automáticamente. Las VMs detenidas (deallocated) no incurren costos de cómputo. Reserved Instances son para VMs que corren 24/7. Cambiar el tamaño no reduce costos si no se necesitan las VMs."
            }
        ]
    },
    "networking": {
        "name": "Implementar y Administrar Redes Virtuales",
        "percentage": "15-20%",
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
                "options": [
                    "A. VPN Gateway",
                    "B. VNet Peering",
                    "C. ExpressRoute",
                    "D. NAT Gateway"
                ],
                "answer": "B",
                "explanation": "VNet Peering conecta dos VNets directamente a través del backbone de Microsoft Azure. El tráfico es privado, de baja latencia, y nunca pasa por Internet. Es la solución más simple y económica para conectar VNets en la misma región o diferentes regiones (Global VNet Peering). VPN Gateway es para conexiones cifradas sobre Internet."
            },
            {
                "id": 2,
                "type": "single",
                "question": """ESCENARIO: Litware, Inc.

Litware tiene una subnet con servidores web que deben ser accesibles SOLO por HTTPS (puerto 443) desde Internet.

Todo otro tráfico entrante debe ser bloqueado.

¿Qué debe configurar?""",
                "options": [
                    "A. Azure Firewall",
                    "B. Network Security Group (NSG)",
                    "C. Application Gateway con WAF",
                    "D. Azure Front Door"
                ],
                "answer": "B",
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
                "options": [
                    "A. Asignar IPs públicas a las VMs",
                    "B. Configurar NAT Gateway",
                    "C. Configurar VNet Peering con una VNet pública",
                    "D. Crear una VPN Point-to-Site"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Load Balancer",
                    "B. Azure Application Gateway",
                    "C. Azure Traffic Manager",
                    "D. Azure Load Balancer Standard"
                ],
                "answer": "B",
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
                "options": [
                    "A. Virtual Network Gateway (VPN Gateway)",
                    "B. Local Network Gateway",
                    "C. ExpressRoute Circuit",
                    "D. Azure Bastion"
                ],
                "answer": ["A", "B"],
                "explanation": "Para Site-to-Site VPN se requieren: 1) Virtual Network Gateway (VPN Gateway) - el endpoint de VPN en Azure, 2) Local Network Gateway - representa el dispositivo VPN on-premises (IP pública 203.0.113.10) y los rangos de red on-premises (192.168.0.0/16). Luego se crea una Connection entre ambos. ExpressRoute es una tecnología diferente."
            },
            {
                "id": 6,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank tiene una VM que actúa como Network Virtual Appliance (firewall).

Todo el tráfico desde la subnet App-Subnet debe pasar por el NVA antes de ir a Internet.

¿Qué debe configurar?""",
                "options": [
                    "A. NSG con regla de denegación",
                    "B. User Defined Route (UDR) con next hop al NVA",
                    "C. VNet Peering",
                    "D. Service Endpoint"
                ],
                "answer": "B",
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
                "options": [
                    "A. Service Endpoint para Microsoft.Sql",
                    "B. Private Endpoint",
                    "C. VNet Peering con la VNet de SQL",
                    "D. Firewall de Azure SQL para permitir la VNet"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure DNS public zone",
                    "B. Azure Private DNS zone con VNet links",
                    "C. DNS servers en las VNets",
                    "D. Archivo hosts en cada VM"
                ],
                "answer": "B",
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
                "options": [
                    "A. Site-to-Site VPN",
                    "B. Point-to-Site VPN",
                    "C. ExpressRoute",
                    "D. VNet Peering"
                ],
                "answer": "C",
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
                "options": [
                    "A. Solo HTTPS (443) desde cualquier origen",
                    "B. HTTPS (443) y tráfico VNet-to-VNet",
                    "C. Todo el tráfico",
                    "D. Ningún tráfico"
                ],
                "answer": "A",
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
                "options": [
                    "A. Azure Load Balancer - Public",
                    "B. Azure Load Balancer - Internal",
                    "C. Application Gateway",
                    "D. Traffic Manager"
                ],
                "answer": "B",
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
                "options": [
                    "A. Crear un VPN Gateway en VNet1",
                    "B. Habilitar 'Allow Gateway Transit' en VNet2 y 'Use Remote Gateway' en VNet1",
                    "C. Crear otro peering bidireccional",
                    "D. No se necesita configuración adicional"
                ],
                "answer": "B",
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
                "options": [
                    "A. Site-to-Site VPN",
                    "B. Point-to-Site VPN",
                    "C. ExpressRoute",
                    "D. Azure Bastion"
                ],
                "answer": "B",
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
                "options": [
                    "A. Una subnet para todos los tiers",
                    "B. Una subnet por tier con NSGs entre ellos",
                    "C. Una VNet por tier con peering",
                    "D. VMs en diferentes regiones"
                ],
                "answer": "B",
                "explanation": "La mejor práctica es usar subnets separadas para cada tier (Web, App, Database) dentro de la misma VNet, con NSGs para controlar el tráfico entre ellos. Por ejemplo: Web permite 443 desde Internet, App permite tráfico solo desde Web, Database permite SQL solo desde App. Una VNet por tier añadiría complejidad innecesaria."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita proteger sus aplicaciones web contra ataques como SQL injection, cross-site scripting (XSS), y otros del OWASP Top 10.

¿Qué debe implementar?""",
                "options": [
                    "A. Network Security Group (NSG)",
                    "B. Azure Firewall",
                    "C. Web Application Firewall (WAF)",
                    "D. DDoS Protection Standard"
                ],
                "answer": "C",
                "explanation": "Web Application Firewall (WAF) protege aplicaciones web contra vulnerabilidades comunes como SQL injection, XSS, y otras amenazas OWASP Top 10. Puede implementarse con Application Gateway o Azure Front Door. NSG es capa 3/4, no inspecciona contenido HTTP. Azure Firewall es capa 3-7 pero no específico para OWASP. DDoS es para ataques volumétricos."
            }
        ]
    },
    "monitoring": {
        "name": "Monitorear y Mantener Recursos de Azure",
        "percentage": "10-15%",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso necesita ser notificado cuando el uso de CPU de una VM supere el 85% durante 5 minutos consecutivos.

La notificación debe enviarse por email al equipo de operaciones.

¿Qué debe configurar?""",
                "options": [
                    "A. Activity Log alert",
                    "B. Metric alert con Action Group",
                    "C. Log Analytics query",
                    "D. Azure Advisor alert"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Monitor Metrics",
                    "B. Log Analytics workspace",
                    "C. Storage Account logs",
                    "D. Azure Diagnostics extension"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Site Recovery",
                    "B. Azure Backup con Recovery Services vault (GRS)",
                    "C. Snapshots manuales del disco",
                    "D. AzCopy programado a otra región"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Monitor",
                    "B. Azure Advisor",
                    "C. Microsoft Defender for Cloud",
                    "D. Azure Cost Management"
                ],
                "answer": "B",
                "explanation": "Azure Advisor analiza la configuración y uso de recursos y proporciona recomendaciones personalizadas en cinco categorías: Reliability (confiabilidad), Security (seguridad), Performance (rendimiento), Cost (costo), y Operational Excellence. Es un servicio gratuito que consolida todas estas áreas. Defender for Cloud es específico para seguridad."
            },
            {
                "id": 5,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita ver quién creó, modificó o eliminó recursos en una suscripción durante los últimos 90 días para una auditoría.

¿Dónde debe buscar esta información?""",
                "options": [
                    "A. Azure Monitor Metrics",
                    "B. Activity Log",
                    "C. Resource health",
                    "D. Microsoft Defender for Cloud"
                ],
                "answer": "B",
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
                "options": [
                    "A. Diagnostic settings",
                    "B. Application Insights",
                    "C. Log Analytics",
                    "D. Azure Monitor Metrics"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Backup",
                    "B. Azure Site Recovery",
                    "C. Availability Zones",
                    "D. Geo-redundant storage"
                ],
                "answer": "B",
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
                "options": [
                    "A. Azure Pricing Calculator",
                    "B. Azure Cost Management + Billing",
                    "C. Azure Advisor (solo)",
                    "D. Azure Monitor"
                ],
                "answer": "B",
                "explanation": "Azure Cost Management + Billing proporciona análisis de costos multi-suscripción, presupuestos con alertas configurables, agrupación por tags/resource groups/suscripciones, y recomendaciones de optimización de costos. Pricing Calculator es para estimar costos futuros, no analizar gastos actuales. Advisor proporciona algunas recomendaciones de costo pero no análisis completo."
            },
            {
                "id": 9,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam necesita enviar logs de Windows Event Viewer de múltiples VMs a un Log Analytics workspace.

¿Qué debe instalar en las VMs?""",
                "options": [
                    "A. Azure Diagnostics extension",
                    "B. Azure Monitor Agent",
                    "C. Application Insights SDK",
                    "D. Custom Script Extension"
                ],
                "answer": "B",
                "explanation": "Azure Monitor Agent (AMA) es el agente recomendado para recopilar logs y métricas de VMs y enviarlos a Log Analytics workspace. Reemplaza al Legacy Log Analytics Agent (MMA) y Azure Diagnostics extension. Usa Data Collection Rules para configurar qué datos recopilar. Application Insights SDK es para aplicaciones, no logs del sistema operativo."
            },
            {
                "id": 10,
                "type": "single",
                "question": """ESCENARIO: A. Datum Corporation

Una VM de Azure muestra estado 'Unavailable' en Resource Health.

¿Qué indica esto?""",
                "options": [
                    "A. La VM está apagada por el usuario",
                    "B. Azure detectó un problema de plataforma que afecta la VM",
                    "C. La VM necesita actualizaciones de sistema operativo",
                    "D. El disco de la VM está lleno"
                ],
                "answer": "B",
                "explanation": "Resource Health muestra el estado actual e histórico de recursos. 'Unavailable' indica que Azure detectó un evento de plataforma (no causado por el usuario) que está afectando la disponibilidad del recurso. Proporciona información sobre la causa raíz y acciones recomendadas. VMs apagadas por usuario muestran 'Unknown' o estado diferente."
            },
            {
                "id": 11,
                "type": "single",
                "question": """ESCENARIO: Tailwind Traders

Tailwind Traders necesita ser notificado proactivamente cuando Azure planea realizar mantenimiento que afectará sus VMs.

¿Qué debe configurar?""",
                "options": [
                    "A. Activity Log alert para eventos de VM",
                    "B. Service Health alerts",
                    "C. Metric alert para disponibilidad",
                    "D. Azure Advisor notifications"
                ],
                "answer": "B",
                "explanation": "Service Health proporciona información personalizada sobre eventos de Azure que afectan sus recursos específicos: service issues (interrupciones), planned maintenance (mantenimiento planificado), y health advisories. Configure alertas de Service Health para recibir notificaciones proactivas sobre mantenimiento que afectará sus recursos."
            },
            {
                "id": 12,
                "type": "single",
                "question": """ESCENARIO: Woodgrove Bank

Woodgrove Bank necesita retener Activity Logs por 2 años para cumplimiento regulatorio.

El Activity Log por defecto solo retiene 90 días.

¿Qué debe configurar?""",
                "options": [
                    "A. Cambiar la configuración de retención del Activity Log",
                    "B. Exportar Activity Log a Log Analytics workspace o Storage Account",
                    "C. No es posible retener más de 90 días",
                    "D. Crear copias manuales cada 90 días"
                ],
                "answer": "B",
                "explanation": "Activity Log tiene retención fija de 90 días que no puede cambiarse. Para retención más larga, configure Diagnostic Settings para exportar a: 1) Log Analytics workspace (hasta 12 años con archive), 2) Storage Account (retención ilimitada, más económico para largo plazo). También puede exportar a Event Hub para streaming a sistemas externos."
            },
            {
                "id": 13,
                "type": "multiple",
                "question": """ESCENARIO: Contoso, Ltd.

Contoso está configurando Azure Backup para proteger VMs.

¿Cuáles DOS afirmaciones son correctas sobre Recovery Services vault? (Seleccione dos)""",
                "options": [
                    "A. El vault debe estar en la misma región que las VMs a proteger",
                    "B. Un vault puede proteger VMs en cualquier región",
                    "C. Se puede configurar soft delete para proteger contra eliminación accidental de backups",
                    "D. Los backups solo funcionan con VMs Windows"
                ],
                "answer": ["A", "C"],
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
                "options": [
                    "A. Azure Portal Dashboard solamente",
                    "B. Azure Monitor Workbooks",
                    "C. Log Analytics queries solamente",
                    "D. Power BI"
                ],
                "answer": "B",
                "explanation": "Azure Monitor Workbooks proporciona reportes interactivos que combinan métricas, logs, y visualizaciones en un solo canvas. Permite crear visualizaciones personalizadas, filtros interactivos, y combinar datos de múltiples fuentes. Los dashboards del portal son más limitados. Log Analytics queries son la base pero Workbooks agrega interactividad."
            },
            {
                "id": 15,
                "type": "single",
                "question": """ESCENARIO: Fabrikam, Inc.

Fabrikam configuró Site Recovery para VMs críticas. Necesita probar el plan de recuperación sin afectar la producción.

¿Qué tipo de failover debe ejecutar?""",
                "options": [
                    "A. Planned failover",
                    "B. Unplanned failover",
                    "C. Test failover",
                    "D. Forced failover"
                ],
                "answer": "C",
                "explanation": "Test failover crea una réplica de las VMs en la región secundaria en una red aislada, sin afectar la replicación ni las VMs de producción. Permite validar que el plan de recuperación funciona correctamente. Después de la prueba, se limpian los recursos de test. Planned/Unplanned failover son para eventos reales que afectan producción."
            }
        ]
    }
}


def clear_screen():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime el encabezado de la aplicación"""
    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}   AZ-104 Microsoft Azure Administrator - Simulador de Examen{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_menu():
    """Imprime el menú principal"""
    total_questions = sum(len(t['questions']) for t in QUESTIONS_DB.values())
    print(f"{Colors.CYAN}📊 {total_questions} preguntas disponibles • 5 temas • ⏱️ 120 min • 70% para aprobar{Colors.ENDC}\n")
    print(f"{Colors.YELLOW}MENÚ PRINCIPAL{Colors.ENDC}")
    print("-" * 40)
    print("1. Practicar por tema")
    print("2. Examen simulado (40 preguntas)")
    print("3. Examen completo (60 preguntas)")
    print("4. Ver estadísticas")
    print("5. Salir")
    print("-" * 40)

def print_topics_menu():
    """Imprime el menú de temas"""
    print(f"\n{Colors.YELLOW}SELECCIONE UN TEMA:{Colors.ENDC}")
    print("-" * 60)
    topics = list(QUESTIONS_DB.keys())
    for i, topic in enumerate(topics, 1):
        topic_data = QUESTIONS_DB[topic]
        print(f"{i}. {topic_data['name']} ({topic_data['percentage']})")
    print(f"{len(topics) + 1}. Volver al menú principal")
    print("-" * 60)

def get_questions_by_topic(topic_key: str, num_questions: int = None) -> List[Dict]:
    """Obtiene preguntas de un tema específico"""
    questions = QUESTIONS_DB[topic_key]['questions'].copy()
    random.shuffle(questions)
    if num_questions:
        return questions[:num_questions]
    return questions

def get_random_questions(num_questions: int) -> List[Dict]:
    """Obtiene preguntas aleatorias de todos los temas"""
    all_questions = []
    for topic_key, topic_data in QUESTIONS_DB.items():
        for q in topic_data['questions']:
            q_copy = q.copy()
            q_copy['topic'] = topic_data['name']
            all_questions.append(q_copy)
    random.shuffle(all_questions)
    return all_questions[:num_questions]

def display_question(question: Dict, question_num: int, total: int) -> None:
    """Muestra una pregunta"""
    print(f"\n{Colors.CYAN}Pregunta {question_num} de {total}{Colors.ENDC}")
    if 'topic' in question:
        print(f"{Colors.YELLOW}Tema: {question['topic']}{Colors.ENDC}")
    print("-" * 60)
    print(f"\n{question['question']}\n")

    for option in question['options']:
        print(f"  {option}")

    if question['type'] == 'multiple':
        print(f"\n{Colors.YELLOW}(Seleccione múltiples respuestas separadas por coma, ej: A,C){Colors.ENDC}")

def get_user_answer(question: Dict) -> str:
    """Obtiene la respuesta del usuario"""
    while True:
        answer = input(f"\n{Colors.BOLD}Tu respuesta: {Colors.ENDC}").upper().strip()

        if question['type'] == 'single':
            if answer in ['A', 'B', 'C', 'D']:
                return answer
            print(f"{Colors.RED}Por favor, ingresa A, B, C o D{Colors.ENDC}")
        else:
            answers = [a.strip() for a in answer.split(',')]
            if all(a in ['A', 'B', 'C', 'D'] for a in answers):
                return sorted(answers)
            print(f"{Colors.RED}Por favor, ingresa opciones válidas separadas por coma (ej: A,C){Colors.ENDC}")

def check_answer(question: Dict, user_answer) -> bool:
    """Verifica si la respuesta es correcta"""
    correct = question['answer']
    if question['type'] == 'single':
        return user_answer == correct
    else:
        return sorted(user_answer) == sorted(correct)

def display_result(question: Dict, user_answer, is_correct: bool) -> None:
    """Muestra el resultado de la respuesta"""
    if is_correct:
        print(f"\n{Colors.GREEN}✓ ¡CORRECTO!{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}✗ INCORRECTO{Colors.ENDC}")
        correct = question['answer']
        if question['type'] == 'single':
            print(f"{Colors.YELLOW}Respuesta correcta: {correct}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}Respuestas correctas: {', '.join(correct)}{Colors.ENDC}")

    print(f"\n{Colors.CYAN}Explicación:{Colors.ENDC}")
    print(f"{question['explanation']}")

def run_practice(topic_key: str) -> Dict:
    """Ejecuta una sesión de práctica por tema"""
    questions = get_questions_by_topic(topic_key)
    topic_name = QUESTIONS_DB[topic_key]['name']

    clear_screen()
    print_header()
    print(f"{Colors.YELLOW}Practicando: {topic_name}{Colors.ENDC}")
    print(f"Total de preguntas: {len(questions)}")

    correct = 0
    total = len(questions)
    results = []

    for i, question in enumerate(questions, 1):
        display_question(question, i, total)
        user_answer = get_user_answer(question)
        is_correct = check_answer(question, user_answer)

        if is_correct:
            correct += 1

        results.append({
            'question_id': question['id'],
            'correct': is_correct
        })

        display_result(question, user_answer, is_correct)

        if i < total:
            input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.ENDC}")
            clear_screen()
            print_header()

    return {
        'topic': topic_name,
        'correct': correct,
        'total': total,
        'percentage': (correct / total) * 100,
        'results': results
    }

def run_exam(num_questions: int) -> Dict:
    """Ejecuta un examen simulado"""
    questions = get_random_questions(num_questions)

    clear_screen()
    print_header()
    print(f"{Colors.YELLOW}EXAMEN SIMULADO - {num_questions} preguntas{Colors.ENDC}")
    print(f"{Colors.CYAN}⏱️  Tiempo límite: 120 minutos (02:00:00){Colors.ENDC}")
    print(f"{Colors.CYAN}Puntaje para aprobar: 70%{Colors.ENDC}")

    input(f"\n{Colors.CYAN}Presiona Enter para comenzar...{Colors.ENDC}")

    correct = 0
    total = len(questions)
    results = []
    answers_review = []

    start_time = datetime.now()

    for i, question in enumerate(questions, 1):
        clear_screen()
        print_header()
        elapsed = datetime.now() - start_time
        elapsed_seconds = int(elapsed.total_seconds())
        remaining = max(0, EXAM_TIME_LIMIT - elapsed_seconds)
        remaining_hours, remainder = divmod(remaining, 3600)
        remaining_mins, remaining_secs = divmod(remainder, 60)

        # Cambiar color según tiempo restante
        if remaining <= 300:  # 5 minutos o menos
            time_color = Colors.RED
        elif remaining <= 600:  # 10 minutos o menos
            time_color = Colors.YELLOW
        else:
            time_color = Colors.CYAN

        print(f"{time_color}⏱️  Tiempo restante: {remaining_hours:02d}:{remaining_mins:02d}:{remaining_secs:02d} (de 02:00:00){Colors.ENDC}")

        # Verificar si se agotó el tiempo
        if remaining <= 0:
            print(f"\n{Colors.RED}{'='*50}")
            print(f"    ⏰ ¡TIEMPO AGOTADO! El examen ha finalizado.")
            print(f"{'='*50}{Colors.ENDC}")
            break

        display_question(question, i, total)
        user_answer = get_user_answer(question)
        is_correct = check_answer(question, user_answer)

        if is_correct:
            correct += 1

        answers_review.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

        results.append({
            'topic': question.get('topic', 'Unknown'),
            'correct': is_correct
        })

    end_time = datetime.now()
    duration = end_time - start_time

    # Mostrar resultados
    clear_screen()
    print_header()
    percentage = (correct / total) * 100
    passed = percentage >= 70

    print(f"\n{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}           RESULTADOS DEL EXAMEN{Colors.ENDC}")
    print(f"{'='*50}\n")

    if passed:
        print(f"{Colors.GREEN}{'='*50}")
        print(f"          ¡APROBADO!")
        print(f"{'='*50}{Colors.ENDC}\n")
    else:
        print(f"{Colors.RED}{'='*50}")
        print(f"          NO APROBADO")
        print(f"{'='*50}{Colors.ENDC}\n")

    print(f"Respuestas correctas: {correct} de {total}")
    print(f"Porcentaje: {percentage:.1f}%")
    print(f"Tiempo total: {str(duration).split('.')[0]}")
    print(f"Puntaje requerido: 70%")

    # Desglose por tema
    print(f"\n{Colors.YELLOW}Desglose por tema:{Colors.ENDC}")
    print("-" * 40)

    topic_stats = {}
    for result in results:
        topic = result['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}
        topic_stats[topic]['total'] += 1
        if result['correct']:
            topic_stats[topic]['correct'] += 1

    for topic, stats in topic_stats.items():
        topic_pct = (stats['correct'] / stats['total']) * 100
        color = Colors.GREEN if topic_pct >= 70 else Colors.RED
        print(f"{topic[:40]:40} {color}{stats['correct']}/{stats['total']} ({topic_pct:.0f}%){Colors.ENDC}")

    # Opción de revisar respuestas
    print(f"\n{Colors.CYAN}¿Deseas revisar las respuestas? (s/n): {Colors.ENDC}", end="")
    review = input().lower().strip()

    if review == 's':
        for i, item in enumerate(answers_review, 1):
            clear_screen()
            print_header()
            print(f"{Colors.YELLOW}Revisión de respuestas ({i}/{len(answers_review)}){Colors.ENDC}")
            display_question(item['question'], i, len(answers_review))
            print(f"\n{Colors.CYAN}Tu respuesta: {item['user_answer']}{Colors.ENDC}")
            display_result(item['question'], item['user_answer'], item['is_correct'])

            if i < len(answers_review):
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.ENDC}")

    return {
        'correct': correct,
        'total': total,
        'percentage': percentage,
        'passed': passed,
        'duration': str(duration).split('.')[0],
        'topic_stats': topic_stats
    }

def show_statistics():
    """Muestra estadísticas de la sesión actual"""
    clear_screen()
    print_header()
    print(f"{Colors.YELLOW}ESTADÍSTICAS{Colors.ENDC}")
    print("-" * 40)
    print("\nLas estadísticas se guardarán en futuras versiones.")
    print("\nTemas disponibles para practicar:")

    for topic_key, topic_data in QUESTIONS_DB.items():
        num_questions = len(topic_data['questions'])
        print(f"  - {topic_data['name']}: {num_questions} preguntas")

    total_questions = sum(len(t['questions']) for t in QUESTIONS_DB.values())
    print(f"\n{Colors.GREEN}Total de preguntas en el banco: {total_questions}{Colors.ENDC}")

    input(f"\n{Colors.CYAN}Presiona Enter para volver al menú...{Colors.ENDC}")

def main():
    """Función principal"""
    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input(f"\n{Colors.BOLD}Selecciona una opción: {Colors.ENDC}").strip()

        if choice == '1':
            # Practicar por tema
            while True:
                clear_screen()
                print_header()
                print_topics_menu()

                topic_choice = input(f"\n{Colors.BOLD}Selecciona un tema: {Colors.ENDC}").strip()
                topics = list(QUESTIONS_DB.keys())

                try:
                    topic_idx = int(topic_choice) - 1
                    if topic_idx == len(topics):
                        break
                    if 0 <= topic_idx < len(topics):
                        result = run_practice(topics[topic_idx])
                        print(f"\n{Colors.GREEN}Sesión completada!{Colors.ENDC}")
                        print(f"Resultado: {result['correct']}/{result['total']} ({result['percentage']:.1f}%)")
                        input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.ENDC}")
                        break
                except ValueError:
                    print(f"{Colors.RED}Opción no válida{Colors.ENDC}")
                    input(f"{Colors.CYAN}Presiona Enter para continuar...{Colors.ENDC}")

        elif choice == '2':
            # Examen simulado (40 preguntas)
            result = run_exam(40)
            input(f"\n{Colors.CYAN}Presiona Enter para volver al menú...{Colors.ENDC}")

        elif choice == '3':
            # Examen completo (60 preguntas)
            result = run_exam(60)
            input(f"\n{Colors.CYAN}Presiona Enter para volver al menú...{Colors.ENDC}")

        elif choice == '4':
            # Ver estadísticas
            show_statistics()

        elif choice == '5':
            # Salir
            clear_screen()
            print(f"\n{Colors.GREEN}¡Gracias por usar el simulador AZ-104!{Colors.ENDC}")
            print(f"{Colors.CYAN}¡Buena suerte en tu examen de certificación!{Colors.ENDC}\n")
            break

        else:
            print(f"{Colors.RED}Opción no válida. Por favor, selecciona 1-5{Colors.ENDC}")
            input(f"{Colors.CYAN}Presiona Enter para continuar...{Colors.ENDC}")

if __name__ == "__main__":
    main()
