import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
import random
import string
import pygame

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier
from fingerImageDisplayer import fingerImageDisplayer

class GestureRecognizer():
    def __init__(self, lang):
        self.lang = lang

    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        parser.add_argument('--use_static_image_mode', action='store_true')
        parser.add_argument("--min_detection_confidence",
                            help='min_detection_confidence',
                            type=float,
                            default=0.7)
        parser.add_argument("--min_tracking_confidence",
                            help='min_tracking_confidence',
                            type=int,
                            default=0.5)

        args = parser.parse_args()

        return args
    
    def cvimage_to_pygame(self, image):
        """Convert cvimage into a pygame image"""
        return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],
                                    "BGR")  
    

    def initialize(self):
        args = self.get_args()
        self.cap_device = args.device
        self.cap_width = args.width
        self.cap_height = args.height
        self.use_static_image_mode = args.use_static_image_mode
        self.min_detection_confidence = args.min_detection_confidence
        self.min_tracking_confidence = args.min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        self.keypoint_classifier = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier.tflite')
        self.keypoint_classifier_single = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier_SingleHand.tflite')

        self.point_history_classifier = PointHistoryClassifier()

        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]
        with open('model/keypoint_classifier/keypoint_classifier_label_singleHand.csv',
                encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels_singleHand = csv.reader(f)
            self.keypoint_classifier_labels_singleHand = [
                row[0] for row in self.keypoint_classifier_labels_singleHand
            ]
        with open(
                'model/point_history_classifier/point_history_classifier_label.csv',
                encoding='utf-8-sig') as f:
            self.point_history_classifier_labels = csv.reader(f)
            self.point_history_classifier_labels = [
                row[0] for row in self.point_history_classifier_labels
            ]
        
        #self.cap = cv.VideoCapture(self.cap_device)
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)




    
    def detectLetter(self, surface, w, h, target):
    # Argument parsing #################################################################
        args = self.get_args()
        '''
        cap_device = args.device
        cap_width = args.width
        cap_height = args.height

        use_static_image_mode = args.use_static_image_mode
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence'''

        use_brect = True

        # Camera preparation ###############################################################
        cap = cv.VideoCapture(self.cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        # Model load #############################################################
        '''mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=self.use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        keypoint_classifier = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier.tflite')
        keypoint_classifier_single = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier_SingleHand.tflite')

        point_history_classifier = PointHistoryClassifier()

        # Read labels ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        with open('model/keypoint_classifier/keypoint_classifier_label_singleHand.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels_singleHand = csv.reader(f)
            keypoint_classifier_labels_singleHand = [
                row[0] for row in keypoint_classifier_labels_singleHand
            ]
        with open(
                'model/point_history_classifier/point_history_classifier_label.csv',
                encoding='utf-8-sig') as f:
            point_history_classifier_labels = csv.reader(f)
            point_history_classifier_labels = [
                row[0] for row in point_history_classifier_labels
            ]
'''
        # FPS Measurement ########################################################
        cvFpsCalc = CvFpsCalc(buffer_len=10)

        # Coordinate history #################################################################
        history_length = 16
        point_history = deque(maxlen=history_length)

        # Finger gesture history ################################################
        finger_gesture_history = deque(maxlen=history_length)
        finger_gesture_historySingle = deque(maxlen=history_length)

        #  ########################################################################
        # 'game settings'
        detectedSign = deque(maxlen=20)

        for i in range(20):
            detectedSign.append(1000)


        print("target is = " + target)
        print("the number is = " + str(string.ascii_uppercase.index(target)))
        imageDisplayer = fingerImageDisplayer("Eng", string.ascii_uppercase.index(target))

        #
        mode = 0
        index = 10000
        detected = True    
        detecting = True

        msg = target

        while detecting:
            fps = cvFpsCalc.get()

            # Process Key (ESC: end) #################################################
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
            if key == 8:
                imageDisplayer.skipCurrent()
            number, mode = self.select_mode(key, mode)

            # Camera capture #####################################################
            ret, image = cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            # Detection implementation #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if (detected == True):
                detected = False
                detectedSign.clear
                for i in range(len(detectedSign)):
                    detectedSign.append(1000)
                    i+=1

            if results.multi_hand_landmarks is not None:
                if len(results.multi_hand_landmarks) == 2:
                    indexHand = 0
                    for hand in results.multi_handedness:
                        handType = hand.classification[0].label
                        if(indexHand == 0 and handType == "Left"):
                        # print("Right was first")
                            temp = results.multi_hand_landmarks[0]
                            results.multi_hand_landmarks[0] = results.multi_hand_landmarks[1]
                            results.multi_hand_landmarks[1] = temp
                            temp2 = results.multi_handedness[0]
                            results.multi_handedness[0] = results.multi_handedness[1]
                            results.multi_handedness[0] = temp2
                            temp3 = results.multi_hand_world_landmarks[0]
                            results.multi_hand_world_landmarks[0] = results.multi_hand_world_landmarks[1]
                            results.multi_hand_world_landmarks[1] = temp3
                            break
                        indexHand = indexHand+1

                        
            #  ####################################################################
            if results.multi_hand_landmarks is not None:
                if len(results.multi_hand_landmarks) == 1:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                        
                        # Bounding box calculation
                        brect = self.calc_bounding_rect(debug_image, hand_landmarks)

                        # Landmark calculation
                        landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                        # Conversion to relative coordinates / normalized coordinates
                        pre_processed_landmark_list = self.pre_process_landmark(landmark_list)
                        pre_processed_point_history_list_Single = self.pre_process_point_history(debug_image, point_history)

                        # Write to the dataset file
                        self.logging_csv(number, mode, pre_processed_landmark_list,
                                    pre_processed_point_history_list_Single)

                        # Hand sign classification
                        hand_sign_id = self.keypoint_classifier_single(pre_processed_landmark_list)
                        if hand_sign_id == 'Ignore this for now':  # Point gesture
                            #point_history.append(landmark_list[8])
                            break
                        else:
                            point_history.append([0, 0])


                        if(hand_sign_id == 0):
                            detected_Hand_Sign = hand_sign_id +2
                            detectedSign.append(detected_Hand_Sign)
                        else:
                            detected_Hand_Sign = hand_sign_id + 50
                            detectedSign.append(detected_Hand_Sign)

                        # Finger gesture classification
                        finger_gesture_id = 0
                        point_history_len = len(pre_processed_point_history_list_Single)
                        if point_history_len == (history_length * 2):
                            finger_gesture_id = self.point_history_classifier(
                                pre_processed_point_history_list_Single)

                        # Calculates the gesture IDs in the latest detection
                        finger_gesture_historySingle.append(finger_gesture_id)
                        most_common_fg_idSingle = Counter(finger_gesture_historySingle).most_common()

                        # Drawing part
                        debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)
                        debug_image = self.draw_landmarks(debug_image, landmark_list)
                        debug_image = self.draw_info_text(
                            debug_image,
                            brect,
                            handedness,
                            self.keypoint_classifier_labels_singleHand[hand_sign_id],
                            self.point_history_classifier_labels[most_common_fg_idSingle[0][0]],)
                elif len(results.multi_hand_landmarks) == 2:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        
                        '''
                        print("Hand landmarks")
                        print(hand_landmarks)
                        print("Handedness")
                        print(handedness)
                        print("multi_handedness")
                        print(results.multi_handedness)'''

                        newLandMarkList = []
                        for handsMarks in results.multi_hand_landmarks:
                            for _, landmark in enumerate(handsMarks.landmark):
                                newLandMarkList.append(landmark)

                        # Bounding box calculation
                        testBrect = self.calc_bounding_rect2(debug_image, newLandMarkList)
                        #brect = calc_bounding_rect(debug_image, hand_landmarks)

                        # Landmark calculation
                        landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
                        testLandmark_list = self.calc_landmark_list2(debug_image, newLandMarkList)

                        # Conversion to relative coordinates / normalized coordinates
                        #pre_processed_landmark_listOld = pre_process_landmark(landmark_list)
                        pre_processed_landmark_listNew = []
                        pre_processed_landmark_listNew = self.pre_process_landmark2(testLandmark_list)
                        pre_processed_point_history_list = self.pre_process_point_history(debug_image, point_history)
                        
                        # Write to the dataset file
                        self.logging_csv(number, mode, pre_processed_landmark_listNew,
                                    pre_processed_point_history_list)

                        # Hand sign classification
                        hand_sign_id = self.keypoint_classifier(pre_processed_landmark_listNew)
                        #if hand_sign_id == 'Ignore this for now':  # Point gesture
                            #point_history.append(landmark_list[8])
                        #    break
                        #else:
                            #point_history.append([0, 0])
                        


                        if(hand_sign_id >= 2):
                            detected_Hand_Sign = hand_sign_id + 1
                            #print("detected sign = " + str(detected_Hand_Sign))
                            #print("expected sign = " + str(imageDisplayer.number))
                            if(detected_Hand_Sign == imageDisplayer.number):
                                #print("Success")
                                detectedSign.append(detected_Hand_Sign)
                            else:
                                detectedSign.append(1000)

                        else:
                            detected_Hand_Sign = hand_sign_id
                            if(detected_Hand_Sign == imageDisplayer.number):
                                #print("Success")
                                detectedSign.append(detected_Hand_Sign)
                            else:
                                detectedSign.append(1000)

                        #print(hand_sign_id)

                        # Finger gesture classification
                        finger_gesture_id = 0
                        point_history_len = len(pre_processed_point_history_list)
                        if point_history_len == (history_length * 2):
                            finger_gesture_id = self.point_history_classifier(
                                pre_processed_point_history_list)

                        # Calculates the gesture IDs in the latest detection
                        finger_gesture_history.append(finger_gesture_id)
                        most_common_fg_id = Counter(finger_gesture_history).most_common()

                        # Drawing part
                        #debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                        debug_image = self.draw_bounding_rect(use_brect, debug_image, testBrect)
                        debug_image = self.draw_landmarks(debug_image, landmark_list)
                        #debug_image = draw_landmarks(debug_image, newLandMarkList)
                        '''debug_image = draw_info_text(
                            debug_image,
                            brect,
                            handedness,
                            keypoint_classifier_labels[hand_sign_id],
                            point_history_classifier_labels[most_common_fg_id[0][0]],
                        )'''
                        debug_image = self.draw_info_text(
                            debug_image,
                            testBrect,
                            handedness,
                            self.keypoint_classifier_labels[hand_sign_id],
                            self.point_history_classifier_labels[most_common_fg_id[0][0]],
                        )   
                        newLandMarkList.clear()
                        
            else:
                point_history.append([0, 0])
                detectedSign.append(1000)

            #print(len(point_history))
            debug_image = self.draw_point_history(debug_image, point_history)
            debug_image = self.draw_info(debug_image, fps, mode, number)

            py_debug_image = self.cvimage_to_pygame(debug_image)
            py_debug_image_rezied = self.resizeImage(py_debug_image, 1.5)


            # Screen reflection #############################################################
            #cv.imshow('Hand Gesture Recognition', debug_image)
            
            if(self.checkIfCorrectSign(detectedSign, string.ascii_uppercase.index(target)) == True):
                print("correct letter found")
                detected = True
                detecting = False

            surface.blit(py_debug_image_rezied, ((w/2, h/2+100)))
            pygame.display.update()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        cap.release()
        cv.destroyAllWindows()
        return True

    def detectWord(self, surface, w, h, target):
    # Argument parsing #################################################################
        '''args = self.get_args()

        cap_device = args.device
        cap_width = args.width
        cap_height = args.height

        use_static_image_mode = args.use_static_image_mode
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence
'''
        use_brect = True

        # Camera preparation ###############################################################
        cap = cv.VideoCapture(self.cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        # Model load #############################################################
        '''mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        keypoint_classifier = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier.tflite')
        keypoint_classifier_single = KeyPointClassifier(model_path='model/keypoint_classifier/keypoint_classifier_SingleHand.tflite')

        point_history_classifier = PointHistoryClassifier()

        # Read labels ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        with open('model/keypoint_classifier/keypoint_classifier_label_singleHand.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels_singleHand = csv.reader(f)
            keypoint_classifier_labels_singleHand = [
                row[0] for row in keypoint_classifier_labels_singleHand
            ]
        with open(
                'model/point_history_classifier/point_history_classifier_label.csv',
                encoding='utf-8-sig') as f:
            point_history_classifier_labels = csv.reader(f)
            point_history_classifier_labels = [
                row[0] for row in point_history_classifier_labels
            ]'''

        # FPS Measurement ########################################################
        cvFpsCalc = CvFpsCalc(buffer_len=10)

        # Coordinate history #################################################################
        history_length = 16
        point_history = deque(maxlen=history_length)

        # Finger gesture history ################################################
        finger_gesture_history = deque(maxlen=history_length)
        finger_gesture_historySingle = deque(maxlen=history_length)

        #  ########################################################################
        # 'game settings'
        detectedSign = deque(maxlen=20)

        
        for i in range(20):
            detectedSign.append(1000)

        imageDisplayer = fingerImageDisplayer("Eng", string.ascii_uppercase.index(target[0]))

        #
        mode = 0
        index = 10000
        detected = True    
        detecting = True

        msg = target

        while detecting:
            fps = cvFpsCalc.get()

            # Process Key (ESC: end) #################################################
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
            if key == 8:
                imageDisplayer.skipCurrent()
            number, mode = self.select_mode(key, mode)

            # Camera capture #####################################################
            ret, image = cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            # Detection implementation #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if (index > len(msg)):
                index = 0

            if (detected == True):
                detected = False
                detectedSign.clear
                for i in range(10):
                    detectedSign.append(1000)
                    i+=1

            if results.multi_hand_landmarks is not None:
                if len(results.multi_hand_landmarks) == 2:
                    indexHand = 0
                    for hand in results.multi_handedness:
                        handType = hand.classification[0].label
                        if(indexHand == 0 and handType == "Left"):
                        # print("Right was first")
                            temp = results.multi_hand_landmarks[0]
                            results.multi_hand_landmarks[0] = results.multi_hand_landmarks[1]
                            results.multi_hand_landmarks[1] = temp
                            temp2 = results.multi_handedness[0]
                            results.multi_handedness[0] = results.multi_handedness[1]
                            results.multi_handedness[0] = temp2
                            temp3 = results.multi_hand_world_landmarks[0]
                            results.multi_hand_world_landmarks[0] = results.multi_hand_world_landmarks[1]
                            results.multi_hand_world_landmarks[1] = temp3
                            break
                        indexHand = indexHand+1

                        
            #  ####################################################################
            if results.multi_hand_landmarks is not None:
                if len(results.multi_hand_landmarks) == 1:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                        # Bounding box calculation
                        brect = self.calc_bounding_rect(debug_image, hand_landmarks)

                        # Landmark calculation
                        landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                        # Conversion to relative coordinates / normalized coordinates
                        pre_processed_landmark_list = self.pre_process_landmark(landmark_list)
                        pre_processed_point_history_list_Single = self.pre_process_point_history(debug_image, point_history)

                        # Write to the dataset file
                        self.logging_csv(number, mode, pre_processed_landmark_list,
                                    pre_processed_point_history_list_Single)

                        # Hand sign classification
                        hand_sign_id = self.keypoint_classifier_single(pre_processed_landmark_list)
                        if hand_sign_id == 'Ignore this for now':  # Point gesture
                            #point_history.append(landmark_list[8])
                            break
                        else:
                            point_history.append([0, 0])

                        if(hand_sign_id == 0):
                            detected_Hand_Sign = hand_sign_id +2
                            detectedSign.append(detected_Hand_Sign)
                        else:
                            detected_Hand_Sign = hand_sign_id + 50
                            detectedSign.append(detected_Hand_Sign)

                        # Finger gesture classification
                        finger_gesture_id = 0
                        point_history_len = len(pre_processed_point_history_list_Single)
                        if point_history_len == (history_length * 2):
                            finger_gesture_id = self.point_history_classifier(
                                pre_processed_point_history_list_Single)

                        # Calculates the gesture IDs in the latest detection
                        finger_gesture_historySingle.append(finger_gesture_id)
                        most_common_fg_idSingle = Counter(finger_gesture_historySingle).most_common()

                        # Drawing part
                        debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)
                        debug_image = self.draw_landmarks(debug_image, landmark_list)
                        debug_image = self.draw_info_text(
                            debug_image,
                            brect,
                            handedness,
                            self.keypoint_classifier_labels_singleHand[hand_sign_id],
                            self.point_history_classifier_labels[most_common_fg_idSingle[0][0]],)
                elif len(results.multi_hand_landmarks) == 2:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        
                        '''
                        print("Hand landmarks")
                        print(hand_landmarks)
                        print("Handedness")
                        print(handedness)
                        print("multi_handedness")
                        print(results.multi_handedness)'''

                        newLandMarkList = []
                        for handsMarks in results.multi_hand_landmarks:
                            for _, landmark in enumerate(handsMarks.landmark):
                                newLandMarkList.append(landmark)

                        # Bounding box calculation
                        testBrect = self.calc_bounding_rect2(debug_image, newLandMarkList)
                        #brect = calc_bounding_rect(debug_image, hand_landmarks)

                        # Landmark calculation
                        landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
                        testLandmark_list = self.calc_landmark_list2(debug_image, newLandMarkList)

                        # Conversion to relative coordinates / normalized coordinates
                        #pre_processed_landmark_listOld = pre_process_landmark(landmark_list)
                        pre_processed_landmark_listNew = []
                        pre_processed_landmark_listNew = self.pre_process_landmark2(testLandmark_list)
                        pre_processed_point_history_list = self.pre_process_point_history(debug_image, point_history)
                        
                        # Write to the dataset file
                        self.logging_csv(number, mode, pre_processed_landmark_listNew,
                                    pre_processed_point_history_list)

                        # Hand sign classification
                        hand_sign_id = self.keypoint_classifier(pre_processed_landmark_listNew)
                        #if hand_sign_id == 'Ignore this for now':  # Point gesture
                            #point_history.append(landmark_list[8])
                        #    break
                        #else:
                            #point_history.append([0, 0])
                    
                        if(hand_sign_id >= 2):
                            detected_Hand_Sign = hand_sign_id + 1
                            #print("detected sign = " + str(detected_Hand_Sign))
                            #print("expected sign = " + str(imageDisplayer.number))
                            if(detected_Hand_Sign == imageDisplayer.number):
                                #print("Success")
                                detectedSign.append(detected_Hand_Sign)
                            else:
                                detectedSign.append(1000)

                        else:
                            detected_Hand_Sign = hand_sign_id
                            if(detected_Hand_Sign == imageDisplayer.number):
                                #print("Success")
                                detectedSign.append(detected_Hand_Sign)
                            else:
                                detectedSign.append(1000)

                        #print(hand_sign_id)

                        # Finger gesture classification
                        finger_gesture_id = 0
                        point_history_len = len(pre_processed_point_history_list)
                        if point_history_len == (history_length * 2):
                            finger_gesture_id = self.point_history_classifier(
                                pre_processed_point_history_list)

                        # Calculates the gesture IDs in the latest detection
                        finger_gesture_history.append(finger_gesture_id)
                        most_common_fg_id = Counter(finger_gesture_history).most_common()

                        # Drawing part
                        #debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                        debug_image = self.draw_bounding_rect(use_brect, debug_image, testBrect)
                        debug_image = self.draw_landmarks(debug_image, landmark_list)
                        #debug_image = draw_landmarks(debug_image, newLandMarkList)
                        '''debug_image = draw_info_text(
                            debug_image,
                            brect,
                            handedness,
                            keypoint_classifier_labels[hand_sign_id],
                            point_history_classifier_labels[most_common_fg_id[0][0]],
                        )'''
                        debug_image = self.draw_info_text(
                            debug_image,
                            testBrect,
                            handedness,
                            self.keypoint_classifier_labels[hand_sign_id],
                            self.point_history_classifier_labels[most_common_fg_id[0][0]],
                        )   
                        newLandMarkList.clear()
                        
            else:
                point_history.append([0, 0])
                detectedSign.append(1000)

            #print(len(point_history))
            debug_image = self.draw_point_history(debug_image, point_history)
            debug_image = self.draw_info(debug_image, fps, mode, number)

            py_debug_image = self.cvimage_to_pygame(debug_image)
            py_debug_image_rezied = self.resizeImage(py_debug_image, 1.5)


            # Screen reflection #############################################################
            #cv.imshow('Hand Gesture Recognition', debug_image)
            
            if(self.checkIfCorrectSign(detectedSign, string.ascii_uppercase.index(msg[index])) == True):
                print("correct letter found")
                detected = True
                index = index + 1

                if (index >= len(msg)):
                    detecting = False
                else:
                    imageDisplayer.number = string.ascii_uppercase.index(msg[index])

            surface.blit(py_debug_image_rezied, ((w/2, h/2+100)))
            pygame.display.update()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        cap.release()
        cv.destroyAllWindows()
        return True

    def resizeImage(self, img, scaleFactor):
        resized = pygame.transform.scale(img, (img.get_width()/scaleFactor, img.get_height()/scaleFactor))
        return resized
    
    def checkIfCorrectSign(self, detected, target):
        rounded = self.getRounded(detected)
        #print("Rounded = " + str(rounded))
        if rounded == target:
            return True
        else:
            return False

    def getRounded(self, detected):
        avg = sum(detected)/len(detected)
        rounded = round(avg)
        #print(rounded)
        return rounded
    
    def select_mode(self, key, mode):
        number = -1
        if 48 <= key <= 57:  # 0 ~ 9
            number = key - 48
        if key == 110:  # n
            mode = 0
        if key == 107:  # k
            print("in key logging mode")
            mode = 1
        if key == 104:  # h
            mode = 2        
        if key == 32:
            #Skipped H = 6, J = 8
            '''
            A=0
            B=1
            D=2
            E=3
            F=4
            G=5
            H=6
            I=7
            J=8
            K=9
            L=10
            M=11
            N=12
            O=13
            P=14
            Q=15
            R=16
            S=17
            T=18
            U=19
            V=20
            W=21
            X=22
            Y=23
            Z=24        
            '''
            number = 8
        return number, mode

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def calc_bounding_rect2(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for landmark in landmarks:
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def calc_landmark_list2(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for landmark in landmarks:
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def pre_process_landmark2(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def pre_process_point_history(self, image, point_history):
        image_width, image_height = image.shape[1], image.shape[0]

        temp_point_history = copy.deepcopy(point_history)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]

            temp_point_history[index][0] = (temp_point_history[index][0] -
                                            base_x) / image_width
            temp_point_history[index][1] = (temp_point_history[index][1] -
                                            base_y) / image_height

        # Convert to a one-dimensional list
        temp_point_history = list(
            itertools.chain.from_iterable(temp_point_history))

        return temp_point_history

    def logging_csv(self, number, mode, landmark_list, point_history_list):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 25) and len(landmark_list) > 50:
            csv_path = 'model/keypoint_classifier/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 1 and (0 <= number <= 25) and len(landmark_list) < 50:
            csv_path = 'model/keypoint_classifier/keypoint_singlehand.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 2 and (0 <= number <= 9):
            csv_path = 'model/point_history_classifier/point_history.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *point_history_list])
        return

    def draw_landmarks(self, image, landmark_point):
        if len(landmark_point) > 0:
            # Thumb
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (255, 255, 255), 2)

            # Index finger
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (255, 255, 255), 2)

            # Middle finger
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (255, 255, 255), 2)

            # Ring finger
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (255, 255, 255), 2)

            # Little finger
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (255, 255, 255), 2)

            # Palm
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (255, 255, 255), 2)

        # Key Points
        for index, landmark in enumerate(landmark_point):
            if index == 0:  # 手首1
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 1:  # 手首2
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 2:  # 親指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 3:  # 親指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 4:  # 親指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 5:  # 人差指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 6:  # 人差指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 7:  # 人差指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 8:  # 人差指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 9:  # 中指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 10:  # 中指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 11:  # 中指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 12:  # 中指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 13:  # 薬指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 14:  # 薬指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 15:  # 薬指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 16:  # 薬指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 17:  # 小指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 18:  # 小指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 19:  # 小指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 20:  # 小指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        return image

    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            # Outer rectangle
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                        (0, 0, 0), 1)

        return image

    def draw_info_text(self, image, brect, handedness, hand_sign_text,
                    finger_gesture_text='Hi'):
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                    (0, 0, 0), -1)

        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ':' + hand_sign_text
        cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

        '''if finger_gesture_text != "":
            cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
            cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv.LINE_AA)'''

        return image

    def draw_point_history(self, image, point_history):
        for index, point in enumerate(point_history):
            if point[0] != 0 and point[1] != 0:
                cv.circle(image, (point[0], point[1]), 1 + int(index / 2),
                        (152, 251, 152), 2)

        return image

    def draw_info(self, image, fps, mode, number):
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, cv.LINE_AA)

        mode_string = ['Logging Key Point', 'Logging Point History']
        if 1 <= mode <= 2:
            cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv.LINE_AA)
            if 0 <= number <= 25:
                cv.putText(image, "NUM:" + str(number), (10, 110),
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                        cv.LINE_AA)
        return image