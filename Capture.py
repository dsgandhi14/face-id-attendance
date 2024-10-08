def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def capture_image():
    import face_recognition
    import cv2
    import csv
    import Trainer
    import os
    import numpy as np

    known_faces_data = np.load('known-faces-data.npy', allow_pickle=True)
    try:
        known_faces_names, known_faces_ids = zip(*known_faces_data)
    except:
        known_faces_names, known_faces_ids=[],[]
    print("Once Added, the Details of the student such as Face cannot be changed. Proceed with Caution!")
    print("press q to exit from the Camera")
    id = input("Enter new ID:")
    while id in known_faces_ids:
        print("This id already exists. Enter a new id")
        id = input("Enter new id:")
    name = input("Enter new Name:")

    cap = cv2.VideoCapture(0)

    if is_number(id) and name.isalpha():
        process_this_frame = True
        while True:
            ret, frame = cap.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # rgb_small_frame = frame[:, :, ::-1]
            if process_this_frame:
                # Find all the faces in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
            process_this_frame = not process_this_frame


#           Display the Results and Save the Images
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Drawing Rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # saving the captured face in the Student Details in Student Pictures Folder
                cv2.imwrite("StudentDetails" + os.sep + "StudentPictures" + os.sep + name + "." + id +
                            ".jpg", rgb_small_frame)


            # display the frame
            cv2.imshow('frame', frame)
            # wait for 100 milliseconds
            print("hi8")
            if cv2.waitKey(100) & 0xFF == ord('q'):
            # if cv2.waitKey(100):
                print("hi9")
                Trainer.train_image()
                print('exited..\n')
                break

        cap.release()
        cv2.destroyAllWindows()
        row = [id, name]
        with open("StudentDetails" + os.sep + "StudentDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        if is_number(id):
            print("Enter Alphabetical Name")
        if name.isalpha():
            print("Enter Numeric ID")
