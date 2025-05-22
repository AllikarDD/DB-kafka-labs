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