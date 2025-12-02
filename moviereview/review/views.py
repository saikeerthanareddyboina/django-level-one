from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt

def basic(request):
    return HttpResponse("hello world")

def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"sucess","result":{"movie_name":movie,"release_date":date}},status=200)



@csrf_exempt
def cinema(request):
    if request.method == "POST":
        data = json.loads(request.body)
        movie = Movie_details.objects.create(
            movie_name = data.get("movie_name"),
            release_date = data.get("release_date"),
            budget = data.get("budget"),
            rating = data.get("rating"),
        )
        return JsonResponse({
            "status": "success",
            "msg": "movie record inserted successfully",
            "data": {
                "id": movie.id,
                "movie_name": movie.movie_name,
                "release_date": movie.release_date,
                "budget": movie.budget,
                "rating": movie.rating * "*",
            }
        }, status=200)
    

@csrf_exempt
def movies(request):
    if request.method=='GET':
        Movie_info=Movie_details.objects.all()
        movie_list=[]
        rating_filter=request.GET.get('rating') 
        min_bud_filter=request.GET.get('min_budget')
        max_bud_filter=request.GET.get('max_budget')
        if rating_filter:
            Movie_info=Movie_info.filter(rating__gte=float(rating_filter))
        for movie in Movie_info:
            if min_bud_filter and max_bud_filter:
                budget_str=movie.budget.lower().replace("cr","")
                budget_value=float(budget_str)   
                if min_bud_filter and budget_value<=float(min_bud_filter):
                    continue     
                if max_bud_filter and budget_value>=float(max_bud_filter):
                    continue         
            movie_list.append({
                'movie_name':movie.movie_name,
                'release_date':movie.release_date,
                'budget':movie.budget,
                'rating':movie.rating
            })
        if len(movie_list)==0:
            return JsonResponse({'status':"success","message":"no movies found matching the criteria"},status=200)
        return JsonResponse({'status':"success",'data':movie_list},status=200)

    elif request.method=='PUT':
        data=json.loads(request.body)
        print("PUT data:",data) #check the incoming data
        ref_id=data.get('id')
        print("referal_id:",ref_id) # check the id coming from the client
        existing_movie=Movie_details.objects.get(id=ref_id)
        print("existing movie:",existing_movie)#check the existing movie object fetched from db
        if data.get("movie_name"):
            new_name=data.get("movie_name")
            existing_movie.movie_name=new_name
            existing_movie.save()
        if data.get("release_date"):
            new_date=data.get("release_date")
            existing_movie.release_date=new_date
            existing_movie.save()
        if data.get("rating"):
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        if data.get("budget"):
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
        return JsonResponse({'status':"success",'message':"movie record updated successfully","data":data},status=200)
        
    elif request.method=='DELETE':
        # data = json.loads(request.body) if request.body else {}
        data=request.GET.get("id")
        ref_id=int(data)
        existing_movie=Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({'status':"success",'message':"movie record deleted successfully","data":data},status=200)

    elif request.method=='POST':
        # data=json.loads(request.body) #whenever we send data in json fromat
        data=request.POST  # whenever we send data in form format
        movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({'status':"success",'message':"Movie record inserted successfully","data":data},status=200)
    return JsonResponse({'error':"error occured"},status=400)




