import pika
import json
import queries

def main():
    connection = pika.BlockingConnection(parameters = pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare('hello2')
    def callback(channel,method,properties,body):
        print(f"Received Message :{body}")

        body = body
        insert_update_response = queries.insert_acknowledgement(body,"listener-1")
        

    channel.basic_consume(
        queue='hello2',
        auto_ack=True,
        on_message_callback=callback
    )
    print("Waiting for message ")
    channel.start_consuming()


if __name__=="__main__":
    main()