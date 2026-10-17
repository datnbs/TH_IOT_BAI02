
import os
from datetime import datetime
import pika

QUEUE_NAME = "iot_lab_queue"


def on_message(channel, method, properties, body):
    message = body.decode("utf-8")
    received_time = datetime.now().strftime("%H:%M:%S")

    print(f"Da nhan message: {message}")
    print(f"Thoi gian nhan: {received_time}")
    print("-" * 50)

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    amqp_url = "amqps://spiqbykv:na-fwQEU7TwfvFZEd71hR_-TE1OSU8QI@rabbit.lmq.cloudamqp.com/spiqbykv"

    connection = None

    try:
        params = pika.URLParameters(amqp_url)
        params.socket_timeout = 5
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=on_message,
            auto_ack=False
        )

        print(f"Dang lang nghe queue: {QUEUE_NAME}")
        print("Nhan Ctrl+C de dung chuong trinh.")

        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nDa dung Consumer.")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Loi ket noi RabbitMQ: {e}")
    except Exception as e:
        print(f"Loi: {e}")
    finally:
        if connection is not None and connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
