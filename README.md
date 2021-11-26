# queue_exchange

There are 3 services in this 
* publisher_service-run on 7000 port
``` uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload-dir ./--reload --env-file ./app/dev.env
* listener_service_chat - run on 5000 port
``` uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload-dir ./--reload --env-file ./app/dev.env
* listener_service_db-run on 6000 port
``` uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload-dir ./--reload --env-file ./app/dev.env
 Install requirements.txt
 Available in all 3 services
 
Check app.log for extensive logging

## How to replicate the Issue

Run the service on the ports mentioned
Create the Database(test_rabbit) use schema.sql


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


