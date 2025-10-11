# Clean Architecture Python - User Profile Management

## 📋 Visão Geral

Este projeto implementa uma **Arquitetura Hexagonal (Ports & Adapters)** para gerenciamento de perfis de usuários, seguindo os princípios de Clean Architecture. A aplicação é construída com Python, Flask e MongoDB, priorizando testabilidade, manutenibilidade e independência de frameworks.

## 🏗️ Arquitetura Hexagonal - Análise da Implementação

### ✅ **Pontos Fortes da Implementação**

1. **Separação de Responsabilidades**: Clara divisão entre domínio, aplicação, infraestrutura e apresentação
2. **Inversão de Dependências**: Uso correto de interfaces para desacoplar camadas
3. **Entidades Imutáveis**: `UserProfile` como dataclass frozen com métodos de negócio
4. **Repository Pattern**: Interface bem definida com implementação MongoDB
5. **Use Cases Explícitos**: Casos de uso isolados e testáveis
6. **Error Handling**: Sistema estruturado de exceções personalizadas
7. **Mappers**: Conversão adequada entre entidades de domínio e documentos

### ⚠️ **Pontos de Melhoria**

1. **Mistura de imports**: Alguns imports quebram a independência de camadas
2. **Utils no Domain**: `UtilsMethods` deveria estar na camada de aplicação
3. **Naming Conventions**: Inconsistência entre snake_case e camelCase
4. **Error Propagation**: Algumas exceções específicas poderiam ser mais granulares

## 🎯 Fluxo de Dados por Camadas

### **1. Presentation Layer (Entrada)**

```
HTTP Request → Flask → FlaskAdapter → HttpRequest
```

**Componentes:**

- `CreateUserProfileController`: Recebe HttpRequest, valida dados de entrada
- `FlaskAdapter`: Converte Request do Flask para HttpRequest interno
- `HttpRequest/HttpResponse`: DTOs para comunicação HTTP

**Responsabilidades:**

- Validação de entrada
- Serialização/Deserialização
- Tratamento de erros HTTP
- Formatação de resposta

### **2. Application Layer (Orquestração)**

```
HttpRequest → Controller → UseCase → Repository Interface
```

**Componentes:**

- `CreateUserProfileUseCase`: Orquestra a criação de usuários
- `CreateUserProfileInput/Output`: DTOs específicos do caso de uso
- `ICreateUserProfile`: Interface do caso de uso

**Responsabilidades:**

- Coordenação de operações
- Aplicação de regras de negócio específicas
- Transformação de dados entre camadas
- Tratamento de exceções de negócio

### **3. Domain Layer (Núcleo)**

```
Business Logic → Entities → Repository Interfaces
```

**Componentes:**

- `UserProfile`: Entidade central com regras de negócio
- `IUserProfileRepository`: Interface para persistência
- Métodos de negócio: `authorize()`, `update()`, `deactivate()`, `restore()`

**Responsabilidades:**

- Regras de negócio puras
- Validações de domínio
- Comportamentos da entidade
- Contratos para infraestrutura

### **4. Infrastructure Layer (Persistência)**

```
Repository Interface → MongoDB Implementation → Database
```

**Componentes:**

- `MongoUserProfileRepository`: Implementação concreta do repositório
- `UserProfileMapper`: Conversão entre entidade e documento
- `MongoDBProvider`: Gerenciamento de conexão
- `MongoSettings`: Configurações do banco

**Responsabilidades:**

- Persistência de dados
- Mapeamento objeto-documento
- Gerenciamento de conexões
- Implementação de consultas específicas

## 🔄 Fluxo Completo de Criação de Usuário

```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant Controller
    participant UseCase
    participant Entity
    participant Repository
    participant MongoDB

    Client->>Flask: POST /usuarios/criar
    Flask->>Controller: HttpRequest
    Controller->>UseCase: CreateUserProfileInput
    UseCase->>Entity: UserProfile.new()
    Entity->>Entity: authorize("system")
    UseCase->>Repository: insert(UserProfile)
    Repository->>MongoDB: insert_one(document)
    MongoDB-->>Repository: inserted_id
    Repository->>MongoDB: find_one(id)
    MongoDB-->>Repository: document
    Repository-->>UseCase: UserProfile
    UseCase-->>Controller: CreateUserProfileOutput
    Controller-->>Flask: HttpResponse
    Flask-->>Client: JSON Response
```

## 📊 Estrutura de Diretórios

```
src/
├── domain/                          # 🎯 NÚCLEO - Regras de Negócio
│   ├── entities/
│   │   └── user_profile.py         # Entidade principal com lógica de negócio
│   ├── repositories_interfaces/     # Contratos para persistência
│   │   └── user_profile_repository.py
│   └── use_cases_interfaces/        # Contratos para casos de uso
│       └── user_profile/
│           └── create.py
│
├── application/                    # 📋 APLICAÇÃO - Casos de Uso
│   ├── use_cases_impl/            # Implementação dos casos de uso
│   │   └── user_profile_cases/
│   │       └── create.py          # Orquestração da criação
│   └── shared/
│       └── custom_exceptions.py   # Exceções específicas da aplicação
│
├── infra/                         # 🔧 INFRAESTRUTURA - Detalhes Técnicos
│   └── mongo/
│       ├── connection.py          # Gerenciamento de conexão
│       ├── provider.py            # Factory de providers
│       ├── settings.py            # Configurações
│       ├── repositories/          # Implementações concretas
│       │   └── mongo_user_profile_repository.py
│       └── mappers/               # Conversão entidade ↔ documento
│           └── user_profile_mapper.py
│
├── presentation/                  # 🌐 APRESENTAÇÃO - Interface Externa
│   ├── controllers/               # Controladores HTTP
│   │   └── user_profile/
│   │       └── create_controller.py
│   ├── http_types/               # DTOs HTTP
│   │   ├── http_request.py
│   │   └── http_response.py
│   └── interfaces/
│       └── controller_interface.py
│
├── main/                         # 🚀 COMPOSIÇÃO - Injeção de Dependência  
|   |                  
│   ├── server/                   # Configuração do servidor
│   │   ├── server.py
│   │   └── advices/              # Tratamento global de erros
│   ├── routes/                   # Definição de rotas
│   ├── adapters/                 # Adaptadores de framework
│   └── composables/              # Factory/DI container
│       └── user_profile/
│           └── user_profile_create.py
│
└── config/                       # ⚙️ CONFIGURAÇÃO
    └── settings.py               # Configurações globais
```

## 🧬 Responsabilidades por Camada

### **Domain (Núcleo)**

- ✅ **Entidades**: `UserProfile` com comportamentos de negócio
- ✅ **Value Objects**: Objetos imutáveis com validação
- ✅ **Repository Interfaces**: Contratos para persistência
- ✅ **Use Case Interfaces**: Contratos para aplicação
- ❌ **SEM**: Dependências externas, frameworks, detalhes técnicos

### **Application (Casos de Uso)**

- ✅ **Use Cases**: Orquestração de operações de negócio
- ✅ **DTOs**: Objetos de transferência de dados
- ✅ **Application Services**: Coordenação entre componentes
- ✅ **Business Rules**: Regras específicas da aplicação
- ❌ **SEM**: UI, banco de dados, frameworks web

### **Infrastructure (Infraestrutura)**

- ✅ **Repository Implementations**: Persistência específica (MongoDB)
- ✅ **Mappers**: Conversão entre domínio e persistência
- ✅ **External Services**: APIs, cache, mensageria
- ✅ **Database Configuration**: Configurações técnicas
- ❌ **SEM**: Regras de negócio, lógica de aplicação

### **Presentation (Interface)**

- ✅ **Controllers**: Coordenação de entrada/saída
- ✅ **HTTP DTOs**: Serialização para web
- ✅ **View Models**: Formatação para apresentação
- ✅ **Input Validation**: Validação de entrada
- ❌ **SEM**: Regras de negócio, persistência

## 🔍 Princípios Aplicados

### **1. Dependency Inversion**

```python
# ✅ Correto: UseCase depende de abstração
class CreateUserProfileUseCase:
    def __init__(self, repository: IUserProfileRepository):
        self.repository = repository

# ✅ Correto: Infrastructure implementa abstração
class MongoUserProfileRepository(IUserProfileRepository):
    def insert(self, user: UserProfile) -> UserProfile:
        # implementação específica
```

### **2. Single Responsibility**

```python
# ✅ Controller: apenas coordenação HTTP
class CreateUserProfileController:
    def handle_request(self, request: HttpRequest) -> HttpResponse:
        # conversão + delegação

# ✅ UseCase: apenas orquestração de negócio
class CreateUserProfileUseCase:
    def execute(self, input: CreateUserProfileInput) -> CreateUserProfileOutput:
        # lógica de aplicação
```

### **3. Open/Closed**

```python
# ✅ Fácil extensão: nova implementação de repositório
class PostgresUserProfileRepository(IUserProfileRepository):
    # nova implementação sem alterar código existente
```

## 🧪 Estratégia de Testes

### **Testes por Camada**

1. **Domain Tests**:

   - Testes unitários das entidades
   - Validação de regras de negócio
   - Comportamentos da `UserProfile`

2. **Application Tests**:

   - Testes dos casos de uso com mocks
   - Validação de orquestração
   - Cenários de exceção

3. **Infrastructure Tests**:

   - Testes de integração com MongoDB
   - Testes de mappers
   - Testes de repository

4. **Presentation Tests**:
   - Testes de controllers
   - Validação de serialização
   - Cenários HTTP

## 🔧 Configuração e Execução

### **Requisitos**

```bash
pip install -r requirements.txt
```

### **Variáveis de Ambiente**

```bash
LOCAL_CONNECTION_STRING=mongodb://admin:admin123@localhost:27017/
LOCAL_DB_NAME=gmon_clean_arch
FLASK_ENV=development
```

### **Executar Aplicação**

```bash
python run.py
```

### **Executar Testes**

```bash
# Todos os testes
pytest

# Por categoria
pytest -m unit
pytest -m integration

# Com coverage
pytest --cov=src --cov-report=html
```

## 📈 Benefícios da Arquitetura

1. **Testabilidade**: Cada camada pode ser testada isoladamente
2. **Manutenibilidade**: Mudanças são localizadas por responsabilidade
3. **Flexibilidade**: Fácil troca de implementações (MongoDB → PostgreSQL)
4. **Escalabilidade**: Adição de novos casos de uso sem impacto
5. **Independence**: Core business não depende de frameworks
6. **Reusabilidade**: Casos de uso podem ser reutilizados em diferentes interfaces

## 🔄 Padrões de Design Utilizados

- **Repository Pattern**: Abstração para persistência
- **Use Case Pattern**: Encapsulamento de regras de negócio
- **Adapter Pattern**: Adaptação entre camadas
- **Factory Pattern**: Criação de dependências
- **Data Mapper Pattern**: Conversão entre representações
- **Exception Translation**: Conversão de exceções técnicas para domínio

## 📋 Próximos Passos

1. **Implementar validações**: Domain validation para UserProfile
2. **Adicionar logging**: Structured logging por camada
3. **Metrics/Monitoring**: Observabilidade da aplicação
4. **Authorização**: Implementar sistema de permissões
5. **API Versioning**: Suporte a múltiplas versões
6. **Documentation**: OpenAPI/Swagger integration
7. **Performance**: Caching e otimizações de consulta

---

**Conclusão**: A implementação demonstra uma sólida compreensão dos princípios de Clean Architecture, com algumas oportunidades de refinamento para atingir uma arquitetura ainda mais pura e independente.
