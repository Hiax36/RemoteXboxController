import vgamepad as vg
import time
import socket
import public_ip as ip
import pickle
import sys
import traceback



#server
try:
    EXTERNAL_IP = "0.0.0.0"
    PORT = 25565

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    gamepad = vg.VX360Gamepad()

    s.bind((EXTERNAL_IP,PORT))
    print("Listening for connection...")
    s.listen()
    conn, addr = s.accept()
    print("Connected!")

    data = b''
    allinputs = dict()
    while True:
        data = conn.recv(512)
        if data:
            print(data)
            print("data is length " + str(len(data)) + " bytes")
            data = bytearray(data)
            for i in range(len(data) - 1,0,-1):
                if data[i] == 255:
                    data = data[:i]
                else:
                    break
            print("truncated to " + str(data) + " with length " + str(len(data)) + " bytes")
            data = bytes(data)
            allinputs = pickle.loads(data)
        #print(allinputs)
        for item in allinputs:
            #print(item)
            if isinstance(item,str):
                if item == "joystickl":
                    gamepad.left_joystick_float(x_value_float=allinputs[item][0],y_value_float=allinputs[item][1])
                elif item == "joystickr":
                    gamepad.right_joystick_float(x_value_float=allinputs[item][0],y_value_float=allinputs[item][1])
                elif item == "lefttrig":
                    gamepad.left_trigger_float(allinputs[item])
                elif item == "righttrig":
                    gamepad.right_trigger_float(allinputs[item])
            else:
                if allinputs[item]:
                    gamepad.press_button(item)
                else:
                    gamepad.release_button(item)
        gamepad.update()
except:
    traceback.print_exc()
    print("Error, connection closing...")
    s.close()
    sys.exit()