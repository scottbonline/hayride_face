import pprint
import os
import boto3
import sys
import cv2
import time

'''
- Need to have AWS creds
- Need to have rekog collection created
'''

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def grab_a_pic():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    s, im = cam.read()
    cv2.imwrite('face.jpg', im)

    with open('face.jpg', 'rb') as source_image:
        source_bytes = source_image.read()

    return source_bytes


def who_is_this(pic_bytes, collection):

    try:
        person_details = client.search_faces_by_image(
            CollectionId=collection,
            Image={
                'Bytes': pic_bytes,
            },
            FaceMatchThreshold=50.0
        )
    except:
        person_details = 'no face found'
        return person_details, False, pic_bytes

    if person_details['FaceMatches']:
        # if we find someone we know, lets get details
        face_details = client.detect_faces(
            Image={
                'Bytes': pic_bytes,
            },
            Attributes=['ALL']
        )
    else:
        person_details = 'unknown face'
        face_details = False

    return person_details, face_details, pic_bytes


def detail_parser(person_details, face_details):
    if person_details == 'unknown face':
        print 'I see you, but not sure who you are'
        return
    elif person_details == 'no face found':
        print 'I do not see a face'
        return
    else:
        name = person_details['FaceMatches'][0]['Face']['ExternalImageId']
        name_certainty = person_details['FaceMatches'][0]['Similarity']
        mental_state = face_details['FaceDetails'][0]['Emotions'][0]['Type'].lower()
        print "Hello %s, I'm %s%% sure it is you!" % (name, name_certainty)

        print 'You appear %s today' % mental_state
        print ''

    return


if __name__ == '__main__':
    # create boto connection to rekog
    client = boto3.client('rekognition')

    count = 1
    while count < 7:
        start = time.time()

        # grab a pic, try to identify, and get details about face
        person_details, face_details, pic_bytes = who_is_this(grab_a_pic(), 'myphotos')

        # interpret the face data and make assertions about the person
        detail_parser(person_details, face_details)

        #pprint.pprint(face_details)

        end = time.time()
        print 'elapsed time:'
        print(end - start)
        count += 1

