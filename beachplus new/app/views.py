from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models import Q
from datetime import datetime
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
# date = datetime.date.today()
# Create your views here.

class SignUpAPIVIew(generics.GenericAPIView):
    permission_classes=(AllowAny,)
    # serializer_class = UserSignupSerializer
    def post(self,request):
        try:
            user=User.objects.get(email=request.data['email'])     
            return Response({"data":None,"message":"Email Already Exist"},status=status.HTTP_400_BAD_REQUEST) 
        except:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user=serializer.save()
                print(serializer.data)
                
                d=dict()   
                d['user']=user.id
                d['device_token']=request.data['DeviceToken']
                d['device_type']=request.data['DeviceType']
                print(d)
                serializer2 = DeviceSerializer(data=d)
                if serializer2.is_valid(raise_exception=True):
                    serializer2.save()
                    return Response({
                        "data":serializer.data,    
                        "status":200,
                        "msg":'Sign Up Successfully'
                        })
                return Response(serializer2.errors,status=status.HTTP_400_BAD_REQUEST)              
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)      



            
   
            # serializer=SignupSerializer(data=request.data)
            # # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # user = serializer.save()

            # d=dict()
            # d['user']=user.id
            # d['device_token']=request.data['DeviceToken']
            # d['device_type']=request.data['DeviceType']
            # print(d)
            # # Device.objects.filter(device_token=d['device_token']).delete()
            # serializer2 = DeviceSerializer(data=d)
            # print(serializer2)
            # serializer2.is_valid(raise_exception=True)
            # serializer2.save()
            # return Response({
            # "data":serializer.data,    
            # "status":200,
            # "msg":'Sign Up Successfully'
            # })


class Signin(generics.GenericAPIView):
    permission_classes=(AllowAny,)
    def post(self,request):
        if "email" in request.data and "password" in request.data:
            email=request.data['email']
            email=email.lower()
            password=request.data['password']
            try:
                user=User.objects.get(email=email) 
            except User.DoesNotExist:
                return Response({"data": None,"message": "User Does Not Exist"},status = status.HTTP_400_BAD_REQUEST)

            if user.check_password(password): #check password if it matches.
                login(request, user)
                serializer=UserLoginSerializer(user)    
                return Response({
                            "data": serializer.data,
                            "code": status.HTTP_200_OK,
                            "message": "Login SuccessFully",
                        },status = status.HTTP_200_OK)
            else:
                return Response({
                        "data": None,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid Credentials",
                        },status = status.HTTP_400_BAD_REQUEST)

class ResetPassword(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user_id=request.data['user_id'] 
        u=User.objects.get(id=user_id)
        password=request.data['password']
        u.set_password(password)      
        u.save()
        return Response({"msg":"password updated",'status':'200'}) 


class ChangePassword(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user_id=request.data['user_id']
        old_password=request.data['old_password']
        new_password=request.data['new_password']
        user=User.objects.get(id=user_id)

        if user.check_password(old_password):
            user=User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return Response({'msg':'your password is changed'})
        return Response({'msg':'password did not match'})    


class CreateProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=ProfileSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'User information saved Successfully','status':200})

class ProfileDetailAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        dictV=dict()
        dictV['profiledetail']=Profile.objects.filter(user_id=request.POST['user_id']).values('profile_image','first_name','location')
        dictV['matchplayed']=len(Profile.objects.filter(user_id=request.POST['user_id']).values('matchplayed'))
        dictV['matchhost']=len(Profile.objects.filter(user_id=request.POST['user_id']).values('matchhost'))
        dictV['matchwon']=len(Profile.objects.filter(user_id=request.POST['user_id']).values('matchwon'))
        dictV['msg']='profile detail'
        dictV['status']='200'
        return Response(dictV)

class HostMatchAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=HostMatchSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Host Match create successfully','status':200})



class InviteListAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated)
    def post(self,request):
        dictV=dict()
        dictV['invitationdetail']=HostInvitation.objects.filter(user_invited=request.POST['user_invited']).values('status','hostmatch_id__title','hostmatch_id__location','hostmatch_id__time','hostmatch_id__user_id__first_name')
        dictV['msg']='invitation_detail'
        dictV['status']='200'
        return Response(dictV)


class FindMatchAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        H=HostMatch.objects.all().values()
        return Response({'data':H,'msg':'All Matches','status':'200'})


class HostmatchSerch(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        try:
            data=request.POST
            if data.get("search"):
                query=data.get('search')
            else:
                query=""

            if data.get("search1"):
                date=data.get('search1')
            else:
                date="" 
            print(date)     

            host_match=HostMatch.objects.all()
            if query:
                host_match=host_match.filter(Q(location__icontains=query))

            if date:
                host_match=host_match.filter(Q(date__icontains=date))    
    
            if host_match:
                serializer=GetHostMatchSerializer(host_match,many=True)
                return ResponseOk(
                        {
                            "data": serializer.data,
                            "code": status.HTTP_200_OK,
                            "message": "HostMatch list",
                        }
                    )
            else:
                return Response({'msg':'search not found'})    
        except:
            return Response({'msg':'search query does not found'})


class SearchByCityState(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        data=request.POST
        if data.get('city'):     
            city=data.get('city')
        else:
            city=""
        
        if data.get('state'):
            state=data.get('state')
        else:
            state=""    
        profile=Profile.objects.all()
        if city:
            profile=profile.filter(Q(city__icontains=city))  
        if state:
            profile=profile.filter(Q(state__icontains=state))      
        if profile:
            serializer=ProfileSerializer(profile,many=True)  
            return Response({
                'data':serializer.data,
                'status':status.HTTP_200_OK,
                'msg':'All profiles by given search'
            })                 
        else:
            return Response({'msg':'search not found'})    
          
class HostedOngoingMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        date = datetime.today()
        time = datetime.now().time()
        host_match=HostMatch.objects.filter(user_id=request.data['user_id'],date__gte=date,time__gte=time).values()
        return Response({'host_match':host_match,'msg':'MyHostedOngoingMatches List','status':'200'})
      
class HostedCompletedMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request,):
        date = datetime.today()
        time = datetime.now().time()
        host_match=HostMatch.objects.filter(user_id=request.data['user_id'],date__lte=date,time__lte=time).values()
        return Response({'host_match':host_match,'msg':'MyHosted Completed Matches List','status':'200'})

# class AttendOngoing(generics.GenericAPIView):
#     def post(self,request):
#         date = datetime.today()
#         time = datetime.now().time()
#         invite_list=HostInvitation.objects.filter(user_invited=request.data['user_id'],status='Attend').values()
#         print(invite_list)
#         host_match=HostMatch.objects.filter(id__in=invite_list).values()
#         print(host_match)
#         return Response({'host_match':host_match,'msg':'Attending Ongoing Matches List','status':'200'})

class AttendOngoing(generics.GenericAPIView):
    # permission_classes=(IsAuthenticated,)
    def post(self,request):
        date = datetime.today()
        time = datetime.now().time()
        invite_list=HostInvitation.objects.filter(user_invited=request.POST['user_invited'],status='Attend').values('hostmatch_id')
        print(invite_list)
        host_match=HostMatch.objects.filter(id__in=invite_list,date__gte=date,time__gte=time).values()
        print(host_match)
        return Response({
            'data':host_match,
            'msg':'MyAttendingOngoingMatches List',
            'status':200
         })


class AttendCompleted(generics.GenericAPIView):
    # permission_classes=(IsAuthenticated,)

    def post(self,request):
        date = datetime.today()
        time = datetime.now().time()
        invite_list=HostInvitation.objects.filter(user_invited=request.POST['user_invited'],status='Attend').values('hostmatch_id')
        print(invite_list)    
        host_match=HostMatch.objects.filter(id__in=invite_list,date__lte=date,time__lte=time).values()
        print(host_match)
        return Response({
            'data':host_match,
            'msg':'MyAttendingCompletedMatches List',
            'status':200
         })


class MatchDetailAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        dictV=dict()
        dictV['Hostatch']=HostMatch.objects.filter(user_id=request.POST['user_id']).values()
        dictV['Team1playerList']=TeamPlayers.objects.filter(host_match__user_id=request.POST['user_id']).values('player_id','player__first_name','player__profile_image')
        dictV['Team2PlayerList']=Team2Players.objects.filter(host_match__user_id=request.POST['user_id']).values('player_id','player__first_name','player__profile_image')
        # dictV['score']=TeamScore.objects.filter(HostMatch=request.POST['HostMatch']).values('Team1Score','Team2Score')
        # dictV['rating']=PlayerRatings.objects.filter(HostMatch=request.POST['HostMatch']).values('Player_id','Player__ProfileImage','Player__FirstName','Player__LastName','Rating').order_by('-Rating')
        dictV['msg']='match detail list'
        dictV['status']=200
        return Response(dictV)
        


# class MatchDetailAPI(generics.GenericAPIView):
#     # permission_classes=(IsAuthenticated,)

#     def post(self,request):
#         dictV=dict()
#         dictV['host_match']=HostMatch.objects.filter(user_id=request.POST['user_id']).values()
#         print(dictV)
#         dictV['team1player']=TeamPlayers.objects.filter(host_match__user_id=request.POST['user_id']).values('player_id','player__first_name','player__profile_image')
#         print(dictV['team1player'])
#         dictV['team2player']=Team2Players.objects.filter(host_match__user_id=request.POST['user_id']).values('player_id','player__first_name','player__profile_image')
#         print(dictV['team2player'])
#         dictV['score']=TeamScore.objects.filter(host_match__user_id=request.POST['user_id']).values('team1_player_score','team2_player_score')
#         dictV['status']=200
#         dictV['msg']='match detail list'
#         return Response(dictV)


class ContactUsAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=ContactUsSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'ContactUs information saved Successfully','status':200})   


class AboutUsAPI(generics.GenericAPIView):
    # permission_classes=(IsAuthenticated,)
    def post(self,request):
        return Response({
            'data':{'text':AboutUs.objects.all().values()},
            'msg':'About Us',
            'status':200
        })
                     

class PrivacyPolicyAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        return Response({
            'data':{'text':PrivacyPolicy.objects.all().values()},
            'msg':'Privacy Policy',
            'status':200
        })            


class TermsConditionAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        return Response({
            'data':{'text':TermsCondition.objects.all().values()},
            'msg':'Terms Condition',
            'status':200
        })                                      













from drf_yasg import openapi
from django.db.models import Q
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from app.response import ResponseBadRequest, ResponseNotFound, ResponseOk
from rest_framework.parsers import FormParser, MultiPartParser
from .models import *
from .serializers import *





class GetAllHostInvitation(APIView):
    """
    Get All HostInvitation
    """
    permission_classes=(IsAuthenticated,)

    @csrf_exempt
    def get(self, request):
        try:
            host_invitation=HostInvitation.objects.all()
            serializer=HostInvitationSerializer(host_invitation,many=True)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "HostInvitation list",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostInvitation Does Not Exist",
                }
            )




class CreateHostInvitation(APIView):
    """
    Create HostInvitation
    """
    
    permission_classes=(IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)


    @swagger_auto_schema(
        operation_description="create HostInvitation",
        request_body=HostInvitationSerializer,
    )
    @csrf_exempt
    def post(self, request):
        serializer = HostInvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "HostInvitation created succesfully",
                }
            )
            
        else:    
            
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostInvitation is not valid",
                }
            )



class GetHostInvitation(APIView):
    """
    Get HostInvitation by pk
    """
    permission_classes=(IsAuthenticated,)
    
    csrf_exempt
    def get_object(self, pk):
        try:
            return HostInvitation.objects.get(pk=pk)
        except HostInvitation.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            host_invitation = self.get_object(pk)
            serializer = HostInvitationSerializer(host_invitation)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get HostInvitation successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostInvitation Does Not Exist",
                }
            )




class UpdateHostInvitation(APIView):
    """
    Update HostInvitation
    """
    permission_classes=(IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)


    def get_object(self, pk):
        try:
            return HostInvitation.objects.get(pk=pk)
        except HostInvitation.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update HostInvitation",
        request_body=HostInvitationSerializer,
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            host_invitation = self.get_object(pk)
            serializer = HostInvitationSerializer(host_invitation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "HostInvitation updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "HostInvitation Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostInvitation Does Not Exist",
                }
            )



class DeleteHostInvitation(APIView):
    """
    Delete HostInvitation
    """
    permission_classes=(IsAuthenticated,)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return HostInvitation.objects.get(pk=pk)
        except HostInvitation.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            host_invitation = self.get_object(pk)
            host_invitation.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "HostInvitation deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostInvitation Does Not Exist",
                }
            )




#Profile

class GetAllProfile(APIView):
    """
    Get All Profile
    """
    permission_classes=(IsAuthenticated,)

  

    @csrf_exempt
    def get(self, request):
        try:
            profile=Profile.objects.all()
            serializer=GetProfileSerializer1(profile,many=True)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Profile list",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile Does Not Exist",
                }
            )




class CreateProfile(APIView):
    """
    Create Profile
    """
    
    permission_classes=(IsAuthenticated,)

 
    parser_classes = (FormParser, MultiPartParser)


    @swagger_auto_schema(
        operation_description="create Profile",
        request_body=ProfileSerializer1,
    )
    @csrf_exempt
    def post(self, request):
        serializer = ProfileSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "Profile created succesfully",
                }
            )
            
        else:    
            
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile is not valid",
                }
            )



class GetProfile(APIView):
    """
    Get Profile by pk
    """
    permission_classes=(IsAuthenticated,)
    


    csrf_exempt
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            profile = self.get_object(pk)
            serializer = GetProfileSerializer1(profile)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get Profile successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile Does Not Exist",
                }
            )




class UpdateProfile(APIView):
    """
    Update Profile
    """
    permission_classes=(IsAuthenticated,)

   
    parser_classes = (FormParser, MultiPartParser)


    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update Profile",
        request_body=ProfileSerializer1,
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            profile = self.get_object(pk)
            serializer = ProfileSerializer1(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "Profile updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Profile Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "profile Does Not Exist",
                }
            )



class DeleteProfile(APIView):
    """
    Delete Profile
    """
    permission_classes=(IsAuthenticated,)


    @csrf_exempt
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            profile = self.get_object(pk)
            profile.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Profile deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile Does Not Exist",
                }
            )


from drf_yasg import openapi
from django.db.models import Q
#HostMatch
class GetAllHostMatch(APIView):
    """
    Get All HostMatch
    """
    permission_classes=(IsAuthenticated,)

    search = openapi.Parameter('search',
                            in_=openapi.IN_QUERY,
                            description='Search location',
                            type=openapi.TYPE_STRING,
                            )
    search1 = openapi.Parameter('date',
                            in_=openapi.IN_QUERY,
                            description='Search date',
                            type=openapi.TYPE_STRING,
                            )                        


    @swagger_auto_schema(
            manual_parameters=[search,search1]
    )

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            if data.get("search"):
                query=data.get('search')
            else:
                query=""   

            if data.get("date"):
                date=data.get('date')
            else:
                date=""     

            host_match=HostMatch.objects.all()
            if query:
                host_match=host_match.filter(Q(location__icontains=query))

            if date:
                host_match=host_match.filter(Q(date__icontains=date))    

            if host_match:
                serializer=GetHostMatchSerializer(host_match,many=True)
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "HostMatch list",
                    }
                )
            else:
                return Response({'msg':'search not found'})    
        except:
            return Response({'msg':'search query does not found'})




class CreateHostMatch(APIView):
    """
    Create HostMatch
    """

    permission_classes=(IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="create HostMatch",
        request_body=HostMatchSerializer,
    )
    @csrf_exempt
    def post(self, request):
        serializer = HostMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "HostMatch created succesfully",
                }
            )
            
        else:    
            
            return ResponseBadRequest(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostMatch is not valid",
                }
            )



class GetHostMatch(APIView):
    """
    Get HostMatch by pk
    """
    permission_classes=(IsAuthenticated,)
    


    csrf_exempt
    def get_object(self, pk):
        try:
            return HostMatch.objects.get(pk=pk)
        except HostMatch.DoesNotExist:
            raise ResponseNotFound()

    def get(self, request, pk):
        try:
            host_match = self.get_object(pk)
            serializer = GetHostMatchSerializer(host_match)
            return ResponseOk(
                {
                    "data": serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "get HostMatch successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostMatch Does Not Exist",
                }
            )




class UpdateHostMatch(APIView):
    """
    Update HostMatch
    """
    permission_classes=(IsAuthenticated,)

    parser_classes = (FormParser, MultiPartParser)


    def get_object(self, pk):
        try:
            return HostMatch.objects.get(pk=pk)
        except HostMatch.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update HostMatch",
        request_body=HostMatchSerializer,
    )
    @csrf_exempt
    def put(self, request, pk):
        try:
            host_match = self.get_object(pk)
            serializer = HostMatchSerializer(host_match, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data": serializer.data,
                        "code": status.HTTP_200_OK,
                        "message": "HostMatch updated successfully",
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data": serializer.errors,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "HostMatch Not valid",
                    }
                )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostMatch Does Not Exist",
                }
            )



class DeleteHostMatch(APIView):
    """
    Delete HostMatch
    """
    permission_classes=(IsAuthenticated,)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return HostMatch.objects.get(pk=pk)
        except HostMatch.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            host_match = self.get_object(pk)
            host_match.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "HostMatch deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "HostMatch Does Not Exist",
                }
            )











