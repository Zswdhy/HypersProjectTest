def get_value_from_request(request, search_param):
    """筛选器获取get请求参数."""
    value = request.query_params.get(search_param, "") or request.data.get(search_param, "")
    if isinstance(value, str):
        value = value.replace("\x00", "").strip()
    return value
