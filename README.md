# queue_exchange

** RABBITMQ should be running on docker service (pd-thirdparty-services)

1. pip install -r requirements.txt
2. Run listener-service : uvicorn main:app --host 0.0.0.0 --port 5000 --reload-dir ./--reload --env-file ./dev.env
3. Run publisher-service : uvicorn main:app --host 0.0.0.0 --port 5001 --reload-dir ./--reload --env-file ./dev.env
4. Run python script : python run_test.py 

Check app.log for istener-service and publisher-service

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


