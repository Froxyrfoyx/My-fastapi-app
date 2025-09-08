from pika import ConnectionParameters, BlockingConnection



connection_params = ConnectionParameters(
    host="localhost",
    port=5672,    
)

def main():
    with BlockingConnection(connection_params) as con:
        with con.channel() as ch:
            ch.queue_declare(queue = "message")
            ch.basic_publish(
                exchange = "",
                routing_key = "message",
                body = "Hello World!"

            )
            print("Message sent!")

if __name__ == "__main__":
    main()            