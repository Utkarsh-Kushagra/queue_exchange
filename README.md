# queue_exchange

** RABBITMQ should be running on docker service (pd-thirdparty-services)

1. pip install -r requirements.txt
2. Run listener-service : uvicorn main:app --host 0.0.0.0 --port 5000 --reload-dir ./--reload --env-file ./dev.env
3. Run publisher-service : uvicorn main:app --host 0.0.0.0 --port 5001 --reload-dir ./--reload --env-file ./dev.env
4. Run python script : python run_test.py 

Check app.log for istener-service and publisher-service

