import pprint
import os
import boto3

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def add_faces(image_file, person, collection):
    # create boto connection to rekog
    client = boto3.client('rekognition')

    # create collection
    # garbage code, need to fix
    try:
        response = client.create_collection(
            CollectionId='myphotos',
        )
    except:
        pass

    with open(image_file, 'rb') as target_image:
        image_bytes = target_image.read()

    response = client.index_faces(
        CollectionId=collection,
        Image={'Bytes': image_bytes},
        ExternalImageId=person,
        DetectionAttributes=['ALL']
    )
    return response

def main():
    # add faces
    #response = add_faces('scott.jpg', 'scott', 'myphotos')
    #pprint.pprint(response)

    # list faces
    #response = client.list_faces(
    #    CollectionId='myphotos'
    #)
    #pprint.pprint(response)

'''
    response = client.compare_faces(
                   SourceImage={ 'Bytes': source_bytes },
                   TargetImage={ 'Bytes': target_bytes },
                   SimilarityThreshold=SIMILARITY_THRESHOLD
    )
'''
if __name__ == '__main__':
    main()