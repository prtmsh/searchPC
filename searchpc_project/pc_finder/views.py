from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .forms import PCSearchForm
from .auth_forms import CustomUserCreationForm, CustomAuthenticationForm
from .utils import validate_inputs, log_search, PCPartsFinder, parse_gemini_recommendation
from .models import SearchLog

class SignUpView(CreateView):
    """User registration view"""
    template_name = 'pc_finder/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response

class CustomLoginView(LoginView):
    """User login view with custom form"""
    template_name = 'pc_finder/login.html'
    authentication_form = CustomAuthenticationForm
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            # Session expires when the user closes their browser
            self.request.session.set_expiry(0)
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, View):
    """Home page view with search form"""
    template_name = 'pc_finder/home.html'
    
    def get(self, request):
        form = PCSearchForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PCSearchForm(request.POST)
        
        if form.is_valid():
            # Extract form data
            budget = form.cleaned_data['budget']
            purpose = form.cleaned_data['purpose']
            location = form.cleaned_data['location']
            preferred_brands = form.cleaned_data['preferred_brands']
            
            # Validate inputs
            if validate_inputs(budget, purpose, location, request):
                # Log the search with current user
                log_search(purpose, budget, location, request.user)
                
                # Store the search parameters in session
                request.session['search_params'] = {
                    'budget': float(budget),
                    'purpose': purpose,
                    'location': location,
                    'preferred_brands': preferred_brands,
                }
                
                # Redirect to results page
                return redirect('search_results')
        
        return render(request, self.template_name, {'form': form})

class ResultsView(LoginRequiredMixin, View):
    """Results page view"""
    template_name = 'pc_finder/results.html'
    
    def get(self, request):
        search_params = request.session.get('search_params')
        
        if not search_params:
            messages.error(request, "No search parameters found. Please start a new search.")
            return redirect('home')
        
        try:
            parts_finder = PCPartsFinder()
            
            recommendations = parts_finder.get_part_recommendations(
                search_params['purpose'],
                search_params['budget'],
                search_params['location'],
                search_params.get('preferred_brands', [])  # Pass preferred brands with empty list as default
            )
            
            # Parse components for better display
            components = parse_gemini_recommendation(recommendations['ai_recommendation'])
            
            context = {
                'search_params': search_params,
                'ai_recommendation': recommendations['ai_recommendation'],
                'part_recommendations': recommendations['part_recommendations'],
                'components': components
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            messages.error(request, f"An error occurred while retrieving results: {e}")
            return redirect('home')

class DashboardView(LoginRequiredMixin, ListView):
    """User dashboard with search history"""
    template_name = 'pc_finder/dashboard.html'
    model = SearchLog
    context_object_name = 'searches'
    paginate_by = 10
    ordering = ['-timestamp']
    
    def get_queryset(self):
        # Filter search logs for current user only
        return SearchLog.objects.filter(user=self.request.user).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_searches = SearchLog.objects.filter(user=self.request.user)
        context['total_searches'] = user_searches.count()
        
        # Get popular purposes and budgets for insights
        purposes = user_searches.values_list('purpose', flat=True)
        purpose_counts = {}
        for purpose in purposes:
            if purpose in purpose_counts:
                purpose_counts[purpose] += 1
            else:
                purpose_counts[purpose] = 1
        
        # Get most popular purpose
        if purpose_counts:
            most_popular = max(purpose_counts.items(), key=lambda x: x[1])
            context['popular_purpose'] = {'name': most_popular[0], 'count': most_popular[1]}
        
        # Calculate average budget
        budgets = user_searches.values_list('budget', flat=True)
        if budgets:
            context['avg_budget'] = sum(budgets) / len(budgets)
        
        return context
