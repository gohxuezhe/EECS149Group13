import paho.mqtt.publish as publish

f= open("2nd_pi's_camera_picture.jpg","rb")
filecontent = f.read()
byteArr = bytearray(filecontent)

publish.single('topiceecs149', byteArr, qos=1, hostname='broker.hivemq.com')
