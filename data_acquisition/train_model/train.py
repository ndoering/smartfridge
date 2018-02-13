from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from glob import glob
import os

def main():
    '''
    bulk upload images of different categories to clarifai to train model
    '''
    app = ClarifaiApp(api_key='b9a2de7676aa4fadb74a5c59ea15ecba')

    # banana_fresh
    image_set = create_image_set('train_images/01banana_fresh',
                                ['banana_fresh'])
    app.inputs.bulk_create_images(image_set)
    print("banana_fresh uploaded")

    # banana_fresh-neutral
    image_set = create_image_set('train_images/02banana_fresh-neutral',
                                ['banana_fresh-neutral'])
    app.inputs.bulk_create_images(image_set)
    print("banana_fresh-neutral uploaded")

    # banana_neutral
    image_set = create_image_set('train_images/03banana_neutral',
                                ['banana_neutral'])
    app.inputs.bulk_create_images(image_set)
    print("banana_neutral uploaded")

    # banana_neutral-bad
    image_set = create_image_set('train_images/04banana_neutral-bad',
                                ['banana_neutral-bad'])
    app.inputs.bulk_create_images(image_set)
    print("banana_neutral-bad uploaded")

    # banana_bad
    image_set = create_image_set('train_images/05banana_bad',
                                ['banana_bad'])
    app.inputs.bulk_create_images(image_set)
    print("banana_bad uploaded")

    '''
    # TOMATO DATASET NOT BIG ENOUGH YET
    # tomato_fresh
    image_set = create_image_set('train_images/01tomato_fresh',
                                ['tomato_fresh'])
    app.inputs.bulk_create_images(image_set)
    print("tomato_fresh uploaded")

    # tomato_fresh-neutral
    image_set = create_image_set('train_images/02tomato_fresh-neutral',
                                ['tomato_fresh-neutral'])
    app.inputs.bulk_create_images(image_set)
    print("tomato_fresh-neutral uploaded")

    # tomato_neutral
    image_set = create_image_set('train_images/03tomato_neutral',
                                ['tomato_neutral'])
    app.inputs.bulk_create_images(image_set)
    print("tomato_neutral uploaded")

    # tomato_neutral-bad
    image_set = create_image_set('train_images/04tomato_neutral-bad',
                                ['tomato_neutral-bad'])
    app.inputs.bulk_create_images(image_set)
    print("tomato_neutral-bad uploaded")

    # tomato_bad
    image_set = create_image_set('train_images/05tomato_bad',
                                ['tomato_bad'])
    app.inputs.bulk_create_images(image_set)
    print("tomato_bad uploaded")
    '''

    print("Upload finished.")

def create_image_set(img_path, concepts):
    '''
    creates a set of jpg images for upload to clarifai
    '''
    images = []
    for file_path in glob(os.path.join(img_path, '*.jpg')):
        img = ClImage(filename=file_path, concepts=concepts)
        images.append(img)

    return images

if __name__ == '__main__':
    main()
    # don't close terminal window unless "enter" is pressed
    input()
