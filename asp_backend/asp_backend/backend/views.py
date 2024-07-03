import json
import os

from django.conf import settings
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST', 'OPTIONS'])
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if username is not None and password is not None:
                token = "admin-token"
                return JsonResponse({'code': 20000, 'data': {'token': token}})
            else:
                return JsonResponse({'code': 60204, 'message': 'Account and password are incorrect.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'code': 40000, 'message': 'Invalid JSON'}, status=400)


@api_view(['GET', 'OPTIONS'])
def getInfo(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token == 'admin-token':
            user_info = {
                'roles': ['admin'],
                'introduction': 'I am a super administrator',
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'name': 'Super Admin'
            }
            return JsonResponse({'code': 20000, 'data': user_info})
        else:
            return JsonResponse({'code': 50008, 'message': 'Login failed, unable to get user details.'}, status=404)


@api_view(['POST'])
def logout(request):
    print(request)
    if request.method == 'POST':
        return JsonResponse({'code': 20000, 'data': 'success'})


@api_view(['POST', 'OPTIONS'])
def solve(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code')
            mode = data.get('mode')
            reference = data.get('reference')
            # 做你的ASP推理
            print(code)
            assumption_sets = [
                {'assumption_set': ['{bird}'], 'belief_set': ['{bird}']},
                {'assumption_set': ['{bird, sick}'], 'belief_set': ['{bird}']},
                {'assumption_set': ['{bird, canfly, sick}'], 'belief_set': ['{bird}']}
            ]
            # 合乎语法
            if True:
                data = {
                    # status不能更改
                    # message 为信息，可以更改属性
                    # 1 代表着语法解析成功
                    'status': 1,
                    'timeUsed': 0.001,
                    'assumptionSets': assumption_sets,
                    'message': 'Solved'
                }
                return JsonResponse({'code': 20000, 'data': data})
            # 语法错误
            else:
                data = {
                    # 0代表着语法解析失败
                    status: 0,
                    'message': 'Unsatisfiable'
                }
                # 返回错误信息
                return JsonResponse({'code': 20000, 'data': data})
        except json.JSONDecodeError:
            return JsonResponse({'code': 50010, 'message': 'Something went wrong.'}, status=500)


@api_view(['GET', 'OPTIONS'])
def getCase(request):
    if request.method == 'GET':
        try:
            cases = [
                {'id': 1, 'description': '判断鸟的飞行问题', 'code': 'canfly :-  bird : canfly, not sick.\nbird.'},
                {'id': 2, 'description': '运动员接力和马拉松选择问题', 'code': 'marthon :- :marthon.\nrelay :- :relay.\n:- marthon, relay.'},
                {'id': 3, 'description': 'n皇后问题', 'code': 'n(8).\n{ queen(X,Y) : X = 1..N, Y = 1..N } = N :- n(N).\n:- queen(X,Y1), queen(X,Y2), Y1 != Y2.'
                                                          '\n:- queen(X1,Y), queen(X2,Y), X1 != X2.\n:- queen(X1,Y1), queen(X2,Y2), X1 != X2, Y1 != Y2, abs(X1-X2) = abs(Y1-Y2).'},
                {'id': 4, 'description': '哈密顿圈问题',
                 'code': 'vertex(1..n).\nedge(1,2). edge(2,3).\n1 { in(X,Y) : edge(Y,X) } 1 :- vertex(X).\n1 { out(X,Y) : edge(X,Y) } 1 :- vertex(X).\nreached(X) :- in(1,X).'
                         '\nreached(X) :- reached(Y), in(X,Y).\n:- vertex(X), not reached(X).\n:- in(X,Y), in(Z,W), reached(X,W), reached(Z,Y), X != Z, Y != W.'},
                {'id': 5, 'description': '运动员赛跑', 'code': 'marthon :- :marthon.\nrelay :- :relay.\n:- marthon, relay.'}
            ]
            # 合乎语法

            return JsonResponse({'code': 20000, 'data': cases})
            # 语法错误
        except json.JSONDecodeError:
            return JsonResponse({'code': 50010, 'message': 'Something went wrong.'}, status=500)
