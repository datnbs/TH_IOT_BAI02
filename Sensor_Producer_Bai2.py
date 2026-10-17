
import argparse
import json
import random
import time
from datetime import datetime

import pika

QUEUE_NAME = "sensor_data_queue"


def main():
    parser = argparse.ArgumentParser(description="RabbitMQ Sensor Producer")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5672)
    parser.add_argument("--user", default="guest")
    parser.add_argument("--password", default="guest")
    parser.add_argument("--device", default="sensor01")
    parser.add_argument("--interval", type=float, default=3.0)
    args = parser.parse_args()

    credentials = pika.PlainCredentials(args.user, args.password)
    params = pika.ConnectionParameters(
        host=args.host, port=args.port, credentials=credentials
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print(f"[{args.device}] Ket noi {args.host}:{args.port}, queue: {QUEUE_NAME}")
    try:
        while True:
            payload = {
                "device_id": args.device,
                "temperature": round(random.uniform(25.0, 38.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
            body = json.dumps(payload)
            channel.basic_publish(
                exchange="",                
                routing_key=QUEUE_NAME,      
                body=body,
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2,        
                ),
            )
            print(f"Da gui: {body}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDung producer.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()