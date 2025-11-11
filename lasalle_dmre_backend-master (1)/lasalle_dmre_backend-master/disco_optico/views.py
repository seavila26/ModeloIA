from rest_framework import viewsets
from disco_optico.serializers import ImageSerializer
from disco_optico.models import Image
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
import pyrebase
import numpy as np
import cv2
import os
import urllib
import distancemap as dm
import math

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

        # Lectura de imagen del storage
        folder = ("{user}/{folder}/original").format(folder = serializer.data['name'], user = serializer.data['user'])
        url = storage.child(folder).get_url(None)
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1) # 'Load it as it is'

        # Inicio del algoritmo
        original_image = image.copy()

        # Adaptative histogram equalization green level
        clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(13,13))
        image[:,:,1] = clahe.apply(image[:,:,1])

        # Thresholding after Gaussian filtering
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_image,(5,5),0)
        _, thresh = cv2.threshold(blur, 165, 255, cv2.THRESH_BINARY)

        # Resize Image
        if image.shape[1] >= 1500:
            inverted_image = cv2.bitwise_not(thresh)
            scale_percent = 10 # percent of original size
            width = int(inverted_image.shape[1] * scale_percent / 100)
            height = int(inverted_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_image = cv2.resize(inverted_image, dim, interpolation = cv2.INTER_AREA)
        elif image.shape[1] >= 1000 and image.shape[1] < 1500:
            inverted_image = cv2.bitwise_not(thresh)
            scale_percent = 20 # percent of original size
            width = int(inverted_image.shape[1] * scale_percent / 100)
            height = int(inverted_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_image = cv2.resize(inverted_image, dim, interpolation = cv2.INTER_AREA)
        elif image.shape[1] >= 700 and image.shape[1] < 1000:
            inverted_image = cv2.bitwise_not(thresh)
            scale_percent = 30 # percent of original size
            width = int(inverted_image.shape[1] * scale_percent / 100)
            height = int(inverted_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_image = cv2.resize(inverted_image, dim, interpolation = cv2.INTER_AREA)
        else:
            inverted_image = cv2.bitwise_not(thresh)
            scale_percent = 50 # percent of original size
            width = int(inverted_image.shape[1] * scale_percent / 100)
            height = int(inverted_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_image = cv2.resize(inverted_image, dim, interpolation = cv2.INTER_AREA)

        # Distance map
        distance_map = np.zeros(resized_image.shape[:2], dtype='uint8')
        map = dm.distance_map_from_binary_matrix(resized_image.astype(bool))
        max_map = map.max()
        for y in range(map.shape[0]):
            for x in range(map.shape[1]):
                if map[y,x] > (max_map / 2):
                    distance_map[y,x] = 255
                else:
                    distance_map[y,x] = 0
        inverted_image = cv2.bitwise_not(distance_map)

        # Upscale Image
        width = int(original_image.shape[1])
        height = int(original_image.shape[0])
        dim = (width, height)
        upscale_image = cv2.resize(distance_map, dim, interpolation = cv2.INTER_AREA)

        # Find the max contour
        contours, _ = cv2.findContours(upscale_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = -1
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                idx_max_area = i
                cnt_max_area = contours[i]
                max_area = area
        cv2.drawContours(original_image, contours, idx_max_area, (255, 255, 255), 2)

        # Convex hull of the max contour
        hull = []
        hull.append(cv2.convexHull(cnt_max_area, False))
        cv2.drawContours(original_image, hull, -1, (0, 255, 0), 2, 8)

        # Find contour of convex hull
        blank = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        cv2.drawContours(blank, hull, -1, (255, 255, 255), -1, 8)
        contours, _ = cv2.findContours(blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Center of mass convex hull
        moment = cv2.moments(contours[0])
        if moment['m00'] != 0:
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])
            cv2.circle(original_image, (cx, cy), 5, (255, 0, 0), -1)

        # Crop optic disc
        ROI = image.shape[1] / 10
        if cy - ROI < 0:
            y1 = 0
        else:
            y1 = cy - ROI
        if cy + ROI > image.shape[0]:
            y2 = image.shape[0]
        else:
            y2 = cy + ROI
        if cx - ROI < 0:
            x1 = 0
        else:
            x1 = cx - ROI
        if cx + ROI > image.shape[1]:
            x2 = image.shape[1]
        else:
            x2 = cx + ROI
        crop_image = gray_image[int(y1):int(y2), int(x1):int(x2)]
        crop_image_color = original_image[int(y1):int(y2), int(x1):int(x2)]

        # Clustering kmeans con k = 4
        blur = cv2.GaussianBlur(crop_image,(17,17),0)
        z = blur.reshape(-1,1)
        z = np.float32(z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)
        _, label, center = cv2.kmeans(z, 4, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        kmeans = center[label.flatten()]
        kmeans = kmeans.reshape(crop_image.shape)

        try:
            # Obtención de la primera y segunda etiqueta
            centers = list(center)
            maximum = max(centers)
            centers.remove(maximum)
            second = max(centers)
            idx_maximum = int(np.where(center == maximum)[0])
            idx_second = int(np.where(center == second)[0])

            # First label optic cup
            blank = np.zeros(center.shape[:2])
            blank[idx_maximum] = 255
            blank = np.uint8(blank)
            maxima = blank[label.flatten()]
            maxima = maxima.reshape(crop_image.shape)

            # Second label optic disc
            blank = np.zeros(center.shape[:2])
            blank[idx_second] = 255
            blank = np.uint8(blank)
            second = blank[label.flatten()]
            second = second.reshape(crop_image.shape)
        except:
            return Response("No se ha podido identificar la imagen de fondo de ojo", status=status.HTTP_206_PARTIAL_CONTENT)

        # Optic cup circle
        try:
            circles = cv2.HoughCircles(maxima,cv2.HOUGH_GRADIENT,1,500, param1=10,param2=10,minRadius=0,maxRadius=int(blur.shape[1]*0.5))
            circles = np.uint16(np.around(circles))
            for j in circles[0,:]:
                cv2.circle(crop_image_color,(j[0],j[1]),j[2],(255,0,255),2) # Contorno
                cv2.circle(crop_image_color,(j[0],j[1]),2,(255,0,255),3) # Centro
            # Area of the disc cup circle
            blank = np.zeros((crop_image.shape[0], crop_image.shape[1]), np.uint8)
            cv2.circle(blank,(j[0],j[1]),j[2],(255,255,255),-1)
            pixels_optic_disc = cv2.countNonZero(blank)
        except:
            return Response("No se ha podido completar la segmentación", status=status.HTTP_206_PARTIAL_CONTENT)

        try:
            circles = cv2.HoughCircles(second,cv2.HOUGH_GRADIENT,1,500,param1=20,param2=20,minRadius=j[2],maxRadius=int(blur.shape[1]*0.5))
            if type(circles) != type(None):
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    # Se valida si el circulo se encuentra dentro del disco optico
                    distSqrt = math.sqrt(((int(i[0])-int(j[0]))*(int(i[0])-int(j[0])))+((int(i[1])-int(j[1]))*(int(i[1])-int(j[1]))))
                    if (distSqrt + j[2] == i[2]) or (distSqrt + j[2] < i[2]):
                        cv2.circle(crop_image_color,(i[0],i[1]),i[2],(0,0,255),2) # Contorno
                        cv2.circle(crop_image_color,(i[0],i[1]),2,(0,0,255),3) # Centro
                        # Area of the optic cup circle
                        blank = np.zeros((crop_image.shape[0], crop_image.shape[1]), np.uint8)
                        cv2.circle(blank,(i[0],i[1]),i[2],(255,255,255),-1)
                        pixels_optic_cup = cv2.countNonZero(blank)
        finally:
            ########################################################################
            # Guarda en local la imagen temporalmente
            cv2.imwrite('firebase/grises.png', image[:,:,1])
            # Carga de imagen al storage
            folder = ("{user}/{folder}/clahe").format(folder = serializer.data['name'], user = serializer.data['user'])
            storage.child(folder).put("firebase/grises.png")
            # Elimina la imagen
            os.remove("firebase/grises.png")
            ###########################################################################
            # Guarda en local la imagen temporalmente
            cv2.imwrite('firebase/grises.png', thresh)
            # Carga de imagen al storage
            folder = ("{user}/{folder}/thresh").format(folder = serializer.data['name'], user = serializer.data['user'])
            storage.child(folder).put("firebase/grises.png")
            # Elimina la imagen
            os.remove("firebase/grises.png")
            ###########################################################################
            # Guarda en local la imagen temporalmente
            cv2.imwrite('firebase/grises.png', crop_image_color)
            # Carga de imagen al storage
            folder = ("{user}/{folder}/detection").format(folder = serializer.data['name'], user = serializer.data['user'])
            storage.child(folder).put("firebase/grises.png")
            # Elimina la imagen
            os.remove("firebase/grises.png")
            ############################################################################

        #Glaucoma diagnosis
        try:
            CDR = pixels_optic_disc / pixels_optic_cup
            CDR = round(CDR, 2)
            if CDR > 0.5:
                return Response("Presenta glaucoma, el resultado del calculo es: {CDR}".format(CDR = CDR), status=status.HTTP_200_OK)
            else:
                return Response("No presenta glaucoma, el resultado del calculo es: {CDR}".format(CDR = CDR), status=status.HTTP_200_OK)
        except:
            return Response("No se ha podido calcular si el paciente tiene glaucoma", status=status.HTTP_200_OK)