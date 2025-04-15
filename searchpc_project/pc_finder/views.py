from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import PCSearchForm
from .utils import validate_inputs, log_search, PCPartsFinder, parse_gemini_recommendation

class HomeView(View):
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
                # Log the search
                log_search(purpose, budget, location)
                
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

class ResultsView(View):
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
                search_params['location']
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
