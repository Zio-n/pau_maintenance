from accounts.models import Staff




def navbar_context(request):
    # Initialize navbar context dictionary
    navbar_context = {}
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve staff information associated with the current user
        try:
            staff = Staff.objects.get(user=request.user)
            # Add staff role to navbar context
            navbar_context['staff_role'] = staff.role
        except Staff.DoesNotExist:
            # Handle case where staff information is not found
            navbar_context['staff_role'] = None  # Or any default value you want
    else:
        navbar_context['staff_role'] = None  # Handle case for anonymous users
    
    return navbar_context