import pickle
import pygame.event
import pygame.joystick as js
from vgamepad import XUSB_BUTTON
import socket
import traceback
import sys
import pygame
import time
try:
    pygame.init()
    PORT = 25565
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    jscnt = 0
    print("Waiting for Xbox Controller...")
    while jscnt < 1:
        jscnt = js.get_count()
        time.sleep(0.1)
    controller = js.Joystick(0)
    print("Xbox Controller Found!")
    GAMEIP = input("Enter Game IP: ")
    s.connect((GAMEIP,PORT))

    JOYSTICK_DIFF = 20
    cnt = 0

    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.JOYAXISMOTION:

                if cnt >= JOYSTICK_DIFF:
                    cnt = 0

                    controllerData = {

                        XUSB_BUTTON.XUSB_GAMEPAD_A : controller.get_button(0),
                        XUSB_BUTTON.XUSB_GAMEPAD_B : controller.get_button(1),
                        XUSB_BUTTON.XUSB_GAMEPAD_X : controller.get_button(2),
                        XUSB_BUTTON.XUSB_GAMEPAD_Y : controller.get_button(3),
                        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER : controller.get_button(4),
                        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER : controller.get_button(5),
                        XUSB_BUTTON.XUSB_GAMEPAD_BACK : controller.get_button(6),
                        XUSB_BUTTON.XUSB_GAMEPAD_START : controller.get_button(7),
                        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB : controller.get_button(8),
                        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB : controller.get_button(9),
                        XUSB_BUTTON.XUSB_GAMEPAD_GUIDE : controller.get_button(10),

                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP : controller.get_hat(0)[1] == 1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN : controller.get_hat(0)[1] == -1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT : controller.get_hat(0)[0] == -1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT : controller.get_hat(0)[0] == 1,

                        "joystickl" : (controller.get_axis(0), controller.get_axis(1) * -1),
                        "lefttrig" : controller.get_axis(2),
                        "joystickr" : (controller.get_axis(3), controller.get_axis(4) * -1),
                        "righttrig" : controller.get_axis(2)
                    }

                    pickledData = pickle.dumps(controllerData)
                    print(pickledData)
                    pickledData = bytearray(pickledData)
                    
                    while len(pickledData) < 512:
                        pickledData.append(255)
                    pickledData = bytes(pickledData)
                    s.send(pickledData)
                else:
                    cnt += 1
            elif ev.type == pygame.JOYBUTTONDOWN or ev.type == pygame.JOYBUTTONUP or ev.type == pygame.JOYHATMOTION:
                controllerData = {

                        XUSB_BUTTON.XUSB_GAMEPAD_A : controller.get_button(0),
                        XUSB_BUTTON.XUSB_GAMEPAD_B : controller.get_button(1),
                        XUSB_BUTTON.XUSB_GAMEPAD_X : controller.get_button(2),
                        XUSB_BUTTON.XUSB_GAMEPAD_Y : controller.get_button(3),
                        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER : controller.get_button(4),
                        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER : controller.get_button(5),
                        XUSB_BUTTON.XUSB_GAMEPAD_BACK : controller.get_button(6),
                        XUSB_BUTTON.XUSB_GAMEPAD_START : controller.get_button(7),
                        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB : controller.get_button(8),
                        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB : controller.get_button(9),
                        XUSB_BUTTON.XUSB_GAMEPAD_GUIDE : controller.get_button(10),

                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP : controller.get_hat(0)[1] == 1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN : controller.get_hat(0)[1] == -1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT : controller.get_hat(0)[0] == -1,
                        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT : controller.get_hat(0)[0] == 1,

                        "joystickl" : (controller.get_axis(0), controller.get_axis(1) * -1),
                        "lefttrig" : controller.get_axis(2),
                        "joystickr" : (controller.get_axis(3), controller.get_axis(4) * -1),
                        "righttrig" : controller.get_axis(2)
                    }

                pickledData = pickle.dumps(controllerData)
                print(pickledData)
                pickledData = bytearray(pickledData)
                while len(pickledData) < 512:
                    pickledData.append(255)
                pickledData = bytes(pickledData)
                s.send(pickledData)


except:
    traceback.print_exc()
    print("Error, connection closing...")
    s.close()
    sys.exit()