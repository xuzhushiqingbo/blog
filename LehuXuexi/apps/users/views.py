from datetime import datetime

from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.views import ObtainJSONWebToken

from LehuXuexi.settings import MEDIA_ROOT, YU_MING, MEDIA_URL
from .models import VerifyCode
from utils.utils import send_verify_code_by_email, generate_code
from .serializers import VerifyCodeSerializer, UserRegSerializer, UserDetailSerializer

User = get_user_model()


class CustomAuthenticateBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update({'username': user.username, 'nickname': user.nickname, 'userid': user.pk})
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """发送邮箱或手机验证码"""

    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_type = serializer.validated_data['account_type']
        account = serializer.validated_data['account']
        verifycode = generate_code()
        if account_type == 'email':
            send_status = send_verify_code_by_email(verifycode, [account])
            if send_status:
                # self.perform_create(serializer)
                vcode = VerifyCode(code=verifycode, account=account, account_type=account_type)
                vcode.save()
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        else:
            pass


class UserRegisterViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """用户注册"""
    queryset = User.objects.all()
    # serializer_class = UserRegSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        # return ArticleSimpleSerializer
        if self.action == 'create':
            return UserRegSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            return []
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated(), ]
        return []

    # def get_authenticators(self):
    #     """
    #     Instantiates and returns the list of authenticators that this view can use.
    #     """
    #     if self.action == 'create':
    #         return []
    #     if self.action == 'retrieve':
    #         return [JSONWebTokenAuthentication(), SessionAuthentication()]
    #     return []

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        ret_data = serializer.data
        headers = self.get_success_headers(serializer.data)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        additional_data = {'nickname': user.nickname, 'userid': user.id, 'token': token}
        ret_data.update(additional_data)
        return Response(ret_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class UserDetailViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserAvatarUpdateView(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request, format=None):
        # print(request.data)
        image = request.data['avatar']
        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
            save_path = MEDIA_ROOT + '/users/avatars/' + image.name[-10:]
            # file_path服务器上保存图片的路径
            file_path = default_storage.save(save_path, image)
            # 把文件的URL返回给前端
            user = request.user
            user.avatar = 'users/avatars/' + image.name[-10:]
            file_url = YU_MING + MEDIA_URL + 'users/avatars/' + file_path.split('/')[-1]
            user.save()
            # print(MEDIA_URL)
            # print(file_url)
            return Response({'avatar': file_url}, status=status.HTTP_201_CREATED)
        else:
            message = '图像扩展名不正确！ 只接受：'+str(['jpg', 'jpeg', 'png', 'gif'])
            # return Response("xxx", status=status.HTTP_201_CREATED)
            return Response({'avatar': message}, status=status.HTTP_400_BAD_REQUEST)