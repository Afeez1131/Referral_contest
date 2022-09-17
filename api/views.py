import rest_framework.authentication
from django.shortcuts import render, get_object_or_404
from base_app.models import Referral, Guest
from auth_app.models import Contest, BusinessOwner
from . import serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from Individual.utils import get_ip_address
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import permissions

User = get_user_model()


class ObtainToken(APIView):
    """
    @:parameter
        Method `POST`<br>
        Format `Json` <br>
        Returns the auth token for a Business Owner
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(Q(username__iexact=username) | Q(phone_number__iexact=username))
            if not user.check_password(password):
                return Response({'Error': 'Incorrect Password Provided'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'Error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class CreateBusinessOwner(generics.CreateAPIView):
    """
    @:parameter
        Method `POST`<br>
        Format `Json` <br>
        For creating new Business Owner
    """
    serializer_class = serializers.BusinessOwnerSerializer
    permission_classes = []
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        context = {'request': request}
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response({'Error': 'Business Owner not Created'}, status=status.HTTP_400_BAD_REQUEST)


class ListBusinessOwners(generics.ListAPIView):
    """
    @:parameter
        Method `GET`<br>
        Format `Json` <br>
        List out all business owners or a single business owner
    """
    queryset = User.objects.all()
    serializer_class = serializers.BusinessOwnerSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = {'request': request}

        if pk:
            user = self.queryset.get(pk=pk)
            serializer = self.serializer_class(user, context=context)
            return Response(serializer.data)

        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)


class CreateContest(generics.CreateAPIView):
    """
    @:parameter
        Method `POST`<br>
        Format `Json` <br>
        creating new Contest
    """
    serializer_class = serializers.ContestSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ListContests(generics.ListAPIView, generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = serializers.ContestSerializer
    queryset = Contest.objects.all()

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        obj = self.get_queryset()
        page = self.paginate_queryset(obj)

        if page is not None:
            serializer = self.serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.serializer_class(obj, many=True, context=context)
            return Response(serializer.data, status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_authenticated:
            contests = qs.filter(business_owner=user)
            return contests
        else:
            return Contest.objects.none()
            # return Response({'Error': 'You are not authenticated'}, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateContest(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = serializers.ContestSerializer
    queryset = Contest.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = {'request': request}
        qs = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(qs, context=context)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            qs = super().get_queryset().filter(business_owner=user)
            return qs
        else:
            return super().get_queryset().none()


#
# class RetrieveUpdateContest(generics.RetrieveUpdateAPIView):
#     """
#     @:parameter
#         Method `GET|PATCH`<br>
#         Format `Json` <br>
#         retrieve or update the details of a contest
#     """
#     serializer_class = serializers.ContestSerializer
#     queryset = Contest.objects.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         contest = self.queryset.filter(pk=pk)
#         context = {'request': request}
#         if contest.exists():
#             serializer = self.serializer_class(contest, many=True, context=context)
#             return Response(serializer.data, status.HTTP_200_OK)
#         else:
#             return Response({'Error': 'Data not Found'}, status.HTTP_400_BAD_REQUEST)


class CreateContestReferral(generics.CreateAPIView):
    """
    @:parameter
        Method `POST`<br>
        Format `Json` <br>
        to create a new referral
    """
    serializer_class = serializers.ReferralSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        contest_id = request.data.get('business_owner')

        context = {'request': request}
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        contest = Contest.objects.get(id=contest_id)
        contest.referral_count += 1
        contest.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class ListReferral(generics.ListAPIView):
    serializer_class = serializers.ReferralSerializer
    permission_classes = []
    queryset = Referral.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        user = self.request.user
        context = {'request': request}
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(qs, many=True, context=context)
        return self.get_paginated_response(serializer.data)

        # return Response({"Error": "You are not authenticated"}, status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            qs = super().get_queryset()
            return qs
        else:
            return super().get_queryset().none()


class RetrieveUpdateReferral(generics.RetrieveUpdateAPIView):
    """
    @:parameter
        Method `GET|PATCH`<br>
        Format `Json` <br>
        retrieve or update the details of a referral
    """
    serializer_class = serializers.ReferralSerializer
    queryset = Referral.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        referral = self.queryset.filter(pk=pk)
        context = {'request': request}
        if referral.exists():
            serializer = self.serializer_class(referral, many=True, context=context)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'Error': 'Data not Found'}, status.HTTP_400_BAD_REQUEST)


class ListGuest(generics.ListAPIView):
    serializer_class = serializers.GuestSerializer
    permission_classes = []
    queryset = Guest.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        user = self.request.user
        context = {'request': request}
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context=context)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(qs, many=True, context=context)
            return Response(serializer.data)

        # return Response({"Error": "You are not authenticated"}, status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            qs = super().get_queryset()
            # Guest.objects.filter(business_owner__business_owner=)
            qs = qs.filter(business_owner__business_owner=user)
            return qs
        else:
            return super().get_queryset().none()


class RetrieveUpdateGuest(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.GuestSerializer
    queryset = Guest.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        qs = self.get_queryset().get(pk=pk)
        context = {'request': request}
        serializer = self.serializer_class(qs, context=context)
        return Response(serializer.data, status.HTTP_200_OK)


class GuestVoteReferral(generics.CreateAPIView):
    """
    @:parameter
        Method `POST`<br>
        Format `Json` <br>
        creating new Guest
    """
    permission_classes = []
    serializer_class = serializers.GuestSerializer

    def create(self, request, *args, **kwargs):
        print(kwargs)
        context = {'request': request}
        data = request.data
        ip = get_ip_address(request)

        # referral = Referral.objects.get(id=data.get('referral'))
        # exist = referral.guest_referral.filter(Q(ip=ip) | Q(phone_number=request.data.get('phone_number')))
        #
        # if not exist.exists():
        #     serializer = self.serializer_class(data=data, context=context)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(ip=ip)
        #     referral.guest_count += 1
        #     referral.save()
        #     return Response(serializer.data, status.HTTP_201_CREATED)
        # else:
        #     return Response({'Error': 'Multiple Vote not allowed'}, status.HTTP_400_BAD_REQUEST)


class GuestRetrieveUpdate(generics.ListAPIView):
    """
    @:parameter
        Method `GET|PATCH`<br>
        Format `Json` <br>
        retrieve or update the details of a guest
    """
    serializer_class = serializers.GuestSerializer
    queryset = Referral.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print('pk', pk)
        context = {'request': request}
        referral = self.queryset.filter(pk=pk)
        if referral.exists():
            referral = self.queryset.get(pk=pk)
            serializer = self.serializer_class(referral.guest_referral.all(), many=True, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': "Guest not found"}, status=status.HTTP_400_BAD_REQUEST)
