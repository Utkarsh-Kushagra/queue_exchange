CREATE DATABASE test_rabbit;

USE test_rabbit;

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

