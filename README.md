## Clase 2 — APIs de IA Generativa y memoria conversacional

### Conversación de 8 turnos (Paso 7)

Ver evidencia en `entregas/s02/evidencia/memoria.png`.

El modelo recordó correctamente que el nombre era Javier y que su color
favorito era el verde porque el programa reenvía el historial de la
conversación en cada llamada.

### Por qué elegí ventana deslizante

Elegí una ventana deslizante porque permite controlar el tamaño del
historial y reducir el consumo de tokens. Para este caso no se necesita
almacenamiento permanente, por lo que conservar los últimos turnos es
suficiente.

### Límite de solicitudes provocado (Paso 9)

Ver evidencia en `entregas/s02/evidencia/rate_limit.png`.

El error 429 fue capturado correctamente y el programa realizó reintentos
con backoff exponencial sin finalizar inesperadamente.