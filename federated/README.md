# Federated Learning (reservado — sin código aún)

Forma futura del subsistema de aprendizaje federado:

- **Servidor agregador**: coordina rondas de entrenamiento y agrega pesos.
- **Cliente FL**: envolverá el entrenamiento de cada `services/<modalidad>`.
- **Estrategia**: por definir (p. ej. FedAvg).
- **Invariante de privacidad**: los datos NUNCA salen del nodo de la institución.
  Solo se comparten pesos/gradientes.

Hoy cada servicio de modalidad expone únicamente inferencia. El entrenamiento federado
se añadirá como un módulo aparte que hable con el agregador de esta carpeta.
