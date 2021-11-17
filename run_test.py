import requests
import time
import json

def run_publisher(number_of_messages):
    url = 'http://0.0.0.0:7000/publisher-service/send-message'
    count = 0
    while count<number_of_messages:
        # if count % 10==0:
        #     try:
        #         a= 1/0
        #         print(a)
        #     except:
        #         count=count+1
        #         print(f"Not able to publish {count}")
        
        message = f'Sample message {count+1}'
        
        payload={"message": "Have you had your medicines \n \n*Before breakfast*\n 1. Pan-40 mg\n\n*After breakfast*\n 1. Dolo-650 mg\n 2. Metformin-500 mg\n 3. Concor-5 mg\n", "utterance_before_translation": "Have you had your medicines \n \n*Before breakfast*\n 1. Pan-40 mg\n\n*After breakfast*\n 1. Dolo-650 mg\n 2. Metformin-500 mg\n 3. Concor-5 mg\n", "preset": ["Taken", "Remind Later", "Help"]}
        #time.sleep(100/1000)
        print(f"Dumping Payload::{payload}")
        response = requests.request("POST", url, data=payload)
        print(response.text)
        count+=1
    
    return count


if __name__=="__main__":
    number_of_messages = int(input('Enter No. of messages to publish:'))
    #delay = int(input('Enter delay between messages (in milliseconds):'))

    total_messages_published = run_publisher(number_of_messages)
    print(f'TOTAL MESSAGES PUBLISHED:{total_messages_published}')




