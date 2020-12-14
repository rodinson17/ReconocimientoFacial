
# importaciones necesarias para le reconocimiento facial
import cv2
import os
import imutils
import numpy as np
# Importaciones necesarias de Django
from django.shortcuts import render, HttpResponse, redirect
from django.core.files.storage import FileSystemStorage
from ReconocimientoFacial.models import Student, Book, loanHistory


# Create your views here.

def home(request):
    #return HttpResponse("home")
    return render(request, "ReconocimientoFacial/home.html")


def capture_faces(request):
    # Metodo para realizar el reconocimiento facial  
    result, name_people = facial_recognition()

    if result == True:
        array_data = name_people.split('-')
        ident = array_data[1]  # Se toma la identificacion para realizar la consulta a la base de datos
        student = Student.objects.get(identification=ident) # Consulta a la DB
        loan_historys = loanHistory.objects.filter(students=student)
        books = Book.objects.all()
        data = {"student": student, "loan_historys": loan_historys, "books": books, "numBooks": loan_historys.count()}
        return render(request, "ReconocimientoFacial/info_student.html", data)

    else:
        msg = "El estudiante no se encuentra registrado en el sistema, por favor diríjase a la opción registrar estudiante"
        return render(request, "ReconocimientoFacial/home.html", {"msg": msg})


def all_students(request):
    students = Student.objects.all()
    #students = []  estudiantes
    return render(request, "ReconocimientoFacial/all_students.html", {"students": students})


def register_student(request):
    if request.method == "POST":
        # se evaluan los datos requeridos
        if request.POST["name"] and request.POST["lastname"] and request.POST["identification"] and request.POST["email"]:
            file_name = ''
            # se evalua si viene un campo de tipo file.
            if request.FILES:
                image = request.FILES['image']
                ruta = FileSystemStorage()
                file_name = ruta.save(image.name, image)
                #uploaded_file_url = ruta.url(file_name)
            else:
                return render(request, "ReconocimientoFacial/register_student.html", {"msg_error": 'La foto de perfil es requerida'})

            # Se crea el object Student
            student = Student(name=request.POST["name"], lastname=request.POST["lastname"], identification=request.POST["identification"],
                            email=request.POST["email"], phone=request.POST["phone"], image=file_name,
                            address=request.POST["address"], birthdate = request.POST["birthdate"], gender = request.POST["gender"],
                            program = request.POST["program"], semester = request.POST["semester"])
            student.save()

            # Se procede a realizar la captura del rostro
            capture_faces_video(request.POST["name"], request.POST["identification"])

            # Se entrena la Red Neuronal
            train_neural_network()
            msg = "El registro del estudiante se realizo con exito."

            return render(request, "ReconocimientoFacial/home.html", {"msg_success": msg})

        else:
            return render(request, "ReconocimientoFacial/register_student.html", {"msg_error": 'Algunos campos son requeridos'})

    return render(request, "ReconocimientoFacial/register_student.html")


def all_books(request, msg):
    books = Book.objects.all()
    message = ''
    
    if msg == '1':
        message = 'El libro se registro exitosamente'
    
    if msg == '2':
        message = 'El libro se actualizo de forma correcta'
    
    if msg == '3':
        message = 'El libro se elimino de forma correcta'
    
    data = {"books": books, "msg": msg, "message": message}

    return render(request, "ReconocimientoFacial/all_books.html", data)


def add_book(request):
    if request.method == "POST":
        if request.POST["name"] and request.POST["author"] and request.POST["category"]:
            file_name = ''
            # se evalua si viene un campo de tipo file.
            if request.FILES:
                image = request.FILES['image']
                ruta = FileSystemStorage()
                file_name = ruta.save(image.name, image)
            else:
                return render(request, "ReconocimientoFacial/add_book.html", {"msg_error": 'La carátula del libro es requerida'})

            book = Book(name=request.POST["name"], author=request.POST["author"], category=request.POST["category"],
                        state=request.POST["state"], observations=request.POST["observations"], image=file_name)
            book.save()

            return redirect('/listado-libros/1')

        else:
            return render(request, "ReconocimientoFacial/add_book.html", {"msg_error": 'Algunos campos son requeridos'})

    return render(request, "ReconocimientoFacial/add_book.html")


def update_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        book.name = request.POST["name"]
        book.author = request.POST["author"]
        book.category = request.POST["category"]
        book.state = request.POST["state"]
        book.observations = request.POST["observations"]

        # se evalua si viene un campo de tipo file.
        if request.FILES:
            image = request.FILES['image']
            ruta = FileSystemStorage()
            book.image = ruta.save(image.name, image)

        book.save()
        return redirect('/listado-libros/2')

    return render(request, "ReconocimientoFacial/update_book.html", {"book": book})


def remove_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/listado-libros/3')


def loan_history(request):
    loanHistorys = loanHistory.objects.all()
    return render(request, "ReconocimientoFacial/loan_history.html", {"loanHistorys": loanHistorys})


def lend_books(request, identification):  
    if request.method == "POST":
        
        loan = loanHistory(state=request.POST["state"], return_date=request.POST["return_date"], 
            observations=request.POST["observations"])
        loan.save()
        
        student = Student.objects.get(id=int(request.POST["student_id"]))
        book = Book.objects.get(id=int(request.POST["book_id"]))

        loan.students.add(student)
        loan.books.add(book)       

        return redirect('/historial-prestamos')

    books = Book.objects.all()

    if identification == '-1':        
        students = Student.objects.all()        
        data = {"students": students, "books": books}
        return render(request, "ReconocimientoFacial/lend_books_all_student.html", data)
    else:
        student = Student.objects.get(identification=identification)
        data = {"student": student, "books": books}
        return render(request, "ReconocimientoFacial/lend_books.html", data)
    

def action_modal(request):
    if request.method == "POST":

        loan = loanHistory(state=request.POST["state"], return_date=request.POST["return_date"], 
            observations=request.POST["observations"])
        loan.save()
        
        student = Student.objects.get(id=int(request.POST["student_id"]))
        book = Book.objects.get(id=int(request.POST["book_id"]))

        loan.students.add(student)
        loan.books.add(book)    

        loan_historys = loanHistory.objects.filter(students=student)
        
        return render(request, "ReconocimientoFacial/list_loan.html", {"loan_historys": loan_historys})
    

def train_neural_network_for_recognition(request):
    train_neural_network()
    return render(request, "ReconocimientoFacial/home.html")


def deudas(request): 
    return HttpResponse("pagina de ejemplo")   
    #return render(request, "ReconocimientoFacial/estudiantes.html")



# Metodo para realizar la captura del rostro por medio de video.
def capture_faces_video(name_person, identification):
    # Ruta donde se guardaran las capturas de pantalla.
    data_path = 'C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/data'
    # Ruta con el nombre de la persona registrada.
    person_path = data_path + '/' + name_person + '-' + identification

    # Se crea la carpeta con el nombre de la persona registrada.
    if not os.path.exists(person_path):
        os.makedirs(person_path)

    # Se instancia la captura de pantalla por medio de video.
    #video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/cristian.mp4')
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/didier.mp4')
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/mauricio.mp4')

    video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/mauricio.mp4')

    # Se emplea el metodo haarcascade para identificar el rostro.
    face_classif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Contador para el número de capturas del rostro.
    count = 0

    while True:
        # Se accede a la camara del dispositivo para realizar las capturas del rostro.
        ret, frame = video_capture.read()

        if ret == False: break

        # Se le da un tamaño al frame que contiene la camara, se pasa a escala de grises y se duplica el frame.
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()

        # Se obtiene un array con los datos del rostro.
        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Se dibuja un rectangulo sobre el rostro identificado.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Se captura el rostro
            face = aux_frame[y:y + h, x:x + w]
            # Se redimensiona el rostro a un tamaño de 150px.
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            # Se guarda la imagen del rostro en la carpeta de la persona registrada.
            cv2.imwrite(person_path + '/face_{}.jpg'.format(count), face)
            count = count + 1

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)

        if k == 27 or count >= 150:
            break

    # Se detiene la captura y se cierra la camara.
    video_capture.release()
    cv2.destroyAllWindows()


# Metodo para obtener el modelo
def get_model(method, faces_data, labels):
    if method == 'EigenFaces': face_recognizer = cv2.face.EigenFaceRecognizer_create()
    if method == 'FisherFaces': face_recognizer = cv2.face.FisherFaceRecognizer_create()
    if method == 'LBPH': face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    face_recognizer.train(faces_data, np.array(labels))
    # Almacenando el modelo obtenido
    face_recognizer.write('modelo' + method + '.xml')


# Metodo para entrenar la red neuronal  train neural network
def train_neural_network():
    data_path = 'C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/data'
    people_list = os.listdir(data_path)
    labels = []
    faces_data = []
    label = 0

    for name_dir in people_list:
        person_path = data_path + '/' + name_dir

        for file_name in os.listdir(person_path):
            labels.append(label)
            faces_data.append(cv2.imread(person_path + '/' + file_name, 0))

        label = label + 1

    #get_model('EigenFaces', faces_data, labels)
    #obtenerModelo('FisherFaces', facesData, labels)
    get_model('LBPH', faces_data, labels)


# Metodo encargado de realizar el reconocimiento
def facial_recognition():
    data_path = 'C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/data'
    image_paths = os.listdir(data_path)
    method = 'LBPH'

    if method == 'EigenFaces': face_recognizer = cv2.face.EigenFaceRecognizer_create()
    if method == 'FisherFaces': face_recognizer = cv2.face.FisherFaceRecognizer_create()
    if method == 'LBPH': face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    face_recognizer.read('modelo' + method + '.xml')

    #video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/otro-mas.mp4')
    # video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/cristian.mp4')
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/didier.mp4')
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/mauricio.mp4')

    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/3-maria-isabel-aguilar.PNG')
    #video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/data/1-angelica-viviana-albarracin.mp4')
    video_capture = cv2.VideoCapture('C:/Users/rodin/Documents/project-django/Reconocimiento/ReconocimientoFacial/videosPrueba/50-ernesto-antonio-torres.mp4')

    face_classif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognition = False
    count = 0
    name_people = ""

    while True:
        ret, frame = video_capture.read()

        if ret == False: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = gray.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = aux_frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(face)

            cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            if method == 'EigenFaces':
                if result[1] < 5700:
                    cv2.putText(frame, '{}'.format(image_paths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    recognition = True
                    name_people = image_paths[result[0]]
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    recognition = False

            if method == 'LBPH':
                if result[1] < 70:
                    cv2.putText(frame, '{}'.format(image_paths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    recognition = True
                    name_people = image_paths[result[0]]
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    recognition = False

            count = count + 1

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)

        if k == 27 or count >= 100:
        #if k == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if recognition == True:
        return True, name_people
    else:
        return False, name_people
