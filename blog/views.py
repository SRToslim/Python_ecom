from django.shortcuts import render


def all_blog(request):

    return render(request, 'home/blog.html')


def blogDetails(request, slug):

    return render(request, 'home/blog-details.html')