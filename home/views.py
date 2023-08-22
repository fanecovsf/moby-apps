from django.shortcuts import render, redirect

class Views:

    @staticmethod
    def home_page(request):
        return redirect('login')
