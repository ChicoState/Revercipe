from .forms import top_search_form

def top_search_global(request):
    navSearch = top_search_form()
    return {"navForm":navSearch}
