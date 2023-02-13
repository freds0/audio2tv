# importing libraries
import argparse
import os
import cv2 
from PIL import Image 
from tqdm import tqdm

def get_mean_size(input_path):
    # Folder which contains all the images
    # from which video is to be generated
      
    mean_height = 0
    mean_width = 0
      
    num_of_images = len(os.listdir(input_path))
    # print(num_of_images)
      
    for file in os.listdir(input_path):
        im = Image.open(os.path.join(input_path, file))
        width, height = im.size
        mean_width += width
        mean_height += height
        # im.show()   # uncomment this for displaying the image
      
    # Finding the mean height and width of all images.
    # This is required because the video frame needs
    # to be set with same width and height. Otherwise
    # images not equal to that width height will not get 
    # embedded into the video
    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)
      
    # print(mean_height)
    # print(mean_width)
  
    return mean_width, mean_height


def resize_images(input_dir, mean_width, mean_height):
    # Resizing of the images to give
    # them same width and height 
    for file in os.listdir('.'):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            # opening image using PIL Image
            im = Image.open(os.path.join(path, file)) 
       
            # im.size includes the height and width of image
            width, height = im.size   
            #print(width, height)
      
            # resizing 
            imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS) 
            imResize.save( file, 'JPEG', quality = 95) # setting quality
            # printing each resized image name
            print(im.filename.split('\\')[-1], " is resized") 
  
  
# Video Generating function
def generate_video(image_folder, video_name='output.avi', duration=40.0):
      
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
     
    total_imgs = len(images)

    # Array images should only consider
    # the image files ignoring others if any
    #print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
    # images per sec
    fps = 20.0 / float(duration) 

    video = cv2.VideoWriter(video_name, 0, fps, (width, height)) 
  
    # Appending the images to the video one by one
    for image in tqdm(images): 
        video.write(cv2.imread(os.path.join(image_folder, image))) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
  
'''
def combine_audio_video(video_filepath, audio_filepath, output_filepath, fps=25):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(video_filepath)
    audio_background = mpe.AudioFileClip(audio_filepath)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_filepath,fps=fps)
'''

def combine_audio_video(video_filepath, audio_filepath, output_filepath):
    import subprocess

    cmd = f'ffmpeg -i {video_filepath} -i {audio_filepath} -c:v copy -c:a aac {output_filepath}'
    subprocess.call(cmd, shell=True)                                     # "Muxing Done
    print('Muxing Done')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-i', '--input_imgs', default='imgs')
    parser.add_argument('-a', '--audio_input', default='audio.mp3')
    parser.add_argument('-d', '--duration', default=40)
    parser.add_argument('-o', '--output_file', default='my_video_clip.avi')
    args = parser.parse_args()

    input_dir = os.path.join(args.base_dir, args.input_imgs)

    # Getting mean images size from input folder
    mean_width, mean_height = get_mean_size(input_dir)

    # Calling the resize images function
    resize_images(input_dir, mean_width, mean_height)

    # Calling the generate_video function
    generate_video(image_folder=input_dir, video_name="temp.avi", duration=args.duration)

    output_filepath = os.path.join(args.base_dir, args.output_file)    

    # Combining audio and video clip
    #combine_audio_video(video_filepath="temp.avi", audio_filepath=args.audio_input, output_filepath=output_filepath, fps=25)
    combine_audio_video(video_filepath="temp.avi", audio_filepath=args.audio_input, output_filepath=output_filepath)

if __name__ == "__main__":
    main()


