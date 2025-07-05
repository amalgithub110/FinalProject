from django.shortcuts import render,redirect,get_object_or_404
from theaters.models import Theater,Seat,showtime
from movies.models import Movie
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from .models import Booking,BookingSeat
from accounts.models import User
import json
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
#dates = [datetime.date.today(),datetime.date.today() + datetime.timedelta(days=1),datetime.date.today() + datetime.timedelta(days=2),datetime.date.today() + datetime.timedelta(days=3),datetime.date.today() + datetime.timedelta(days=4)]
dates = [datetime.date.today()+datetime.timedelta(days=i) for i in range(9)]
current_time = datetime.datetime.now().time()
@login_required(login_url='login')
def Theater_Showtime_view(request,slug,date_str=datetime.date.today()):
    if not Movie.objects.filter(slug=slug).exists():
        messages.error(request,'Movie not found')
        return redirect('movie_list')
    movie = Movie.objects.get(slug=slug)
    selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    if selected_date == datetime.date.today():
        theater_showtimes = [showtime.objects.filter(movie=movie,showtime__date=selected_date,
                                                 theater=theater,showtime__time__gte=current_time).order_by('showtime') 
                                                 for theater in Theater.objects.all()
                                                 if showtime.objects.filter(movie=movie,showtime__date=selected_date,theater=theater,showtime__time__gte=current_time).exists()]
    else:
        theater_showtimes = [showtime.objects.filter(movie=movie,showtime__date=selected_date,
                                                 theater=theater).order_by('showtime') 
                                                 for theater in Theater.objects.all()
                                                 if showtime.objects.filter(movie=movie,showtime__date=selected_date,theater=theater).exists()]

    context = {
        'movie':movie,
        'theater_showtimes':theater_showtimes,
        'dates':dates,
        'slug':slug,    
        'current_date' : selected_date,
        
    }
    return render(request,'theaters/theater_showtime.html',context)


def Seat_Selection_view(request,show_id):
    Showtime = showtime.objects.get(id=show_id)
    theater = Showtime.theater
    movie = Showtime.movie
    seats = Seat.objects.filter(theater=theater).order_by('row_label','seat_number')
    seat_rows = {}
    booked_seat = [booking_seat.seat for booking_seat in BookingSeat.objects.filter(showtime=Showtime)]
    for seat in seats:
        row = (seat.row_label, seat.seat_type)
        if row not in seat_rows:
            seat_rows[row] = []
        if seat not in booked_seat:
            seat_rows[row].append(seat)
        else:
            seat_rows[row].append(0)
    context = {
        'movie': movie,
        'theater': theater,
        'showtime': Showtime,
        'seats': seats,
        'seat_rows': seat_rows,
    }

    return render(request, 'theaters/seatselection.html', context)

@login_required(login_url='login')
def Book_Ticket_View(request,show_id):
    if request.method == 'POST':
        selected_seats = json.loads(request.POST['selected_seats'])
        total_amount = eval(request.POST['total_amount'])
        tickets=[]
        user = User.objects.get(username = request.user.username)
        Showtime = showtime.objects.get(id=show_id)
        convenience_fee = total_amount * 0.1
        sub_total = total_amount + convenience_fee
        booking = Booking.objects.create(
            user = user,
            showtime = Showtime,
            total_amount = sub_total
        )
        for seat in selected_seats:
            tickets.append(seat['key'])
            id=seat['id']
            seat_obj = Seat.objects.get(id=id)
            BookingSeat.objects.create(
                booking = booking,
                seat = seat_obj,
                showtime=Showtime,
            )

        context={
            'tickets': tickets,
            'convenience_fee':convenience_fee,
            'sub_total':sub_total,
            'total_amount':total_amount,
            'showtime':showtime,
            'booking':booking,
            'stripe_public_key':settings.STRIPE_PUBLIC_KEY

        
        }
        # return HttpResponse('Booking intiatrd')
        return render(request,'bookings/proceed_to_pay.html',context)
    return HttpResponse('Invalid Request')



@login_required
def cancel_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Optionally delete related BookingSeat entries
        booking.bookingseat_set.all().delete()
        booking.delete()
        messages.success(request, "Your ticket has been cancelled successfully.")
        return redirect('booked_ticktes')  # Replace with your actual view name

    messages.error(request, "Invalid request method.")
    return redirect('booked_ticktes')


@login_required(login_url='login')
def booked_ticket_view(request):
    user=User.objects.get(username=request.user.username)
    # print(request.user.username)
    qs=Booking.objects.filter(user=user.id)
    # seats=[]
    # for i in qs:
    #     obj=BookingSeat.objects.get(id=i.id)
    #     # print(obj.seat)
    #     seats.append(obj.seat)
    # details=list(zip(qs,seats))
    # print(details)
    return render(request,'bookings/b_t.html',{'details':qs})
