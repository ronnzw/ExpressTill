import os
import time
from datetime import datetime

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from PIL import Image
from pyzbar.pyzbar import decode
from scanner.camera import CameraStreamingWidget


def detect(request):
    stream = CameraStreamingWidget()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    return render(request, 'scanner/detected.html', context={'cam_status': status})

# Camera feed
def camera_feed(request):
    stream = CameraStreamingWidget()
    frames = stream.get_frames()

    # if ajax request is sent
    if request.is_ajax():
        print('Ajax request received')
        time_stamp = str(datetime.now().strftime("%d-%m-%y"))
        image = os.path.join(os.getcwd(), "media",
                             "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            # open image if exists
            im = Image.open(image)
            # decode barcode
            if decode(im):
                for barcode in decode(im):
                    barcode_data = (barcode.data).decode('utf-8')
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    # return decoded barcode as json response
                    return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at})
            else:
                return JsonResponse(data={'barcode_data': None})
        else:
            return JsonResponse(data={'barcode_data': None})
    # else stream the frames from camera feed
    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')

def scanner_page(request):
	return render(request, 'scanner/scanner.html')

def gen(camera):
	while True:
		frame,info_bar = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + info_bar + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')
# Create your views here.
'''




def camera_feed(request):
    stream = CameraStreamingWidget()
    frames = stream.get_frames()

    # if ajax request is sent
    if request.is_ajax():
        print('Ajax request received')
        image = os.path.join(os.getcwd(), "media",
                             "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            # open image if exists
            im = Image.open(image)
            # decode barcode
            if decode(im):
                for barcode in decode(im):
                    barcode_data = (barcode.data).decode('utf-8')
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    # return decoded barcode as json response
                    return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at})
            else:
                return JsonResponse(data={'barcode_data': None})
        else:
            return JsonResponse(data={'barcode_data': None})
    # else stream the frames from camera feed
    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def barcodeDisplay(request):
    streamValue = None
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    while True:
        success, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        print(success)

        if not success:
            break
        else:
            color_image = np.asanyarray(frame)

            if decode(color_image):
                for barcode in decode(color_image):
                    barcode_data = (barcode.data).decode('utf-8')
                    print(barcode_data)

                    if barcode_data:
                        pts = np.array([barcode.polygon], np.int32)
                        pts = pts.reshape((-1,1,2))

                        cv2.polylines(
                            img=color_image,
                            pts=[pts],
                            isClosed=True,
                            color=(0,255,0),
                            thickness=3
                        )
                        pts2 = barcode.rect
                        barcode_frame = cv2.putText(
                            img=color_image,
                            text=barcode_data,
                            org=(pts2[0],pts2[1]),
                            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                            fontScale=0.9,
                            color=(0,0,255),
                            thickness=2
                        )
                        _, buffer_ = cv2.imencode('.jpg', barcode_frame)
                        barcode_frame = buffer_.tobytes()
                        yield (b'--frame\r\n' 
                                b'Content-Type: image/jpeg\r\n\r\n' + barcode_frame + b'\r\n\r\n')
                        print("I am here")
                        #streamValue = render(request, 'scanner/detected.html', context={'cam_status': barcode_data})
            else:
                print("Else statement")
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return streamValue

'''


