from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer
from django.core.mail import send_mail
from django.conf import settings
import cv2
import os
from datetime import datetime
from django.conf import settings

THRESHOLD_VALUE = 0.03

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all().order_by('-timestamp')
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data

        # Check if the sensor value exceeds the threshold
        if data['value'] > THRESHOLD_VALUE:
            # Capture the image and get the path
            image_path = self.capture_image()  # Ensure you have this method defined
            
            # Send an email alert
            self.send_threshold_exceed_email(data['value'], image_path)
            
            # Return response with an alert message
            return Response({
                "message": "Alert! Value exceeds threshold", 
                "blink": True
            }, status=status.HTTP_201_CREATED)

        return response

    def send_threshold_exceed_email(self, value, image_path):
        subject = 'Threshold Alert: Sensor Value Exceeded'
        message = f'The sensor value has exceeded the threshold. Current value: {value}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['']  # Replace with actual recipient email addresses

        # Create an EmailMessage object
        email = EmailMessage(subject, message, from_email, recipient_list)

        # Attach the image
        try:
            with open(image_path, 'rb') as image_file:
                email.attach(image_path, image_file.read(), 'image/jpeg')
            email.send(fail_silently=False)
        except Exception as e:
            print(f"Error sending email: {e}")

    def capture_image(self):
        # Capture the image from the camera
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        ret, frame = cap.read()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = f"sensor_capture_{timestamp}.jpg"
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        cv2.imwrite(image_path, frame)
        cap.release()

        print(f"Image saved at: {image_path}")

        return image_path

from django.core.mail import EmailMessage

def send_threshold_exceed_email(self, value, image_path):
    subject = 'Threshold Alert: Sensor Value Exceeded'
    message = f'The sensor value has exceeded the threshold. Current value: {value}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['sivasubramanian.v2023ece@sece.ac.in']
    email = EmailMessage(subject, message, from_email, recipient_list)
    try:
        with open(image_path, 'rb') as image_file:
            email.attach(image_path, image_file.read(), 'image/jpeg')
        email.send(fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {e}")



@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Graph plotting view
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from .models import SensorData

def plot_graph(request):
    data = SensorData.objects.all().order_by('-timestamp')[:10]
    values = [d.value for d in data]
    timestamps = [d.timestamp.strftime("%H:%M") for d in data]
    fig, ax = plt.subplots()
    ax.bar(timestamps, values)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Sensor Value')
    ax.set_title('Sensor Data over Time')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')
