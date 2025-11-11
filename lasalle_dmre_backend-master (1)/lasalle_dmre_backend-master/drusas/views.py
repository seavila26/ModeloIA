from rest_framework import viewsets
from drusas.serializers import ImageSerializer
from drusas.models import Image
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
import pyrebase
import numpy as np
import cv2
import os
import urllib

class ImageViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Configuracion firebase es la misma que en el front
        firebaseConfig = {
            "apiKey": "AIzaSyA8g3WsotiCGR4fN1J54YiKLfLmEQHCtEg",
            "authDomain": "lasalle-2f485.firebaseapp.com",
            "databaseURL": "https://lasalle-2f485-default-rtdb.firebaseio.com",
            "projectId": "lasalle-2f485",
            "storageBucket": "lasalle-2f485.appspot.com",
            "serviceAccount": "firebase/serviceAccountKey.json"
        }
        firebase_storage = pyrebase.initialize_app(firebaseConfig)
        storage = firebase_storage.storage()

        print("serializer", serializer.data)
        # Lectura de imagen del storage
        folder = ("{user}/{folder}/original").format(folder = serializer.data['name'], user = serializer.data['user'])
        url = storage.child(folder).get_url(None)
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Guarda en local la imagen temporalmente
        cv2.imwrite('firebase/grises.png', gray_image)
        # cv2.imshow('gray', gray_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Carga de imagen al storage
        folder = ("{user}/{folder}/drusas").format(folder = serializer.data['name'], user = serializer.data['user'])
        storage.child(folder).put("firebase/grises.png")

        # Elimina la imagen
        os.remove("firebase/grises.png")

        return Response("Completada la segmentación de drusas", status=status.HTTP_201_CREATED)

