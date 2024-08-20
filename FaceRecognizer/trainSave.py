import face_recognition
import os
import pickle


print('Train a whole folder...')
print(f'Face_Recognition_version: {face_recognition.__version__}')

Encodings = [] # array of encoding
Names = [] # same dimension array of encoding

# expect that traning data be NAMED for face to be found in image ex:"Donald Trump.jpg"
trainingPath = '/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/known'
testingPath = '/home/bubba/Downloads/Python_stuff/FaceRecognizer/demoImages/unknown'


# recursively walk thru every file in ... getting array of files

print(f'Training on data from \"{trainingPath}\"')

for root, dirs, files in os.walk(trainingPath):
#    print(files)
    for filename in files:
        fullpath = os.path.join(root, filename)
#        print(fullpath)
        name = os.path.splitext(filename)[0]  # remove extension leaving just 'person name'
        print(f'Encoding \"{name}\" ')
        person = face_recognition.load_image_file(fullpath)
        encoding = face_recognition.face_encodings(person)[0] # take first person if more than one
        # save off data pair of encoding and name
        Encodings.append(encoding)
        Names.append(name)

if len(Names) > 0:
    print(f'Saving {len(Names)} file encoded data as \"Train.pkl\"')
    with open('Train.pkl','wb') as theFile:
        pickle.dump(Names, theFile)
        pickle.dump(Encodings, theFile)
        theFile.close()
else:
    print("No Training Data was found!")    
