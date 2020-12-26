from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

# rest framework imports
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# local imports
from .serializers import QuestionSerializer, ResultSerializer, QuestionWithOptionSerializer
from .models import Question, Result


# index page api
@api_view(["GET"])
@permission_classes((AllowAny,))
def index(request):
    """
    Index API
    """
    return Response({"message": "Welcome to assessment API service"})


#######################################
# User APIs below
#######################################

# register new user to exam portal
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup_api(request):
    """
    Register new user to the exam portal
    """
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'username already exist'}, status=HTTP_400_BAD_REQUEST)

    if username and password:
        user = User(username=username)
        user.set_password(raw_password=password)
        user.save()
        return Response({'success': 'User has been created'}, status=HTTP_201_CREATED)
    return Response({'error': 'Please provide username and password'}, status=HTTP_400_BAD_REQUEST)


# login existing user to exam portal
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_api(request):
    """
    Login the user to exam portal
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


# start test api
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def start_exam_api(request):
    """
    Start the new exam giving list of all question papers
    """
    # get all questions
    ques = Question.objects.all()
    serializer = QuestionWithOptionSerializer(ques, many=True)
    data = {'questions': serializer.data}
    return Response(data, status=HTTP_200_OK)


# calculate test result
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def store_result_api(request):
    """
    Create score card based on options selected by users for each questions
    strongly_agree = 2
    agree = 1
    neutral = 0
    disagree = -1
    strongly_disagree = -2
    """
    answer_sheet = request.data
    score = 0

    for item in answer_sheet:
        ans = item['selected_option']
        if ans == 'strongly_agree':
            score += 2
        if ans == 'agree':
            score += 1
        if ans == 'neutral':
            score += 0
        if ans == 'disagree':
            score += -1
        if ans == 'strongly_disagree':
            score += -2

    score_card = {'user': request.user.username, 'score': score, 'top_qualities': []}

    if Result.objects.filter(user=request.user).exists():
        result = Result.objects.get(user=request.user)
        result.score = score
        result.save()

        return Response(
            {
                "success": "Exam submitted successfully",
                "score_card": score_card
            },
            status=HTTP_200_OK
        )
    else:
        result = Result.objects.create(score=score, user=request.user)
        result.save()
        return Response(
            {
                "success": "Exam submitted successfully",
                "score_card": score_card
            },
            status=HTTP_200_OK
        )


#######################################
# Admin only APIs below
#######################################

# upload questions csv file
@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAdminUser,))
def upload_question_api(request):
    """
    Uploads CSV file having 3 columns- sr/no, questions, questions type
    """
    csv_file = request.FILES['questions']
    # check whether file is csv or not
    if not csv_file.name.endswith('.csv'):
        return Response({"error": "please upload valid csv file"}, status=HTTP_400_BAD_REQUEST)

    # if file is too large, return
    if csv_file.multiple_chunks():
        return Response({"error": "Uploaded file is too big"}, status=HTTP_400_BAD_REQUEST)

    file = csv_file.read().decode('UTF-8')
    lines = file.split("\n")[1:-1]
    for row in lines:
        line = row.split(',')
        question = Question.objects.create(question=line[1], que_type=line[2])
        question.save()
    return Response({"success": "Questions uploaded successfully"}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAdminUser,))
def questions_api(request, que_id=None):
    """
    Let admin view all questions
    """
    # get all questions
    if request.method == 'GET':
        ques = Question.objects.all()
        ser = QuestionSerializer(ques, many=True)
        data = {'questions': ser.data}
        return Response(data, status=HTTP_200_OK)

    # get one question object by id
    try:
        question = Question.objects.get(pk=que_id)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    # update given question
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = QuestionSerializer(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Question updated successfully'}, status=HTTP_200_OK)
        return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    # delete given question
    if request.method == 'DELETE':
        question.delete()
        return Response({"success": "Question deleted successfully"}, status=HTTP_204_NO_CONTENT)


# get result of all users
@api_view(["GET"])
@permission_classes((IsAdminUser,))
def result_api(request):
    """
    Let admin view all users result
    """
    try:
        results = Result.objects.all()
    except Result.DoesNotExist:
        return HttpResponse(status=404)

    # get all questions
    if request.method == 'GET':
        ser = ResultSerializer(results, many=True)
        data = {'result': ser.data}
        return Response(data, status=HTTP_200_OK)
