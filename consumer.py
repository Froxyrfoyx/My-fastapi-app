from pika import ConnectionParameters, BlockingConnection



connection_params = ConnectionParameters(
    host="localhost",
    port=5672,    
)
def process(ch, method , properties, body):
    print(f"Получено сообщение: {body}")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    with BlockingConnection(connection_params) as con:
        with con.channel() as ch:
            ch.queue_declare(queue = "message")
            ch.basic_consume(
                queue= "message",
                on_message_callback = process,
            )
            print("Жду сообщение")
            ch.start_consuming()

if __name__ == "__main__":
    main()            