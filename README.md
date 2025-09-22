# Second Traefik Workshop

## Diagrama de la solución

![Diagrama de la solucion](./images/diagram.jpg)

## Hosts usados

- 127.0.0.1 api.localhost
- 127.0.0.1 ops.localhost

## Checklist de comprobaciones con resultados

###  API en api.localhost responde /health

![Respuesta health](./images/health-response.png)

### Dashboard  accesible  solo  en  ops.localhost/dashboard/  y  con auth

#### Dashboard no accesible desde la dirección default

![Error dashboard](./images/dashboard-1.png)

#### Solicitud de autenticación por medio del middleware

![Solicitud autenticacion](./images/dashboard-2.png)

#### Dashboard accesible desde ops.localhost

![Dashboard traefik](./images/dashboard-3.png)

### Servicios y routers en el dashboard

#### Servicios

![Services](./images/services.png)

#### Routers

![Routers](./images/routers.png)

### Rate-limit aplicado y verificado

Haciendo uso de la libreria *hey*, se realiza múltiples peticiones, se muestra el codigo 429 (Too Many Request)

![Rate limit](./images/rate-limit.png)

#### Balanceo

![Balanceo](./images/balance.png)

## Reflexión técnica

### ¿Qué aporta Traefik frente a mapear puertos directamente?

Mientrar que mapeando los puertos directamente implica hacerlo de forma manual, con Treafik es automático entre las replicas del servicio.

### ¿Qué middlewares usarían en producción y por qué? 

Middlewares de autenticación como (BasicAuth, ForwardAuth), rate limiting para prevenir ataques DoS, de compresión para reducir los tamaños de respuesta y mejorar el rendimiento.

### Riesgos de dejar el dashboard “abierto” y cómo mitigarlos

