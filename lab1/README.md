# Установка Kafka

#### Предварительные требования

Для запуска Kafka в Docker необходимо:

1. Установить **Docker Desktop**.
2. Установить **Docker Compose** (включён в Docker Desktop).
3. Иметь аккаунт на **Docker Hub** для загрузки образов.

---

### Docker Compose файл

```yaml
services:
  broker:
    image: apache/kafka:latest
    hostname: broker
    container_name: broker
    ports:
      - 9092:9092
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_NODE_ID: 1
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@broker:29093
      KAFKA_LISTENERS: PLAINTEXT://broker:29092,CONTROLLER://broker:29093,PLAINTEXT_HOST://0.0.0.0:9092
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LOG_DIRS: /tmp/kraft-combined-logs
      CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
```

### Основные параметры контейнера

1. ​**​`image: apache/kafka:latest`​**​

    * Использует последнюю версию официального образа Apache Kafka.
2. ​**​`hostname: broker`​**​

    * Задает hostname контейнера как `broker`​.
3. ​**​`container_name: broker`​**​

    * Присваивает имя контейнеру `broker`​.
4. ​**​`ports: - 9092:9092`​**​

    * Пробрасывает порт 9092 контейнера на порт 9092 хоста для клиентских подключений.

### Параметры конфигурации Kafka (environment)

#### Идентификация и роли

5. ​**​`KAFKA_BROKER_ID: 1`​**​

    * Уникальный идентификатор брокера в кластере.
6. ​**​`KAFKA_PROCESS_ROLES: broker,controller`​**​

    * Указывает, что нода выполняет две роли в режиме KRaft:

        * ​`broker`​ - обработка данных
        * ​`controller`​ - управление метаданными кластера
7. ​**​`KAFKA_NODE_ID: 1`​**​

    * Уникальный ID ноды в KRaft-режиме.
8. ​**​`CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk`​**​

    * Уникальный идентификатор кластера.

#### Настройки слушателей (listeners)

9. ​**​`KAFKA_LISTENERS`​**​  
   Определяет endpoint'ы для подключения:

    * ​`PLAINTEXT://broker:29092`​ - для внутренней коммуникации между брокерами
    * ​`CONTROLLER://broker:29093`​ - для KRaft-контроллера
    * ​`PLAINTEXT_HOST://0.0.0.0:9092`​ - для внешних клиентов
10. ​**​`KAFKA_ADVERTISED_LISTENERS`​**​

    * Анонсируемые адреса для клиентов:

        * ​`PLAINTEXT://broker:29092`​ - для внутренних соединений
        * ​`PLAINTEXT_HOST://localhost:9092`​ - для внешних подключений
11. ​**​`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`​**​

    * Сопоставление имен listener'ов с протоколами безопасности (все PLAINTEXT - без шифрования).
12. ​**​`KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT`​**​

    * Указывает, какой listener использовать для связи между брокерами.
13. ​**​`KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER`​**​

    * Указывает listener для KRaft-контроллера.

#### Настройки KRaft

14. ​**​`KAFKA_CONTROLLER_QUORUM_VOTERS: 1@broker:29093`​**​

    * Список кворум-голосующих контроллеров (формат: `nodeId@host:port`​).

#### Настройки топиков

15. ​**​`KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1`​**​

    * Фактор репликации для внутреннего топика `__consumer_offsets`​.
16. ​**​`KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1`​**​

    * Фактор репликации для топика `__transaction_state`​.
17. ​**​`KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1`​**​

    * Минимальное количество in-sync реплик для топика транзакций.

#### Прочие настройки

18. ​**​`KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0`​**​

    * Устраняет задержку при первом rebalance потребителей.
19. ​**​`KAFKA_LOG_DIRS: /tmp/kraft-combined-logs`​**​

    * Директория для хранения логов (данных) Kafka.

### Особенности данной конфигурации

1. **Режим KRaft**  
   Конфигурация использует новый режим работы без ZooKeeper (начиная с Kafka 3.3+).
2. **Однонодовая установка**  
   Все параметры репликации (`...REPLICATION_FACTOR: 1`​) настроены для работы с одним брокером, что подходит только для разработки.
3. **Двойная роль**  
   Нода работает и как broker, и как controller, что упрощает локальную разработку.
4. **Доступность**

    * Внутри Docker-сети: `broker:29092`​
    * С хоста: `localhost:9092`​

---

### Запуск Kafka

1. Запустите контейнер в фоновом режиме:

    ```bash
    docker compose up -d
    ```
2. Проверьте логи:

    ```bash
    docker logs broker
    ```

   Успешный запуск покажет:

    ```bash
    [BrokerServer id=1] Transition from STARTING to STARTED
    Kafka version: 3.7.0
    ```

---

### Работа с Kafka

#### 1. Создание топика

Подключитесь к контейнеру и создайте топик:

```bash
docker exec -it -w /opt/kafka/bin broker sh
./kafka-topics.sh --create --topic my-topic --bootstrap-server broker:29092
```

Результат:

```bash
Created topic my-topic.
```

> **Важно**:
>
> * Внутри контейнера используйте `broker:29092`​.
> * Снаружи (например, с локальной машины) — `localhost:9092`​.

#### 2. Отправка сообщений

Запустите консольного продюсера:

```bash
./kafka-console-producer.sh --topic my-topic --bootstrap-server broker:29092
```

Введите сообщения:

```bash
All streams
lead to Kafka
```

Завершите работу клавишей **Ctrl+C**.

#### 3. Чтение сообщений

Запустите консольного потребителя:

```bash
./kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server broker:29092
```

Вывод:

```bash
All streams
lead to Kafka
```

Завершите работу клавишей **Ctrl+C** и выйдите из контейнера (`exit`​).

---

### Остановка контейнера

```bash
docker compose down -v
```

---

# Работа с кафкой в Python

Установите библиотеку confluent-kafka

```bash
pip install confluent-kafka
```

Запустите программу ниже:

```python
from confluent_kafka import Consumer  # Импорт клиента Consumer из библиотеки confluent_kafka
import time  # Импорт модуля для работы с временными задержками

print("Starting Kafka Consumer")  

# mysecret = "yourjksPassword"  # пример хранения пароля (небезопасно!)
#you can call remote API to get JKS password instead of hardcoding like above  

# Конфигурация потребителя
conf = {
    'bootstrap.servers' : 'localhost:9092',  # Адреса брокеров Kafka
    'group.id' : 'KfConsumer1',  # Идентификатор consumer group
    # 'security.protocol' : 'SSL',  # Настройка SSL
    'auto.offset.reset' : 'earliest',  # Чтение с начала топика при отсутствии сохраненного offset
    'enable.auto.commit' : True,  # Автоматическое подтверждение обработки сообщений
    # 'max.poll.records' : 5,  # Максимальное количество сообщений за один poll
    'heartbeat.interval.ms' : 25000,  # Частота heartbeat-сообщений (25 сек)
    'max.poll.interval.ms' : 90000,  # Максимальное время между вызовами poll (90 сек)
    # 'session.timeout.ms' : 180000,  # Таймаут сессии 
    # 'ssl.keystore.password' : mysecret,  # Пароль keystore 
    # 'ssl.keystore.location' : './certkey.p12'  # Путь к keystore
}

print("connecting to Kafka topic")  # Сообщение о подключении

consumer = Consumer(conf)  # Создание экземпляра потребителя с указанной конфигурацией

consumer.subscribe(['my-topic'])  # Подписка на топик 'my-topic'

# Основной цикл обработки сообщений
while True:
    msg = consumer.poll(1.0)  # Получение сообщения с таймаутом 1 секунда
    
    if msg is None:  # Если сообщений нет
        continue  # Продолжить ожидание
    
    if msg.error():  # Если произошла ошибка
        print("Consumer error happened: {}".format(msg.error()))  # Вывод ошибки
        continue  # Продолжить обработку
    
    # Вывод информации о полученном сообщении:
    print("Connected to Topic: {} and Partition : {}".format(msg.topic(), msg.partition()))
    print("Received Message : {} with Offset : {}".format(msg.value().decode('utf-8'), msg.offset()))
    
    time.sleep(2.5)  # Искусственная задержка для демонстрационных целей

#consumer.close()  # закрытие потребителя 
```

‍

