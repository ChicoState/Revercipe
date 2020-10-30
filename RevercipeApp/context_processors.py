from .forms import top_search_form

def top_search_global(request):
    navSearch = basNav()
    return {"navForm":navSearch}
