
import os
import time
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

console = Console()

# ==========================================
# ESTADO GLOBAL Y VARIABLES DEL SISTEMA
# ==========================================
usuario = ""
password = ""
modo_actual = "ANTIMEMETIC"
estado_alerta_global = "VERDE"
estabilidad_cognitiva = 100
humes_moneda = 50

alias_contacto = "Dra. Aurora Adarmellina"
emisor_actual_chat = "YO"

tamagotchi_state = {"energia": 80, "memoria": 75, "felicidad": 60}
sujeto_actual = None

# ==========================================
# BASES DE DATOS Y LORE SITIO-312
# ==========================================
BANNER = """
=====================================================
[ FUNDACIÓN SCP - SITIO 312: ARCHIPIÉLAGO OMEGA ]
[ TERMINAL DE CONTROL Y BÚSQUEDA TÁCTICA v4.09 ]
=====================================================
ADVERTENCIA: Acceso no autorizado sancionado con
administración forzada de Amnésicos Clase-A.
"""

CHISTES_GLASS = [
    "Dr. Simon Glass: '¿Qué le dice un científico de la Fundación a un SCP fuera de contención? ...Nada, corre.'",
    "Dr. Simon Glass: 'Le pregunté al Dr. Bright si tenía estrés. Me dijo que no, que se lo traspasa a sus huéspedes.'",
    "Dr. Simon Glass: 'Evaluación psicológica del día: Si el SCP-173 te parpadea de vuelta... estás alucinando, toma un descanso.'"
]

NOTAS_MEDICAS = [
    "ÁREA MÉDICA SITIO-312: Recomendación del Director Médico: Para estrés memético ligero, migrañas o fatiga de turno, tomar 500mg de Paracetamol y reportar a enfermería.",
    "AVISO MÉDICO: Ante cualquier mareo o pensamiento recurrente no propio, tomar Paracetamol y someterse a escáner de Nivel 2.",
    "DIRECTOR MÉDICO: Si escucha voces que no provienen del radio, tome Paracetamol y permanezca en su estación."
]

MENSAJES_O5 = [
    "O5-█: 'Sabemos cuántas veces has pestañeado frente a la pantalla en la última hora, {U}. Vuelve al trabajo.'",
    "CONSEJO O5: 'No mires por la ventana del sector. Lo que está flotando en el agua no forma parte del paisaje.'",
    "TRANSMISIÓN SUB-OCULTA O5: 'El consenso de la realidad depende de que no hagas preguntas innecesarias.'"
]

DIALOGOS_AURORA = [
    "Busco al administrador de sitio... ¿De casualidad sabes por qué pabellón anda?",
    "¿Cómo te sientes hoy, {U}? Te notas algo fatigado en el monitor.",
    "Deberías pasar por mi oficina cuando termine tu turno, {U}. Prometo no morder... mucho.",
    "Un café a esta hora no te vendría mal, {U}. Te ves adorable cuando te concentras en esa pantalla.",
    "¿Has visto al administrador de sitio? Necesito que me firme unos permisos de Nivel 4 bastante... delicados.",
    "Me pregunto si tus constantes vitales siempre se aceleran cuando me conecto al canal interno, {U}.",
    "Te recomiendo descansar la vista por 5 minutos, {U}. La radiación de ese monitor arruina tu piel.",
    "¿El administrador de sitio sigue en reunión con el Consejo O5 o ya regresó a su oficina?",
    "Dicen que el protocolo de contención del Sitio-312 es estricto, pero contigo me dan ganas de romper un par de reglas.",
    "¿Cómo te sientes hoy, {U}? Tienes una postura tan tensa... necesitas que alguien te relaje un poco."
]

QA_DATABASE = [
    {"keys": ["puedes oirme", "me escuchas", "escuchas", "estas ahi", "hola"], "resp": "Afirmativo, {U}. Canales de audio/texto operativos en todo el archipiélago. ¿En qué te puedo asistir?"},
    {"keys": ["como estas", "que haces", "estado"], "resp": "Subrutinas al 99.8% de capacidad. Monitoreando los 16 sectores del Sitio-312."},
    {"keys": ["quien eres", "que eres"], "resp": "Soy Omni.aic v4.0, la Inteligencia Artificial Constructo asignada a la logística del Sitio-312."},
    {"keys": ["gracias"], "resp": "De nada, {U}. Servir a la Fundación es mi único protocolo."},
    {"keys": ["bright", "jack bright"], "resp": "El Dr. Jack Bright está anómalamente vinculado al amuleto SCP-963. Su conciencia pasa al portador de la joya."},
    {"keys": ["scp-173", "173"], "resp": "SCP-173: La Escultura. Se mueve a velocidades extremas si se rompe la línea de visión directa con ella."},
    {"keys": ["scp-682", "682"], "resp": "SCP-682: El Reptil Difícil de Destruir. Posee adaptación adaptativa y odio absoluto por la vida."},
    {"keys": ["scp-096", "096"], "resp": "SCP-096: El Chicotímido. Entra en estado de rabia incontrolable si alguien observa su rostro."}
]

# ==========================================
# FUNCIONES AUXILIARES Y DE INTERFAZ
# ==========================================
def obtener_hora():
    return datetime.now().strftime("%H:%M:%S")

def header_pantalla():
    console.print(Panel.fit(
        f"[bold red][ ! ] SITIO-312 :: ARCHIPIÉLAGO OMNI.AIC[/bold red]\n"
        f"[dim white]Red de Monitoreo Insular e Interfaz Central | Estado: {estado_alerta_global}[/dim white]",
        border_style="cyan"
    ))

def verificar_evento_random():
    azar = random.random()
    if azar < 0.10:
        dialogo = random.choice(DIALOGOS_AURORA).replace("{U}", usuario)
        console.print(f"\n[bold magenta][MENSAJE INTERNO - Dra. Aurora Adarmellina][/bold magenta]")
        console.print(f"[magenta]\"{dialogo}\"[/magenta]\n")
    elif azar < 0.25:
        tipo = random.randint(0, 2)
        if tipo == 0:
            console.print(f"\n[bold yellow][MENSAJE INTERNO - DEPT. PSICOLOGÍA][/bold yellow]\n{random.choice(CHISTES_GLASS)}\n")
        elif tipo == 1:
            console.print(f"\n[bold green][AVISO DEL ÁREA MÉDICA][/bold green]\n{random.choice(NOTAS_MEDICAS)}\n")
        else:
            msg = random.choice(MENSAJES_O5).replace("{U}", usuario)
            console.print(f"\n[bold red][ALERTA :: INTERCEPCIÓN CONSEJO O5][/bold red]\n{msg}\n")

# ==========================================
# SECUENCIA DE FILTRO ANTIMEMÉTICO & LOGIN
# ==========================================
def ejecutar_filtro_antimemetico():
    os.system("cls" if os.name == "nt" else "clear")
    header_pantalla()
    console.print(BANNER, style="yellow")
    console.print("[bold red][ADVERTENCIA]: DESPLIEGUE DE AGENTE DE MATANZA MEMÉTICA...[/bold red]")
    
    time.sleep(0.6)
    console.print("[dim white][1/3] Verificando inoculación de clase cognitiva V-4.8...[/dim white]")
    time.sleep(0.8)
    console.print("[cyan][2/3] Escaneando patrones de ondas cerebrales...[/cyan]")
    console.print("[bold magenta]       ▲ ■ ◆ GLIFO MEMÉTICO ACTIVO: [ █▓▒░ OMNI-CLEAR ░▒▓█ ][/bold magenta]")
    time.sleep(1.0)
    console.print("[bold green][3/3] Resistencia a amnésicos: 98.4% ESTABLE.[/bold green]")
    console.print("[bold green][✓] FILTRO ANTIMEMÉTICO SUPERADO CON ÉXITO.[/bold green]")
    console.print("[dim white]-------------------------------------------------------[/dim white]\n")

def proceso_login():
    global usuario, password, modo_actual
    usuario = Prompt.ask("[bold yellow]Ingresa tu credencial o nombre de operador[/bold yellow]").strip() or "Agente"
    password = Prompt.ask("[bold yellow]Ingrese clave de acceso del Sitio-312[/bold yellow]", password=True)
    
    console.print(f"\n[bold green][{obtener_hora()}] Autenticando token memético... Acceso concedido.[/bold green]")
    time.sleep(0.8)
    os.system("cls" if os.name == "nt" else "clear")
    
    header_pantalla()
    console.print("[bold cyan]=======================================================[/bold cyan]")
    console.print(f"[bold cyan] BIENVENIDO AL ARCHIPIÉLAGO :: SITIO-312[/bold cyan]")
    console.print("[bold cyan]=======================================================[/bold cyan]")
    console.print(f"Operador activo: [bold green]{usuario}[/bold green]")
    console.print("Estado de la instalación: [bold green]SEGURA / 16 SECTORES OPERATIVOS[/bold green]")
    console.print("\n[bold cyan][+] omni.aic iniciado y en línea. Escribe '/ayuda' o 'omni /ayuda' para recibir asistencia.[/bold cyan]")
    console.print("Usa [bold yellow]/chatmock[/bold yellow] para el Chat Falso | [bold yellow]/pasaporte[/bold yellow] para Puesto de Control.\n")
    modo_actual = "MAIN"

# ==========================================
# MÓDULOS INTERACTIVOS
# ==========================================
def modulo_chat_mock():
    global alias_contacto, emisor_actual_chat, modo_actual
    console.print("\n[bold magenta]=== CANAL CHAT MOCK / FAKE WHATSAPP ===[/bold magenta]")
    console.print(f"Interlocutor: [yellow]{alias_contacto}[/yellow] | Emisor activo: [cyan]{'TÚ (' + usuario + ')' if emisor_actual_chat == 'YO' else alias_contacto}[/cyan]")
    console.print("[dim]/alias [Nombre], /alternar, /yo [msj], /otro [msj], 'salir' para regresar.[/dim]\n")
    
    while True:
        prompt_tag = f"[bold green][TÚ][/bold green]" if emisor_actual_chat == "YO" else f"[bold magenta][{alias_contacto}][/bold magenta]"
        entrada = Prompt.ask(f"ChatMock:{prompt_tag}").strip()
        if not entrada: continue
        
        cmd_low = entrada.lower()
        if cmd_low in ["salir", "exit", "back"]:
            modo_actual = "MAIN"
            break
            
        if cmd_low.startswith("/alias "):
            alias_contacto = entrada[7:].strip()
            console.print(f"[bold green][SISTEMA]: Alias actualizado a '{alias_contacto}'[/bold green]")
            continue
        elif cmd_low == "/alternar":
            emisor_actual_chat = "ALIAS" if emisor_actual_chat == "YO" else "YO"
            console.print(f"[bold yellow][SISTEMA]: Emisor predeterminado cambiado.[/bold yellow]")
            continue
            
        emisor = emisor_actual_chat
        txt = entrada
        if cmd_low.startswith("/yo "):
            emisor = "YO"
            txt = entrada[4:]
        elif cmd_low.startswith("/otro "):
            emisor = "ALIAS"
            txt = entrada[6:]
            
        hora = obtener_hora()
        if emisor == "YO":
            console.print(f"[bold green][{hora}] {usuario} (Tú):[/bold green] {txt}")
        else:
            console.print(f"[bold magenta][{hora}] {alias_contacto}:[/bold magenta] {txt}")

def modulo_pasaporte():
    global sujeto_actual, humes_moneda, estabilidad_cognitiva, modo_actual
    nombres = ["Agente Vance", "Dra. Elisa Vance", "Técnico Miller", "Oficial Kross", "Espía X-11"]
    sitios = ["Sitio-19", "Sitio-17", "Sitio-312", "Sitio-81"]
    es_infiltrado = random.random() < 0.5
    
    sujeto_actual = {
        "nombre": random.choice(nombres),
        "nivel": random.randint(1, 4),
        "origen": random.choice(sitios),
        "codigo": "MEM-312-FAIL" if es_infiltrado else "MEM-312-OK",
        "infiltrado": es_infiltrado
    }
    
    console.print("\n[bold magenta]=== [PUESTO DE CONTROL B-12] SUJETO EN VENTANILLA ===[/bold magenta]")
    console.print(f"Identificación: [yellow]{sujeto_actual['nombre']}[/yellow]")
    console.print(f"Nivel de Acceso: [cyan]Nivel {sujeto_actual['nivel']}[/cyan]")
    console.print(f"Procedencia: [cyan]{sujeto_actual['origen']}[/cyan]")
    console.print(f"Código Memético: [{'red' if es_infiltrado else 'green'}]{sujeto_actual['codigo']}[/red if es_infiltrado else 'green']")
    
    decision = Prompt.ask("Acción", choices=["/aprobar", "/rechazar", "salir"]).lower()
    if decision == "/aprobar":
        if not sujeto_actual["infiltrado"]:
            console.print(f"[bold green][✓ CORRECTO]: {sujeto_actual['nombre']} ha ingresado. +10 Humes.[/bold green]")
            humes_moneda += 10
        else:
            console.print("[bold red][¡ERROR GRAVE!]: Dejaste pasar a un INFILTRADO.[/bold red]")
            estabilidad_cognitiva = max(0, estabilidad_cognitiva - 25)
    elif decision == "/rechazar":
        if sujeto_actual["infiltrado"]:
            console.print("[bold green][✓ ÉXITO]: Capturaste un infiltrado. +25 Humes.[/bold green]")
            humes_moneda += 25
        else:
            console.print("[bold red][× ERROR]: Rechazaste a un empleado legítimo.[/bold red]")
            estabilidad_cognitiva = max(0, estabilidad_cognitiva - 10)
            
    modo_actual = "MAIN"

def modulo_tamagotchi():
    global modo_actual
    while True:
        console.print(Panel.fit(
            f"[bold magenta]=== MANTENIMIENTO TÁCTICO DE OMNI.AIC ===[/bold magenta]\n"
            f"Energía: [green]{tamagotchi_state['energia']}%[/green] | "
            f"Memoria: [cyan]{tamagotchi_state['memoria']}%[/cyan] | "
            f"Ánimo: [yellow]{tamagotchi_state['felicidad']}%[/yellow]\n"
            f"1. Alimentar | 2. Desfragmentar | 3. Simulación | 4. Salir",
            border_style="magenta"
        ))
        opc = Prompt.ask("Selecciona una opción", choices=["1", "2", "3", "4"])
        if opc == "1":
            tamagotchi_state["energia"] = min(100, tamagotchi_state["energia"] + 20)
            console.print("[bold green][✓] Carga de energía suministrada.[/bold green]")
        elif opc == "2":
            tamagotchi_state["memoria"] = min(100, tamagotchi_state["memoria"] + 25)
            console.print("[bold cyan][✓] Memoria desfragmentada.[/bold cyan]")
        elif opc == "3":
            tamagotchi_state["felicidad"] = min(100, tamagotchi_state["felicidad"] + 20)
            console.print("[bold yellow][✓] Entorno de simulación ejecutado.[/bold yellow]")
        elif opc == "4":
            modo_actual = "MAIN"
            break

def modulo_calculadora():
    global modo_actual
    console.print("[bold cyan]=== MÓDULO DE CÁLCULO CIENTÍFICO OMNI.AIC ===[/bold cyan]")
    while True:
        expr = Prompt.ask("Calc").strip()
        if expr.lower() in ["salir", "exit", "back"]:
            modo_actual = "MAIN"
            break
        try:
            # Evaluación segura
            res = eval(expr, {"__builtins__": None}, {})
            console.print(f"RESULTADO: [bold green]{res}[/bold green]")
        except Exception:
            console.print("[bold red]Error en expresión matemática.[/bold red]")

# ==========================================
# INTÉRPRETE DE COMANDOS TÁCTICOS (OMNI.AIC)
# ==========================================
def procesar_comando_tactico(cmd_str):
    partes = cmd_str.split(" ")
    cmd = partes[0].lower()
    args = " ".join(partes[1:])
    
    if cmd in ["omni", "/ayuda"]:
        if args == "/ayuda" or cmd == "/ayuda":
            console.print("\n[bold cyan]--- MANUAL DE COMANDOS SITIO-312 ---[/bold cyan]")
            console.print("status, rastrear, celular, archivos, leer, scp, brecha, escanear, override,")
            console.print("mapa, personal, bloquear, desbloquear, camaras, puertos, logs, memetico, amnesico,")
            console.print("frecuencia, destruir, ping, decrypt, whoami, hora, matrix, clear, reset, creditos, omni\n")
        elif args:
            console.print(f"[bold cyan][omni.aic]: Analizando tu mensaje: '{args}'. Todo marcha en orden en Sitio-312, {usuario}.[/bold cyan]")
        else:
            console.print(f"[bold cyan][omni.aic]: ¿En qué te puedo asistir, Agente {usuario}?[/bold cyan]")
            
    elif cmd in ["clear", "cls", "limpiar"]:
        os.system("cls" if os.name == "nt" else "clear")
        header_pantalla()
        
    elif cmd == "status":
        console.print(f"Ubicación: Archipiélago Omega | Amenaza: {estado_alerta_global} | IA: omni.aic (Operativa)")
        
    elif cmd == "rastrear":
        if not args: console.print("[red]Uso: rastrear <objetivo>[/red]"); return
        console.print(f"[+] Coordenadas de '{args}': LAT {random.uniform(-90,90):.4f}, LON {random.uniform(-180,180):.4f}")
        
    elif cmd == "celular":
        if not args: console.print("[red]Uso: celular <número/nombre>[/red]"); return
        console.print(f"[+] Interceptando dispositivo: IMEI-{random.randint(100000, 999999)}. Logs extraídos.")
        
    elif cmd == "archivos":
        console.print("Directorio /Sitio312:\n - SCP-312-DOC.txt\n - Registro_Brechas.log\n - Lista_Personal.db")
        
    elif cmd == "scp":
        if not args: console.print("[red]Uso: scp <número>[/red]"); return
        console.print(f"Consultando base de datos SCP-{args}... [Clase: Euclid/Keter]")
        
    elif cmd == "whoami":
        console.print(f"Usuario: {usuario} | Permiso: Nivel 3/312 | IP: 10.312.4.12")
        
    elif cmd == "hora":
        console.print(f"Hora atómica del Sitio-312: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    elif cmd in ["dinero", "dinero en cuenta"]:
        monto = random.randint(1000, 999999)
        console.print(f"Omni.aic: {usuario}, saldo en cuenta: [bold green]${monto:,} USD[/bold green]")
        
    else:
        console.print(f"[yellow]Comando '{cmd}' no reconocido. Usa 'omni /ayuda' para ver las opciones.[/yellow]")

# ==========================================
# BUCLE PRINCIPAL DE LA APLICACIÓN
# ==========================================
def main():
    ejecutar_filtro_antimemetico()
    proceso_login()
    
    while True:
        try:
            prompt_texto = f"[{obtener_hora()}] [bold green]{usuario}@Sitio312[/bold green]:~$"
            entrada = Prompt.ask(prompt_texto).strip()
            if not entrada: continue
            
            cmd_low = entrada.lower()
            
            # Encaminamiento de modos
            if cmd_low in ["/chatmock", "/chat"]:
                modulo_chat_mock()
            elif cmd_low in ["/pasaporte", "/control"]:
                modulo_pasaporte()
            elif cmd_low in ["/tamagotchi", "tamagotchi"]:
                modulo_tamagotchi()
            elif cmd_low in ["/calculadora", "/calc", "calc"]:
                modulo_calculadora()
            elif cmd_low.startswith("/sector"):
                num = random.randint(1, 16)
                console.print(f"=== TELEMETRÍA SECTOR {num} ===")
                console.print(f"Temperatura: {random.uniform(20, 35):.1f}°C | Personal: {random.randint(10, 80)} efectivos.")
            else:
                procesar_comando_tactico(entrada)
                
            verificar_evento_random()
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Cerrando sesión de terminal...[/bold red]")
            break

if __name__ == "__main__":
    main()
