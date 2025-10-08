# HBnB Documentación Técnica 🛠️

**Integrantes:**
* Erick Gaiero
* Gamaliel Perez
* Nahuel Bica

---

## 1. Introducción

El presente documento reúne los diagramas y notas técnicas desarrolladas durante las etapas de diseño y planificación del proyecto **HBnB**. El objetivo es ofrecer una visión clara y completa de la **arquitectura del sistema**.

HBnB busca replicar, en una versión simplificada, la lógica de una plataforma de alojamiento tipo AirBnB, permitiendo la gestión de **usuarios, lugares, reseñas y servicios** a través de una **API REST**.

Este documento sirve como guía técnica esencial para las fases de implementación, detallando los diagramas de paquetes, clases y secuencia, junto con las explicaciones que describen las decisiones de diseño y la interacción entre los distintos componentes del sistema.

---

## 2. Arquitectura de Alto Nivel: Diseño en Capas

Se ha adoptado una **Arquitectura en Capas** para asegurar la separación de responsabilidades, facilitando la escalabilidad, el mantenimiento y la sustitución de componentes (por ejemplo, el almacenamiento). El sistema se organiza en tres capas principales: **Presentación**, **Lógica de Negocio** y **Persistencia**.

### 2.1. Diagrama de Paquetes (Layers)

Este diagrama lo pueden encontrar en el repositorio

## 3. Lógica de Negocio (Business Logic Layer)

### 3.1. Diagrama de Clases

El diagrama de clases detalla las principales entidades del sistema (**Models**) y sus relaciones, ilustrando la estructura de datos y los comportamientos clave.

```mermaid
classDiagram
direction TB
    class Base {
        -id : String
        -created_at : DateTime
        -updated_at : DateTime
        +create()
        +update()
        +delete()
        +list()
    }

    class Place {
        -title : String
        -description : String
        -price : Float
        -latitude : Float
        -longitude : Float
        +getReviews()
        +getOwner()
        +checkAvailability(startDate, endDate)
        +getAverageRating()
        +searchAmenity(name)
    }

    class Review {
        -rating : Integer
        -comment : String
        +report()
    }

    class Amenity {
        -name : String
        -description : String
    }

    class User {
        -first_name : String
        -last_name : String
        -email : String
        -password : String
        -is_admin : Boolean
        +login()
        +logout()
        +getOwnedPlaces()
        +rateUser(targetUser, rating, comment)
        +sendPrivateMessage(targetUser, message)
    }

    class Like {
        -id : int
        -userId : int
        -postId : int
    }

    Base <|-- User
    Base <|-- Place
    Base <|-- Review
    Base <|-- Amenity
    Base <|-- Like

    User "1" --> "N" Place : owns
    User "1" --> "N" Review : writes
    Place "1" --> "N" Review : receives
    Place "N" --> "N" Amenity : has
    User "1" <-- "N" Like : gives
    Place "1" <-- "N" Like : receives
    Like "1" --> "1" User : by
    Like "1" --> "1" Place : for
  ```
## 4. Flujo de Interacción (API Interaction Flow)

### 4.1. Diagrama de Secuencia

El diagrama de secuencia ilustra la interacción entre las capas durante una operación crucial, como la creación de un nuevo usuario, manteniendo un flujo de **validación, persistencia y respuesta coherente**.

```mermaid
sequenceDiagram
    title Sequence Diagram

    participant Client
    participant API
    participant Logic
    participant DB as "DB - Persistence"

    %% --- USER CREATION ---
    
    Client ->>API: Register User
    API->>Logic: create_user()
    Logic->>Logic: Validate User

    alt User validated
        Logic->>DB: Save Data
        DB-->>Logic: Confirmation Message
        Logic-->>API: User created
        API-->>Client: HTTP 201

    else User Not Valid
        Logic-->>API: Invalid User Data
        API->>Client: HTTP 400

    end

    %% --- PLACE CREATION ---
    Client->>API: Create Place
    API->>Logic: create_place()
    Logic->>Logic: Validate Place

    alt Place validated
        Logic->>DB: Save Data
        DB-->>Logic: Confirmation Message
        Logic-->>API: Place created
        API-->>Client: HTTP 201

    else Place Not Valid
        Logic-->>API: Invalid Place Data
        API->>Client: HTTP 400
    
    end

    %% --- REVIEW CREATION ---
    Client->>API: Create Review
    API->>Logic: create_Review()
    Logic->>Logic: Validate Review

    alt Review validated
        Logic->>DB: Save Review
        DB-->>Logic: Confirmation Message
        Logic-->>API: Review created
        API-->>Client: HTTP 201

    else Review Not Valid
        Logic-->>API: Invalid Review Data
        API->>Client: HTTP 400
    end

    %% --- FETCH PLACES ---
    Client->>API: Fetch Places
    API->>Logic: get_places()
    Logic->>DB: Query all Listings
    DB-->>Logic: Return List of Listings
    Logic-->>API: Return Places List
    API-->>Client: HTTP 200
  ```
## 5. Decisiones de Diseño y Conclusiones

## 6. Conclusión

Este documento resume la estructura técnica del proyecto HBnB, integrando los diferentes diagramas y explicaciones necesarias para comprender su funcionamiento.
Sirve como guía para las fases de desarrollo, pruebas y mantenimiento, asegurando una comprensión común del diseño y la arquitectura del sistema.
