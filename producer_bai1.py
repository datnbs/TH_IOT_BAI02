
import os
import pika

QUEUE_NAME = "iot_lab_queue"


def main():
    amqp_url = "amqps://spiqbykv:na-fwQEU7TwfvFZEd71hR_-TE1OSU8QI@rabbit.lmq.cloudamqp.com/spiqbykv"

    connection = None

    try:
        params = pika.URLParameters(amqp_url)
        params.socket_timeout = 5
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        full_name = input("Nhap ho ten sinh vien: ").strip()
        student_id = input("Nhap ma sinh vien: ").strip()

        if not full_name or not student_id:
            print("Ho ten va ma sinh vien khong duoc de trong.")
            return

        message = (
            f"Xin chao tu ung dung Python AMQP - "
            f"{student_id} - {full_name}"
        )

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="text/plain",
                content_encoding="utf-8"
            )
        )

        print(f"Da gui message: {message}")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Loi ket noi RabbitMQ: {e}")
    except Exception as e:
        print(f"Loi: {e}")
    finally:
        if connection is not None and connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
