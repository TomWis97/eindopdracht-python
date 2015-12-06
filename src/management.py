from pysimplesoap.client import SoapClient, SoapFault

# create a simple consumer
client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

# call a few remote methods
r1=str(client.get_value(number=1).resultaat)
print "Resultaat number=1 :", r1

r3=str(client.get_value(number=3).resultaat)
print "Resultaat number=3 :", int(r3) # r3 is a number!

r4=str(client.get_value(number=4).resultaat)
print "Resultaat number=4 :", r4.rstrip() # This is a multiline: strip the newline from the result!

r5=str(client.get_value(number=5).resultaat)
print "Resultaat number=5 :", r5.rstrip()

