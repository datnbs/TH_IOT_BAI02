import sys
import pika

BROKER_HOST = 'localhost'
EXCHANGE_NAME = 'iot_alert_exchange'
QUEUE_NAME = 'critical_queue'
ROUTING_KEY = 'critical'

def callback(ch, method, properties, body):
  message = body.decode('utf-8')
  print(f'[{QUEUE_NAME}] Da nhan: {message}')

def main():
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=BROKER_HOST)
  )
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
  channel.queue_declare(queue=QUEUE_NAME)
  channel.queue_bind(
      exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY
  )
  print(
      f"[*] Dang lang nghe canh bao muc '{ROUTING_KEY}' tren '{QUEUE_NAME}'."
      ' Nhan Ctrl+C de thoat.'
  )
  channel.basic_consume(
      queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True
  )
  channel.start_consuming()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('\n[!] Da dung Critical Consumer.')
    sys.exit(0)
