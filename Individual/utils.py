def get_ip_address(request):
    """use request object to fetch client machine's IP Address"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")  ### Real IP address of client Machine
    return ip


def phone_num_val(phone_number):
    phone_number_list = list(phone_number)
    phone_number_list[0] = "234"
    p = "".join([str(elem) for elem in phone_number_list])
    return p
