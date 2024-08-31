# CCTV Surveillance App with Face and Object Recognition

## Overview

Welcome to the **CCTV Surveillance App**! This Windows application provides real-time video surveillance by utilizing your webcam or other camera sources, functioning as a CCTV system with advanced AI capabilities. The app not only streams video but also recognizes faces and objects using state-of-the-art machine learning models like **YOLOv8** for object detection and a face recognition model for identifying individuals.

The graphical user interface (GUI) is built using **CustomTkinter**, providing a modern and user-friendly experience.

![Screenshot 2024-08-31 173552](https://github.com/user-attachments/assets/a53dafb5-57c1-47c8-b5ea-ba5affb0b0f3)

### Features

- **Real-Time Video Surveillance:** Stream live video from your webcam or other connected cameras.
- **Face Recognition:** Identify and track known and unknown faces in real-time. Maintain a database of known individuals and update it by adding or removing people.
- **Object Detection:** Detect and classify various objects in the video stream using the YOLOv8 model.
- **Event Logging:** Automatically save logs of detected faces and objects with timestamps for future reference.
- **Image Scanning:** Analyze and recognize faces and objects in static images.
- **Database Management:** Easily manage the list of individuals recognized by the AI, including options to add or remove them from the known persons list.
- **Modern GUI:** The application features a sleek and responsive user interface designed with CustomTkinter.

## Usage

### Real-Time Surveillance

- Launch the app using the command line.
- The main window will display the live video feed from your selected camera.
- Detected faces and objects will be highlighted in real-time, with logs being automatically saved.


### Face Management

- Use the **Face Management** interface to add or remove individuals from the known persons database.
- Simply upload a photo of the individual to add them to the database or remove them from the list of recognized faces.

![Screenshot 2024-08-31 174140](https://github.com/user-attachments/assets/6d4852af-55b6-4d99-b11e-ae892981db53)


### Image Scanning

- Use the **Image Scanning** feature to upload and analyze static images. The app will detect and log any recognized faces or objects within the image.

![Screenshot 2024-08-31 173946](https://github.com/user-attachments/assets/f0f25bfe-dd9d-4c73-8207-ec5532737153)


## YOLOv8 Model

The application uses the YOLOv8 model for object detection. You can download the weights from the official YOLOv8 GitHub repository.

## Logs

All logs are stored in the `log`. Each log entry includes:

- **Timestamp:** When the face/object was detected.
- **Face/Object Details:** Information about the detected face or object.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
