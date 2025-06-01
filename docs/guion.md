# Presentación del Proyecto – Baywatchers

Hola, somos el equipo de Baywatchers, y esta es nuestra solución para el monitoreo automático de precios a través de Telegram. Baywatchers es un bot diseñado para ayudar a los usuarios a vigilar productos online y recibir estadísticas sobre sus precios de forma simple y directa.

Nuestra solución está construida con las siguientes tecnologías:

- Python como lenguaje principal.
- FastAPI para la estructura de la API.
- SQLite como base de datos ligera.
- SQLAlchemy para la capa de acceso a datos.
- APScheduler para tareas programadas de revisión.
- python-telegram-bot para integrar con Telegram.
- Docker y Docker Compose para contenerización y despliegue.
- Poetry para la gestión de dependencias.
- Documentación técnica con Markdown y UML usando PlantUML.

Hemos diseñado una arquitectura modular que facilita el mantenimiento y la escalabilidad. El proyecto se divide en varios módulos:  
`api/` contiene el punto de entrada con FastAPI; `services/` la lógica de vigilancia; `models/` los esquemas de datos; `db/` gestiona operaciones con la base de datos; y `bot/` la lógica del bot en Telegram.  
Todo se ejecuta dentro de un contenedor Docker, lo que permite portabilidad y consistencia en todos los entornos.

Durante la demostración del bot en Telegram, mostramos cómo un usuario puede interactuar de forma sencilla:  
Se inicia con el comando `/start`. Con `/vigilar <url>` se comienza a monitorear un producto. El comando `/misproductos` muestra los productos vigilados. Con `/estadisticas <url>` se obtiene un resumen con media, máximo, mínimo y últimos precios. Además, se puede cambiar la frecuencia de revisión con `/checkinterval <minutos>` y detener la vigilancia con `/detener <url>`.

Entre los puntos fuertes del proyecto destacamos su facilidad de uso directamente desde Telegram, su arquitectura modular que facilita su escalabilidad, y su autonomía, ya que revisa los precios de forma periódica sin intervención del usuario.  
Aporta valor al permitir a los usuarios un seguimiento pasivo y automático del precio de los productos que les interesan.

Como propuestas de mejora, planteamos implementar notificaciones automáticas cuando el precio baja, soporte para más sitios de e-commerce, exportación de estadísticas en formatos PDF o CSV, y eventualmente un frontend web. Además, en un entorno más robusto, podríamos usar PostgreSQL como base de datos.

Gracias por ver esta presentación de Baywatchers. Esperamos que esta solución sea útil y estamos abiertos a seguir mejorándola con nuevas funcionalidades.


:tm: :shipit: :recycle: :goberserk: