from rest_framework import viewsets, serializers
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) #유저를 자동으로 저장

    # 현재 request를 보낸 유저
    # == self.request.user

    def get_queryset(self):  # 본인의 글만 보이게 한다.
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:  # 관리자가 아니면 필터 적용
                qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()
        return qs


class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    # parser_class 지정
    parser_classes = (MultiPartParser, FormParser)
    
    # create() 오버라이딩
    # API HTTP -> get() post() ...

    # create() -> post()
    
    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_vaild():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)
