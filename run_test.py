import requests
import time
import json

def run_publisher(number_of_messages):
    url = 'http://localhost:7000/publisher-service/send-message'
    count = 0
    #while count<number_of_messages:
        # if count % 10==0:
        #     try:
        #         a= 1/0
        #         print(a)
        #     except:
        #         count=count+1
        #         print(f"Not able to publish {count}")
        
    message = f'Sending {count+1}'
    payload={"message": number_of_messages}
    response = requests.request("POST", url, data=payload)
    count+=1
    
    return count


if __name__=="__main__":
    number_of_messages = int(input('Enter No. of Conversation Objects to make:'))
    #delay = int(input('Enter delay between messages (in milliseconds):'))

    total_messages_published = run_publisher(number_of_messages)




