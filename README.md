# queue_exchange

There are 3 services in this 
* publisher_service-run on 7000 port
 uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload-dir ./--reload --env-file ./app/dev.env
* listener_service_chat - run on 5000 port
 uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload-dir ./--reload --env-file ./app/dev.env
* listener_service_db-run on 6000 port
 uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload-dir ./--reload --env-file ./app/dev.env
 Install requirements.txt
 Available in all 3 services
 
Check app.log for extensive logging

## How to replicate the Issue

Run the service on the ports mentioned
Create the Database(test_rabbit) use schema.sql
Now run run_test.py from base directory
On being asked Enter 15 as input for number of conversation objects
This will run 15 threads which will send 100 messages in a loop with a sleep of 2 seconds
code for the thread is available in 
queue_exchange/queue_exchange/publisher_service/app/worker/worker.py

Error to look out for in app.log of publisher_service is 
### Error to look put for
2021-11-26 21:44:59,711 | ERROR  | connection_lost: StreamLostError: ('Transport indicated EOF',) | pika.adapters.base_connection._proto_connection_lost():429 
2021-11-26 21:44:59,711 | INFO   | AMQP stack terminated, failed to connect, or aborted: opened=True, error-arg=StreamLostError: ('Transport indicated EOF',); pending-error=None | pika.connection._on_stream_terminated():1999
2021-11-26 21:44:59,711 | DEBUG  | Removing timer for next heartbeat send interval | pika.heartbeat.stop():138 
2021-11-26 21:44:59,711 | INFO   | RMQ Publisher: Connection is closing or already closed | app.message_exchange.rabbitmq.close_connection():530



# Table Requirement
CREATE DATABASE test_rabbit;

CREATE TABLE `t_rabbitmq_message_tracker` (
  `message_id` varchar(40) NOT NULL,
  `publisher_message` text,
  `publisher_time` datetime(6) DEFAULT NULL,
  `listener_time` datetime(6) DEFAULT NULL,
  `from_service` varchar(25) DEFAULT NULL,
  `to_service` varchar(25) DEFAULT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


