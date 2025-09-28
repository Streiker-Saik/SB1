from rest_framework.pagination import PageNumberPagination


class BuyRatePaginator(PageNumberPagination):
    """
    Пагинатор для приложения buyrate
    К-во элементов 4 (максимум 4) на странице
    """

    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 4
