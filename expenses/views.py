from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/list.html', {'expenses': expenses})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add.html', {'form': form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/edit.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('expense_list')
    

@login_required
def dashboard(request):
    # Get all expenses for the logged-in user
    expenses = Expense.objects.filter(user=request.user)

    # Total expenses
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Monthly expenses (current month)
    current_month = datetime.now().month
    monthly_expense = expenses.filter(date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0

    # Total number of expense records
    total_records = expenses.count()

    # Recent 5 expenses
    recent_expenses = expenses.order_by('-date')[:5]

    # Prepare chart data: group by month
    monthly_labels = []
    monthly_data = []
    monthly_summary = {}

    for e in expenses:
        month_label = e.date.strftime('%b %Y')
        if month_label in monthly_summary:
            monthly_summary[month_label] += e.amount
        else:
            monthly_summary[month_label] = e.amount

    # Sort months chronologically
    for month, amount in sorted(monthly_summary.items(), key=lambda x: datetime.strptime(x[0], '%b %Y')):
        monthly_labels.append(month)
        monthly_data.append(amount)

    context = {
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'total_records': total_records,
        'recent_expenses': recent_expenses,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
    }

    return render(request, 'expenses/dashboard.html', context)