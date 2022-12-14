import paho.mqtt.publish as publish

f= open("test.jpg")
filecontent = f.read()
byteArr = bytearray(filecontent)

publish.single('topiceecs149', byteArr, qos=1, hostname='m2m.eclipse.org')
