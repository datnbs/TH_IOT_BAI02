
import argparse
import json

import pika

QUEUE_NAME = "sensor_data_queue"
TEMP_MAX = 35.0   
HUMI_MIN = 40.0  


def on_message(channel, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        device = data["device_id"]
        temp = float(data["temperature"])
        humi = float(data["humidity"])
    except (ValueError, KeyError, TypeError) as err:
        print(f"Payload khong hop le ({err}): {body!r}\n")
        channel.basic_ack(delivery_tag=method.delivery_tag)  
        return

    print(f"Device: {device}")
    print(f"Temperature: {temp:.1f}")
    print(f"Humidity: {humi:.1f}")
    if "timestamp" in data:
        print(f"Time: {data['timestamp']}")
    if temp > TEMP_MAX:
        print("CANH BAO: Nhiet do cao")
    if humi < HUMI_MIN:
        print("CANH BAO: Do am thap")
    print("-" * 30)

   
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    parser = argparse.ArgumentParser(description="RabbitMQ Monitoring Consumer")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5672)
    parser.add_argument("--user", default="guest")
    parser.add_argument("--password", default="guest")
    args = parser.parse_args()

    credentials = pika.PlainCredentials(args.user, args.password)
    params = pika.ConnectionParameters(
        host=args.host, port=args.port, credentials=credentials
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

    print(f"Dang cho du lieu tu queue '{QUEUE_NAME}'. Nhan CTRL+C de thoat.\n")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()