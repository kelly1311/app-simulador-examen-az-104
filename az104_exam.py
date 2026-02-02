#!/usr/bin/env python3
"""
AZ-104 Microsoft Azure Administrator - Simulador de Examen
Aplicación para practicar la certificación AZ-104
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

# Banco de preguntas por tema
QUESTIONS_DB = {
    "governance": {
        "name": "Administrar Identidades y Gobernanza de Azure",
        "percentage": "20-25%",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": "Su empresa tiene una suscripción de Azure llamada Sub1. Necesita asegurarse de que un usuario llamado Admin1 pueda asignar roles a otros usuarios para los recursos dentro de Sub1, pero no pueda realizar otras tareas administrativas. ¿Qué rol debe asignar a Admin1?",
                "options": [
                    "A. Owner",
                    "B. User Access Administrator",
                    "C. Contributor",
                    "D. Security Admin"
                ],
                "answer": "B",
                "explanation": "El rol 'User Access Administrator' permite gestionar el acceso de usuarios a los recursos de Azure. Este rol puede asignar roles a usuarios, grupos y service principals en el ámbito asignado. El rol Owner tiene permisos completos, Contributor puede gestionar recursos pero no asignar roles, y Security Admin es para gestionar configuraciones de seguridad."
            },
            {
                "id": 2,
                "type": "single",
                "question": "Tiene un tenant de Azure AD que contiene un usuario llamado User1. User1 debe crear grupos de Azure AD. ¿Cuál es el rol con mínimos privilegios que debe asignar a User1?",
                "options": [
                    "A. Global Administrator",
                    "B. Groups Administrator",
                    "C. User Administrator",
                    "D. Directory Writers"
                ],
                "answer": "B",
                "explanation": "El rol 'Groups Administrator' es el rol con mínimos privilegios que permite crear y gestionar grupos en Azure AD. Global Administrator tiene todos los permisos, User Administrator puede crear usuarios y grupos pero tiene más permisos de los necesarios, y Directory Writers es para tareas de directorio básicas pero no específicamente para grupos."
            },
            {
                "id": 3,
                "type": "single",
                "question": "Su empresa planea usar Azure Policy para implementar gobernanza. Necesita asegurarse de que los recursos solo puedan crearse en las regiones East US y West US. ¿Qué debe usar?",
                "options": [
                    "A. Una política con efecto 'Audit'",
                    "B. Una política con efecto 'Deny'",
                    "C. Una política con efecto 'Append'",
                    "D. Una política con efecto 'DeployIfNotExists'"
                ],
                "answer": "B",
                "explanation": "El efecto 'Deny' previene la creación de recursos que no cumplan con la política. 'Audit' solo registra el incumplimiento pero no lo previene. 'Append' agrega campos adicionales al recurso. 'DeployIfNotExists' despliega recursos relacionados si no existen."
            },
            {
                "id": 4,
                "type": "single",
                "question": "Tiene una suscripción de Azure con varios grupos de recursos. Necesita aplicar las mismas etiquetas a todos los recursos dentro de un grupo de recursos específico automáticamente. ¿Qué debe configurar?",
                "options": [
                    "A. Azure Policy con efecto 'Modify'",
                    "B. Un bloqueo de recurso",
                    "C. Control de acceso basado en roles (RBAC)",
                    "D. Azure Blueprints"
                ],
                "answer": "A",
                "explanation": "Azure Policy con efecto 'Modify' puede agregar, actualizar o eliminar propiedades de un recurso durante la creación o actualización. Es ideal para aplicar etiquetas automáticamente. Los bloqueos previenen cambios/eliminaciones, RBAC controla acceso, y Blueprints es para despliegues repetibles de entornos."
            },
            {
                "id": 5,
                "type": "multiple",
                "question": "Su empresa tiene los siguientes requisitos para Azure AD:\n- Los usuarios deben registrar sus propios dispositivos\n- Los administradores deben poder restablecer contraseñas de usuarios\n- Se requiere autenticación multifactor para administradores\n\n¿Qué dos características de Azure AD debe configurar? (Seleccione dos)",
                "options": [
                    "A. Azure AD Join",
                    "B. Self-Service Password Reset (SSPR)",
                    "C. Conditional Access",
                    "D. Azure AD Device Registration"
                ],
                "answer": ["C", "D"],
                "explanation": "Azure AD Device Registration permite a los usuarios registrar sus dispositivos. Conditional Access permite configurar MFA para roles específicos como administradores. SSPR es para que los usuarios restablezcan sus propias contraseñas, no administradores. Azure AD Join es para unir dispositivos al directorio corporativo."
            },
            {
                "id": 6,
                "type": "single",
                "question": "Tiene un grupo de administración llamado MG1 que contiene dos suscripciones: Sub1 y Sub2. Aplica una política en MG1 que restringe la creación de recursos a la región West Europe. ¿Qué afirmación es correcta?",
                "options": [
                    "A. Solo Sub1 heredará la política",
                    "B. Ambas suscripciones heredarán la política",
                    "C. Ninguna suscripción heredará la política",
                    "D. Solo los grupos de recursos heredarán la política"
                ],
                "answer": "B",
                "explanation": "Las políticas aplicadas a un grupo de administración se heredan a todas las suscripciones y recursos dentro de ese grupo de administración. Es un principio fundamental de la jerarquía de Azure: Tenant Root Group > Management Groups > Subscriptions > Resource Groups > Resources."
            },
            {
                "id": 7,
                "type": "single",
                "question": "Necesita crear una identidad que será usada por una aplicación para acceder a recursos de Azure. La identidad no debe requerir gestión de credenciales. ¿Qué debe crear?",
                "options": [
                    "A. Un usuario de Azure AD",
                    "B. Un Service Principal con secreto",
                    "C. Una Managed Identity",
                    "D. Un grupo de Azure AD"
                ],
                "answer": "C",
                "explanation": "Managed Identity es una identidad gestionada automáticamente por Azure que no requiere gestión de credenciales (rotación de secretos, certificados, etc.). Azure gestiona automáticamente las credenciales. Service Principal requiere gestión manual de secretos o certificados."
            },
            {
                "id": 8,
                "type": "single",
                "question": "Su empresa requiere que todos los recursos tengan una etiqueta llamada 'CostCenter'. Los recursos sin esta etiqueta no deben poder crearse. ¿Qué definición de política debe usar?",
                "options": [
                    "A. Require a tag on resources",
                    "B. Require a tag on resource groups",
                    "C. Inherit a tag from the resource group",
                    "D. Add a tag to resources"
                ],
                "answer": "A",
                "explanation": "'Require a tag on resources' es una política incorporada que deniega la creación de recursos que no tengan la etiqueta especificada. 'Require a tag on resource groups' aplica a grupos de recursos, no a recursos individuales. 'Inherit' y 'Add' agregan etiquetas pero no las requieren."
            },
            {
                "id": 9,
                "type": "single",
                "question": "Tiene un tenant de Azure AD con Azure AD Premium P2. Necesita configurar revisiones de acceso periódicas para los miembros de un grupo. ¿Dónde debe configurar esto?",
                "options": [
                    "A. Azure AD Privileged Identity Management",
                    "B. Azure AD Identity Protection",
                    "C. Azure AD Identity Governance",
                    "D. Azure AD Conditional Access"
                ],
                "answer": "C",
                "explanation": "Azure AD Identity Governance incluye Access Reviews, que permite configurar revisiones periódicas de membresía de grupos, acceso a aplicaciones y asignaciones de roles. PIM es para gestión de roles privilegiados, Identity Protection para detección de riesgos, y Conditional Access para políticas de acceso condicional."
            },
            {
                "id": 10,
                "type": "single",
                "question": "Un usuario reporta que no puede crear máquinas virtuales en una suscripción. Tiene el rol Contributor en la suscripción. ¿Cuál es la causa más probable?",
                "options": [
                    "A. El usuario no tiene permisos suficientes",
                    "B. Existe una política de Azure que lo impide",
                    "C. Existe un bloqueo ReadOnly en la suscripción",
                    "D. B y C son posibles causas"
                ],
                "answer": "D",
                "explanation": "El rol Contributor tiene permisos para crear VMs. Si no puede hacerlo, puede ser debido a: 1) Una Azure Policy que restrinja la creación de VMs o ciertos SKUs, 2) Un bloqueo ReadOnly que previene cualquier modificación. Ambas son causas válidas que pueden bloquear la creación a pesar de tener el rol correcto."
            },
            {
                "id": 11,
                "type": "single",
                "question": "Necesita delegar la capacidad de crear y gestionar recursos en un grupo de recursos específico sin permitir acceso a otros grupos de recursos. ¿En qué ámbito debe asignar el rol?",
                "options": [
                    "A. Suscripción",
                    "B. Grupo de administración",
                    "C. Grupo de recursos",
                    "D. Recurso individual"
                ],
                "answer": "C",
                "explanation": "Los roles RBAC se heredan hacia abajo en la jerarquía. Para limitar el acceso a un grupo de recursos específico, debe asignar el rol en el ámbito del grupo de recursos. Asignar en suscripción o grupo de administración daría acceso a más recursos de los deseados."
            },
            {
                "id": 12,
                "type": "single",
                "question": "Su empresa tiene usuarios que necesitan acceso temporal a roles de administrador. Debe implementar una solución que requiera aprobación y justificación para activar estos roles. ¿Qué debe implementar?",
                "options": [
                    "A. Azure AD Conditional Access",
                    "B. Azure AD Privileged Identity Management (PIM)",
                    "C. Azure AD Identity Protection",
                    "D. Azure RBAC con roles personalizados"
                ],
                "answer": "B",
                "explanation": "Azure AD Privileged Identity Management (PIM) proporciona acceso privilegiado just-in-time, requiere aprobación y justificación para activar roles, y registra todas las activaciones. Es la solución diseñada específicamente para gestionar acceso privilegiado temporal."
            },
            {
                "id": 13,
                "type": "multiple",
                "question": "Está configurando Azure AD Connect para sincronizar usuarios on-premises con Azure AD. ¿Cuáles dos métodos de autenticación puede usar con Azure AD Connect? (Seleccione dos)",
                "options": [
                    "A. Password Hash Synchronization",
                    "B. Certificate-based authentication",
                    "C. Pass-through Authentication",
                    "D. RADIUS authentication"
                ],
                "answer": ["A", "C"],
                "explanation": "Azure AD Connect soporta tres métodos principales: Password Hash Synchronization (sincroniza hash de contraseñas a Azure AD), Pass-through Authentication (valida contraseñas contra AD on-premises en tiempo real), y Federation con AD FS. Certificate-based y RADIUS no son métodos de Azure AD Connect."
            },
            {
                "id": 14,
                "type": "single",
                "question": "Necesita asegurarse de que un usuario pueda ver los costos de todos los recursos en una suscripción pero no pueda realizar cambios. ¿Qué rol debe asignar?",
                "options": [
                    "A. Reader",
                    "B. Cost Management Reader",
                    "C. Billing Reader",
                    "D. Contributor"
                ],
                "answer": "B",
                "explanation": "Cost Management Reader permite ver configuraciones y datos de costos pero no realizar cambios. Reader permite ver recursos pero no específicamente datos de costos detallados. Billing Reader es para facturación a nivel de cuenta, no de suscripción. Contributor tiene permisos de modificación."
            },
            {
                "id": 15,
                "type": "single",
                "question": "Tiene múltiples suscripciones y necesita aplicar una configuración de gobernanza consistente incluyendo políticas, RBAC y Blueprints. ¿Cuál es la mejor solución?",
                "options": [
                    "A. Aplicar configuraciones individualmente en cada suscripción",
                    "B. Crear un grupo de administración y aplicar configuraciones allí",
                    "C. Usar Azure Automation para replicar configuraciones",
                    "D. Crear plantillas ARM para cada suscripción"
                ],
                "answer": "B",
                "explanation": "Los grupos de administración permiten organizar suscripciones y aplicar gobernanza de forma centralizada. Las políticas, RBAC y Blueprints aplicados a un grupo de administración se heredan a todas las suscripciones contenidas. Es la solución más eficiente y escalable para gobernanza multi-suscripción."
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
                "question": "Necesita almacenar datos que serán accedidos frecuentemente durante el primer mes y raramente después. Debe minimizar costos. ¿Qué tipo de acceso debe configurar inicialmente y qué característica debe habilitar?",
                "options": [
                    "A. Hot tier con lifecycle management",
                    "B. Cool tier con lifecycle management",
                    "C. Archive tier sin lifecycle management",
                    "D. Hot tier sin lifecycle management"
                ],
                "answer": "A",
                "explanation": "Hot tier es óptimo para datos accedidos frecuentemente. Lifecycle management puede mover automáticamente los datos a Cool o Archive tier después de un período definido, optimizando costos. Comenzar en Cool tendría costos de acceso mayores durante el primer mes."
            },
            {
                "id": 2,
                "type": "single",
                "question": "Su empresa requiere que los datos en una cuenta de almacenamiento estén disponibles incluso si toda una región de Azure falla. Los costos deben mantenerse lo más bajo posible. ¿Qué tipo de replicación debe elegir?",
                "options": [
                    "A. Locally Redundant Storage (LRS)",
                    "B. Zone-Redundant Storage (ZRS)",
                    "C. Geo-Redundant Storage (GRS)",
                    "D. Geo-Zone-Redundant Storage (GZRS)"
                ],
                "answer": "C",
                "explanation": "GRS replica datos a una región secundaria, proporcionando disponibilidad si toda una región falla. Es más económico que GZRS que también incluye redundancia de zona. LRS y ZRS no proporcionan redundancia geográfica."
            },
            {
                "id": 3,
                "type": "single",
                "question": "Necesita compartir archivos entre múltiples máquinas virtuales Windows en Azure. Los archivos deben ser accesibles usando el protocolo SMB. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Blob Storage",
                    "B. Azure File Storage",
                    "C. Azure Queue Storage",
                    "D. Azure Table Storage"
                ],
                "answer": "B",
                "explanation": "Azure File Storage proporciona file shares completamente administrados accesibles via protocolo SMB (Server Message Block). Es ideal para compartir archivos entre VMs y soporta montaje en Windows, Linux y macOS. Blob Storage es para objetos, Queue para mensajes, y Table para datos NoSQL."
            },
            {
                "id": 4,
                "type": "single",
                "question": "Tiene una cuenta de almacenamiento con blobs que contienen datos sensibles. Necesita asegurarse de que los datos estén cifrados con una clave que su empresa controla. ¿Qué debe configurar?",
                "options": [
                    "A. Storage Service Encryption con claves administradas por Microsoft",
                    "B. Storage Service Encryption con claves administradas por el cliente (CMK)",
                    "C. Azure Disk Encryption",
                    "D. Client-side encryption únicamente"
                ],
                "answer": "B",
                "explanation": "Customer-Managed Keys (CMK) permite usar sus propias claves almacenadas en Azure Key Vault para cifrar datos en reposo. Microsoft-managed keys no dan control sobre las claves. Azure Disk Encryption es para discos de VM, no para cuentas de almacenamiento."
            },
            {
                "id": 5,
                "type": "single",
                "question": "Necesita permitir acceso temporal a un blob específico a un usuario externo sin proporcionarle las claves de la cuenta de almacenamiento. ¿Qué debe usar?",
                "options": [
                    "A. Access Keys",
                    "B. Shared Access Signature (SAS)",
                    "C. Azure AD authentication",
                    "D. Anonymous public access"
                ],
                "answer": "B",
                "explanation": "Shared Access Signature (SAS) proporciona acceso delegado granular a recursos en una cuenta de almacenamiento. Puede especificar permisos, recursos específicos y tiempo de expiración. Access Keys dan acceso completo, Azure AD requiere que el usuario tenga una cuenta, y anonymous access no es seguro para datos sensibles."
            },
            {
                "id": 6,
                "type": "multiple",
                "question": "Está configurando una cuenta de almacenamiento para una aplicación web. Necesita que la aplicación pueda escribir logs y que usuarios externos puedan descargar archivos públicos. ¿Qué dos configuraciones debe realizar? (Seleccione dos)",
                "options": [
                    "A. Habilitar acceso público en el contenedor de archivos públicos",
                    "B. Configurar Static Website hosting",
                    "C. Asignar un rol RBAC a la identidad de la aplicación",
                    "D. Deshabilitar Secure transfer required"
                ],
                "answer": ["A", "C"],
                "explanation": "Para que la aplicación escriba logs, necesita permisos - un rol RBAC (como Storage Blob Data Contributor) para la identidad de la aplicación. Para archivos públicos descargables, el contenedor necesita acceso público (blob o container level). Static Website es para hosting de sitios estáticos, no para este escenario."
            },
            {
                "id": 7,
                "type": "single",
                "question": "Tiene datos en Azure Blob Storage que deben cumplir con requisitos legales de retención de 7 años. Los datos no deben poder ser eliminados ni modificados durante este período. ¿Qué debe configurar?",
                "options": [
                    "A. Soft delete con retención de 7 años",
                    "B. Immutable storage con time-based retention policy",
                    "C. Lifecycle management policy",
                    "D. Legal hold sin retention policy"
                ],
                "answer": "B",
                "explanation": "Immutable storage con time-based retention policy garantiza que los blobs no puedan ser modificados ni eliminados durante el período especificado (WORM - Write Once, Read Many). Cumple con regulaciones como SEC 17a-4. Soft delete permite recuperación pero no previene eliminación. Legal hold no tiene período definido."
            },
            {
                "id": 8,
                "type": "single",
                "question": "Necesita migrar 50 TB de datos desde un centro de datos on-premises a Azure Blob Storage. La conexión de red tiene ancho de banda limitado. ¿Cuál es la mejor solución?",
                "options": [
                    "A. AzCopy sobre Internet",
                    "B. Azure Data Box",
                    "C. Azure File Sync",
                    "D. Storage Explorer"
                ],
                "answer": "B",
                "explanation": "Azure Data Box es un dispositivo físico que Microsoft envía para transferir grandes cantidades de datos (hasta 80 TB por dispositivo) cuando el ancho de banda es limitado. Es más rápido y económico que transferir 50 TB por Internet. AzCopy y Storage Explorer usan la red, y File Sync es para sincronización continua, no migración masiva."
            },
            {
                "id": 9,
                "type": "single",
                "question": "Tiene una aplicación que necesita almacenar millones de mensajes pequeños para procesamiento asíncrono. Los mensajes deben procesarse en orden FIFO. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Blob Storage",
                    "B. Azure Queue Storage",
                    "C. Azure Service Bus Queue",
                    "D. Azure Table Storage"
                ],
                "answer": "C",
                "explanation": "Azure Service Bus Queue garantiza procesamiento FIFO (First-In-First-Out) con la opción de sesiones. Azure Queue Storage no garantiza estrictamente el orden FIFO. Service Bus también ofrece características empresariales como detección de duplicados y transacciones."
            },
            {
                "id": 10,
                "type": "single",
                "question": "Necesita sincronizar archivos entre un servidor de archivos Windows on-premises y Azure File Storage. Los usuarios deben poder acceder a los archivos más usados localmente mientras los menos usados se mantienen solo en la nube. ¿Qué debe implementar?",
                "options": [
                    "A. Azure Backup",
                    "B. Azure File Sync con cloud tiering",
                    "C. Robocopy scheduled task",
                    "D. Azure Data Box Gateway"
                ],
                "answer": "B",
                "explanation": "Azure File Sync permite sincronizar servidores Windows con Azure Files. Cloud tiering mantiene los archivos más accedidos localmente y convierte los menos usados en punteros que se descargan on-demand desde Azure. Optimiza el espacio local mientras mantiene acceso a todos los archivos."
            },
            {
                "id": 11,
                "type": "single",
                "question": "Una cuenta de almacenamiento tiene habilitado el firewall y solo permite acceso desde una red virtual específica. Una aplicación en otra VNet no puede acceder. ¿Qué debe configurar sin deshabilitar el firewall?",
                "options": [
                    "A. Service endpoint en la segunda VNet",
                    "B. Private endpoint en la segunda VNet",
                    "C. VNet peering únicamente",
                    "D. A o B son soluciones válidas"
                ],
                "answer": "D",
                "explanation": "Tanto Service Endpoints como Private Endpoints permiten acceso seguro a la cuenta de almacenamiento desde otras VNets. Service Endpoint requiere agregar la VNet al firewall de la cuenta de almacenamiento. Private Endpoint crea una IP privada en la VNet para la cuenta de almacenamiento. Ambos son válidos."
            },
            {
                "id": 12,
                "type": "single",
                "question": "Necesita copiar blobs de una cuenta de almacenamiento a otra en una región diferente. La copia debe ser asíncrona y manejada por Azure. ¿Qué método debe usar?",
                "options": [
                    "A. AzCopy sync",
                    "B. Start-AzStorageBlobCopy (Copy Blob API)",
                    "C. Azure Data Factory",
                    "D. Storage Explorer drag and drop"
                ],
                "answer": "B",
                "explanation": "La operación Copy Blob (Start-AzStorageBlobCopy en PowerShell) es asíncrona y manejada por Azure. El blob se copia en el servidor sin necesidad de descargar/subir datos a través del cliente. AzCopy sync es síncrono desde el cliente. Data Factory es válido pero más complejo para copias simples."
            },
            {
                "id": 13,
                "type": "single",
                "question": "Tiene blobs en el tier Archive y necesita acceder a uno de ellos urgentemente. ¿Qué debe hacer y cuánto tiempo tomará aproximadamente?",
                "options": [
                    "A. Acceder directamente, toma segundos",
                    "B. Rehidratar a Hot o Cool tier, toma hasta 15 horas con prioridad estándar",
                    "C. Rehidratar a Hot o Cool tier, toma hasta 1 hora con prioridad alta",
                    "D. B o C dependiendo de la prioridad seleccionada"
                ],
                "answer": "D",
                "explanation": "Los blobs en Archive tier deben ser rehidratados antes de poder accederse. Con prioridad estándar puede tomar hasta 15 horas, con prioridad alta (High Priority) puede completarse en menos de 1 hora para blobs menores a 10 GB. No se puede acceder directamente a datos archivados."
            },
            {
                "id": 14,
                "type": "single",
                "question": "Necesita crear una cuenta de almacenamiento que soporte Azure Data Lake Storage Gen2 para análisis de big data. ¿Qué debe habilitar durante la creación?",
                "options": [
                    "A. Large file shares",
                    "B. Hierarchical namespace",
                    "C. NFS 3.0",
                    "D. SFTP"
                ],
                "answer": "B",
                "explanation": "Hierarchical namespace es el requisito para habilitar Azure Data Lake Storage Gen2 en una cuenta de almacenamiento. Proporciona un sistema de archivos jerárquico sobre Blob Storage, necesario para operaciones eficientes de análisis de big data. Las otras opciones son características separadas."
            },
            {
                "id": 15,
                "type": "single",
                "question": "Una cuenta de almacenamiento tiene soft delete habilitado para blobs con retención de 14 días. Un usuario elimina accidentalmente un blob importante. ¿Cómo puede recuperarlo?",
                "options": [
                    "A. No es posible recuperarlo",
                    "B. Restaurar desde Azure Backup",
                    "C. Undelete el blob desde el portal o usando código",
                    "D. Contactar a Microsoft Support"
                ],
                "answer": "C",
                "explanation": "Con soft delete habilitado, los blobs eliminados se mantienen en estado 'soft deleted' durante el período de retención configurado. Pueden ser recuperados (undelete) desde el portal de Azure, PowerShell, CLI o código. El blob y sus snapshots se restauran completamente."
            }
        ]
    },
    "compute": {
        "name": "Desplegar y Administrar Recursos de Cómputo",
        "percentage": "20-25%",
        "questions": [
            {
                "id": 1,
                "type": "single",
                "question": "Necesita desplegar una máquina virtual que ejecutará una aplicación crítica. Debe asegurarse de que la VM tenga un SLA de 99.99%. ¿Qué debe configurar?",
                "options": [
                    "A. Desplegar la VM en un Availability Set",
                    "B. Desplegar la VM en diferentes Availability Zones",
                    "C. Desplegar múltiples VMs en un Availability Set",
                    "D. Desplegar múltiples VMs en diferentes Availability Zones"
                ],
                "answer": "D",
                "explanation": "Para lograr un SLA de 99.99%, necesita desplegar múltiples VMs en diferentes Availability Zones. Availability Zones son ubicaciones físicas separadas dentro de una región con energía, red y refrigeración independientes. Una sola VM o Availability Set proporciona SLAs menores."
            },
            {
                "id": 2,
                "type": "single",
                "question": "Tiene una VM de Azure que necesita ser redimensionada a un tamaño diferente. La VM está actualmente en ejecución. ¿Qué sucederá cuando cambie el tamaño?",
                "options": [
                    "A. La VM se redimensionará sin interrupción",
                    "B. La VM se reiniciará",
                    "C. La VM se detendrá permanentemente",
                    "D. Se creará una nueva VM con los datos"
                ],
                "answer": "B",
                "explanation": "Cuando redimensiona una VM en ejecución, Azure la reiniciará para aplicar el nuevo tamaño. Si el nuevo tamaño no está disponible en el cluster actual, la VM debe ser desasignada primero. Siempre planifique una ventana de mantenimiento para redimensionamiento."
            },
            {
                "id": 3,
                "type": "single",
                "question": "Necesita ejecutar scripts de configuración automáticamente después de que una VM sea desplegada. ¿Qué característica debe usar?",
                "options": [
                    "A. Boot diagnostics",
                    "B. Custom Script Extension",
                    "C. Run Command",
                    "D. Serial Console"
                ],
                "answer": "B",
                "explanation": "Custom Script Extension permite ejecutar scripts automáticamente como parte del despliegue de la VM o después. Los scripts pueden descargarse desde Azure Storage o GitHub. Run Command es para ejecución ad-hoc, Boot diagnostics es para diagnóstico de arranque, y Serial Console es para acceso de consola."
            },
            {
                "id": 4,
                "type": "single",
                "question": "Tiene un Azure App Service Plan en el tier Standard. Necesita configurar auto-scaling para manejar picos de tráfico. ¿Qué tipo de scaling puede configurar?",
                "options": [
                    "A. Solo scale up (vertical)",
                    "B. Solo scale out (horizontal)",
                    "C. Scale up y scale out",
                    "D. Ninguno, Standard no soporta scaling"
                ],
                "answer": "C",
                "explanation": "App Service Plan Standard y superiores soportan tanto scale up (cambiar a un tier mayor) como scale out (agregar más instancias). Scale out puede ser manual, basado en métricas o programado. Scale up requiere cambio manual del tier."
            },
            {
                "id": 5,
                "type": "single",
                "question": "Necesita desplegar contenedores Docker en Azure sin gestionar infraestructura de servidores. Las cargas de trabajo son de corta duración y basadas en eventos. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Virtual Machines con Docker",
                    "B. Azure Kubernetes Service (AKS)",
                    "C. Azure Container Instances (ACI)",
                    "D. Azure App Service for Containers"
                ],
                "answer": "C",
                "explanation": "Azure Container Instances es un servicio serverless para ejecutar contenedores sin gestionar servidores. Es ideal para cargas de trabajo de corta duración, procesamiento batch y escenarios basados en eventos. AKS es para orquestación compleja, y VMs/App Service requieren más gestión."
            },
            {
                "id": 6,
                "type": "multiple",
                "question": "Está creando un Virtual Machine Scale Set (VMSS) para una aplicación web. ¿Qué dos configuraciones debe establecer para habilitar auto-scaling basado en métricas? (Seleccione dos)",
                "options": [
                    "A. Definir reglas de scale out basadas en CPU",
                    "B. Configurar un Load Balancer",
                    "C. Definir reglas de scale in para reducir costos",
                    "D. Habilitar Accelerated Networking"
                ],
                "answer": ["A", "C"],
                "explanation": "Para auto-scaling efectivo basado en métricas necesita reglas de scale out (aumentar instancias cuando la demanda sube) y scale in (reducir instancias cuando la demanda baja). Load Balancer es recomendado pero no requerido para auto-scaling. Accelerated Networking es para rendimiento de red."
            },
            {
                "id": 7,
                "type": "single",
                "question": "Una VM de Azure no arranca correctamente después de un cambio de configuración. Necesita acceder a la VM para diagnosticar el problema sin usar RDP/SSH. ¿Qué debe usar?",
                "options": [
                    "A. Azure Bastion",
                    "B. Serial Console",
                    "C. Run Command",
                    "D. Boot diagnostics screenshot"
                ],
                "answer": "B",
                "explanation": "Serial Console proporciona acceso de consola de texto a la VM, útil cuando RDP/SSH no funcionan debido a problemas de configuración de red o sistema operativo. Permite interactuar con el bootloader y el sistema operativo directamente. Boot diagnostics solo muestra screenshots, Run Command requiere que la VM responda."
            },
            {
                "id": 8,
                "type": "single",
                "question": "Necesita desplegar una aplicación .NET en Azure App Service. La aplicación requiere .NET 6 y debe poder escalar automáticamente. ¿Qué tier mínimo del App Service Plan necesita?",
                "options": [
                    "A. Free (F1)",
                    "B. Basic (B1)",
                    "C. Standard (S1)",
                    "D. Premium (P1v2)"
                ],
                "answer": "C",
                "explanation": "El tier Standard (S1) es el mínimo que soporta auto-scaling en App Service. Free y Shared no soportan scaling. Basic soporta scale up manual y hasta 3 instancias pero no auto-scaling basado en métricas. Standard agrega auto-scaling, staging slots y backups diarios."
            },
            {
                "id": 9,
                "type": "single",
                "question": "Tiene una VM con un disco OS y necesita expandir el disco de 128 GB a 256 GB. ¿Qué pasos debe seguir?",
                "options": [
                    "A. Expandir el disco desde el portal mientras la VM está en ejecución",
                    "B. Detener (deallocate) la VM, expandir el disco, iniciar la VM, extender la partición en el OS",
                    "C. Crear un nuevo disco de 256 GB y copiar los datos",
                    "D. No es posible expandir el disco OS"
                ],
                "answer": "B",
                "explanation": "Para expandir un disco OS managed: 1) Deallocate la VM, 2) Expandir el disco en Azure, 3) Iniciar la VM, 4) Dentro del OS, extender la partición/volumen para usar el espacio adicional. El disco no puede expandirse con la VM en ejecución para discos OS."
            },
            {
                "id": 10,
                "type": "single",
                "question": "Necesita desplegar un cluster de Kubernetes administrado en Azure. ¿Qué servicio debe usar y qué componente gestiona Azure automáticamente?",
                "options": [
                    "A. AKS, Azure gestiona los worker nodes",
                    "B. AKS, Azure gestiona el control plane",
                    "C. Azure Container Instances, Azure gestiona todo",
                    "D. Azure Container Apps, Azure gestiona el runtime"
                ],
                "answer": "B",
                "explanation": "Azure Kubernetes Service (AKS) es el servicio de Kubernetes administrado. Azure gestiona automáticamente el control plane (API server, etcd, scheduler, etc.) sin costo adicional. Los worker nodes son gestionados por el usuario pero pueden usar node pools con auto-scaling."
            },
            {
                "id": 11,
                "type": "single",
                "question": "Tiene una aplicación web en App Service que necesita acceder a secretos almacenados en Azure Key Vault. ¿Cuál es la forma más segura de autenticar la aplicación?",
                "options": [
                    "A. Almacenar la connection string de Key Vault en App Settings",
                    "B. Usar un Service Principal con secreto almacenado en App Settings",
                    "C. Habilitar System-Assigned Managed Identity",
                    "D. Usar las claves de acceso de Key Vault"
                ],
                "answer": "C",
                "explanation": "System-Assigned Managed Identity es la forma más segura porque Azure gestiona automáticamente las credenciales, no hay secretos que almacenar o rotar, y la identidad está vinculada al ciclo de vida del App Service. Las otras opciones requieren gestión manual de secretos."
            },
            {
                "id": 12,
                "type": "single",
                "question": "Necesita crear una imagen personalizada de una VM para usarla como plantilla para nuevas VMs. La imagen debe incluir el OS y las aplicaciones instaladas. ¿Qué debe hacer?",
                "options": [
                    "A. Crear un snapshot del disco OS",
                    "B. Sysprep/deprovision la VM y capturar como imagen generalizada",
                    "C. Exportar la VM a un VHD",
                    "D. Copiar el disco a otra cuenta de almacenamiento"
                ],
                "answer": "B",
                "explanation": "Para crear una imagen reutilizable: 1) Ejecutar Sysprep (Windows) o waagent -deprovision (Linux) para generalizar la VM, 2) Deallocate la VM, 3) Marcarla como generalizada, 4) Capturar como imagen. Las imágenes generalizadas pueden usarse para crear múltiples VMs con identidades únicas."
            },
            {
                "id": 13,
                "type": "single",
                "question": "Una VM de Azure tiene alta latencia de disco. Actualmente usa Standard HDD. ¿Qué tipo de disco proporcionará mejor rendimiento para cargas de trabajo intensivas en IOPS?",
                "options": [
                    "A. Standard SSD",
                    "B. Premium SSD",
                    "C. Ultra Disk",
                    "D. B o C dependiendo de los requisitos"
                ],
                "answer": "D",
                "explanation": "Premium SSD ofrece mejor rendimiento que Standard para la mayoría de cargas de trabajo. Ultra Disk proporciona el mejor rendimiento con IOPS y throughput configurables independientemente, ideal para cargas de trabajo muy intensivas (bases de datos, SAP HANA). La elección depende de los requisitos específicos de IOPS y latencia."
            },
            {
                "id": 14,
                "type": "single",
                "question": "Tiene un App Service con deployment slots (production y staging). Necesita intercambiar el contenido de staging a production sin tiempo de inactividad. ¿Qué operación debe realizar?",
                "options": [
                    "A. Copiar los archivos de staging a production",
                    "B. Realizar un Swap de slots",
                    "C. Redirigir el tráfico manualmente",
                    "D. Crear un nuevo App Service"
                ],
                "answer": "B",
                "explanation": "Swap de slots intercambia las configuraciones y contenido entre slots instantáneamente. Incluye warm-up automático del slot de destino antes del swap para evitar cold start. Es la forma estándar de implementar deployments blue-green en App Service sin tiempo de inactividad."
            },
            {
                "id": 15,
                "type": "single",
                "question": "Necesita reducir costos de VMs que solo se usan durante horario laboral (8am-6pm). ¿Qué solución debe implementar?",
                "options": [
                    "A. Cambiar a VMs más pequeñas",
                    "B. Usar Reserved Instances",
                    "C. Configurar Azure Automation para start/stop programado",
                    "D. Mover las VMs a otra región"
                ],
                "answer": "C",
                "explanation": "Azure Automation con runbooks permite programar el inicio y detención de VMs. Las VMs detenidas (deallocated) no incurren costos de cómputo, solo almacenamiento. Para VMs usadas solo 10 horas al día, esto puede reducir costos significativamente. Reserved Instances son para uso continuo."
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
                "question": "Tiene dos VNets en la misma región que necesitan comunicarse directamente. El tráfico no debe pasar por Internet. ¿Qué debe configurar?",
                "options": [
                    "A. VPN Gateway",
                    "B. VNet Peering",
                    "C. ExpressRoute",
                    "D. NAT Gateway"
                ],
                "answer": "B",
                "explanation": "VNet Peering conecta dos VNets directamente a través del backbone de Microsoft Azure. El tráfico es privado, de baja latencia y no pasa por Internet. VPN Gateway es para conexiones cifradas sobre Internet o entre sitios, ExpressRoute es para conexiones privadas a on-premises, NAT Gateway es para tráfico saliente a Internet."
            },
            {
                "id": 2,
                "type": "single",
                "question": "Necesita asegurarse de que solo el tráfico HTTPS (puerto 443) pueda llegar a una subnet que contiene servidores web. ¿Qué debe configurar?",
                "options": [
                    "A. Azure Firewall",
                    "B. Network Security Group (NSG)",
                    "C. Application Gateway",
                    "D. Route Table"
                ],
                "answer": "B",
                "explanation": "Network Security Group (NSG) filtra tráfico de red hacia y desde recursos de Azure. Puede crear reglas para permitir/denegar tráfico basado en puerto, protocolo, origen y destino. Para este caso simple, un NSG con regla permitiendo solo puerto 443 entrante es suficiente y más económico que Azure Firewall."
            },
            {
                "id": 3,
                "type": "single",
                "question": "Una VM en una subnet privada necesita acceder a Internet para descargar actualizaciones, pero no debe ser accesible desde Internet. ¿Qué debe configurar?",
                "options": [
                    "A. Asignar una IP pública a la VM",
                    "B. Configurar un NAT Gateway en la subnet",
                    "C. Crear un VPN Gateway",
                    "D. Configurar VNet peering con otra VNet"
                ],
                "answer": "B",
                "explanation": "NAT Gateway permite que recursos en una subnet privada accedan a Internet para tráfico saliente sin exponer una IP pública. Todo el tráfico saliente usa la IP del NAT Gateway. Las conexiones entrantes desde Internet no son posibles, cumpliendo el requisito de seguridad."
            },
            {
                "id": 4,
                "type": "single",
                "question": "Tiene una aplicación web que necesita balanceo de carga con terminación SSL y enrutamiento basado en URL. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Load Balancer",
                    "B. Azure Application Gateway",
                    "C. Azure Traffic Manager",
                    "D. Azure Front Door"
                ],
                "answer": "B",
                "explanation": "Application Gateway es un load balancer de capa 7 (aplicación) que soporta terminación SSL, enrutamiento basado en URL/host, y WAF. Load Balancer es capa 4 sin estas características. Traffic Manager es DNS-based para enrutamiento global. Front Door es similar a App Gateway pero para escenarios globales."
            },
            {
                "id": 5,
                "type": "multiple",
                "question": "Está configurando una conexión Site-to-Site VPN entre su red on-premises y Azure. ¿Qué dos componentes necesita en Azure? (Seleccione dos)",
                "options": [
                    "A. Virtual Network Gateway",
                    "B. Local Network Gateway",
                    "C. ExpressRoute Circuit",
                    "D. Application Gateway"
                ],
                "answer": ["A", "B"],
                "explanation": "Para Site-to-Site VPN necesita: 1) Virtual Network Gateway (VPN Gateway) - el endpoint de VPN en Azure, 2) Local Network Gateway - representa su dispositivo VPN on-premises, incluyendo su IP pública y rangos de direcciones. ExpressRoute es una tecnología diferente, y Application Gateway es para HTTP load balancing."
            },
            {
                "id": 6,
                "type": "single",
                "question": "Necesita que el tráfico de una subnet pase por un Network Virtual Appliance (firewall VM) antes de llegar a Internet. ¿Qué debe configurar?",
                "options": [
                    "A. NSG con regla de denegación",
                    "B. User Defined Route (UDR) con next hop al NVA",
                    "C. VNet peering",
                    "D. Service endpoint"
                ],
                "answer": "B",
                "explanation": "User Defined Routes (UDR) permiten personalizar el enrutamiento de tráfico en Azure. Para dirigir tráfico a través de un NVA, cree una route table con una ruta que tenga next hop type 'Virtual Appliance' apuntando a la IP del NVA, y asóciela a la subnet origen."
            },
            {
                "id": 7,
                "type": "single",
                "question": "Tiene una aplicación en una VM que necesita acceder a Azure SQL Database de forma privada, sin usar endpoints públicos. ¿Qué debe configurar?",
                "options": [
                    "A. Service Endpoint para Microsoft.Sql",
                    "B. Private Endpoint para Azure SQL",
                    "C. VNet peering",
                    "D. ExpressRoute"
                ],
                "answer": "B",
                "explanation": "Private Endpoint crea una interfaz de red privada en su VNet para el servicio de Azure (SQL Database), con una IP privada. El tráfico va completamente por la red privada. Service Endpoint también es privado pero el servicio mantiene su IP pública; Private Endpoint proporciona mayor aislamiento."
            },
            {
                "id": 8,
                "type": "single",
                "question": "Necesita implementar resolución de nombres DNS privada entre recursos en múltiples VNets. ¿Qué debe usar?",
                "options": [
                    "A. Azure DNS public zone",
                    "B. Azure Private DNS zone con VNet links",
                    "C. DNS servers personalizados en cada VNet",
                    "D. Archivo hosts en cada VM"
                ],
                "answer": "B",
                "explanation": "Azure Private DNS zones proporcionan resolución DNS dentro y entre VNets. Vincule la zona privada a las VNets que necesitan resolver los nombres. Es una solución administrada que no requiere servidores DNS personalizados y soporta registro automático de VMs."
            },
            {
                "id": 9,
                "type": "single",
                "question": "Tiene VMs en una VNet que necesitan acceder a un servicio on-premises con latencia muy baja y ancho de banda garantizado. La conexión no debe pasar por Internet público. ¿Qué debe implementar?",
                "options": [
                    "A. Site-to-Site VPN",
                    "B. Point-to-Site VPN",
                    "C. ExpressRoute",
                    "D. VNet Peering"
                ],
                "answer": "C",
                "explanation": "ExpressRoute proporciona conexión privada dedicada entre on-premises y Azure a través de un proveedor de conectividad. Ofrece menor latencia, mayor ancho de banda y más confiabilidad que VPN sobre Internet. Es ideal para cargas de trabajo que requieren rendimiento consistente."
            },
            {
                "id": 10,
                "type": "single",
                "question": "Un NSG tiene las siguientes reglas entrantes:\n- Priority 100: Allow TCP 443 from Any\n- Priority 200: Deny All from Any\n- Priority 65000: Allow VNet to VNet (default)\n\n¿Qué tráfico será permitido?",
                "options": [
                    "A. Solo TCP 443",
                    "B. TCP 443 y tráfico VNet a VNet",
                    "C. Todo el tráfico",
                    "D. Ningún tráfico"
                ],
                "answer": "A",
                "explanation": "Las reglas NSG se evalúan por prioridad (menor número = mayor prioridad). TCP 443 es permitido (priority 100). Todo otro tráfico es denegado (priority 200) antes de que se evalúe la regla default de VNet (priority 65000). La regla Deny All bloquea efectivamente el tráfico VNet-to-VNet."
            },
            {
                "id": 11,
                "type": "single",
                "question": "Necesita balancear carga de tráfico TCP/UDP entre múltiples VMs para alta disponibilidad. El balanceador debe estar dentro de la VNet. ¿Qué debe usar?",
                "options": [
                    "A. Azure Load Balancer (Internal/Private)",
                    "B. Azure Load Balancer (Public)",
                    "C. Application Gateway",
                    "D. Traffic Manager"
                ],
                "answer": "A",
                "explanation": "Internal (Private) Load Balancer distribuye tráfico dentro de una VNet usando una IP privada. Es ideal para balancear carga de tráfico interno entre tiers de aplicación. Public Load Balancer usa IP pública para tráfico de Internet. Application Gateway es capa 7, Traffic Manager es DNS-based."
            },
            {
                "id": 12,
                "type": "single",
                "question": "Tiene dos VNets con peering configurado. VNet1 tiene una VM y VNet2 tiene un VPN Gateway conectado a on-premises. Necesita que la VM en VNet1 acceda a recursos on-premises a través del gateway en VNet2. ¿Qué configuración adicional necesita?",
                "options": [
                    "A. Configurar VPN adicional en VNet1",
                    "B. Habilitar 'Use Remote Gateway' en VNet1 y 'Allow Gateway Transit' en VNet2",
                    "C. Crear otro peering",
                    "D. No se necesita configuración adicional"
                ],
                "answer": "B",
                "explanation": "Gateway Transit permite que una VNet use el VPN/ExpressRoute gateway de otra VNet peered. En el peering de VNet2 (que tiene el gateway), habilite 'Allow Gateway Transit'. En el peering de VNet1, habilite 'Use Remote Gateway'. Esto evita desplegar gateways redundantes."
            },
            {
                "id": 13,
                "type": "single",
                "question": "Necesita conectar usuarios remotos a recursos en una VNet de Azure desde sus laptops. Los usuarios están en diferentes ubicaciones. ¿Qué tipo de conexión debe configurar?",
                "options": [
                    "A. Site-to-Site VPN",
                    "B. Point-to-Site VPN",
                    "C. ExpressRoute",
                    "D. VNet Peering"
                ],
                "answer": "B",
                "explanation": "Point-to-Site (P2S) VPN permite que clientes individuales se conecten a una VNet de Azure desde cualquier ubicación. Es ideal para trabajadores remotos o escenarios donde no hay un dispositivo VPN dedicado. Site-to-Site es para conexiones entre redes completas."
            },
            {
                "id": 14,
                "type": "single",
                "question": "Está diseñando la arquitectura de red para una aplicación de 3 tiers (web, app, db). ¿Cuál es la mejor práctica para segmentación?",
                "options": [
                    "A. Una subnet para todos los tiers",
                    "B. Una subnet por tier con NSGs",
                    "C. Una VNet por tier",
                    "D. VMs en diferentes regiones"
                ],
                "answer": "B",
                "explanation": "Best practice es usar subnets separadas para cada tier (web, app, database) con NSGs para controlar el tráfico entre ellos. Esto proporciona segmentación de seguridad mientras mantiene baja latencia dentro de la misma VNet. Una VNet por tier añadiría complejidad innecesaria."
            },
            {
                "id": 15,
                "type": "single",
                "question": "Necesita proteger aplicaciones web contra ataques comunes como SQL injection y XSS. ¿Qué debe implementar?",
                "options": [
                    "A. NSG con reglas personalizadas",
                    "B. Azure Firewall",
                    "C. Web Application Firewall (WAF)",
                    "D. DDoS Protection Standard"
                ],
                "answer": "C",
                "explanation": "Web Application Firewall (WAF) protege aplicaciones web contra vulnerabilidades comunes como SQL injection, XSS, y otras amenazas OWASP Top 10. Se puede implementar con Application Gateway o Front Door. NSG es capa 3/4, Azure Firewall es capa 3-7 pero no específico para web, DDoS es para ataques volumétricos."
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
                "question": "Necesita recibir una notificación por email cuando el uso de CPU de una VM supere el 80% durante 5 minutos. ¿Qué debe configurar?",
                "options": [
                    "A. Activity Log alert",
                    "B. Metric alert con Action Group",
                    "C. Log Analytics query",
                    "D. Azure Advisor recommendation"
                ],
                "answer": "B",
                "explanation": "Metric alerts monitorean métricas de recursos (CPU, memoria, etc.) y pueden disparar acciones cuando se cumplen condiciones. Action Groups definen las acciones a tomar (email, SMS, webhook, etc.). Activity Log alerts son para eventos de administración, no métricas de rendimiento."
            },
            {
                "id": 2,
                "type": "single",
                "question": "Necesita analizar logs de múltiples VMs para encontrar patrones de errores. Los logs deben ser consultables usando un lenguaje de queries. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Monitor Metrics",
                    "B. Log Analytics workspace",
                    "C. Storage Account logs",
                    "D. Event Hubs"
                ],
                "answer": "B",
                "explanation": "Log Analytics workspace almacena y permite consultar logs usando Kusto Query Language (KQL). Puede centralizar logs de múltiples recursos, crear dashboards y configurar alertas basadas en queries. Azure Monitor Metrics es para datos numéricos de series de tiempo, no logs detallados."
            },
            {
                "id": 3,
                "type": "single",
                "question": "Tiene una VM crítica que necesita backups diarios con retención de 30 días. Los backups deben poder restaurar archivos individuales. ¿Qué debe configurar?",
                "options": [
                    "A. Azure Site Recovery",
                    "B. Azure Backup con Recovery Services vault",
                    "C. Snapshots manuales del disco",
                    "D. Copiar VHDs a otra cuenta de almacenamiento"
                ],
                "answer": "B",
                "explanation": "Azure Backup con Recovery Services vault proporciona backups programados, retención configurable, y permite restauración tanto de VM completa como de archivos individuales (File Recovery). Site Recovery es para disaster recovery, snapshots son manuales y no tienen retención automática."
            },
            {
                "id": 4,
                "type": "single",
                "question": "Necesita identificar recursos de Azure que no están siguiendo las mejores prácticas de seguridad, rendimiento y costos. ¿Qué herramienta debe usar?",
                "options": [
                    "A. Azure Monitor",
                    "B. Azure Advisor",
                    "C. Azure Security Center",
                    "D. Azure Cost Management"
                ],
                "answer": "B",
                "explanation": "Azure Advisor analiza sus recursos y proporciona recomendaciones personalizadas en 5 categorías: Confiabilidad, Seguridad, Rendimiento, Costo y Excelencia Operacional. Security Center se enfoca solo en seguridad, Cost Management en costos, y Monitor en métricas/logs."
            },
            {
                "id": 5,
                "type": "multiple",
                "question": "Está configurando Azure Backup para VMs. ¿Cuáles dos afirmaciones son correctas? (Seleccione dos)",
                "options": [
                    "A. Se requiere un Recovery Services vault en la misma región que las VMs",
                    "B. Se puede hacer backup de VMs en cualquier región desde un único vault",
                    "C. Azure Backup puede proteger VMs con discos managed y unmanaged",
                    "D. Los backups de VM solo funcionan con VMs Windows"
                ],
                "answer": ["A", "C"],
                "explanation": "Recovery Services vault debe estar en la misma región que las VMs que protege (o en una región emparejada para ciertos escenarios). Azure Backup soporta tanto discos managed como unmanaged, y funciona con VMs Windows y Linux."
            },
            {
                "id": 6,
                "type": "single",
                "question": "Necesita ver quién creó o eliminó recursos en una suscripción durante los últimos 90 días. ¿Dónde debe buscar esta información?",
                "options": [
                    "A. Azure Monitor Metrics",
                    "B. Activity Log",
                    "C. Resource health",
                    "D. Azure Advisor"
                ],
                "answer": "B",
                "explanation": "Activity Log registra operaciones de administración (plano de control) realizadas en recursos: quién hizo qué, cuándo y desde dónde. Incluye creación, modificación y eliminación de recursos. Se retiene por 90 días por defecto. Puede exportarse a Log Analytics para retención más larga."
            },
            {
                "id": 7,
                "type": "single",
                "question": "Una aplicación web en App Service está experimentando errores 500 intermitentes. Necesita correlacionar errores con requests específicos y ver el stack trace. ¿Qué debe habilitar?",
                "options": [
                    "A. Diagnostic settings",
                    "B. Application Insights",
                    "C. Azure Monitor logs",
                    "D. Activity Log"
                ],
                "answer": "B",
                "explanation": "Application Insights es una herramienta de Application Performance Management (APM) que proporciona telemetría detallada de aplicaciones: requests, excepciones con stack traces, dependencias, métricas personalizadas y correlación de extremo a extremo. Es ideal para diagnóstico de aplicaciones web."
            },
            {
                "id": 8,
                "type": "single",
                "question": "Necesita implementar disaster recovery para VMs críticas con RPO de 15 minutos y RTO de 1 hora. ¿Qué servicio debe usar?",
                "options": [
                    "A. Azure Backup",
                    "B. Azure Site Recovery",
                    "C. Availability Zones",
                    "D. VM Scale Sets"
                ],
                "answer": "B",
                "explanation": "Azure Site Recovery (ASR) proporciona replicación continua de VMs a una región secundaria con RPO de segundos a minutos. Permite failover rápido cumpliendo RTO de 1 hora. Azure Backup tiene RPO de horas (frecuencia de backup) y RTO más largo. Availability Zones son para alta disponibilidad regional, no DR."
            },
            {
                "id": 9,
                "type": "single",
                "question": "Tiene múltiples suscripciones y necesita una vista consolidada de costos con la capacidad de crear presupuestos y alertas. ¿Qué debe usar?",
                "options": [
                    "A. Azure Pricing Calculator",
                    "B. Azure Cost Management + Billing",
                    "C. Azure Advisor",
                    "D. Azure Monitor"
                ],
                "answer": "B",
                "explanation": "Azure Cost Management + Billing proporciona análisis de costos, presupuestos, alertas de costo, y recomendaciones de ahorro. Soporta múltiples suscripciones y puede agrupar costos por tags, grupos de recursos, etc. Pricing Calculator es para estimar costos futuros, no analizar gastos actuales."
            },
            {
                "id": 10,
                "type": "single",
                "question": "Necesita configurar una VM para enviar sus logs de eventos de Windows a un Log Analytics workspace. ¿Qué debe instalar en la VM?",
                "options": [
                    "A. Azure Diagnostics extension",
                    "B. Log Analytics agent (MMA) o Azure Monitor Agent",
                    "C. Application Insights SDK",
                    "D. Custom Script Extension"
                ],
                "answer": "B",
                "explanation": "Log Analytics agent (Microsoft Monitoring Agent) o el nuevo Azure Monitor Agent recopila logs y métricas de VMs y los envía a Log Analytics workspace. Azure Diagnostics extension envía datos a Storage Account. Application Insights es para aplicaciones, no logs del sistema operativo."
            },
            {
                "id": 11,
                "type": "single",
                "question": "Una VM de Azure muestra estado 'Unavailable' en Resource Health. ¿Qué indica esto?",
                "options": [
                    "A. La VM está apagada por el usuario",
                    "B. Azure detectó un problema que afecta la VM",
                    "C. La VM necesita actualizaciones",
                    "D. El agente de la VM no está respondiendo"
                ],
                "answer": "B",
                "explanation": "Resource Health muestra el estado actual e histórico de recursos. 'Unavailable' indica que Azure detectó un problema de plataforma que afecta al recurso (no causado por el usuario). Proporciona información sobre la causa y acciones recomendadas. VMs apagadas por usuario muestran estado diferente."
            },
            {
                "id": 12,
                "type": "single",
                "question": "Necesita crear un dashboard personalizado que muestre métricas de múltiples recursos de Azure en una sola vista. ¿Qué debe usar?",
                "options": [
                    "A. Azure Monitor Workbooks",
                    "B. Log Analytics queries",
                    "C. Azure Portal Dashboard",
                    "D. Todas las anteriores son opciones válidas"
                ],
                "answer": "D",
                "explanation": "Todas son opciones válidas para visualización: Azure Portal Dashboard permite crear dashboards arrastrando tiles de métricas. Workbooks proporciona reportes interactivos más complejos. Log Analytics permite crear queries y fijarlas a dashboards. La elección depende de la complejidad y requisitos."
            },
            {
                "id": 13,
                "type": "single",
                "question": "Necesita retener Activity Logs por más de 90 días para cumplimiento. ¿Qué debe configurar?",
                "options": [
                    "A. Cambiar la configuración de retención en Activity Log",
                    "B. Exportar Activity Log a Log Analytics workspace o Storage Account",
                    "C. No es posible retener más de 90 días",
                    "D. Crear alertas para guardar los logs importantes"
                ],
                "answer": "B",
                "explanation": "Activity Log tiene retención fija de 90 días que no puede cambiarse. Para retención más larga, configure Diagnostic Settings para exportar a Log Analytics workspace (hasta 2 años o más) o Storage Account (retención ilimitada). También puede exportar a Event Hubs para streaming externo."
            },
            {
                "id": 14,
                "type": "single",
                "question": "Una política de backup tiene configurada retención diaria de 30 días, semanal de 12 semanas, mensual de 12 meses. ¿Cuántos puntos de recuperación se mantendrán aproximadamente?",
                "options": [
                    "A. 30 puntos",
                    "B. 54 puntos (30 + 12 + 12)",
                    "C. Depende de los días/semanas/meses específicos configurados",
                    "D. 30 diarios + 12 semanales + 12 mensuales sin superposición"
                ],
                "answer": "C",
                "explanation": "El número exacto de puntos de recuperación depende de qué días/semanas/meses se seleccionan para retención. Azure Backup mantiene el punto más reciente para cada período. Puede haber superposición (un backup diario puede ser también el semanal y mensual). La UI muestra el cálculo exacto."
            },
            {
                "id": 15,
                "type": "single",
                "question": "Necesita ser notificado cuando Azure planea realizar mantenimiento en sus VMs. ¿Qué debe configurar?",
                "options": [
                    "A. Activity Log alert para eventos de mantenimiento",
                    "B. Service Health alerts",
                    "C. Metric alert para disponibilidad",
                    "D. Azure Advisor notifications"
                ],
                "answer": "B",
                "explanation": "Service Health proporciona información personalizada sobre eventos de Azure que afectan sus recursos: interrupciones, mantenimiento planificado y advisories. Configure alertas de Service Health para recibir notificaciones proactivas sobre mantenimiento planificado que afectará sus VMs específicas."
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
