from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',SignUpAPIVIew.as_view(),name="signup"),
    path('signin/',Signin.as_view(),name="signin"),
    path('reset_password/',ResetPassword.as_view(),name="resetpassword"),
    path('change_password/',ChangePassword.as_view(),name="changepassword"),
    path('createprofile/',CreateProfileAPI.as_view(),name="createprofile"),
    path('contact_us/',ContactUsAPI.as_view(),name="contactus"),
    path('about_us/',AboutUsAPI.as_view(),name="aboutus"),
    path('privacy_policy/',PrivacyPolicyAPI.as_view(),name="aboutus"),
    path('profile_detail/',ProfileDetailAPI.as_view(),name="profiledetail"),
    path('host_match/',HostMatchAPI.as_view(),name="hostmatch"),
    path('invite_list/',InviteListAPI.as_view(),name="invitelist"),
    path('find_match/',FindMatchAPI.as_view(),name="findmatch"),
    path('hostmatch_search/',HostmatchSerch.as_view(),name="search"),
    path('city_state_search/',SearchByCityState.as_view(),name="searchcitystate"),
    path('hosted_ongoing_matches/',HostedOngoingMatches.as_view(),name="hostedongoingmatches"),
    path('hosted_completed_matches/',HostedCompletedMatches.as_view(),name="hostedcompletedmatches"),
    path('Attend_Ongoing_matches/',AttendOngoing.as_view(),name="attendtongoingmatches"),
    path('Attend_Complete_matches/',AttendCompleted.as_view(),name="attendtongoingmatches"),
    path('match_detail/',MatchDetailAPI.as_view(),name="attendtongoingmatches"),

    # HostInvitation
    path("host_invitation/api/v1/list/", GetAllHostInvitation.as_view()),
    path("host_invitation/api/v1/create/", CreateHostInvitation.as_view()),
    path("host_invitation/api/v1/get/<int:pk>/", GetHostInvitation.as_view()),
    path("host_invitation/api/v1/update/<int:pk>/", UpdateHostInvitation.as_view()),
    path("host_invitation/api/v1/delete/<int:pk>/", DeleteHostInvitation.as_view()),
    # Profile
    path("profile/api/v1/list/", GetAllProfile.as_view()),
    path("profile/api/v1/create/", CreateProfile.as_view()),
    path("profile/api/v1/get/<int:pk>/", GetProfile.as_view()),
    path("profile/api/v1/update/<int:pk>/", UpdateProfile.as_view()),
    path("profile/api/v1/delete/<int:pk>/", DeleteProfile.as_view()),
    # HostMatch
    path("host_match/api/v1/list/", GetAllHostMatch.as_view()),
    path("host_match/api/v1/create/", CreateHostMatch.as_view()),
    path("host_match/api/v1/get/<int:pk>/", GetHostMatch.as_view()),
    path("host_match/api/v1/update/<int:pk>/", UpdateHostMatch.as_view()),
    path("host_match/api/v1/delete/<int:pk>/", DeleteHostMatch.as_view()),
]