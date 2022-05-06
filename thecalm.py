from asyncore import poll
from thecalm_impl import *
from parsing import parsing as parser
if __name__ == "__main__":
    epcServer = EPCServer
    epcServer.init_server()
    poll_again = True
    while (poll_again):
        decoded, poll_again = epcServer.get_packet()
        # epcServer.close_server()
        if (decoded):
            (type, value) = S1AP.S1AP_PDU_Descriptions.S1AP_PDU()
            if type == 'initiatingMessage':
                procedure, protocolIEs_list = value['value'][0], value['value'][1]['protocolIEs']
                if procedure == 'S1SetupRequest':
                    if parser.S1SetupRequest(epcServer,protocolIEs_list):
                        parser.S1SetupResponse(epcServer,True)
                    else:
                        parser.S1SetupResponse(epcServer,False)
                elif procedure == 'InitialUEMessage':
                    parser.InitialUEMessage(epcServer,protocolIEs_list)
                else:
                    for i in protocolIEs_list:
                        print(i)
            elif type == 'successfulOutcome':
                procedure, protocolIEs_list = value['value'][0], value['value'][1]['protocolIEs']
                if procedure == 'S1SetupResponse':
                    raise Exception("received message that should be sent by us, not to us")
                else:
                    print("it is not that but instead is",procedure)
                    for i in protocolIEs_list:
                        print(i)
            elif type == 'unsuccessfulOutcome':
                if procedure == 'S1SetupFailure':
                    pass

