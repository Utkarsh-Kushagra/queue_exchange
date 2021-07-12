import requests
import time

def run_publisher(number_of_messages,delay):
    url = 'http://0.0.0.0:5001/publisher-service/send-message'
    count = 0
    while count<number_of_messages:
        message = f'Sample message {count+1}'
        payload={'message': message}
        time.sleep(delay)
        response = requests.request("POST", url, data=payload)
        print(response.text)
        count+=1
    
    return count


if __name__=="__main__":
    number_of_messages = int(input('Enter No. of messages to publish:'))
    delay = int(input('Enter delay between messages (in seconds):'))

    total_messages_published = run_publisher(number_of_messages,delay)
    print(f'TOTAL MESSAGES PUBLISHED:{total_messages_published}')




