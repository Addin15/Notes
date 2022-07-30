from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Note, NoteAttachment
from .serializers import NoteSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db.models import Q


# Note API


@api_view(['GET', 'POST'])
def notes(request):
    # GETALLNOTES
    if request.method == 'GET':
        notes = Note.objects.all()

        data = []
        for note in notes:
            serializedNote = NoteSerializer(note, many=False)
            attchs = NoteAttachment.objects.filter(
                note=str(note.id))

            files = []
            for attachment in attchs:
                files.append({
                    'id': attachment.id,
                    'url': request.scheme + '://' + request.META['HTTP_HOST'] + '/media/' + str(attachment.attachment),
                })
            data.append({
                'note': serializedNote.data,
                'attachments': files,
            })

        return Response(data, status=status.HTTP_200_OK)

    # CREATENOTE
    elif request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user

            attachments = request.FILES.getlist('attachments', None)

            data = {
                "user": current_user.id,
                "text": request.POST['text'],
            }

            serializedNote = NoteSerializer(
                data=data, context={'attachments': attachments})

            if serializedNote.is_valid():
                serializedNote.save()

                attchs = NoteAttachment.objects.filter(
                    note=str(serializedNote.data['id']))

                files = []
                for attachment in attchs:
                    files.append({
                        'id': attachment.id,
                        'url': request.scheme + '://' + request.META['HTTP_HOST'] + '/media/' + str(attachment.attachment),
                    })

                return Response({'note': serializedNote.data, 'attachments': files, }, status=status.HTTP_201_CREATED)
            return Response(serializedNote.data, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
def note(request, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GETNOTE
    if request.method == 'GET':
        serializedNote = NoteSerializer(note)
        attchs = NoteAttachment.objects.filter(
            note=str(serializedNote.data['id']))

        files = []
        for attachment in attchs:
            files.append({
                'id': attachment.id,
                'url': request.scheme + '://' + request.META['HTTP_HOST'] + '/media/' + str(attachment.attachment),
            })
        return Response({'note': serializedNote.data, 'attachments': files, }, status=status.HTTP_200_OK)

    # EDITNOTE
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            current_user = request.user
            if str(current_user.id) == str(note.user):
                attachments = request.FILES.getlist('attachments', None)

                data = {
                    "user": current_user.id,
                    "text": request.POST['text'],
                }

                serializedNote = NoteSerializer(note, data=request.data, context={
                                                'attachments': attachments, })
                if serializedNote.is_valid():
                    serializedNote.save()
                    attchs = NoteAttachment.objects.filter(
                        note=str(serializedNote.data['id']))

                    files = []
                    for attachment in attchs:
                        files.append({
                            'id': attachment.id,
                            'url': request.scheme + '://' + request.META['HTTP_HOST'] + '/media/' + str(attachment.attachment),
                        })

                    return Response({'note': serializedNote.data, 'attachments': files, }, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)

    # DELETENOTE
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            current_user = request.user
            if str(current_user.id) == str(note.user):
                note.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)

# GETNOTESBYUSERID


@api_view(['GET'])
def notes_by_user(request):
    id = request.GET['id']
    notes = Note.objects.filter(user=str(id))
    serializedNote = NoteSerializer(notes, many=True)
    return Response(serializedNote.data, status=status.HTTP_200_OK)


# SEARCHNOTES
@api_view(['GET'])
def search_notes(request):
    query = request.GET['query']
    notes = Note.objects.filter(Q(text__icontains=query))
    serializedNote = NoteSerializer(notes, many=True)
    return Response(serializedNote.data, status=status.HTTP_200_OK)


# User API

# LOGIN


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token,
    })


# GET USER
@api_view(['GET'])
def get_user(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })

    return Response({'Error': 'Not Authenticated'}, status=status.HTTP_400_BAD_REQUEST)


# REGISTER
@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    _, token = AuthToken.objects.create(user)

    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token,
    })
