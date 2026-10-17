import time
import pika

BROKER_HOST = 'localhost'
EXCHANGE_NAME = 'iot_alert_exchange'

def main():
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=BROKER_HOST)
  )
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
  alerts = [
      ('info', 'He thong cam bien hoat dong binh thuong info'),
      ('warning', 'Nhiet do phong may vuot nguong warning'),
      ('critical', 'Cam bien kho lanh mat ket noi critical'),
  ]
  print(f"[*] Bat dau gui canh bao qua exchange '{EXCHANGE_NAME}'...\n")
  for routing_key, message in alerts:
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message.encode('utf-8'),
    )
    print(f'[x] Da gui [{routing_key}]: {message}')
    time.sleep(1)
  connection.close()
  print('\n[*] Hoan tat gui canh bao.')

if __name__ == '__main__':
  main()