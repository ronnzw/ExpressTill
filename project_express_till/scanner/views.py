from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from scanner.camera import VideoCamera

# Create your views here.
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