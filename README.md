El Presente folder contiene la información del back end de nuestra plataforma de aprendizaje. 
El back end opera con docker y usa google cloud run para que sea accesible desde cualquier dispositivo.

El servidor tiene una serie de callable functions para poder recibir requests y usar una API de Chat GPT como un chatbot.
Dicho chatbot está entrenado con libros financieros. Incluimos un libro aquí. Con los que entrenamos al agente para generar contenido educativo.
Los JSON son files que guardan el contenido de los requests de la app en firestore de forma legible para la plataforma.

Así, nuestros cursos vienen de forma fácil de procesar tanto para motores de texto como para IA, permitiéndonos escalar nuestra plataforma de gran forma sin complicaciones.

Como best practice escondimos la API KEY en un documento .env

El front end de swift se encarga de servir como un vínculo entre el agente y el usuario para la experiencia personalizada de aprendizaje.

Esta experiencia de aprendizaje permite que los usuarios reciban una lista ordenada de contenido nuevo gracias a un agente de IA y que además les genere contenido adicional.

Consideramos que el uso de agentes para la creación de contenido facilita el crecimiento de la plataforma, y el aprovechamiento las bases de datos para guardar el 
contexto de cada interacción así como la generación de contenido genérico reduce costos futuros mientras se mantiene la frescura de la plataforma.

Creemos que además se pueden implementar exámenes personalizados de igual manera basados en las herramientas de IA, y mecanismos multimodales para incrementar el engagement. Tristemente, por las limitaciones de tiempo del hackathon no fuimos capaces de ejecutarlos.

El servidor está corriendo ya en fastapi, se necesitan user id + files para invocar algunas funciones.
