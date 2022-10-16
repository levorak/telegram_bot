# Telegram bot

### Minimo Producto Viable (MPV)

* Servidor: 
    * Montar servidor en Heroku
		* CPU, RAM, Disco dependen de como se vaya a manjear el almacenamiento!!
		* Software Requirements:
			Probado en "Ubuntu 22.04.1 LTS" 
			Python3
			pip
			python-telegram-bot
			telegram_menu	
	* Script en python que ejecute el bot 🔃
	* Correr el script de python como servicio

* Limitar acceso: 
    * Acceso unicamente basado en el chat id ✅
    * Agregar archivo/db de registro para asociar chat (?) (probado en json ✅)
	* Configurar el bot para evitar que agregdo a grupos 

* Base de datos de registro	
	* Puede ser tan sencillo como un csv,json o una db (?)
	* Como se alimentar la BD (manual, UI, script) (?)

* Menú :
    * Al abrir el chat se envia un mensaje bienvenida(?) ✅
    * Menu de botones con productos ✅
	* Poder agregar emojis en el menu (porque asi se ve mas lindo 😋) ✅
    * Sub menu de bontones con cantidad(?) ✅
	* La cantidad se recibe por una entrada de texto (?)

* Almacenamiento
	* Donde se van a guardar los pedidos (?)
	* Que información se va a almacenar (Usuario, chatid, fecha, producto, cantidad) (?)
	* Debe permitir sacar luego stats (?)

### Journey
	* Se pueden pedir varios productos a la vez (?)
	* Al final a tiene un resumen de lo que pidió(?)
	* Puede editar el pedido (?)

* Agregar un boton de confirmar el pedido (?)
	* lista de producto con cantidad 
	* boton de confirmar (si/no)
	* habilita el boton de completar pedido

* Agregar un boton de completar el pedido (?)
	* Envía un mensaje que confirma la recepción del pedido con un resumen del mismo (?)
	* Activa la funcion de eliminar el chat history automaticamente (?)
	
* Menu de commandos del bot
	* Con bootfather agregar los comandos al menu del bot 
	

### Pruebas


