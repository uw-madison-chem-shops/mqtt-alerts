import time
import smtplib
from email.message import EmailMessage
from paho.mqtt.client import Client
client = Client()
client.connect("mqtt.chem.wisc.edu")

client.subscribe("homie/zanni-weather-000000/#")
client.subscribe("homie/zanni-weather-000001/#")


img0="https://graphite.chem.wisc.edu/render/?width=586&height=308&target=zanni.weather.*.*.temperature, &from=-1d" #graph of temperature v time, from=-1d is for past day
msg = EmailMessage()
msg["Subject"] = "Laser Room Abnormal Temperature Alert"
msg["From"] = "zannibot@chem.wisc.edu"
msg["To"] = ",".join(["wjeong25@wisc.edu"]) #Zanni group: zanni_group@chem.wisc.edu


def callback(client, userdata, message):
    # this is where you would put your code watching for trigger conditions
    # and trigger your message to be sent (email, SMS...)
    #Following if statement prints temperature of each room (and warning msg and graph if triggered)
    if message.topic == "homie/zanni-weather-000000/bme280/temperature":
        B_W_temp= float(message.payload.split(b' ')[0]) #trims down to just temperature value
        print("Room temperature of Black and Wisconsin: ", B_W_temp)
        if B_W_temp > 21 or B_W_temp < 19: #trigger condition, need to develop into email
            msg.set_content(f"Temperature of laser room with Black and Wisconsin is outside the usual range. Please check the laser room at your earliest convenience. \nTime={time.asctime()} MQTT site: https://mqtt.chem.wisc.edu/zanni/ Temp graph:{img0}")
            with smtplib.SMTP_SSL("localhost") as s:
                s.send_message(msg) #sends email
            time.sleep(3600) #when email is triggered, pauses for 1 hr (to minimize spamming mails)
    elif message.topic == "homie/zanni-weather-000001/bme280/temperature":
        K_P_temp= float(message.payload.split(b' ')[0]) #trims down to just temperature value
        print("Room temperature of Kickapoo and Pecatonica: ", K_P_temp)
        if K_P_temp > 22 or K_P_temp < 21: #trigger condition 2, need to develop into email
            msg.set_content(f"Temperature of laser room with Kickapoo and Pecatonica is outside the usual range. Please check the laser room at your earliest convenience. \nTime={time.asctime()} MQTT site: https://mqtt.chem.wisc.edu/zanni/ Temp graph:{img0}")
            with smtplib.SMTP_SSL("localhost") as s:
                s.send_message(msg) #sends email
            time.sleep(3600) #when email is triggered, pauses for 1 hr (to minimize spamming mails)
    else:
        pass
    
client.on_message = callback

client.loop_forever()
