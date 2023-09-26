En este taller conoceremos cómo se usa la API de OpenAI para la creación de un asistente virtual
# 1. Registrarse en [OpenAI](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjrgrao5MSBAxVaQjABHa5xAAUQFnoECAYQAQ&url=https%3A%2F%2Fopenai.com%2F&usg=AOvVaw0428uXC88P9g34t6DemBOv&opi=89978449)

# 2. [Playground](https://platform.openai.com/playground) de OpenAI

El playground nos ayuda entender cómo funciona la IA de forma sencilla y rápida de usar, puede servir para ver cómo se desempeña en ejemplos concretos o para realizar consultas rápidas.

El Playground en modo chat nos presenta las siguientes casillas.

1. System: Aquí van las instrucciones de cómo tiene que funcionar nuestra IA (por ejemplo si quieres que autocomplete texto o que resuelva ejercicios matemáticos)
2. User: Este es el apartado en donde nosotros ingresamos los datos de los cuales esperamos una respuesta. (por ejemplo si la IA es un chat acá ingresaremos nuestros mensajes)
3. Assistant: Este es la respuesta que nos retorna la IA, que nosotros podremos modificar luego o podemos usarla cómo el User para condicionar como tiene que funciona la IA en un intento de Few-Shoot learning.
## Importancia de las Iteraciones

Se define iteración a cada vez que nosotros hacemos una petición, por qué? Con un ejemplo es más claro. Digamos que estamos creando una IA de chat. Suponiendo que usamos el playground (importante esto) y creamos un mensaje como user entonces este mensaje se manda a los servidores de OpenAI y recibimos la respuesta de assistant, ahora si queremos mandar otro mensaje como user, además de enviarse este último mensaje, se enviara de nuevo el mensaje anterior y la respuesta del assistant, haciendo que no solo tenga que calcular la respuesta del nuevo mensaje, aumentando consigo la cantidad de tokens. Esto solo pasa en el playground, si usamos la API tenemos que programar esta función. Cada mensaje de System, User, Assistant, se mandan como arrays a la API de OpenAI, y puedes anidarlos para crear esta funcionalidad, por obvias razones es importante considerar esto ya que luego de muchos mensajes las peticiones serán de miles de tokens, y tendrás que crear la lógica para ir eliminando sistemáticamente los mensajes.
## Buenas prácticas

Es importante recordar que las buenas prácticas nos permiten conseguir el resultado esperado en su mejor forma, OpenAI ya comento su lista [buenas prácticas](https://platform.openai.com/docs/guides/gpt-best-practices), a forma de resumen estás son las relevantes para este caso.

1. Escribe instrucciones precisas: Lo ideal es ser lo más preciso, ya sea en el System, User o Assistant, por ejemplo si estás creando una IA que resuelve ejercicios matemáticos, podrías indicarle en el system que temas son los que esta IA sabe más.
2. Step-by-Step: Busca que la IA realice sus conclusiones de forma estructurada, por ejemplo, si estas creando una IA que resuelve ejercicios matemáticos podrías decirle que lo muestre cada paso y porque.
3. Dar ejemplos: Puedes darle ejemplos en el prompt a la IA, recuerda que puedes crear tantos user y assistant cómo quieras para esto, esto sin duda volverá más potente a la IA en cada iteración.
4. Conocer sus limites: El modelo GPT-3.5 suele ser bastante básico, sirve muy bien para una cantidad bastante grande de tareas, pero hay otras que requieren un poco más de "inteligencia", entonces podremos recurrir a GPT-4 para realizarlas, esto casimente solo se consigue saber a prueba y error.
5. El tamaño de la respuesta: El slider dedicado al tamaño de la respuesta (Maximum length) nos puede ayudar en variedad de casos, más que todo para ahorrar gastos, daré 2 casos que pueden llegar a ser sumamente útiles
		1. Imagina que estas creando una IA que clasifica Tweets o mensajes, y los clasifica en base a su contenido y lo que evocan, aquí el tamaño de la respuesta tiene que ser corto, porque no necesitamos que nos explique porque piensa eso.
		2. Si estamos creando una IA que resuelva ejercicios matemáticos y estamos usando GPT-4, es importante considerar cómo usaremos la IA, aquí es importante que siguiendo las anteriores prácticas el tamaño de la respuesta tiene que ser grande, digamos 2000 tokens, para que la IA, en una sola iteración pueda resolver todo el ejercicio sin necesidad de volver a mandar otra petición.
# 3. Obtener la [key](https://platform.openai.com/account/api-keys) de OpenAI

## Variables de Entorno

Debido a que llaves de OpenAI son secretas y no tienen que ser compartidas por nadie, tienen que ser guardadas como variable de entorno para luego invocarse con la siguiente linea de código:

```python
import os
TOKEN = os.getenv("OPENAI_API_KEY")
```

Para crear las variables de entorno seguimos los siguientes pasos:

### Windows

1. Apreta la tecla Win y escribe env, en el apartado Best Match te saldrá la opción "Edit the system environment variables"
2. Apreta el botón en la esquina inferior derecha que dice "Environment Variables"
3. Apreta el botón que dice "New"
4. En donde dice "Variable Name" escribe preferiblemente OPENAI_API_KEY
5. En donde dice "Variable Value" agrega la key que obtuviste en la página de OpenAI

### Linux

1. Escribe en la consola:
```bash
$ nano ~/.zshrc
```
2. Al final del texto agrega:
```bash
export OPENAI_API_KEY="TU KEY AQUÍ"
```
3. Aprete Ctrl+O seguido de enter y luego Ctrl+X
# 4. Instalar dependencias

En este caso con Python ocupamos instalar la librería de openai, esto no quiere decir que si no queremos trabajar con esta librería no podremos acceder a la API, simplemente el código sería diferente, esta librería nos facilita el trabajo a la hora de querer gestionar los llamados a la API, para instalarla usaremos pip.

```shell
$ pip install openai
```

Recuerda que es importante reinciar la consola luego de esto para que se actualicen las dependencias.


# 5. Funcionamiento de la librería

- Setear el token de OpenAI: Para usar nuestro token para las peticiones, solamente consta con usar el parámetro api_key de la librería:
```python
import os
import openai
TOKEN = os.getenv("OPENAI_API_KEY") # Dentro de TOKEN se guarda el valor de la variable de entorno
openai.api_key = TOKEN
```

- Método create de la clase ChatCompletion: este método recibe varios atributos, los más relevantes son:
	1. model: (Obligatorio) un string del modelo a usar, se recomienda usar "gpt-3.5-turbo".
	2. messages: (Obligatorio) es un array de tipo JSON que contiene en sus llaves "role" y "content" por ejemplo.
	3. max_tokens: (Opcional) Un int que determinará que tanto texto tendrá el content del assistant.

```JSON
// Ejemplo del messages
[{
	"role": "system",
	"content": "Eres un autocompletador de texto"
 },{
	"role": "user",
	"content": "En la historia de Julio Cesar, se sabía que él era un"
 }
]
```

```python
response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",
	messages=[
		{
		"role": "system",
		"content": "Eres un autocompletador de texto"
		 },{
		"role": "user",
		"content": "En la historia de Julio Cesar, se sabía que él fue un"
		 }
	],
	max_tokens=203
)
```

- El valor que devuelve el método: El response devolverá un JSON que además de contener la respuesta del assistant, también contendrá valores que nos pueden llegar a ser útiles para más información [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/making-requests). 

```json
{
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1677858242,
    "model": "gpt-3.5-turbo",
    "usage": {
        "prompt_tokens": 13,
        "completion_tokens": 7,
        "total_tokens": 20
    },
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "gran líder militar y político romano. Nació el 13 de julio del año 100 a.C. y destacó por sus habilidades estratégicas y su ambición de poder. Junto a Pompeyo y Craso, formó el primer triunvirato de Roma en el año 59 a.C., consolidando así su influencia política..."
            },
            "finish_reason": "stop",
            "index": 0
        }
    ]
}
```

Si es de nuestro interés acceder solamente al mensaje que nos da el assistant, podemos asignarlo a una variable

```python
msg = response["choices"][0][message][content]
```
# 6. Leer la [documentación](https://platform.openai.com/docs/introduction)
Para profundizar en otras cosas, cómo qué es el function calling o usar otras de las funcionalidades que ofreces OpenAI, puedes revisar la documentación para una investigación más exhaustiva.