import requests
from django.shortcuts import render,  redirect
from .models import Contact
from django.contrib import messages

# Currency symbols dictionary
CURRENCY_SYMBOLS = {
    'USD': '🇺🇸 $',
    'EUR': '🇪🇺 €',
    'INR': '🇮🇳 ₹',
    'GBP': '🇬🇧 £',
}

def home(request):
    converted = None
    symbol = None
    error_message = None
    from_currency = None
    to_currency = None
    amount = None

    if request.method == 'POST':
        from_currency = request.POST.get('from')
        to_currency = request.POST.get('to')
        amount = request.POST.get('amount')

        try:
            amount = float(amount)

            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
            response = requests.get(url)
            data = response.json()

            if "rates" in data and to_currency in data["rates"]:
                converted = data["rates"][to_currency]
                symbol = CURRENCY_SYMBOLS.get(to_currency, to_currency)
            else:
                error_message = "Currency rates are currently unavailable. Please try again later."
        except (TypeError, ValueError):
            error_message = "Please enter a valid amount."
        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, 'home.html', {
        'converted': converted,
        'symbol': symbol,
        'error_message': error_message,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
    })


# # FOR CONTACT 
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        contact = Contact(name=name, email=email, message=message)
        contact.save()

        return redirect('contact') 

    return render(request, 'contact.html')